import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class SignalStats extends StatefulWidget {
  final int signalId;
  late Map signalStats;
  SignalStats({super.key, required this.signalId, required this.signalStats});

  @override
  State<SignalStats> createState() => _SignalStatsState();
}

class _SignalStatsState extends State<SignalStats> {
  late Timer timer;

  Future fetchStats() async {
    final response = await http.get(
        Uri.parse('https://no1rz2.deta.dev/signals/stats/${widget.signalId}'));

    final statsJson = jsonDecode(response.body)['signal_stats'];
    widget.signalStats = statsJson;
  }

  @override
  void initState() {
    // TODO: implement initState
    timer = Timer.periodic(const Duration(seconds: 5), (timer) {
      setState(() {
        fetchStats();
      });
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Mean',
              style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              widget.signalStats['mean'].toStringAsFixed(2),
              style: const TextStyle(fontSize: 20),
            ),
            const SizedBox(
              height: 15,
            ),
            Text(
              'Median',
              style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              widget.signalStats['median'].toStringAsFixed(2),
              style: const TextStyle(fontSize: 20),
            ),
          ],
        ),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Max',
              style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              widget.signalStats['max'].toStringAsFixed(2),
              style: const TextStyle(fontSize: 20),
            ),
            const SizedBox(
              height: 15,
            ),
            Text(
              'Min',
              style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              widget.signalStats['min'].toStringAsFixed(2),
              style: const TextStyle(fontSize: 20),
            ),
          ],
        ),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Standard\nDeviation',
              style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              widget.signalStats['std'].toStringAsFixed(2),
              style: const TextStyle(fontSize: 20),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              'Variance',
              style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              widget.signalStats['var'].toStringAsFixed(2),
              style: const TextStyle(fontSize: 20),
            ),
          ],
        ),
      ],
    );
  }

  @override
  void dispose() {
    // TODO: implement dispose
    timer.cancel();
    super.dispose();
  }
}
