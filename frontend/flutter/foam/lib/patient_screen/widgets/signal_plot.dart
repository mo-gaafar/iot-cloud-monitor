import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;
import 'package:http/http.dart' as http;

import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class SignalPlot extends StatefulWidget {
  final signalId;
  final double windowSec;
  final int decimalPlaces;
  const SignalPlot(
      {super.key,
      required this.signalId,
      required this.windowSec,
      required this.decimalPlaces});

  @override
  State<SignalPlot> createState() => _SignalPlotState();
}

class _SignalPlotState extends State<SignalPlot> {
  final Color sinColor = Colors.redAccent;
  final Color cosColor = Colors.blueAccent;

  final secondsWindow = 1;
  final sinPoints = <FlSpot>[];
  final cosPoints = <FlSpot>[];

  double xValue = 0;
  double step = 0.05;

  late Timer samplesTimer;
  late Timer statsTimer;

  List<Color> gradientColors = [
    const Color(0xff23b6e6),
    const Color(0xff02d39a),
  ];

  List<FlSpot> samples = <FlSpot>[];
  var monitorDisplay;
  late Map signalStats = {};

  Future fetchSamples() async {
    List<FlSpot> temp = [];
    final response = await http.get(Uri.parse(
        'https://no1rz2.deta.dev/signals/last/seconds/${widget.signalId}?seconds=${widget.windowSec}'));
    final List samplesJson = jsonDecode(response.body)['signal_values'];
    xValue = 0;
    for (int i = 0; i < samplesJson.length; i++) {
      temp.add(
        FlSpot(xValue, samplesJson[i].toDouble()),
      );
      xValue += widget.windowSec / samplesJson.length;
    }

    samples = temp;
    monitorDisplay = samplesJson.last;
  }

  Future fetchStats() async {
    final response = await http.get(
        Uri.parse('https://no1rz2.deta.dev/signals/stats/${widget.signalId}'));

    final statsJson = jsonDecode(response.body)['signal_stats'];
    signalStats = statsJson;
  }

  @override
  void initState() {
    super.initState();
    samplesTimer = Timer.periodic(Duration(milliseconds: 700), (timer) {
      setState(() {
        fetchSamples();
      });
    });

    statsTimer =
        Timer.periodic(Duration(seconds: widget.windowSec.toInt()), (timer) {
      setState(() {
        fetchStats();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      // mainAxisAlignment: MainAxisAlignment.start,
      children: [
        // Text(
        //   'x: ${xValue.toStringAsFixed(1)}',
        //   style: const TextStyle(
        //     color: Colors.black,
        //     fontSize: 18,
        //     fontWeight: FontWeight.bold,
        //   ),
        // ),
        // Text(
        //   'sin: ${sinPoints.last.y.toStringAsFixed(1)}',
        //   style: TextStyle(
        //     color: sinColor,
        //     fontSize: 18,
        //     fontWeight: FontWeight.bold,
        //   ),
        // ),
        // Text(
        //   'cos: ${cosPoints.last.y.toStringAsFixed(1)}',
        //   style: TextStyle(
        //     color: cosColor,
        //     fontSize: 18,
        //     fontWeight: FontWeight.bold,
        //   ),
        // ),
        // const SizedBox(
        //   height: 12,
        // ),
        Container(
          padding: EdgeInsets.fromLTRB(0, 0, 0, 0),
          clipBehavior: Clip.hardEdge,
          // width: 300,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.all(
              Radius.circular(10),
            ),
            color: Colors.transparent,
          ),
          height: 200,
          child: LineChart(
            swapAnimationDuration: Duration(milliseconds: 0),
            LineChartData(
              borderData: FlBorderData(show: false),
              // minY: -1,
              // maxY: 1,
              // minX: sinPoints.first.x,
              // maxX: 1,
              lineTouchData: LineTouchData(enabled: false),
              clipData: FlClipData.all(),
              gridData: FlGridData(
                show: true,
                drawVerticalLine: true,
                // horizontalInterval: 1,
                // verticalInterval: 1,
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
                linePlot(samples),
                // cosLine(cosPoints),
              ],
              titlesData: FlTitlesData(
                show: false,
              ),
            ),
          ),
        ),
        SizedBox(
          height: 20,
        ),
        Text(
          monitorDisplay != null
              ? monitorDisplay.toStringAsFixed(widget.decimalPlaces)
              : '',
          style: TextStyle(fontSize: 100),
        ),
        Text((signalStats['mean']).toString()),
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

  LineChartBarData cosLine(List<FlSpot> points) {
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
    );
  }

  @override
  void dispose() {
    samplesTimer.cancel();
    statsTimer.cancel();
    super.dispose();
  }
}
