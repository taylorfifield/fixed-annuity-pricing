
# Actuarial Methodology

## 1. Objective

This project models a hypothetical homogeneous portfolio of fixed deferred annuities over 10 years.

The objective is to analyze how investment returns, policyholder interest crediting, withdrawals, surrenders, and expenses affect insurer assets and surplus.

The model is deterministic and operates on annual time steps.

## 2. Initial Conditions

At time zero:

- Policyholders deposit a combined premium of $100,000.
- The insurer receives $100,000 in assets.
- Policyholder account liabilities equal $100,000.
- Initial insurer surplus is zero.
- The portfolio contains 100 identical hypothetical policies.

There are no additional premiums or acquisition expenses.

## 3. Annual Timing Convention

All calculations follow the same order:

1. Calculate investment income using opening insurer assets.
2. Calculate credited interest using opening account balances.
3. Add credited interest to policyholder liabilities.
4. Calculate partial withdrawals on balances after interest.
5. Calculate gross full surrenders on remaining balances.
6. Deduct surrender charges from surrender cash payments.
7. Calculate operating expenses using opening balances.
8. Determine closing assets and liabilities.
9. Calculate insurer surplus.

All transactions are aggregated into annual reporting periods.

## 4. Model Equations

Let:

- A(t) = insurer assets at the beginning of year t
- B(t) = policyholder account balance at the beginning of year t
- r = annual investment return
- c = annual credited interest rate
- w = annual partial withdrawal rate
- s = annual full surrender rate
- k = surrender charge rate
- e = annual operating expense rate

### Investment Income

Investment income is:

I(t) = A(t) × r

Investment income is modeled as a realized cash inflow and remains within insurer assets unless used for payments.

### Credited Interest

Interest credited to policyholder accounts is:

C(t) = B(t) × c

This increases the policyholder account liability.

### Account Balance After Crediting

BC(t) = B(t) + C(t)

### Partial Withdrawals

W(t) = BC(t) × w

Partial withdrawals are cash paid to policyholders and reduce their account balances by the same amount.

### Gross Full Surrenders

S(t) = [BC(t) - W(t)] × s

This represents the account value associated with the expected proportion of policies surrendering their entire remaining balances.

### Surrender Charges

SC(t) = S(t) × k

### Cash Paid on Surrender

SP(t) = S(t) - SC(t)

The insurer removes the full surrendered account value from liabilities but pays the amount after charges.

Surrender charges are amounts withheld, not separate cash receipts.

### Operating Expenses

E(t) = B(t) × e

Operating expenses are paid from insurer assets.

### Closing Policyholder Balances

B(t+1) = BC(t) - W(t) - S(t)

### Closing Insurer Assets

A(t+1) = A(t) + I(t) - W(t) - SP(t) - E(t)

### Annual Net Asset Cash Flow

NetCashFlow(t) = I(t) - W(t) - SP(t) - E(t)

This excludes the initial premium because it occurs at time zero.

### Insurer Surplus

Surplus(t) = A(t) - B(t)

### Annual Change in Surplus

ChangeInSurplus(t) = Surplus(t+1) - Surplus(t)

Algebraically:

ChangeInSurplus(t) = I(t) - C(t) + SC(t) - E(t)

This identity is used for model reconciliation.

## 5. Profitability Interpretation

Terminal surplus is the main financial measure.

It represents the difference between projected insurer assets and remaining policyholder account liabilities at the end of 10 years.

The change in surplus reflects investment earnings, interest credited, surrender charges, and expenses under the model's simplified accounting assumptions.

It does not represent:

- Discounted present value of insurer profits
- Market-consistent embedded value
- Statutory earnings
- Risk-adjusted pricing profit
- Available regulatory capital
- Guaranteed cash available for distribution

The remaining annuity liabilities after year 10 are not treated as expired or settled.

## 6. Policyholder Behavior

The portfolio is homogeneous.

Every active policy has the same average account value and is subject to the same modeled partial withdrawal assumption.

Full surrenders are modeled using expected proportions of remaining policies.

Expected active policy count evolves as:

ActivePolicies(t+1) = ActivePolicies(t) × (1 - s)

Expected counts may be fractional because this is an aggregate actuarial expectation rather than a simulation of specific individuals.

Partial withdrawals do not reduce the number of active policies.

## 7. Interest-Rate Source

The model includes published Treasury yield observations from FRED.

Series ID: DGS10

Series name: Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis.

Original source: Board of Governors of the Federal Reserve System.

URL: https://fred.stlouisfed.org/series/DGS10

Units: Percent per annum, not seasonally adjusted.

Observation dates:

- October 1, 2026
- October 2, 2026
- October 5, 2026
- October 6, 2026
- October 7, 2026

The final included observation is 5.28%, converted to 0.0528 for the annual model.

This rate is an illustrative constant investment-return proxy. It is not an estimate of actual realized investment performance, portfolio yield, or future returns.

A real annuity pricing study would require an investment strategy, asset cash-flow projection, reinvestment assumptions, and risk modeling.

## 8. Sensitivity Methodology

The model evaluates changes of:

- -100 basis points
- 0 basis points
- +100 basis points

for each of four assumptions:

- Investment return
- Credited interest rate
- Partial withdrawal rate
- Full surrender rate

One basis point equals 0.01 percentage point.

Each one-way scenario changes only one assumption and then repeats the entire projection.

The two-way sensitivity grid changes investment return and credited interest rate together.

Grid shocks are:

- -100 basis points
- -50 basis points
- 0 basis points
- +50 basis points
- +100 basis points

The grid contains 25 separate financial projections.

## 9. Validation Approach

The automated test suite contains both known numerical examples and general financial reconciliation checks.

Important tests include:

- Asset conservation through cash-flow reconciliation
- Account-balance conservation
- Interest-crediting accuracy
- Investment-income accuracy
- Surrender charge and payment consistency
- Annual surplus-change consistency
- Year-to-year continuity
- Invalid financial input rejection
- Excel formula presence
- Investment-return sensitivity direction

These checks help find coding errors and inconsistent assumptions.

They cannot establish whether the simplified assumptions are realistic for any actual insurer.

## 10. Excel Implementation

The workbook is generated using openpyxl.

It includes live Excel formulas referencing assumption cells.

The Python and Excel models use equivalent financial equations.

The workbook is independently usable after generation. Changing Excel inputs recalculates Excel results but does not modify the repository's Python output files.

Because openpyxl is not a spreadsheet calculation engine, Excel formulas may lack cached results until Microsoft Excel or compatible software recalculates them.

The 10-year horizon is fixed within the generated workbook. Other financial inputs are editable.

## 11. Important Limitations

The model excludes:

- Mortality
- Detailed lapse studies
- Dynamic policyholder behavior
- Contract-specific guarantees
- Crediting-rate floors and resets
- Asset-liability duration matching
- Fixed-income security valuation
- Reinvestment and default risk
- Liquidity constraints
- Policy commissions
- Acquisition expenses
- Taxes
- Statutory and financial reporting reserves
- Risk-based capital
- Stochastic simulations
- Required financing when projected assets become insufficient
- Discounted cash-flow pricing

The surrender charge percentage is held constant throughout the projection rather than following a real contract's surrender-charge schedule.

The model should be interpreted as an introductory financial modeling exercise, not a pricing recommendation.

## 12. Reproducibility

All project assumptions and source observations are stored in the repository.

GitHub Actions installs the required packages, executes tests, generates the outputs, and makes them available as downloadable workflow artifacts.

The repository contains the source code and instructions needed to reproduce the calculations.
