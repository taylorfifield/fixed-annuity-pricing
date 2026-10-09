
"""Run the baseline annuity projection and save outputs."""

from dataclasses import asdict
from pathlib import Path
import json

import pandas as pd

from src.assumptions import (
    base_assumptions,
    load_interest_rates,
)
from src.annuity_model import (
    project_annuity,
    summarize_projection,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    assumptions = base_assumptions()
    observations = load_interest_rates()

    records = project_annuity(assumptions)
    results = summarize_projection(records)

    # Save the full annual projection.
    dataframe = pd.DataFrame(records)

    dataframe.to_csv(
        OUTPUT_DIR / "annual_projection.csv",
        index=False,
        float_format="%.10f",
    )

    # Save assumptions and results with their data source.
    report = {
        "model_name": "Fixed Annuity Pricing and Sensitivity",
        "status": "hypothetical_educational_model",
        "interest_rate_reference": {
            "series": "DGS10",
            "latest_included_observation": observations[-1],
            "use": "Illustrative constant annual investment return",
        },
        "assumptions": asdict(assumptions),
        "results": results,
    }

    with open(
        OUTPUT_DIR / "summary.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(report, file, indent=2)

    print("Baseline annuity projection complete.")
    print(f"Projection years: {assumptions.years}")
    print(f"Investment return: {assumptions.investment_rate:.2%}")
    print(
        "Ending policyholder balance: "
        f"${results['ending_account_balance']:,.2f}"
    )
    print(
        "Ending insurer assets: "
        f"${results['ending_insurer_assets']:,.2f}"
    )
    print(
        "Ending insurer surplus: "
        f"${results['ending_insurer_surplus']:,.2f}"
    )

    print("Saved annual_projection.csv and summary.json.")


if __name__ == "__main__":
    main()
