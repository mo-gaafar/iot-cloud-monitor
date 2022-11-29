import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:foam/homescreen.dart/minimalist_card.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/utils/colorpalette.dart';

class PatientsSection extends StatelessWidget {
  const PatientsSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 200),
      child: Container(
        decoration: const BoxDecoration(
          color: CustomColors.secondary2,
          borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Patients',
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              MinimalistCard(
                patient: Patient(
                    name: 'Abdullah Saeed',
                    id: 'PID: 1190222',
                    age: '21',
                    imagePath: 'assets/images/patient1crop.jpg',
                    monitorId: 'HM1'),
              )
            ],
          ),
        ),
      ),
    );
  }
}
