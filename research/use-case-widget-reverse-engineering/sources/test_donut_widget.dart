import 'package:flutter/material.dart';
import 'donut_widget.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Donut Widget Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'sans-serif',
      ),
      home: DonutWidgetTestScreen(),
    );
  }
}

class DonutWidgetTestScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Prepare test data according to specification
    final List<DonutSegment> segments = [
      DonutSegment(
        name: 'Liquidity',
        value: 56553.99,
        color: Color(0xFFF3AB40),
      ),
      DonutSegment(
        name: 'Bonds',
        value: 24135.12,
        color: Color(0xFF4D758E),
      ),
      DonutSegment(
        name: 'Equities',
        value: 48415.12,
        color: Color(0xFF888888),
      ),
      DonutSegment(
        name: 'Commodities',
        value: 3567.10,
        color: Color(0xFF8C1C5F),
      ),
    ];
    
    // Calculate total value
    double totalValue = segments.fold(0, (sum, segment) => sum + segment.value);
    
    return Scaffold(
      appBar: AppBar(
        title: Text('Donut Widget Test'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: DonutWidget(
            segments: segments,
            title: 'Total',
            currencySymbol: 'CHF',
            totalValue: totalValue,
          ),
        ),
      ),
    );
  }
}

