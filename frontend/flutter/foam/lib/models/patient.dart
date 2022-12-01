import 'dart:convert';

import 'package:foam/models/signal_data.dart';
import 'package:http/http.dart' as http;

class Patient {
  final String firstName;
  final String lastName;
  final String id;
  final String age;
  final String imagePath;
  final String monitorId;

  late List<SignalData> vitals = [];

  Patient(
      {required this.firstName,
      required this.lastName,
      required this.id,
      required this.age,
      required this.imagePath,
      required this.monitorId}) {
    // fetchVitals();
  }

  Future fetchVitals() async {
    final response = await http.get(Uri.parse(
        'https://no1rz2.deta.dev/signals/last/seconds/1?seconds=0.05'));

    print(jsonDecode(response.body));
    // final List json = jsonDecode(response.body)['signals'];

    // for (int i = 0; i < json.length; i++) {
    //   vitals.add(SignalData.fromJson(json[i]));
    // }

    // print(vitals[0].signalId);
    // return SignalData.fromJson(jsonDecode(response.body));

    // if (response.statusCode == 200) {
    //   // If the server did return a 200 OK response,
    //   // then parse the JSON.
    //   return Album.fromJson(jsonDecode(response.body));
    // } else {
    //   // If the server did not return a 200 OK response,
    //   // then throw an exception.
    //   throw Exception('Failed to load album');
    // }
  }
}
