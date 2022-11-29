import 'package:flutter/material.dart';
import 'package:foam/homescreen.dart/widgets/greeting.dart';
import 'package:foam/homescreen.dart/widgets/patients_section.dart';
import 'package:foam/utils/colorpalette.dart';

class MainScaffold extends StatelessWidget {
  const MainScaffold({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.black,
        title: RichText(
          text: const TextSpan(
            style: TextStyle(fontFamily: 'Helvetica Neue'),
            children: [
              TextSpan(
                text: 'FOAM\n',
                style: TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.normal,
                ),
              ),
              TextSpan(
                text: 'The Father Of All Monitors.',
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.normal,
                ),
              )
            ],
          ),
        ),
      ),
      backgroundColor: Colors.black,
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
