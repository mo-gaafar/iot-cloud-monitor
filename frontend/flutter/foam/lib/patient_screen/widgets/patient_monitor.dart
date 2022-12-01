import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/patient_screen/widgets/signal_chart%20copy.dart';
import 'package:foam/patient_screen/widgets/signal_chart.dart';
import 'package:foam/patient_screen/widgets/signal_plot.dart';
import 'package:foam/utils/colorpalette.dart';
import 'package:tab_container/tab_container.dart';

import 'package:http/http.dart' as http;

class PatientMonitor extends StatefulWidget {
  final Patient patient;
  const PatientMonitor({super.key, required this.patient});

  @override
  State<PatientMonitor> createState() => _PatientMonitorState();
}

class _PatientMonitorState extends State<PatientMonitor> {
  late List signalData;
  Future fetchSignalsInfo() async {
    final response =
        await http.get(Uri.parse('https://no1rz2.deta.dev/signals/all'));
    signalData = jsonDecode(response.body)['signals'];
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    fetchSignalsInfo();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 150),
      child: TabContainer(
        childPadding: const EdgeInsets.fromLTRB(10, 15, 10, 0),
        color: CustomColors.blueBg,
        selectedTextStyle: const TextStyle(fontSize: 15, color: Colors.white),
        unselectedTextStyle:
            TextStyle(fontSize: 15, color: Colors.grey.shade700),
        tabs: [
          signalData[0]['signal_name'],
          signalData[1]['signal_name'],
          signalData[2]['signal_name'],
        ],
        children: [
          Column(
            children: [
              SignalPlot(
                signalId: signalData[0]['signal_id'],
                windowSec: 5,
                decimalPlaces: 0,
              ),
              // Text(http.get(url))
            ],
          ),
          SignalPlot(
              signalId: signalData[1]['signal_id'],
              windowSec: 5,
              decimalPlaces: 0),
          SignalPlot(
            signalId: signalData[2]['signal_id'],
            windowSec: 5,
            decimalPlaces: 2,
          ),
        ],
      ),
    );
    // Padding(
    //   padding: const EdgeInsets.only(top: 200),
    //   child: Container(
    //     decoration: const BoxDecoration(
    //       color: CustomColors.secondary2,
    //       borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    //     ),
    //     child: Padding(
    //       padding: const EdgeInsets.all(20),
    //       child: Column(
    //         crossAxisAlignment: CrossAxisAlignment.start,
    //         children: [
    //           // const Text(
    //           //   'Monitor',
    //           //   style: TextStyle(
    //           //     color: Colors.black,
    //           //     fontSize: 20,
    //           //     fontWeight: FontWeight.bold,
    //           //   ),
    //           // ),
    //           // SizedBox(
    //           //   height: 10,
    //           // ),
    //           // StackOver()
    //           SizedBox(
    //             height: 400,
    //             child: TabContainer(
    //               // childPadding: EdgeInsets.fromLTRB(10, 15, 10, 0),
    //               color: CustomColors.blueBg,
    //               children: [
    //                 Container(
    //                   child: LineChartSample10(),
    //                 ),
    //                 Container(
    //                   child: LineChartSample2(),
    //                 ),
    //                 Container(
    //                   child: Text('Child 3'),
    //                 ),
    //               ],
    //               selectedTextStyle:
    //                   const TextStyle(fontSize: 15, color: Colors.white),
    //               unselectedTextStyle:
    //                   TextStyle(fontSize: 15, color: Colors.grey.shade700),
    //               tabs: [
    //                 'Tab 1',
    //                 'Tab 2',
    //                 'Tab 3',
    //               ],
    //             ),
    //           )
    //         ],
    //       ),
    //     ),
    //   ),
    // );
  }
}
