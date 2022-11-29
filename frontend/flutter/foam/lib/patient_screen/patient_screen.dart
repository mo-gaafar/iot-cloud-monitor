import 'package:flutter/material.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/patient_screen/widgets/patient_header.dart';
import 'package:foam/patient_screen/widgets/patient_monitor.dart';
import 'package:foam/utils/colorpalette.dart';

class PatientScreen extends StatelessWidget {
  final Patient patient;
  const PatientScreen({super.key, required this.patient});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: CustomColors.secondary2,
      ),
      backgroundColor: CustomColors.secondary2,
      body: Stack(
        fit: StackFit.expand,
        alignment: Alignment.topCenter,
        children: [
          PatientHeader(patient: patient),
          PatientMonitor(),
        ],
      ),
    );
  }
}
