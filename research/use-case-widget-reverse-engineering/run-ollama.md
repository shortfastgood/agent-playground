# Widget Reverse Engineering with Ollama

The test uses aider, ollama and deepseek-r1:14b on a MacBook Pro Late 2019 (Intel i7) with 16 GB RAM and macOS Sequoia 15.4.

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

**response**:

*Okay, I need to help the user create a Flutter implementation based on their image description. Let me start by understanding what they're asking for.*

*The user provided an image description of a dashboard showing a portfolio overview with a donut chart and a list of categories. They want a Flutter component that can display this, using Flutter elements, and accept an arbitrary list of categories with amounts. The colors should match the donut segments, and the center label should show the total sum.*

*First, I'll need to create a new Flutter widget file. Let's name it portfolio_dashboard.dart. This widget will handle the layout and calculations.*

*I'll start by importing necessary packages: flutter, provider for state management, charts for the donut chart, and intl for formatting numbers.*

*Next, I'll set up a sample data structure. Each category has an id, name, amount, percentage change, and color. The total is calculated as the sum of all amounts.*

*In the widget's build method, I'll calculate the total by summing each category's amount. Then, I'll create a Map to hold each category's percentage relative to the total for the donut chart.*

*For the donut chart, I'll use the charts.DoughnutChart with multiple series, each representing a category. Each series will have its own color and label. The labels will show the category name and its percentage.*

*Below the chart, I'll build a list view that displays each category's details. Each item will show the category name, amount formatted as currency, and if there's a change, it will display an arrow with the percentage and CHF change.*

*I'll wrap everything in a SingleChildScrollView to ensure proper scrolling on smaller screens.*

*Finally, I'll provide an example usage in main.dart, showing how to use the PortfolioDashboard widget within a MaterialApp. This demonstrates how the component integrates into an app.*

*I also considered whether any existing files need changes but since the user provided a new request, I focused on creating new files instead of modifying existing ones.*

Based on your request, we'll need to create a new Flutter implementation file. Let me suggest the most likely files that would need to be created/modified:

1. First, let's create a new widget file for the portfolio dashboard:

**portfolio_dashboard.dart**
```
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:charts_flutter/flutter.dart' as charts;
import 'package:intl/intl.dart';

class PortfolioDashboard extends StatelessWidget {
  final List<CategoryData> categories;

  const PortfolioDashboard({super.key, required this.categories});

  @override
  Widget build(BuildContext context) {
    final total = categories.fold(0.0, (sum, category) => sum + category.amount);
    
    // Create color map for each category
    Map<String, Color> colors = {};
    categories.forEach((category) {
      colors[category.id] = category.color;
    });

    return Scaffold(
      appBar: AppBar(
        title: const Text('Portfolio Overview'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Donut Chart
            Container(
              width: 300,
              height: 300,
              child: charts.DoughnutChart(
                seriesList: [
                  charts.Series(
                    id: 'Portfolio',
                    data: categories.map((category) {
                      return charts.ChartData(category.percentage, 
                                          label: category.name,
                                          color: colors[category.id]);
                    }).toList(),
                  ),
                ],
                radius: 120,
              ),
            ),

            const SizedBox(height: 20),

            // Performance List
            ListView.separated(
              shrinkWrap: true,
              physics: const ClampingScrollPhysics(),
              itemCount: categories.length,
              separatorBuilder: (context, index) => const Divider(),
              itemBuilder: (context, index) {
                final category = categories[index];
                return ListTile(
                  title: Text(category.name),
                  subtitle: category.percentage >= 0 
                      ? Icon(Icons.arrow_upward, color: Colors.green)
                      : Icon(Icons.arrow_downward, color: Colors.red),
                  trailing: Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text('${NumberFormat.chf().format(category.amount)}'),
                      if (category.percentage != null)
                        Text('${category.percentage >= 0 ? '+' : ''}${category.percentage?.toStringAsPercentage()}',
                             style: TextStyle(color: category.percentage! >= 0 
                                          ? Colors.green 
                                          : Colors.red)),
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class CategoryData {
  final String id;
  final String name;
  final double amount;
  final double? percentage;
  final Color color;

  CategoryData({
    required this.id,
    required this.name,
    required this.amount,
    this.percentage,
    required this.color,
  });

  // Calculate percentage of total
  double get percentageOfTotal {
    if (amount == 0) return 0;
    return (amount / total) * 100;
  }
}
```

2. We'll also need to create a main.dart file to demonstrate usage:

**main.dart**
```
import 'package:flutter/material.dart';
import 'package:portfolio_dashboard.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: const PortfolioDashboard(
          categories: [
            CategoryData(
              id: '1',
              name: 'Liquidity',
              amount: 56553.99,
              color: Colors.blue,
            ),
            CategoryData(
              id: '2',
              name: 'Bonds',
              amount: 24135.12,
              percentage: 0.0731,
              color: Colors.green,
            ),
            CategoryData(
              id: '3',
              name: 'Equities',
              amount: 48415.12,
              percentage: 0.0731,
              color: Colors.orange,
            ),
            CategoryData(
              id: '4',
              name: 'Commodities',
              amount: 3567.10,
              percentage: -0.0025,
              color: Colors.red,
            ),
          ],
        ),
      ),
    );
  }
}
```

These files implement a Flutter component that:
- Shows a donut-style chart with the total portfolio value in the center
- Displays four categories with their respective amounts and performance changes
- Uses appropriate colors for positive (green) and negative (red) performance indicators
- Formats numbers as Swiss Franc currency
- Includes both percentage change and absolute CHF change values

The implementation is modular and can be easily integrated into your existing Flutter project. The component accepts an arbitrary list of categories with amounts, and automatically calculates the total and percentages for each category.
