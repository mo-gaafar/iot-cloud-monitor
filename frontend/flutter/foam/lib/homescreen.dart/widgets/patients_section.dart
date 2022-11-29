import 'package:flutter/material.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/utils/colorpalette.dart';

import 'minimalist_card.dart';

class PatientsSection extends StatelessWidget {
  const PatientsSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 200),
      child: Container(
        decoration: const BoxDecoration(
          color: CustomColors.blueBg,
          borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: Padding(
          padding: const EdgeInsets.all(15),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Patients',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              MinimalistCard(
                patient: Patient(
                    firstName: 'Abdullah',
                    lastName: 'Saeed',
                    id: '1190222',
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
