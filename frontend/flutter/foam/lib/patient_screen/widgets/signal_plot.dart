import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;
import 'package:http/http.dart' as http;

import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class SignalPlot extends StatefulWidget {
  final int signalId;
  final int windowSec;
  final int decimalPlaces;
  final double minY;
  final double maxY;
  late List<FlSpot> samples;
  SignalPlot({
    super.key,
    required this.signalId,
    required this.windowSec,
    required this.decimalPlaces,
    required this.minY,
    required this.maxY,
    required this.samples,
  });

  @override
  State<SignalPlot> createState() => _SignalPlotState();
}

class _SignalPlotState extends State<SignalPlot> {
  final Color sinColor = Colors.redAccent;

  double xValue = 0;

  late Timer timer;

  List<Color> gradientColors = [
    const Color(0xff23b6e6),
    const Color(0xff02d39a),
  ];

  bool alarmTriggered = false;

  Future fetchSamples() async {
    List<FlSpot> temp = [];
    final response = await http.get(Uri.parse(
        'https://no1rz2.deta.dev/signals/last/seconds/${widget.signalId}?seconds=${widget.windowSec}'));
    final List samplesJson = jsonDecode(response.body)['signal_values'];
    alarmTriggered = jsonDecode(response.body)['alarm_triggered'];
    xValue = 0;
    for (int i = 0; i < samplesJson.length; i++) {
      temp.add(
        FlSpot(xValue, samplesJson[i].toDouble()),
      );
      xValue += widget.windowSec / samplesJson.length;
    }

    widget.samples = temp;
  }

  @override
  void initState() {
    super.initState();
    // monitorDisplay = widget.samples.last;
    timer = Timer.periodic(const Duration(milliseconds: 700), (timer) {
      setState(() {
        fetchSamples();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.fromLTRB(0, 0, 0, 0),
          clipBehavior: Clip.hardEdge,
          decoration: const BoxDecoration(
            borderRadius: BorderRadius.all(
              Radius.circular(10),
            ),
            color: Colors.transparent,
          ),
          height: 200,
          child: LineChart(
            swapAnimationDuration: const Duration(milliseconds: 0),
            LineChartData(
              minY: widget.minY,
              maxY: widget.maxY,
              borderData: FlBorderData(show: false),
              lineTouchData: LineTouchData(enabled: false),
              clipData: FlClipData.all(),
              gridData: FlGridData(
                show: true,
                drawVerticalLine: true,
                getDrawingHorizontalLine: (value) {
                  return FlLine(
                    color: const Color(0xff37434d),
                    strokeWidth: 1,
                  );
                },
                getDrawingVerticalLine: (value) {
                  return FlLine(
                    color: const Color(0xff37434d),
                    strokeWidth: 1,
                  );
                },
              ),
              lineBarsData: [
                linePlot(widget.samples),
              ],
              titlesData: FlTitlesData(
                show: false,
              ),
            ),
          ),
        ),
        Text(
          widget.samples.last.y.abs().toStringAsFixed(widget.decimalPlaces),
          style: TextStyle(
              fontSize: 120,
              color: alarmTriggered ? Colors.red.shade900 : Colors.white),
        ),
      ],
    );
  }

  LineChartBarData linePlot(List<FlSpot> points) {
    return LineChartBarData(
      spots: points,
      dotData: FlDotData(
        show: false,
      ),
      gradient: LinearGradient(
        colors: [sinColor.withOpacity(0), sinColor],
        stops: const [0.1, 1.0],
      ),
      barWidth: 4,
      isCurved: false,
      belowBarData: BarAreaData(
        show: true,
        gradient: LinearGradient(
          colors: [
            ColorTween(begin: gradientColors[0], end: gradientColors[1])
                .lerp(0.2)!
                .withOpacity(0.1),
            ColorTween(begin: gradientColors[0], end: gradientColors[1])
                .lerp(0.2)!
                .withOpacity(0.1),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    timer.cancel();
    super.dispose();
  }
}
