import 'package:flutter/material.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/utils/colorpalette.dart';

class PatientHeader extends StatelessWidget {
  final Patient patient;
  const PatientHeader({super.key, required this.patient});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300,
      child: Column(
        // mainAxisAlignment: MainAxisAlignment.,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              RichText(
                text: TextSpan(
                  style: const TextStyle(fontFamily: 'Helvetica Neue'),
                  children: [
                    TextSpan(
                      text: '${patient.firstName}\n',
                      style: const TextStyle(
                          fontSize: 40,
                          color: Colors.black,
                          fontWeight: FontWeight.bold),
                    ),
                    TextSpan(
                      text: patient.lastName,
                      style: TextStyle(
                        color: Colors.grey.shade700,
                        fontSize: 40,
                      ),
                    ),
                  ],
                ),
              ),
              CircleAvatar(
                radius: 45,
                backgroundImage: AssetImage(patient.imagePath),
              ),
            ],
          ),
          const SizedBox(
            height: 5,
          ),
          Padding(
            padding: const EdgeInsets.only(left: 35),
            child: RichText(
              text: TextSpan(
                style: TextStyle(
                    fontFamily: 'Helvetica Neue',
                    fontSize: 9,
                    color: Colors.grey.shade600),
                children: [
                  TextSpan(
                    text: 'PID: ${patient.id}\n',
                  ),
                  TextSpan(
                    text: 'Age: ${patient.age}\n',
                  ),
                  TextSpan(
                    text: 'Monitor: ${patient.monitorId}',
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
