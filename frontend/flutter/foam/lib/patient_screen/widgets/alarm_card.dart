import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:foam/homescreen.dart/homescreen.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/patient_screen/patient_screen.dart';
import 'package:foam/utils/colorpalette.dart';

class AlarmCard extends StatelessWidget {
  final String description;
  final String threshold;
  final String threshold_direction;
  final String threshold_unit;
  final String type;

  const AlarmCard({
    Key? key,
    required this.description,
    required this.threshold,
    required this.threshold_direction,
    required this.threshold_unit,
    required this.type,
  }) : super(key: key);

  // Setup alarm card layout after passing array/map of alarm data

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.only(bottom: 15),
      height: 80,
      width: double.infinity,
      decoration: BoxDecoration(
        color: Colors.grey.shade50.withOpacity(0.1),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 10, 20, 10),
        child: Material(
          color: Colors.transparent,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Text(
                    description,
                    style: const TextStyle(
                        fontFamily: 'Helvetica Neue',
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(
                    height: 5,
                  ),
                  SizedBox(
                    width: 250,
                    child: Text(
                      '${type.toUpperCase()} is ${threshold_direction} ${threshold} ${threshold_unit}. Please attend to the patient immediately.',
                      style: TextStyle(
                          fontFamily: 'Helvetica Neue',
                          color: Colors.grey.shade300,
                          fontSize: 11,
                          fontWeight: FontWeight.normal),
                    ),
                  ),
                ],
              ),
              Icon(Icons.sick)
            ],
          ),
        ),
      ),
    );
  }
}
