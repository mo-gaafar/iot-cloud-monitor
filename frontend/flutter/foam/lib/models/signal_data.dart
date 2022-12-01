class SignalData {
  final int signalId;
  final String signalName;
  // final int fsample;
  List<int> lastFiveSecSamples = [];

  SignalData({
    required this.signalId,
    required this.signalName,
  });

  factory SignalData.fromJson(Map<String, dynamic> json) {
    return SignalData(
      signalId: json['signal_id'],
      signalName: json['signal_name'],
    );
  }
}
