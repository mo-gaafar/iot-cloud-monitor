import 'dart:convert';

import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:foam/patient_screen/widgets/signal_plot.dart';
import 'package:foam/patient_screen/widgets/signal_stats.dart';
import 'package:foam/utils/colorpalette.dart';
import 'package:http/http.dart' as http;

class MonitorContents extends StatefulWidget {
  final int signalId;
  final int windowSec;
  final int decimalPlaces;
  final double minY;
  final double maxY;
  const MonitorContents({
    super.key,
    required this.signalId,
    required this.windowSec,
    required this.decimalPlaces,
    required this.minY,
    required this.maxY,
  });

  @override
  State<MonitorContents> createState() => _MonitorContentsState();
}

class _MonitorContentsState extends State<MonitorContents> {
  double xValue = 0;
  List<FlSpot> initSamples = <FlSpot>[];
  late Map initSignalStats = {};

  var initMonitorDisplay;

  Future fetchInitData() async {
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

    initSamples = temp;
    initMonitorDisplay = samplesJson.last;

    final statsResponse = await http.get(
        Uri.parse('https://no1rz2.deta.dev/signals/stats/${widget.signalId}'));

    final statsJson = jsonDecode(statsResponse.body)['signal_stats'];
    initSignalStats = statsJson;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: fetchInitData(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const CircularProgressIndicator(
            color: CustomColors.blueBg,
          );
        } else {
          return Column(
            children: [
              SignalPlot(
                signalId: widget.signalId,
                windowSec: widget.windowSec,
                decimalPlaces: widget.decimalPlaces,
                minY: widget.minY,
                maxY: widget.maxY,
                samples: initSamples,
              ),
              SignalStats(
                  signalId: widget.signalId, signalStats: initSignalStats),
            ],
          );
        }
      },
    );
  }
}
