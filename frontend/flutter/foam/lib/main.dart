import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:foam/homescreen.dart/homescreen.dart';
import 'package:foam/skeleton/main_scaffold.dart';
import 'package:http/http.dart' as http;

import 'utils/local_notice_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  NotificationService n = NotificationService();
  await n.init();
  Timer timer = Timer.periodic(const Duration(seconds: 20), (timer) {
    _notificationHandler(n);
  });

  runApp(const MyApp());
}

Future _notificationHandler(NotificationService n) async {
  final response = await http.get(
      Uri.parse('https://no1rz2.deta.dev/signals/all/trigalarms/formatted/'));
  List notifications = jsonDecode(response.body);

  if (notifications.isNotEmpty) {
    for (int index = 0; index < notifications.length; index++) {
      await n.show(notifications[index]['notification_id'],
          notifications[index]['title'], notifications[index]['body']);
    }
  }
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
      home: const Homescreen(),
    );
  }
}
