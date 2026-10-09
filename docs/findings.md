
# Findings and Sensitivity Analysis

## Fixed Annuity Pricing & Sensitivity Analysis

**Status:** Completed and successfully executed

**Validation:** Automated tests passed through GitHub Actions

**Execution:** October 8, 2026

---

## 1. Executive Summary

This project evaluates the financial performance of a hypothetical fixed deferred annuity portfolio over a 10-year projection period.

The model calculates insurer assets, policyholder account liabilities, investment income, credited interest, withdrawals, surrender payments, operating expenses, and insurer surplus.

Under the base assumptions, the model produced:

- **Ending insurer assets:** $74,577.53
- **Ending policyholder liabilities:** $57,573.85
- **Ending insurer surplus:** $17,003.68

The positive terminal surplus indicates that projected insurer assets exceeded remaining policyholder account liabilities under the selected assumptions.

Sensitivity analysis identified investment returns and credited interest rates as the two most influential financial drivers.

A combined adverse scenario, involving lower investment returns and higher credited interest rates, generated a negative terminal surplus of $3,532.48.

These findings illustrate how changes in asset earnings and policyholder obligations can materially influence an annuity portfolio's financial position.

The analysis is educational and does not represent actual insurer profitability, statutory reserves, or regulatory capital adequacy.

---

## 2. Base Scenario Assumptions

The model begins with $100,000 in aggregate premium deposits across 100 hypothetical policies.

| Assumption | Base Value |
|---|---:|
| Initial premium | $100,000 |
| Initial policy count | 100 |
| Projection period | 10 years |
| Annual investment return | 5.28% |
| Annual credited interest rate | 3.25% |
| Annual partial withdrawal rate | 2.50% |
| Annual full surrender rate | 6.00% |
| Surrender charge rate | 2.00% |
| Annual operating expense rate | 0.50% |

The investment return uses the latest included DGS10 observation in the project's interest-rate CSV, dated October 7, 2026.

The other financial assumptions are hypothetical values selected for educational modeling.

Investment earnings are calculated on opening insurer assets, while credited interest is calculated on opening policyholder account balances.

Partial withdrawals and full surrenders reduce policyholder liabilities and generate cash payments.

Operating expenses reduce insurer assets.

---

## 3. Base Scenario Financial Results

The model generated the following cumulative financial results over 10 years.

| Financial Measure | Result |
|---|---:|
| Initial insurer assets | $100,000.00 |
| Total investment income | $45,669.13 |
| Total credited interest | $25,670.33 |
| Total partial withdrawals | $20,388.17 |
| Total gross surrenders | $47,708.31 |
| Total surrender cash payouts | $46,754.14 |
| Total surrender charges retained | $954.17 |
| Total operating expenses | $3,949.28 |
| Total annual cash inflows | $45,669.13 |
| Total annual cash outflows | $71,091.59 |
| Total annual net asset cash flow | -$25,422.47 |
| **Ending insurer assets** | **$74,577.53** |
| **Ending policyholder liabilities** | **$57,573.85** |
| **Ending insurer surplus** | **$17,003.68** |
| Remaining expected active policies | 53.86 |

### Interpretation

Although insurer assets declined from $100,000 to $74,577.53, policyholder account liabilities declined further, to $57,573.85.

The insurer earned $45,669.13 in cumulative investment income while crediting $25,670.33 in interest to policyholders.

Surrender charges contributed $954.17 toward the insurer's financial results, while operating expenses reduced surplus by $3,949.28.

Under the model's simplified accounting convention:

**Change in surplus = Investment income - Credited interest + Surrender charges - Operating expenses**

The resulting change in surplus was approximately $17,003.68. Small differences when combining displayed amounts may arise from rounding to cents.

The insurer's total annual net cash flow was negative because withdrawals, surrender payouts, and expenses exceeded annual investment cash inflows.

However, negative asset cash flow does not necessarily imply negative surplus. Withdrawals and surrenders also reduce the liabilities owed to policyholders.

### Important Financial Distinction

The $17,003.68 ending surplus is an asset-minus-account-liability measure.

It should not be interpreted as:

- Net accounting income
- Discounted economic profit
- Distributable shareholder earnings
- Statutory capital
- Risk-adjusted actuarial profit

The model does not value the full future cost of remaining policyholder obligations beyond year 10.

---

## 4. Ten-Year Financial Development

The model produced positive annual changes in insurer surplus throughout the base projection.

| Year | Ending Insurer Surplus |
|---|---:|
| 1 | $1,650.80 |
| 2 | $3,300.10 |
| 3 | $4,952.57 |
| 4 | $6,612.88 |
| 5 | $8,285.73 |
| 6 | $9,975.80 |
| 7 | $11,687.83 |
| 8 | $13,426.59 |
| 9 | $15,196.90 |
| 10 | $17,003.68 |

### Interpretation

The model's surplus increases consistently over the projection period.

This reflects the combined effects of investment income, interest crediting, operating expenses, and surrender charges.

The result is specific to the selected assumptions and deterministic model structure.

It does not establish that a real annuity portfolio would generate consistent annual profits.

### Policyholder Behavior

The expected number of remaining active policies declines from 100 to approximately 53.86 by year 10.

The model uses expected policy counts, which may be fractional. These figures represent an aggregate actuarial expectation rather than individual contracts.

---

## 5. One-Way Sensitivity Analysis

The analysis measures the effect of changing one financial assumption while holding all other assumptions constant.

Each assumption is tested at:

- 100 basis points below the base rate
- The base rate
- 100 basis points above the base rate

One basis point equals 0.01 percentage point.

Each scenario recalculates the entire 10-year projection.

### Results

The table shows ending insurer surplus under each scenario.

| Assumption Changed | -100 bps | Base | +100 bps |
|---|---:|---:|---:|
| Investment return | $6,371.19 | $17,003.68 | $28,734.06 |
| Credited interest | $26,352.57 | $17,003.68 | $6,957.56 |
| Partial withdrawal | $17,666.92 | $17,003.68 | $16,372.49 |
| Full surrender | $17,462.88 | $17,003.68 | $16,561.88 |

### 5.1 Investment Return Sensitivity

Reducing the annual investment return from 5.28% to 4.28% decreased terminal surplus to $6,371.19.

Increasing the annual investment return from 5.28% to 6.28% increased terminal surplus to $28,734.06.

The higher-return scenario produced approximately $11,730.38 more terminal surplus than the base scenario.

**Finding:** Investment returns were the largest individual driver of terminal surplus within the tested one-way scenarios.

This result demonstrates the importance of asset earnings in supporting fixed annuity obligations.

### 5.2 Credited Interest Sensitivity

Reducing the credited interest rate from 3.25% to 2.25% increased terminal surplus to $26,352.57.

Increasing the credited interest rate from 3.25% to 4.25% reduced terminal surplus to $6,957.56.

The higher-crediting scenario produced approximately $10,046.12 less terminal surplus than the base scenario.

**Finding:** Higher credited interest reduces modeled surplus because it increases policyholder liabilities.

Investment returns and credited interest rates therefore have opposing effects on the insurer's simplified financial position.

### 5.3 Partial Withdrawal Sensitivity

Reducing the partial withdrawal assumption from 2.50% to 1.50% increased terminal surplus to $17,666.92.

Increasing the partial withdrawal assumption to 3.50% reduced terminal surplus to $16,372.49.

**Finding:** Higher partial withdrawals modestly reduced terminal surplus in this model.

Withdrawals reduce both insurer assets and policyholder liabilities.

Their overall impact also depends on how lower future balances affect investment earnings, credited interest, and expenses.

### 5.4 Full Surrender Sensitivity

Reducing the full surrender assumption from 6.00% to 5.00% increased terminal surplus to $17,462.88.

Increasing the full surrender assumption to 7.00% reduced terminal surplus to $16,561.88.

**Finding:** Higher surrender rates produced a modest reduction in terminal surplus under the modeled assumptions.

Although surrender charges provide a financial benefit, surrenders also reduce the assets available to generate future investment income.

The net effect depends on the interaction of these factors.

---

## 6. Two-Way Interest-Rate Sensitivity

The model also evaluated combinations of investment returns and credited interest rates.

Both rates were tested at changes of:

- -100 basis points
- -50 basis points
- 0 basis points
- +50 basis points
- +100 basis points

This produced 25 scenarios.

### Best Scenario

| Assumption | Value |
|---|---:|
| Annual investment return | 6.28% |
| Annual credited interest | 2.25% |
| **Ending insurer surplus** | **$38,226.68** |

This scenario produced the highest terminal surplus in the tested grid.

The combination of higher investment earnings and lower credited interest improved the insurer's financial position.

### Worst Scenario

| Assumption | Value |
|---|---:|
| Annual investment return | 4.28% |
| Annual credited interest | 4.25% |
| **Ending insurer surplus** | **-$3,532.48** |

This scenario produced the lowest terminal surplus in the tested grid.

It demonstrates that a narrowing investment-versus-crediting spread can materially weaken the insurer's financial position.

Operating expenses and other modeled cash flows may produce negative surplus even when the investment return is slightly above the credited interest rate.

### Overall Finding

Of the 25 combinations tested:

- 24 produced positive terminal surplus.
- 1 produced negative terminal surplus.

These are deterministic scenarios, not probabilities or forecasts.

The proportion of negative scenarios should not be interpreted as an estimate of the probability of insurer insolvency.

---

## 7. Key Actuarial Findings

### Finding 1: Investment Returns Were the Most Influential Assumption

Changes in investment return produced the largest movements in terminal surplus across the tested one-way sensitivity scenarios.

This highlights the importance of investment performance in a fixed annuity portfolio.

### Finding 2: Credited Interest Was a Major Financial Driver

Higher credited interest increased policyholder account liabilities and reduced insurer surplus.

The relationship between investment returns and credited interest is central to the financial performance of fixed annuities.

### Finding 3: Policyholder Behavior Affected Financial Outcomes

Changes in withdrawal and surrender assumptions had smaller effects than the tested interest-rate changes.

However, these assumptions influenced cash payments, remaining assets, policyholder liabilities, and future earnings.

### Finding 4: Positive Interest-Rate Spread Alone Was Not Sufficient

The worst combined scenario generated negative terminal surplus despite a slightly positive difference between the investment return and the credited rate.

This demonstrates why insurer profitability should not be measured solely as investment earnings minus credited interest.

Expenses and other contractual cash-flow effects must also be considered.

### Finding 5: Scenario Analysis Revealed Financial Vulnerability

The base scenario produced positive terminal surplus, but a plausible hypothetical change in two assumptions generated a projected shortfall.

This illustrates why actuarial analysis must evaluate multiple scenarios rather than relying exclusively on one set of assumptions.

---

## 8. Financial Visualizations

The successful workflow generated four charts:

| Chart | Purpose |
|---|---|
| `account_and_assets.png` | Compares insurer assets with policyholder liabilities |
| `investment_vs_crediting.png` | Compares annual investment income with credited interest |
| `one_way_sensitivity.png` | Shows surplus changes under individual assumption shocks |
| `investment_crediting_heatmap.png` | Illustrates joint investment and credited-rate sensitivity |

These charts are included in the downloadable GitHub Actions artifact under `charts/`.

They support the interpretation of the model and provide visual evidence of the financial relationships discussed above.

---

## 9. Model Validation

The project includes automated tests covering:

- Assumption validation
- Investment income calculations
- Credited interest calculations
- Partial withdrawals
- Full surrenders
- Surrender charges
- Known numerical examples
- Account-balance reconciliation
- Insurer asset reconciliation
- Annual surplus reconciliation
- Year-to-year continuity
- Sensitivity direction
- Excel workbook formula presence

The automated validation stage passed during GitHub Actions Run #4.

The workflow then successfully generated the baseline projection, Excel workbook, sensitivity data, and financial visualizations.

This establishes that the implemented checks passed and the project executed successfully.

It does not establish that the model is appropriate for production insurance pricing or regulatory reporting.

Excel formulas were generated using openpyxl. A compatible spreadsheet application is required to calculate their values.

---

## 10. Model Limitations

This model is deliberately simplified for educational purposes.

It does not include:

- Mortality assumptions
- Individual policy-level projections
- Dynamic policyholder behavior
- Stochastic interest-rate scenarios
- Fixed-income asset valuation
- Asset defaults and reinvestment risk
- Liquidity constraints
- Contract-specific guarantees
- Acquisition expenses and commissions
- Taxes
- Regulatory reserves
- Risk-based capital
- Discounted present value of future earnings
- Financial obligations beyond the modeled projection horizon

The investment-return assumption is based on an illustrative Treasury yield reference rather than a modeled investment portfolio.

Surrender rates, withdrawal rates, and credited interest assumptions are hypothetical.

The financial findings should not be interpreted as a recommendation regarding any real insurance product.

---

## 11. Conclusion

The completed 10-year fixed annuity model produced $74,577.53 in insurer assets and $57,573.85 in remaining policyholder account liabilities, resulting in positive terminal surplus of $17,003.68.

Sensitivity analysis demonstrated that investment returns and credited interest rates were the dominant drivers of financial performance among the tested assumptions.

A combined adverse scenario produced a negative terminal surplus of $3,532.48, illustrating the potential impact of an unfavorable interest-rate relationship.

The project demonstrates practical introductory actuarial skills in:

- Financial projection modeling
- Insurance cash-flow analysis
- Assumption development and validation
- Spreadsheet modeling
- Scenario and sensitivity analysis
- Automated testing
- Financial visualization
- Interpretation and communication of results

Overall, the analysis shows how a simplified actuarial model can be used to evaluate financial relationships, identify key assumptions, and communicate the implications of changing insurance and investment conditions.

---

## 12. Supporting Results

All numerical findings were derived from the successfully executed Python model.

Relevant generated files include:

- `summary.json`
- `annual_projection.csv`
- `sensitivity_results.csv`
- `sensitivity_grid.csv`
- `sensitivity_summary.json`
- `fixed_annuity_model.xlsx`

These files are available in the `annuity-analysis-results` artifact associated with the successful GitHub Actions workflow.


Results reflect the model assumptions and source-data snapshot used for that execution. Rerunning the model with updated inputs may produce different results.
