import 'package:flutter/material.dart';

class Greeting extends StatelessWidget {
  const Greeting({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 60),
      child: Align(
        alignment: Alignment.center,
        child: RichText(
          text: TextSpan(
            style: const TextStyle(fontFamily: 'Helvetica Neue'),
            children: [
              TextSpan(
                text: 'Welcome back,\n',
                style: TextStyle(color: Colors.grey.shade800),
              ),
              const TextSpan(
                text: 'Dr Zeyad.',
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 40,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
