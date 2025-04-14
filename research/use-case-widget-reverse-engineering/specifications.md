# Donut Widget Specification

## Requirements

- The widget is divided vertically into two equal sections: the top section for the donut chart and the bottom section for the legend.
- The donut widget should be a circular chart that displays data in a donut shape.
- The legend should display the labels and values of each segment of the donut chart.
- The data is composed by a list of items in a portfolio, each with a name and a value.
- The donut chart should be able to display a maximum of 10 segments.
- The legend should display the name and value of each segment in the donut chart.
- The legend should be scrollable if the number of segments exceeds the available space.
- The legend should be displayed in a vertical list format.
- In the middle of the donut, there should be a label that displays the total value of all segments combined.

## Graphics
- The whole widget should be dynamic and responsive to the size of the container.
- The donut displays the data in a circular format, with each segment representing a different category.
- The segments should be color-coded to represent different categories.
- The segments aren't contiguous, but rather separated by a small gap to create the donut effect.
- The donut should have a hole in the center, which is the same color as the background of the widget.
- The donut should have an outer border.
- The donut container should have a padding of 10 pixels vertically.
- The donut and the legend are separated by a 1 pixel horizontal line. 
- The line begins after 10 pixels of padding from the left and ends 10 pixels before the right of the widget.
- The legend should have a padding of 10 pixels on the left and right.
- The legend should have a margin of 10 pixels on the top and bottom.
- The legend label is left-aligned and preceded by a colored square that matches the color of the segment in the donut chart.
- The legend value is right-aligned and preceded by the currency symbol.
- The label in the middle of the donut consists of a title and a value that are centered in the donut. The title is displayed above the value. The currency symbol is displayed before the value.
- The reference screen resolution is 360x640 pixels, this is also the minimum size of the widget and the aspect ratio of the widget.
- If the screen is rotated to landscape:
  - The donut chart maintains its size and remains in the center of its container
  - The division line becomes vertical and runs down the full height of the widget
  - The legend expands to use the remaining width of the screen
  - The widget uses a Row layout instead of a Column layout, with the donut on the left side and the legend on the right

## Styling

- The widget background should be white.
- The separation line should be a light gray color.
- The donut should have an 8 px width light gray border. The gap between the segments and the border should be 8 pixels.
- The donut segments should be 25 pixels width.
- The values should be displayed using ' as the thousands separator and '.' as the decimal separator.
- The font used for the labels, title and values should be a sans-serif font. 
- On the reference screen, the default font size should be 16 pixels. The font size should scale proportionally to the size of the widget.
- On the reference screen, the font size of the values in the legend should be 18 pixels. The font size should scale proportionally to the size of the widget.
- On the reference screen, the font size of the donut currency symbol and of the donut value should be 30 pixels. The font size should scale proportionally to the size of the widget.
- On the reference screen, the font size of the donut title should be 26 pixels. The font size should scale proportionally to the size of the widget.
- The default font weight should be normal. The font weight of the labels in the legend, of the donut title, donut of the currency symbol and of the donut value should be 700.
- The gap between currency symbol and value is 5 pixels.
- The gap between the colored square and the label in the legend is 5 pixels.
- The default color of the text should be black.

## Interface

- The widget should have a method to set the data for the donut chart and legend.
- The widget should have a method to set the title of the donut chart.
- The widget should have a method to set the currency symbol.
- The widget should have a method to set the value of the value in the middle of the donut.

## Testing

- The test program should create a donut widget and set the data, title, currency symbol and value.
- The colors of the segments are #F3AB40, #4D758E, #888888, #8C1C5F.
- The labels of the segments are "Liquidity", "Bonds", "Equities", "Commodities".
- The values of the segments are 56553.99, 24135,12, 48415.12, 3567.10.

## Coding

- The code should be written in Dart and use the Flutter framework.
- Expected are two files:
  - donut_widget.dart: the widget implementation
  - test_donut_widget.dart: the test program
