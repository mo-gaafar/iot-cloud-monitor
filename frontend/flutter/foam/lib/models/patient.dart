class Patient {
  final String firstName;
  final String lastName;
  final String id;
  final String age;
  final String imagePath;
  final String monitorId;

  Patient(
      {required this.firstName,
      required this.lastName,
      required this.id,
      required this.age,
      required this.imagePath,
      required this.monitorId});
}
