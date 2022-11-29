import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:foam/patient_screen/widgets/signal_chart%20copy.dart';
import 'package:foam/patient_screen/widgets/signal_chart.dart';
import 'package:foam/patient_screen/widgets/tabbar.dart';
import 'package:foam/utils/colorpalette.dart';
import 'package:tab_container/tab_container.dart';

class PatientMonitor extends StatelessWidget {
  const PatientMonitor({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(top: 150),
      child: TabContainer(
        childPadding: EdgeInsets.fromLTRB(10, 15, 10, 0),
        color: CustomColors.blueBg,
        children: [
          Container(
            child: LineChartSample10(),
          ),
          Container(
            child: LineChartSample2(),
          ),
          Container(
            child: Text('Child 3'),
          ),
        ],
        selectedTextStyle: const TextStyle(fontSize: 15, color: Colors.white),
        unselectedTextStyle:
            TextStyle(fontSize: 15, color: Colors.grey.shade700),
        tabs: [
          'Tab 1',
          'Tab 2',
          'Tab 3',
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
