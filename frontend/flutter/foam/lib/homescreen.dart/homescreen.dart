import 'package:flutter/material.dart';
import 'package:foam/utils/colorpalette.dart';

import 'widgets/greeting.dart';
import 'widgets/patients_section.dart';

class Homescreen extends StatelessWidget {
  const Homescreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: CustomColors.secondary2,
        title: Padding(
          padding: const EdgeInsets.only(top: 5),
          child: RichText(
            text: TextSpan(
              style: TextStyle(fontFamily: 'Helvetica Neue'),
              children: [
                TextSpan(
                  text: 'FOAM\n',
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                TextSpan(
                  text: 'The Father Of All Monitors.',
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 9,
                    fontWeight: FontWeight.normal,
                  ),
                )
              ],
            ),
          ),
        ),
      ),
      backgroundColor: CustomColors.secondary2,
      body: Stack(
        fit: StackFit.expand,
        alignment: Alignment.topCenter,
        children: const [
          Positioned(top: 0, left: 50, child: Greeting()),
          PatientsSection(),
        ],
      ),
    );
  }
}
