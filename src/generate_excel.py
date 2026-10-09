
"""Generate an independent, formula-driven Excel annuity model."""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
)
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.properties import CalcProperties

from src.assumptions import (
    base_assumptions,
    load_interest_rates,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "output" / "fixed_annuity_model.xlsx"

NAVY = "17324D"
BLUE = "DDEBF7"
WHITE = "FFFFFF"
GREEN = "E2F0D9"
INPUT_BLUE = "EAF3FF"
GRAY = "667085"

MONEY_FORMAT = '#,##0.00;[Red](#,##0.00)'
PERCENT_FORMAT = "0.00%"


def style_header(worksheet, row, last_column):
    """Format a table header."""

    for cells in worksheet.iter_rows(
        min_row=row,
        max_row=row,
        min_col=1,
        max_col=last_column,
    ):
        for cell in cells:
            cell.fill = PatternFill(
                "solid", fgColor=NAVY
            )
            cell.font = Font(
                bold=True, color=WHITE
            )
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True,
            )


def add_decimal_validation(worksheet, address, minimum, maximum):
    """Restrict editable inputs to sensible numeric ranges."""

    validation = DataValidation(
        type="decimal",
        operator="between",
        formula1=str(minimum),
        formula2=str(maximum),
        allow_blank=False,
    )

    validation.error = "Enter a value within the allowed range."
    validation.errorTitle = "Invalid assumption"
    validation.showErrorMessage = True

    worksheet.add_data_validation(validation)
    validation.add(address)


def generate_workbook(destination=OUTPUT_FILE):
    """Create the Excel workbook with formulas and source data."""

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    assumptions = base_assumptions()
    observations = load_interest_rates()

    workbook = Workbook()

    guide = workbook.active
    guide.title = "Guide"

    inputs = workbook.create_sheet("Assumptions")
    rates = workbook.create_sheet("Rates")
    projection = workbook.create_sheet("Projection")
    summary = workbook.create_sheet("Summary")

    # Request calculation when a spreadsheet engine opens the file.
    workbook.calculation = CalcProperties(
        calcMode="auto",
        fullCalcOnLoad=True,
        forceFullCalc=True,
    )

    # ---------------------------------------------------------
    # GUIDE SHEET
    # ---------------------------------------------------------

    guide["A1"] = "FIXED ANNUITY PRICING & SENSITIVITY ANALYSIS"
    guide["A1"].font = Font(
        size=17, bold=True, color=NAVY
    )

    instructions = [
        "Educational model of a hypothetical fixed deferred annuity portfolio.",
        "1. Open the Assumptions sheet to inspect or edit model inputs.",
        "2. The initial investment return references the latest rate on the Rates sheet.",
        "3. Overwrite Assumptions!B4 to try a different investment return.",
        "4. Review the 10-year formulas on the Projection sheet.",
        "5. Review results and reconciliation checks on the Summary sheet.",
        "6. Monetary amounts use the same hypothetical currency units.",
        "7. Initial premium is received at time zero, not in annual cash inflows.",
        "8. Investment income is modeled as an annual cash inflow.",
        "9. Surrender charges reduce surrender payments; they are not separate cash receipts.",
        "10. Policies shown are expected counts and may be fractional.",
        "11. The workbook's 10-year horizon is fixed; other rates are editable.",
        "12. Excel or a compatible spreadsheet engine must calculate the formulas.",
        "13. openpyxl writes formulas but does not evaluate their numerical results.",
        "14. The workbook operates independently of Python after generation.",
        "15. This is not a reserve, capital, or production insurance pricing model.",
    ]

    for row, text in enumerate(instructions, start=3):
        guide.cell(row=row, column=1, value=text)

    guide.column_dimensions["A"].width = 100
    guide.freeze_panes = "A3"

    # ---------------------------------------------------------
    # SOURCE INTEREST-RATE SHEET
    # ---------------------------------------------------------

    rates["A1"] = "PUBLISHED TREASURY INTEREST-RATE OBSERVATIONS"
    rates["A1"].font = Font(
        size=14, bold=True, color=NAVY
    )

    rate_headers = [
        "Observation date",
        "FRED series",
        "Rate (percent)",
        "Units",
        "Source URL",
    ]

    for column, heading in enumerate(rate_headers, start=1):
        rates.cell(row=3, column=column, value=heading)

    style_header(rates, 3, len(rate_headers))

    for row_number, observation in enumerate(
        observations, start=4
    ):
        rates.cell(
            row=row_number,
            column=1,
            value=observation["date"],
        )
        rates.cell(
            row=row_number,
            column=2,
            value=observation["series"],
        )
        rates.cell(
            row=row_number,
            column=3,
            value=observation["rate_percent"],
        )
        rates.cell(
            row=row_number,
            column=4,
            value=observation["units"],
        )
        rates.cell(
            row=row_number,
            column=5,
            value=observation["source_url"],
        )

    latest_rate_row = 3 + len(observations)

    rates.column_dimensions["A"].width = 21
    rates.column_dimensions["B"].width = 18
    rates.column_dimensions["C"].width = 19
    rates.column_dimensions["D"].width = 23
    rates.column_dimensions["E"].width = 53

    rates.freeze_panes = "A4"
    rates.auto_filter.ref = f"A3:E{latest_rate_row}"

    # ---------------------------------------------------------
    # EDITABLE ASSUMPTIONS SHEET
    # ---------------------------------------------------------

    inputs["A1"] = "MODEL ASSUMPTIONS"
    inputs["A1"].font = Font(
        size=17, bold=True, color=NAVY
    )

    inputs["A2"] = "Assumption"
    inputs["B2"] = "Value"
    inputs["C2"] = "Explanation"

    style_header(inputs, 2, 3)

    assumption_rows = [
        (
            3,
            "Initial premium",
            assumptions.initial_premium,
            "Total initial policyholder deposits",
        ),
        (
            4,
            "Annual investment return",
            f"=Rates!C{latest_rate_row}/100",
            "Initially linked to the most recent included Treasury yield",
        ),
        (
            5,
            "Annual credited interest",
            assumptions.credited_rate,
            "Interest credited to policyholder accounts",
        ),
        (
            6,
            "Annual partial withdrawal rate",
            assumptions.withdrawal_rate,
            "Percentage withdrawn after interest crediting",
        ),
        (
            7,
            "Annual full surrender rate",
            assumptions.surrender_rate,
            "Expected fraction of remaining policies surrendering",
        ),
        (
            8,
            "Surrender charge rate",
            assumptions.surrender_charge_rate,
            "Charge withheld from gross surrendered balances",
        ),
        (
            9,
            "Annual operating expense rate",
            assumptions.expense_rate,
            "Applied to opening policyholder account balances",
        ),
        (
            10,
            "Projection years",
            assumptions.years,
            "Fixed at 10 years in this workbook",
        ),
        (
            11,
            "Initial policy count",
            assumptions.initial_policies,
            "Homogeneous policies with equal average balances",
        ),
    ]

    for row, label, value, description in assumption_rows:
        inputs.cell(row=row, column=1, value=label)
        inputs.cell(row=row, column=2, value=value)
        inputs.cell(row=row, column=3, value=description)

        if row != 10:
            inputs.cell(row=row, column=2).fill = PatternFill(
                "solid", fgColor=INPUT_BLUE
            )

    inputs["B3"].number_format = MONEY_FORMAT

    for row in range(4, 10):
        inputs[f"B{row}"].number_format = PERCENT_FORMAT

    inputs["A13"] = "Blue cells can be edited."
    inputs["A14"] = (
        "Investment return starts as a formula linked to Rates."
    )
    inputs["A15"] = (
        "Replacing that formula with a number creates a manual scenario."
    )
    inputs["A16"] = (
        "Excel formula results require a compatible calculation engine."
    )

    inputs.column_dimensions["A"].width = 34
    inputs.column_dimensions["B"].width = 18
    inputs.column_dimensions["C"].width = 75

    add_decimal_validation(inputs, "B3", 0.01, 1000000000)
    add_decimal_validation(inputs, "B4", -0.999, 1)

    for row in range(5, 10):
        add_decimal_validation(inputs, f"B{row}", 0, 1)

    add_decimal_validation(inputs, "B11", 1, 1000000000)

    inputs.freeze_panes = "B3"

    # ---------------------------------------------------------
    # FORMULA-DRIVEN PROJECTION
    # ---------------------------------------------------------

    projection["A1"] = "10-YEAR ANNUITY FINANCIAL PROJECTION"
    projection["A1"].font = Font(
        size=15, bold=True, color=NAVY
    )

    projection["A2"] = (
        "Assets and policyholder balances are projected separately."
    )

    headers = [
        "Year",
        "Opening account balance",
        "Opening insurer assets",
        "Investment income",
        "Credited interest",
        "Balance after interest",
        "Partial withdrawals",
        "Gross full surrenders",
        "Surrender charges",
        "Surrender cash payouts",
        "Operating expenses",
        "Annual cash inflows",
        "Annual cash outflows",
        "Annual net asset cash flow",
        "Closing account balance",
        "Closing insurer assets",
        "Opening surplus",
        "Closing surplus",
        "Change in surplus",
        "Opening active policies",
        "Closing active policies",
    ]

    for column, heading in enumerate(headers, start=1):
        projection.cell(row=4, column=column, value=heading)

    style_header(projection, 4, len(headers))
    projection.row_dimensions[4].height = 48

    start_row = 5
    last_row = start_row + assumptions.years - 1

    for year in range(1, assumptions.years + 1):
        row = start_row + year - 1

        projection[f"A{row}"] = year

        if year == 1:
            projection[f"B{row}"] = "=Assumptions!$B$3"
            projection[f"C{row}"] = "=Assumptions!$B$3"
            projection[f"Q{row}"] = f"=C{row}-B{row}"
            projection[f"T{row}"] = "=Assumptions!$B$11"

        else:
            previous = row - 1
            projection[f"B{row}"] = f"=O{previous}"
            projection[f"C{row}"] = f"=P{previous}"
            projection[f"Q{row}"] = f"=R{previous}"
            projection[f"T{row}"] = f"=U{previous}"

        formulas = {
            "D": f"=C{row}*Assumptions!$B$4",
            "E": f"=B{row}*Assumptions!$B$5",
            "F": f"=B{row}+E{row}",
            "G": f"=F{row}*Assumptions!$B$6",
            "H": f"=(F{row}-G{row})*Assumptions!$B$7",
            "I": f"=H{row}*Assumptions!$B$8",
            "J": f"=H{row}-I{row}",
            "K": f"=B{row}*Assumptions!$B$9",
            "L": f"=D{row}",
            "M": f"=G{row}+J{row}+K{row}",
            "N": f"=L{row}-M{row}",
            "O": f"=F{row}-G{row}-H{row}",
            "P": f"=C{row}+N{row}",
            "R": f"=P{row}-O{row}",
            "S": f"=R{row}-Q{row}",
            "U": f"=T{row}*(1-Assumptions!$B$7)",
        }

        for column, formula in formulas.items():
            projection[f"{column}{row}"] = formula

        for column in range(2, 20):
            projection.cell(
                row=row, column=column
            ).number_format = MONEY_FORMAT

        for column in (20, 21):
            projection.cell(
                row=row, column=column
            ).number_format = "0.00"

        if year % 2 == 0:
            for column in range(1, 22):
                projection.cell(
                    row=row, column=column
                ).fill = PatternFill(
                    "solid", fgColor="F3F7FB"
                )

    projection.column_dimensions["A"].width = 10

    for column in range(2, 22):
        letter = projection.cell(
            row=4, column=column
        ).column_letter
        projection.column_dimensions[letter].width = 19

    projection.freeze_panes = "B5"
    projection.auto_filter.ref = f"A4:U{last_row}"

    # ---------------------------------------------------------
    # FINANCIAL SUMMARY
    # ---------------------------------------------------------

    summary["A1"] = "ANNUITY FINANCIAL RESULTS"
    summary["A1"].font = Font(
        size=17, bold=True, color=NAVY
    )

    summary["A2"] = "Financial measure"
    summary["B2"] = "Formula-driven result"

    style_header(summary, 2, 2)

    summary_formulas = [
        (3, "Ending insurer surplus", f"=Projection!R{last_row}"),
        (4, "Ending policyholder balances", f"=Projection!O{last_row}"),
        (5, "Ending insurer assets", f"=Projection!P{last_row}"),
        (6, "Cumulative change in surplus", f"=SUM(Projection!S{start_row}:S{last_row})"),
        (7, "Total investment income", f"=SUM(Projection!D{start_row}:D{last_row})"),
        (8, "Total credited interest", f"=SUM(Projection!E{start_row}:E{last_row})"),
        (9, "Total surrender charges", f"=SUM(Projection!I{start_row}:I{last_row})"),
        (10, "Total operating expenses", f"=SUM(Projection!K{start_row}:K{last_row})"),
        (11, "Total partial withdrawals", f"=SUM(Projection!G{start_row}:G{last_row})"),
        (12, "Total surrender payouts", f"=SUM(Projection!J{start_row}:J{last_row})"),
        (13, "Annual cash inflows total", f"=SUM(Projection!L{start_row}:L{last_row})"),
        (14, "Annual cash outflows total", f"=SUM(Projection!M{start_row}:M{last_row})"),
        (15, "Annual net cash flow total", f"=SUM(Projection!N{start_row}:N{last_row})"),
        (16, "Remaining expected policies", f"=Projection!U{last_row}"),
        (17, "Surplus change reconciliation", "=B3-B6"),
        (18, "Asset-liability reconciliation", "=B5-B4-B3"),
        (19, "Profit components reconciliation", "=B7-B8+B9-B10-B3"),
        (20, "Asset cash-flow reconciliation", "=Assumptions!B3+B15-B5"),
    ]

    for row, label, formula in summary_formulas:
        summary.cell(row=row, column=1, value=label)
        summary.cell(row=row, column=2, value=formula)
        summary.cell(row=row, column=2).number_format = MONEY_FORMAT

    summary["B16"].number_format = "0.00"

    for row in (3, 4, 5, 6):
        summary[f"B{row}"].fill = PatternFill(
            "solid", fgColor=GREEN
        )
        summary[f"B{row}"].font = Font(
            bold=True, color=NAVY
        )

    for row in (17, 18, 19, 20):
        summary[f"B{row}"].fill = PatternFill(
            "solid", fgColor=BLUE
        )

    summary["A22"] = "Reconciliation values should be approximately zero."
    summary["A23"] = (
        "Surplus is assets minus policyholder account liabilities."
    )
    summary["A24"] = (
        "It is not discounted economic profit or statutory capital."
    )

    summary.column_dimensions["A"].width = 42
    summary.column_dimensions["B"].width = 28
    summary.column_dimensions["C"].width = 4

    # ---------------------------------------------------------
    # EXCEL CHARTS
    # ---------------------------------------------------------

    asset_chart = LineChart()
    asset_chart.title = "Policyholder Balances vs Insurer Assets"
    asset_chart.style = 13
    asset_chart.y_axis.title = "Amount"
    asset_chart.x_axis.title = "Projection year"
    asset_chart.height = 9
    asset_chart.width = 18

    asset_data = Reference(
        projection,
        min_col=15,
        max_col=16,
        min_row=4,
        max_row=last_row,
    )

    years = Reference(
        projection,
        min_col=1,
        min_row=start_row,
        max_row=last_row,
    )

    asset_chart.add_data(
        asset_data, titles_from_data=True
    )
    asset_chart.set_categories(years)

    summary.add_chart(asset_chart, "E3")

    income_chart = BarChart()
    income_chart.title = "Investment Income and Credited Interest"
    income_chart.style = 10
    income_chart.y_axis.title = "Amount"
    income_chart.x_axis.title = "Projection year"
    income_chart.height = 9
    income_chart.width = 18

    income_data = Reference(
        projection,
        min_col=4,
        max_col=5,
        min_row=4,
        max_row=last_row,
    )

    income_chart.add_data(
        income_data, titles_from_data=True
    )
    income_chart.set_categories(years)

    summary.add_chart(income_chart, "E21")

    summary.freeze_panes = "B3"

    # Highlight workbook purpose on each worksheet.
    for worksheet in workbook.worksheets:
        worksheet.sheet_view.showGridLines = False

    workbook.active = 0
    workbook.save(destination)

    print(f"Excel workbook generated: {destination}")

    return destination


if __name__ == "__main__":
    generate_workbook()
