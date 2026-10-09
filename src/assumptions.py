
"""Inputs and validation for the fixed annuity model."""

from dataclasses import dataclass, replace
from datetime import date
from math import isfinite
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RATE_FILE = ROOT / "data" / "interest_rates.csv"


@dataclass(frozen=True)
class Assumptions:
    """Financial inputs expressed as annual decimal rates."""

    initial_premium: float = 100_000.0
    initial_policies: int = 100
    years: int = 10

    investment_rate: float = 0.05
    credited_rate: float = 0.0325
    withdrawal_rate: float = 0.025
    surrender_rate: float = 0.06
    surrender_charge_rate: float = 0.02
    expense_rate: float = 0.005

    def validate(self):
        """Reject invalid financial assumptions."""

        if not isinstance(self.years, int) or isinstance(self.years, bool):
            raise ValueError("Years must be a whole number.")

        if not 1 <= self.years <= 40:
            raise ValueError("Years must be between 1 and 40.")

        if not isinstance(self.initial_policies, int) or isinstance(
            self.initial_policies, bool
        ):
            raise ValueError("Initial policies must be a whole number.")

        if self.initial_policies <= 0:
            raise ValueError("Initial policies must be positive.")

        if not isinstance(self.initial_premium, (int, float)):
            raise ValueError("Initial premium must be numeric.")

        if not isfinite(self.initial_premium) or self.initial_premium <= 0:
            raise ValueError("Initial premium must be finite and positive.")

        rates = {
            "investment_rate": self.investment_rate,
            "credited_rate": self.credited_rate,
            "withdrawal_rate": self.withdrawal_rate,
            "surrender_rate": self.surrender_rate,
            "surrender_charge_rate": self.surrender_charge_rate,
            "expense_rate": self.expense_rate,
        }

        for name, value in rates.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"{name} must be numeric.")

            if not isfinite(value):
                raise ValueError(f"{name} must be finite.")

        if not -1.0 < self.investment_rate <= 1.0:
            raise ValueError(
                "Investment return must exceed -100% and not exceed 100%."
            )

        if not 0 <= self.credited_rate <= 1:
            raise ValueError(
                "Credited rate must be between 0% and 100%."
            )

        for name in (
            "withdrawal_rate",
            "surrender_rate",
            "surrender_charge_rate",
            "expense_rate",
        ):
            if not 0 <= getattr(self, name) <= 1:
                raise ValueError(
                    f"{name} must be between 0% and 100%."
                )

        return True


def load_interest_rates(path=RATE_FILE):
    """Load validated DGS10 data, skipping empty CSV lines."""

    observations = []

    with open(path, mode="r", newline="", encoding="utf-8-sig") as file:

        # Remove blank lines BEFORE parsing the CSV.
        # This prevents an empty first row from being
        # mistaken for the CSV column headers.
        nonempty_lines = (line for line in file if line.strip())

        reader = csv.DictReader(
            nonempty_lines,
            skipinitialspace=True,
        )

        # Handle extra spaces and invisible BOM characters.
        reader.fieldnames = [
            column.strip().lstrip("\ufeff")
            for column in (reader.fieldnames or [])
        ]

        expected_columns = {
            "date",
            "series",
            "rate_percent",
            "units",
            "source_url",
        }

        if set(reader.fieldnames) != expected_columns:
            raise ValueError(
                "Unexpected interest-rate CSV columns. "
                f"Expected: {sorted(expected_columns)}. "
                f"Found: {reader.fieldnames!r}"
            )

        for row in reader:

            if None in row:
                raise ValueError("CSV row contains extra columns.")

            if any(row.get(column) is None for column in expected_columns):
                raise ValueError("CSV row is missing required columns.")

            cleaned = {
                key: value.strip()
                for key, value in row.items()
            }

            observation_date = date.fromisoformat(
                cleaned["date"]
            )

            rate = float(cleaned["rate_percent"])

            if cleaned["series"] != "DGS10":
                raise ValueError(
                    "Unsupported interest-rate series."
                )

            if cleaned["units"] != "percent_per_annum":
                raise ValueError(
                    "Incorrect interest-rate units."
                )

            if cleaned["source_url"] != (
                "https://fred.stlouisfed.org/series/DGS10"
            ):
                raise ValueError(
                    "Unexpected data source URL."
                )

            if not isfinite(rate) or not 0 <= rate <= 100:
                raise ValueError(
                    "Invalid Treasury interest rate."
                )

            observations.append({
                "date": observation_date.isoformat(),
                "series": cleaned["series"],
                "rate_percent": rate,
                "units": cleaned["units"],
                "source_url": cleaned["source_url"],
            })

    if not observations:
        raise ValueError(
            "No Treasury observations were found."
        )

    observations.sort(
        key=lambda item: item["date"]
    )

    dates = [
        item["date"]
        for item in observations
    ]

    if len(dates) != len(set(dates)):
        raise ValueError(
            "Duplicate observation dates."
        )

    return observations


def base_assumptions():
    """Use the latest included Treasury yield as the scenario return."""

    observations = load_interest_rates()

    latest_rate = (
        observations[-1]["rate_percent"] / 100.0
    )

    assumptions = replace(
        Assumptions(),
        investment_rate=latest_rate,
    )

    assumptions.validate()

    return assumptions
