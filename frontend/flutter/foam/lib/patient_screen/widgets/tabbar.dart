import 'package:flutter/material.dart';
import 'package:foam/patient_screen/widgets/signal_chart%20copy.dart';
import 'package:foam/patient_screen/widgets/signal_chart.dart';

class StackOver extends StatefulWidget {
  @override
  _StackOverState createState() => _StackOverState();
}

class _StackOverState extends State<StackOver>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    _tabController = TabController(length: 3, vsync: this);
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
    _tabController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0, 0, 0, 10),
      child: Column(
        children: [
          Container(
            width: 330,
            height: 70,
            decoration: BoxDecoration(
              color: Colors.white70,
              borderRadius: BorderRadius.circular(
                15.0,
              ),
            ),
            child: TabBar(
              labelStyle: TextStyle(
                  fontFamily: 'Helvetica Neue',
                  fontSize: 15,
                  fontWeight: FontWeight.normal),
              indicatorPadding: EdgeInsets.all(2.5),
              controller: _tabController,
              // give the indicator a decoration (color and border radius)
              indicator: BoxDecoration(
                borderRadius: BorderRadius.circular(
                  15.0,
                ),
                color: Colors.black,
              ),
              labelColor: Colors.white,
              unselectedLabelColor: Colors.black,
              tabs: [
                // first tab [you can add an icon using the icon property]
                Tab(
                  icon: Icon(Icons.graphic_eq),
                  text: 'Signal',
                ),

                // second tab [you can add an icon using the icon property]
                Tab(
                  icon: Icon(Icons.graphic_eq),
                  text: 'Signal',
                ),

                Tab(
                  icon: Icon(Icons.graphic_eq),
                  text: 'Signal',
                ),
              ],
            ),
          ),
          SizedBox(
            height: 330,
            child: ListView(
              itemExtent: 400,
              children: [
                Padding(
                  padding: const EdgeInsets.only(top: 10),
                  child: TabBarView(
                    controller: _tabController,
                    children: [
                      LineChartSample10(),
                      LineChartSample2(),
                      Text('k'),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
