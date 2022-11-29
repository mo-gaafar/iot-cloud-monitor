import 'package:flutter/material.dart';
import 'package:foam/skeleton/main_scaffold.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // primarySwatch: Colors.blue,
        fontFamily: 'Helvetica Neue',
        colorScheme: const ColorScheme.dark(),
      ),
      home: const MainScaffold(),
    );
  }
}
