# Widget Reverse Engineering with Ollama

Currently, a suitable Small Language Model (SLM) is not available for image inference and local use.

To proceed with the test, it is therefore necessary to use the description of ChatGPT and add it to the prompt for code generation.

**prompt**:
Starting from the following image description: "The image appears to be a dashboard or summary screen of an investment or portfolio overview in Swiss francs (CHF).
At the top, there is a circular (donut-style) chart labeled “Total CHF 99’212.30,” divided into four color-coded segments. Below the chart, there is a list
of four categories, each showing a monetary value and, where applicable, a percentage change and the corresponding gain/loss in CHF:

1. Liquidity: CHF 56’553.99 (no percentage change shown)
2. Bonds: CHF 24’135.12, showing a green arrow with +7.31% and CHF +200.50
3. Equities: CHF 48’415.12, also showing a green arrow with +7.31% and CHF +200.50
4. Commodities: CHF 3’567.10, with a red arrow indicating -0.25% and CHF -56.50

Each category is color-coded in the chart, and the total at the center (99,212.30 CHF) presumably represents the overall value of the portfolio or assets.
The green and red arrows indicate positive or negative performance for the respective categories." I need a flutter implementation of this component,
the implementation should use flutter elements.  The generated code should accept an arbitrary list of categories associated with any amount of money.
The colors used for the categories should match the colors displayed by the donut. The label in the middle of the chart is the sum of the categories.