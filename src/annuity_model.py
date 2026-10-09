
"""Ten-year aggregate fixed deferred annuity projection."""

from math import isclose


def project_annuity(assumptions):
    """
    Project annual insurer assets and policyholder liabilities.

    Timing for each year:
    1. Earn investment return on opening insurer assets.
    2. Credit interest on opening policyholder balances.
    3. Apply partial withdrawals.
    4. Apply full surrenders after partial withdrawals.
    5. Deduct operating expenses.
    6. Reconcile insurer assets and account liabilities.

    The premium is received at time zero.
    """

    assumptions.validate()

    account_balance = float(assumptions.initial_premium)
    insurer_assets = float(assumptions.initial_premium)
    active_policies = float(assumptions.initial_policies)

    records = []

    for year in range(1, assumptions.years + 1):

        opening_balance = account_balance
        opening_assets = insurer_assets
        opening_policies = active_policies

        opening_surplus = opening_assets - opening_balance

        # Earnings accrue on the insurer's opening assets.
        investment_income = (
            opening_assets * assumptions.investment_rate
        )

        # Policyholder interest increases account liabilities.
        credited_interest = (
            opening_balance * assumptions.credited_rate
        )

        post_credit_balance = (
            opening_balance + credited_interest
        )

        # Partial withdrawal across the active portfolio.
        partial_withdrawals = (
            post_credit_balance * assumptions.withdrawal_rate
        )

        remaining_after_partial = (
            post_credit_balance - partial_withdrawals
        )

        # Full surrenders remove entire accounts for the
        # expected proportion of policies surrendering.
        gross_surrenders = (
            remaining_after_partial * assumptions.surrender_rate
        )

        # Surrender charges are withheld from cash payments.
        surrender_charges = (
            gross_surrenders * assumptions.surrender_charge_rate
        )

        surrender_payouts = (
            gross_surrenders - surrender_charges
        )

        # Expenses are calculated on opening policyholder funds.
        operating_expenses = (
            opening_balance * assumptions.expense_rate
        )

        # No additional premium is received after time zero.
        # Investment income is assumed to be realized as cash.
        cash_inflows = investment_income

        cash_outflows = (
            partial_withdrawals
            + surrender_payouts
            + operating_expenses
        )

        net_cash_flow = cash_inflows - cash_outflows

        closing_balance = (
            post_credit_balance
            - partial_withdrawals
            - gross_surrenders
        )

        closing_assets = (
            opening_assets + net_cash_flow
        )

        closing_policies = (
            opening_policies * (1 - assumptions.surrender_rate)
        )

        closing_surplus = (
            closing_assets - closing_balance
        )

        annual_profit_change = (
            closing_surplus - opening_surplus
        )

        # Independent accounting-style relationship.
        expected_profit_change = (
            investment_income
            - credited_interest
            + surrender_charges
            - operating_expenses
        )

        if not isclose(
            annual_profit_change,
            expected_profit_change,
            rel_tol=1e-9,
            abs_tol=1e-7,
        ):
            raise ArithmeticError(
                f"Surplus reconciliation failed in year {year}."
            )

        records.append({
            "year": year,
            "opening_balance": opening_balance,
            "opening_assets": opening_assets,
            "opening_surplus": opening_surplus,
            "opening_policies": opening_policies,
            "investment_income": investment_income,
            "credited_interest": credited_interest,
            "post_credit_balance": post_credit_balance,
            "partial_withdrawals": partial_withdrawals,
            "gross_surrenders": gross_surrenders,
            "surrender_charges": surrender_charges,
            "surrender_payouts": surrender_payouts,
            "operating_expenses": operating_expenses,
            "cash_inflows": cash_inflows,
            "cash_outflows": cash_outflows,
            "net_cash_flow": net_cash_flow,
            "closing_balance": closing_balance,
            "closing_assets": closing_assets,
            "closing_surplus": closing_surplus,
            "annual_profit_change": annual_profit_change,
            "closing_policies": closing_policies,
        })

        account_balance = closing_balance
        insurer_assets = closing_assets
        active_policies = closing_policies

    return records


def summarize_projection(records):
    """Produce financial totals from a completed projection."""

    if not records:
        raise ValueError("Projection contains no annual records.")

    last = records[-1]

    return {
        "projection_years": len(records),
        "ending_account_balance": last["closing_balance"],
        "ending_insurer_assets": last["closing_assets"],
        "ending_insurer_surplus": last["closing_surplus"],
        "remaining_expected_policies": last["closing_policies"],
        "total_investment_income": sum(
            item["investment_income"] for item in records
        ),
        "total_credited_interest": sum(
            item["credited_interest"] for item in records
        ),
        "total_partial_withdrawals": sum(
            item["partial_withdrawals"] for item in records
        ),
        "total_gross_surrenders": sum(
            item["gross_surrenders"] for item in records
        ),
        "total_surrender_payouts": sum(
            item["surrender_payouts"] for item in records
        ),
        "total_surrender_charges": sum(
            item["surrender_charges"] for item in records
        ),
        "total_operating_expenses": sum(
            item["operating_expenses"] for item in records
        ),
        "total_annual_cash_inflows": sum(
            item["cash_inflows"] for item in records
        ),
        "total_annual_cash_outflows": sum(
            item["cash_outflows"] for item in records
        ),
        "total_annual_net_cash_flow": sum(
            item["net_cash_flow"] for item in records
        ),
        "total_change_in_surplus": sum(
            item["annual_profit_change"] for item in records
        ),
    }
