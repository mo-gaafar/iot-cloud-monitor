import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:foam/models/patient.dart';
import 'package:foam/utils/colorpalette.dart';

class MinimalistCard extends StatelessWidget {
  final Patient patient;
  const MinimalistCard({Key? key, required this.patient}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CupertinoButton(
      padding: const EdgeInsets.fromLTRB(0, 10, 10, 0),
      child: Container(
        height: 70,
        width: double.infinity,
        decoration: BoxDecoration(
          color: CustomColors.blueBg.withOpacity(0.0),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Padding(
          padding: const EdgeInsets.all(0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  CircleAvatar(
                    // backgroundColor: color,
                    radius: 25,
                    backgroundImage: AssetImage(patient.imagePath),
                  ),
                  const SizedBox(
                    width: 20,
                  ),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        patient.name,
                        style: const TextStyle(
                            fontFamily: 'Helvetica Neue',
                            color: Colors.black,
                            fontSize: 17,
                            fontWeight: FontWeight.normal),
                      ),
                      const SizedBox(
                        height: 5,
                      ),
                      Text(
                        patient.id,
                        style: TextStyle(
                            fontFamily: 'Helvetica Neue',
                            color: Colors.grey.shade700,
                            fontSize: 10,
                            fontWeight: FontWeight.normal),
                      ),
                    ],
                  ),
                ],
              ),
              Text(
                patient.monitorId,
                style: const TextStyle(
                    fontFamily: 'Helvetica Neue',
                    color: Colors.black,
                    fontSize: 17,
                    fontWeight: FontWeight.normal),
              ),
            ],
          ),
        ),
      ),
      onPressed: () {
        debugPrint('Card tapped.');
      },
    );
  }
}
