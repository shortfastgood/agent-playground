import 'package:flutter/material.dart';
import 'dart:math';

class DonutSegment {
  final String name;
  final double value;
  final Color color;

  DonutSegment({
    required this.name,
    required this.value,
    required this.color,
  });
}

class DonutWidget extends StatefulWidget {
  final List<DonutSegment> segments;
  final String title;
  final String currencySymbol;
  final double totalValue;
  final double aspectRatio;

  DonutWidget({
    Key? key,
    List<DonutSegment>? segments,
    this.title = 'Total',
    this.currencySymbol = 'CHF',
    double? totalValue,
    this.aspectRatio = 360 / 640,
  })  : segments = segments ?? [],
        totalValue = totalValue ?? segments?.fold<double>(0, (sum, segment) => sum + segment.value) ?? 0,
        super(key: key);

  @override
  _DonutWidgetState createState() => _DonutWidgetState();
}

class _DonutWidgetState extends State<DonutWidget> {
  @override
  Widget build(BuildContext context) {
    // Get current orientation
    final isLandscape = MediaQuery.of(context).orientation == Orientation.landscape;
    
    if (isLandscape) {
      return Container(
        decoration: BoxDecoration(
          color: Colors.white,
          border: Border.all(color: Colors.grey[300]!),
        ),
        child: Row(
          children: [
            // Fixed size container for the donut chart
            SizedBox(
              width: MediaQuery.of(context).size.height * widget.aspectRatio,
              child: _buildDonutChart(),
            ),
            Container(
              width: 1,
              height: double.infinity,
              margin: EdgeInsets.symmetric(vertical: 10),
              color: Colors.grey[300],
            ),
            // Expanded container for the legend
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(10.0),
                child: _buildLegend(),
              ),
            ),
          ],
        ),
      );
    } else {
      // Portrait mode - keep the original layout
      return AspectRatio(
        aspectRatio: widget.aspectRatio,
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            border: Border.all(color: Colors.grey[300]!),
          ),
          child: Column(
            children: [
              Expanded(
                flex: 1,
                child: _buildDonutChart(),
              ),
              Container(
                height: 1,
                margin: EdgeInsets.only(left: 10, right: 10),
                color: Colors.grey[300],
              ),
              Expanded(
                flex: 1,
                child: Padding(
                  padding: const EdgeInsets.only(left: 10, right: 10, top: 10, bottom: 10),
                  child: _buildLegend(),
                ),
              ),
            ],
          ),
        ),
      );
    }
  }

  Widget _buildDonutChart() {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10.0),
      child: Center(
        child: LayoutBuilder(
          builder: (context, constraints) {
            double donutSize = min(constraints.maxWidth, constraints.maxHeight) * 0.9;
            return SizedBox(
              width: donutSize,
              height: donutSize,
              child: CustomPaint(
                painter: DonutChartPainter(
                  segments: widget.segments,
                  title: widget.title,
                  currencySymbol: widget.currencySymbol,
                  totalValue: widget.totalValue,
                  reference: Size(360, 320), // Half of reference screen height for chart
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildLegend() {
    return ListView.builder(
      itemCount: widget.segments.length,
      itemBuilder: (context, index) {
        final segment = widget.segments[index];
        final formattedValue = _formatValue(segment.value);
        
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 5.0),
          child: Row(
            children: [
              Container(
                width: 15,
                height: 15,
                color: segment.color,
                margin: EdgeInsets.only(right: 5),
              ),
              Expanded(
                child: Text(
                  segment.name,
                  style: TextStyle(
                    fontSize: 16,
                    fontFamily: 'sans-serif',
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
              SizedBox(width: 5),
              Row(
                children: [
                  Text(
                    widget.currencySymbol,
                    style: TextStyle(
                      fontSize: 18,
                      fontFamily: 'sans-serif',
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  SizedBox(width: 5),
                  Text(
                    formattedValue,
                    style: TextStyle(
                      fontSize: 18,
                      fontFamily: 'sans-serif',
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }

  String _formatValue(double value) {
    String stringValue = value.toStringAsFixed(2);
    List<String> parts = stringValue.split('.');
    
    String integerPart = parts[0];
    String formattedInteger = '';
    
    for (int i = 0; i < integerPart.length; i++) {
      if (i > 0 && (integerPart.length - i) % 3 == 0) {
        formattedInteger += '\'';
      }
      formattedInteger += integerPart[i];
    }
    
    return '$formattedInteger.${parts[1]}';
  }
}

class DonutChartPainter extends CustomPainter {
  final List<DonutSegment> segments;
  final String title;
  final String currencySymbol;
  final double totalValue;
  final Size reference;

  DonutChartPainter({
    required this.segments,
    required this.title,
    required this.currencySymbol,
    required this.totalValue,
    required this.reference,
  });

  @override
  void paint(Canvas canvas, Size size) {
    // Calculate the scaling factor based on reference size
    final scale = size.width / reference.width;
    
    final center = Offset(size.width / 2, size.height / 2);
    final radius = min(center.dx, center.dy) - (8 * scale); // Account for border
    final strokeWidth = 25.0 * scale;
    final segmentGap = 0.2; // Gap between segments in radians (increased 10x)
    
    // Draw outer border
    final borderPaint = Paint()
      ..color = Colors.grey[300]!
      ..style = PaintingStyle.stroke
      ..strokeWidth = 8 * scale;
    
    canvas.drawCircle(center, radius + (strokeWidth / 2) + (8 * scale), borderPaint);
    
    // Calculate total for proportions
    double total = segments.fold(0, (sum, segment) => sum + segment.value);
    if (total <= 0) return;
    
    // Draw donut segments
    double startAngle = -pi / 2; // Start at 12 o'clock
    
    for (var segment in segments) {
      final sweepAngle = (2 * pi * segment.value / total) - segmentGap;
      
      final segmentPaint = Paint()
        ..color = segment.color
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round
        ..strokeWidth = strokeWidth;
        
      canvas.drawArc(
        Rect.fromCircle(center: center, radius: radius),
        startAngle,
        sweepAngle,
        false,
        segmentPaint,
      );
      
      startAngle += sweepAngle + segmentGap;
    }
    
    // Draw center text
    final titleTextStyle = TextStyle(
      color: Colors.black,
      fontSize: 26 * scale,  // Updated from 20 to 26
      fontFamily: 'sans-serif',
      fontWeight: FontWeight.w700,  // Updated from w500 to w700
    );
    
    final currencyTextStyle = TextStyle(
      color: Colors.black,
      fontSize: 30 * scale,  // Updated from 24 to 30
      fontFamily: 'sans-serif',
      fontWeight: FontWeight.w700,  // Updated from w500 to w700
    );
    
    final valueTextStyle = TextStyle(
      color: Colors.black,
      fontSize: 30 * scale,  // Updated from 20 to 30
      fontFamily: 'sans-serif',
      fontWeight: FontWeight.w700,  // Updated from w500 to w700
    );
    
    // Render title
    final titleSpan = TextSpan(
      text: title,
      style: titleTextStyle,
    );
    
    final titlePainter = TextPainter(
      text: titleSpan,
      textDirection: TextDirection.ltr,
      textAlign: TextAlign.center,
    );
    
    titlePainter.layout();
    
    // Render value with currency symbol
    final formattedValue = _formatValue(totalValue);
    final valueSpan = TextSpan(
      children: [
        TextSpan(text: currencySymbol, style: currencyTextStyle),
        TextSpan(text: ' $formattedValue', style: valueTextStyle),
      ],
    );
    
    final valuePainter = TextPainter(
      text: valueSpan,
      textDirection: TextDirection.ltr,
      textAlign: TextAlign.center,
    );
    
    valuePainter.layout();
    
    // Position and draw text
    final titlePosition = center.translate(-titlePainter.width / 2, -valuePainter.height / 2 - 5);
    final valuePosition = center.translate(-valuePainter.width / 2, 5);
    
    titlePainter.paint(canvas, titlePosition);
    valuePainter.paint(canvas, valuePosition);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
  
  String _formatValue(double value) {
    String stringValue = value.toStringAsFixed(2);
    List<String> parts = stringValue.split('.');
    
    String integerPart = parts[0];
    String formattedInteger = '';
    
    for (int i = 0; i < integerPart.length; i++) {
      if (i > 0 && (integerPart.length - i) % 3 == 0) {
        formattedInteger += '\'';
      }
      formattedInteger += integerPart[i];
    }
    
    return '$formattedInteger.${parts[1]}';
  }
}
