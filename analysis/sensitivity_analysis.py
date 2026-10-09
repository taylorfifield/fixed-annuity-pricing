
"""Run one-way and two-way annuity sensitivity analyses."""

from dataclasses import replace
from pathlib import Path
import json

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.assumptions import base_assumptions
from src.annuity_model import (
    project_annuity,
    summarize_projection,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
CHART_DIR = OUTPUT_DIR / "charts"


def terminal_surplus(assumptions):
    """Calculate ending surplus for one assumption set."""

    records = project_annuity(assumptions)
    results = summarize_projection(records)

    return float(results["ending_insurer_surplus"])


def save_chart(filename):
    """Apply consistent chart formatting and save a PNG."""

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / filename,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close()


def run_sensitivity():
    """Produce sensitivity tables, charts, and a JSON summary."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    base = base_assumptions()

    base_records = project_annuity(base)
    base_summary = summarize_projection(base_records)

    base_surplus = base_summary["ending_insurer_surplus"]

    # ---------------------------------------------------------
    # ONE-WAY SENSITIVITY ANALYSIS
    # ---------------------------------------------------------

    drivers = {
        "Investment return": "investment_rate",
        "Credited interest": "credited_rate",
        "Partial withdrawal": "withdrawal_rate",
        "Full surrender": "surrender_rate",
    }

    # -100, 0, and +100 basis points.
    # 100 basis points = 1 percentage point.
    shocks = [-0.01, 0.0, 0.01]

    sensitivity_rows = []

    for driver_name, attribute in drivers.items():

        starting_rate = getattr(base, attribute)

        for shock in shocks:
            scenario_rate = starting_rate + shock

            scenario = replace(
                base,
                **{attribute: scenario_rate},
            )

            scenario.validate()

            result = terminal_surplus(scenario)

            sensitivity_rows.append({
                "driver": driver_name,
                "shock_basis_points": int(round(shock * 10000)),
                "base_rate": starting_rate,
                "scenario_rate": scenario_rate,
                "terminal_surplus": result,
                "change_from_base": result - base_surplus,
            })

    sensitivity_df = pd.DataFrame(sensitivity_rows)

    sensitivity_df.to_csv(
        OUTPUT_DIR / "sensitivity_results.csv",
        index=False,
        float_format="%.10f",
    )

    # ---------------------------------------------------------
    # TWO-WAY SENSITIVITY ANALYSIS
    # ---------------------------------------------------------

    # Evaluate simultaneous changes in investment return
    # and credited interest rate.
    grid_shocks = np.linspace(-0.01, 0.01, 5)

    grid_values = np.zeros((5, 5))
    grid_rows = []

    for row_index, credit_shock in enumerate(grid_shocks):

        for column_index, return_shock in enumerate(grid_shocks):

            scenario = replace(
                base,
                investment_rate=(
                    base.investment_rate + float(return_shock)
                ),
                credited_rate=(
                    base.credited_rate + float(credit_shock)
                ),
            )

            scenario.validate()

            result = terminal_surplus(scenario)

            grid_values[row_index, column_index] = result

            grid_rows.append({
                "investment_shock_bps": int(
                    round(float(return_shock) * 10000)
                ),
                "crediting_shock_bps": int(
                    round(float(credit_shock) * 10000)
                ),
                "investment_rate": scenario.investment_rate,
                "credited_rate": scenario.credited_rate,
                "terminal_surplus": result,
            })

    grid_df = pd.DataFrame(grid_rows)

    grid_df.to_csv(
        OUTPUT_DIR / "sensitivity_grid.csv",
        index=False,
        float_format="%.10f",
    )

    # ---------------------------------------------------------
    # CHART 1: ASSETS AND POLICYHOLDER BALANCES
    # ---------------------------------------------------------

    projection_df = pd.DataFrame(base_records)

    plt.figure(figsize=(10, 6))

    plt.plot(
        projection_df["year"],
        projection_df["closing_balance"],
        marker="o",
        linewidth=2,
        label="Policyholder account liabilities",
    )

    plt.plot(
        projection_df["year"],
        projection_df["closing_assets"],
        marker="s",
        linewidth=2,
        label="Insurer assets",
    )

    plt.title("10-Year Annuity Portfolio Projection")
    plt.xlabel("Projection Year")
    plt.ylabel("Amount")
    plt.xticks(projection_df["year"])
    plt.grid(alpha=0.25)
    plt.legend()

    save_chart("account_and_assets.png")

    # ---------------------------------------------------------
    # CHART 2: INVESTMENT VS CREDITING
    # ---------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        projection_df["year"],
        projection_df["investment_income"],
        marker="o",
        linewidth=2,
        label="Investment income",
    )

    plt.plot(
        projection_df["year"],
        projection_df["credited_interest"],
        marker="s",
        linewidth=2,
        label="Credited interest",
    )

    plt.title("Investment Income vs Credited Interest")
    plt.xlabel("Projection Year")
    plt.ylabel("Annual Amount")
    plt.xticks(projection_df["year"])
    plt.grid(alpha=0.25)
    plt.legend()

    save_chart("investment_vs_crediting.png")

    # ---------------------------------------------------------
    # CHART 3: ONE-WAY SENSITIVITY
    # ---------------------------------------------------------

    plt.figure(figsize=(12, 6))

    x = np.arange(len(drivers))
    width = 0.25

    for index, shock in enumerate(shocks):

        shock_bps = int(round(shock * 10000))

        values = []

        for driver_name in drivers:
            matching = sensitivity_df[
                (sensitivity_df["driver"] == driver_name)
                & (
                    sensitivity_df["shock_basis_points"]
                    == shock_bps
                )
            ]

            values.append(
                float(matching.iloc[0]["change_from_base"])
            )

        plt.bar(
            x + (index - 1) * width,
            values,
            width,
            label=f"{shock_bps:+d} bps",
        )

    plt.axhline(0, linewidth=1, color="black")

    plt.xticks(
        x,
        list(drivers.keys()),
        rotation=15,
        ha="right",
    )

    plt.title("Change in Terminal Surplus by Assumption")
    plt.ylabel("Surplus Change from Base")
    plt.xlabel("Assumption Changed")
    plt.legend(title="Assumption Shock")
    plt.grid(axis="y", alpha=0.2)

    save_chart("one_way_sensitivity.png")

    # ---------------------------------------------------------
    # CHART 4: TWO-WAY HEATMAP
    # ---------------------------------------------------------

    plt.figure(figsize=(9, 7))

    image = plt.imshow(
        grid_values,
        cmap="Blues",
        aspect="auto",
    )

    labels = [
        f"{int(round(float(value) * 10000)):+d}"
        for value in grid_shocks
    ]

    plt.xticks(range(5), labels)
    plt.yticks(range(5), labels)

    plt.xlabel("Investment Return Shock (basis points)")
    plt.ylabel("Credited Rate Shock (basis points)")
    plt.title("Terminal Surplus: Two-Way Sensitivity")

    plt.colorbar(
        image,
        label="Ending Insurer Surplus",
    )

    for row_index in range(5):
        for column_index in range(5):
            plt.text(
                column_index,
                row_index,
                f"{grid_values[row_index, column_index]:,.0f}",
                ha="center",
                va="center",
                fontsize=9,
                color="black",
            )

    save_chart("investment_crediting_heatmap.png")

    # ---------------------------------------------------------
    # STRUCTURED OUTPUT SUMMARY
    # ---------------------------------------------------------

    driver_ranges = []

    for driver_name in drivers:

        subset = sensitivity_df[
            sensitivity_df["driver"] == driver_name
        ]

        driver_ranges.append({
            "driver": driver_name,
            "minimum_terminal_surplus": float(
                subset["terminal_surplus"].min()
            ),
            "maximum_terminal_surplus": float(
                subset["terminal_surplus"].max()
            ),
        })

    report = {
        "base_terminal_surplus": float(base_surplus),
        "one_way_shocks_basis_points": [-100, 0, 100],
        "two_way_grid_shocks_basis_points": [
            -100, -50, 0, 50, 100
        ],
        "driver_ranges": driver_ranges,
        "method": "Reproject all 10 years for each scenario",
        "financial_measure": (
            "Ending insurer assets less policyholder "
            "account liabilities"
        ),
        "warning": (
            "Hypothetical educational scenario results; "
            "not real insurer pricing estimates."
        ),
    }

    with open(
        OUTPUT_DIR / "sensitivity_summary.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(report, file, indent=2)

    print("Sensitivity analysis complete.")
    print(f"Base terminal surplus: ${base_surplus:,.2f}")
    print("Generated sensitivity CSV files and four PNG charts.")


if __name__ == "__main__":
    run_sensitivity()
