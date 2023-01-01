import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/patient_screen/widgets/patient_monitor_contents.dart';
import 'package:foam/utils/colorpalette.dart';
import 'package:sliding_up_panel/sliding_up_panel.dart';
import 'package:tab_container/tab_container.dart';
import 'package:collection/collection.dart';

import 'package:http/http.dart' as http;

import 'alarm_card.dart';

class PatientMonitor extends StatefulWidget {
  final Patient patient;
  const PatientMonitor({super.key, required this.patient});

  @override
  State<PatientMonitor> createState() => _PatientMonitorState();
}

class _PatientMonitorState extends State<PatientMonitor> {
  late List signalData = [];
  late TabContainerController controller;
  late Map signalStats = {};
  int indexHandler = 0;

  List alarms = [];
  late Timer timer;
  Function deepEq = const DeepCollectionEquality().equals;

  // Call this periodically with timer in initState
  Future fetchAlarms() async {
    final response = await http
        .get(Uri.parse('https://no1rz2.deta.dev/signals/all/trigalarms/'));
    List data = jsonDecode(response.body);
    if (data.isNotEmpty && !deepEq(data, alarms)) {
      setState(() {
        alarms = data;
      });
    } else if (data.isEmpty && !deepEq(data, alarms)) {
      setState(() {
        alarms.clear();
      });
    }
  }

  Future fetchSignalsInfo() async {
    final response =
        await http.get(Uri.parse('https://no1rz2.deta.dev/signals/all'));
    signalData = jsonDecode(response.body)['signals'];
    controller = TabContainerController(length: signalData.length);
    setState(() {});
  }

  void _handleTabChange() {
    setState(() {
      indexHandler = controller.index;
    });
  }

  @override
  void initState() {
    // TODO: implement initState
    timer = Timer.periodic(const Duration(seconds: 5), (timer) {
      fetchAlarms();
    });
    super.initState();
    fetchSignalsInfo();
    // controller = TabContainerController(length: signalData.length);
  }

  @override
  Widget build(BuildContext context) {
    return signalData.isNotEmpty
        ? SlidingUpPanel(
            backdropOpacity: 0.9,
            padding: EdgeInsets.fromLTRB(10, 0, 10, 0),
            maxHeight: 400,
            minHeight: alarms.isEmpty ? 0 : 50,
            color: Colors.red.shade900.withOpacity(0.7),
            header: Material(
              color: Colors.transparent,
              child: Padding(
                padding: EdgeInsets.fromLTRB(95, 15, 0, 0),
                child: Text(
                  textAlign: TextAlign.center,
                  'ALARM TRIGGERED',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      backgroundColor: Colors.transparent,
                      fontWeight: FontWeight.bold),
                ),
              ),
            ),
            borderRadius: const BorderRadius.all(Radius.circular(20)),
            parallaxEnabled: true,
            backdropEnabled: true,
            panel: alarms.isEmpty
                ? Container()
                : ListView.builder(
                    physics: NeverScrollableScrollPhysics(),
                    padding: EdgeInsets.only(top: 60),
                    itemCount: alarms.length,
                    itemBuilder: (context, index) => AlarmCard(
                        description: alarms[index]['description'],
                        threshold: alarms[index]['threshold'].toString(),
                        threshold_direction: alarms[index]
                            ['threshold_direction'],
                        threshold_unit: alarms[index]['threshold_unit'],
                        type: alarms[index]['type']),
                  ), // build listview of alarm cards
            body: Padding(
              padding: const EdgeInsets.only(top: 140),
              child: TabContainer(
                // tabDuration: Duration(seconds: 0),
                // childDuration: Duration(seconds: 0),
                onEnd: _handleTabChange,
                controller: controller,
                childPadding: const EdgeInsets.fromLTRB(10, 5, 10, 0),
                color: CustomColors.blueBg,
                selectedTextStyle:
                    const TextStyle(fontSize: 15, color: Colors.white),
                unselectedTextStyle:
                    TextStyle(fontSize: 15, color: Colors.grey.shade700),
                tabs: List.generate(
                  signalData.length,
                  (index) => signalData[index]['signal_name'],
                ),

                // [
                //   signalData[0]['signal_name'],
                //   signalData[1]['signal_name'],
                //   signalData[2]['signal_name'],
                // ],
                children: List.generate(
                  signalData.length,
                  (index) {
                    if (index == indexHandler) {
                      return MonitorContents(
                        signalId: signalData[indexHandler]['signal_id'],
                        windowSec: signalData[indexHandler]['window_sec'],
                        decimalPlaces: signalData[indexHandler]
                            ['decimal_point'],
                        // minY: 50,
                        // maxY: 200,
                        minY: signalData[indexHandler]['range_y'][0].toDouble(),
                        maxY: signalData[indexHandler]['range_y'][1].toDouble(),
                      );
                    } else {
                      return Container();
                    }
                  },
                ),

                // [
                //   index == 0
                //       ? MonitorContents(
                //           signalId: signalData[0]['signal_id'],
                //           windowSec: signalData[0]['window_sec'],
                //           decimalPlaces: signalData[0]['decimal_point'])
                //       : Container(),
                //   index == 1
                //       ? MonitorContents(
                //           signalId: signalData[1]['signal_id'],
                //           windowSec: signalData[1]['window_sec'],
                //           decimalPlaces: signalData[1]['decimal_point'])
                //       : Container(),
                //   index == 2
                //       ? MonitorContents(
                //           signalId: signalData[2]['signal_id'],
                //           windowSec: signalData[2]['window_sec'],
                //           decimalPlaces: signalData[2]['decimal_point'])
                //       : Container(),
                // ],
              ),
            ),
          )
        : const Center(
            child: CircularProgressIndicator(
            color: CustomColors.blueBg,
          ));
  }

  @override
  void dispose() {
    timer.cancel();
    controller.dispose();
    super.dispose();
  }
}
