import 'package:flutter/material.dart';
import 'package:lida/screens/calculation/AddWastePage.dart';
import 'package:lida/utilities/custom_color.dart';
import 'package:lida/widgets/lida_app_bar.dart';
import 'package:provider/provider.dart';

class CNRatioApp extends StatelessWidget {
  const CNRatioApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'C:N Ratio Calculator',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const Calculation(),
    );
  }
}

class Calculation extends StatefulWidget {
  const Calculation({super.key});

  @override
  _CalculationState createState() => _CalculationState();
}

class _CalculationState extends State<Calculation> {
  final TextEditingController _carbonController = TextEditingController();
  final TextEditingController _nitrogenController = TextEditingController();
  String? _result;
  List<Waste> wasteList = []; // To store the waste cards
  bool _isCalculated = false;

  void addWaste(Waste waste) {
    setState(() {
      wasteList.add(waste);
    });
  }

  void _addWasteFromAddPage() async {
    final Waste? addedWaste = await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => ChangeNotifierProvider(
          create: (context) => WasteData(),
          child: const AddWastePage(),
        ),
      ),
    );

    if (addedWaste != null) {
      print("Waste added: ${addedWaste.selectedValue}");
      final wasteData = Provider.of<WasteData>(context, listen: false);
      wasteData.addWaste(addedWaste);

      setState(() {
        wasteList.add(addedWaste);
      });
    }
  }

  String calculateOverallCnRatio(List<Waste> items) {
    List<double> topRow = [];
    List<double> bottomRow = [];

    Map<String, Map<String, double>> cnDetails = {
      'Coffee Grounds': {'Carbon': 47.10,'Nitrogen': 2.70,'pH': 5.66,'Moisture': 58},
      'Vegetables': {'Carbon': 37.50,'Nitrogen': 2.50,'pH': 4.98,'Moisture': 92},
      'Fruits': {'Carbon': 56.00, 'Nitrogen': 1.40, 'pH': 4.53, 'Moisture': 89},
      'Food Waste': {'Carbon': 46.40,'Nitrogen': 2.90,'pH': 5.74,'Moisture': 69},
      'Sawdust': {'Carbon': 106.10, 'Nitrogen': 0.20, 'pH': 4.63, 'Moisture': 5}
    };

    for (Waste item in items) {
      double qn = double.parse(item.weight);
      print("Weight: $qn");


      if (item.selectedValue == "Other") {
        double? cn = double.parse(item.carbon);
        double? mn = double.parse(item.moisture);
        double? nn = double.parse(item.nitrogen);
        double hundredMn = 100 - (mn ?? 0);

        print(item.name);
        print(cn.toString());
        print(mn.toString());
        print(nn.toString());

        topRow.add(qn * (cn ?? 0) * hundredMn); //Top formula: Qn * Cn * (100 - Mn) // Default to 0 if Cn is null
        bottomRow.add(qn * (nn ?? 0) * hundredMn); //Bottom formula: Qn * Nn * (100 - Mn) // Default to 0 if Nn is null

      } else {
        print(item.selectedValue);
        double? cn = cnDetails[item.selectedValue]?['Carbon']; // Handle nullable values if they dont exist
        print('Carbon Value: $cn');
        double? mn = cnDetails[item.selectedValue]?['Moisture'];
        print('Moisture Value: $mn');
        double? nn = cnDetails[item.selectedValue]?['Nitrogen'];
        print('Nitrogen Value: $nn');
        double hundredMn = 100 - (mn ?? 0); // Default to 0 if Mn is null

        topRow.add(qn * (cn ?? 0) * hundredMn); //Top formula: Qn * Cn * (100 - Mn) // Default to 0 if Cn is null
        bottomRow.add(qn * (nn ?? 0) * hundredMn); //Bottom formula: Qn * Nn * (100 - Mn) // Default to 0 if Nn is null
      }
    }

    if (topRow.length == 0) {
      throw Exception("Total weight cannot be zero.");
    }

    double finalRatio = (sum(topRow) / sum(bottomRow));
    return finalRatio.toStringAsFixed(2);
  }

  double sum(List<double> values) {
    return values.reduce((a, b) => a + b);
  }

  void calculateRatioForWasteItems() {
    try {
      String overallCnRatio = calculateOverallCnRatio(wasteList);
      setState(() {
        _result = overallCnRatio;
      });

      // Show the result in a dialog
      showDialog(
        context: context,
        barrierDismissible: true,
        barrierColor: Colors.black54, // This will darken the background
        builder: (context) => CnRatioCard(result: _result),
      );
    } catch (e) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Error'),
          content: Text(e.toString()),
          actions: [
            TextButton(
              child: const Text('OK'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const LidaAppBar(),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          children: [
            // This part will scroll
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Horizontal Card with the title and button
                    Card(
                      elevation: 4.0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                        side: const BorderSide(
                            color: Color(0xff15aa65), width: 2.0),
                      ),
                      child: SizedBox(
                        width: 370.0, // setting width
                        height: 60.0,
                        child: Padding(
                          padding: const EdgeInsets.all(10.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: <Widget>[
                              const Text(
                                'Calculate C:N',
                                style: TextStyle(
                                  fontSize: 18.0,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black,
                                ),
                              ),
                              ElevatedButton(
                                onPressed: _addWasteFromAddPage,
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.transparent,
                                  shadowColor: Colors.transparent,
                                  padding: EdgeInsets.zero,
                                ),
                                child: DecoratedBox(
                                  decoration: BoxDecoration(
                                    gradient: const LinearGradient(
                                      colors: [
                                        Color(0xFF147B4B),
                                        Color(0xFF14AF67)
                                      ],
                                      begin: Alignment.centerLeft,
                                      end: Alignment.centerRight,
                                    ),
                                    borderRadius: BorderRadius.circular(4.0),
                                  ),
                                  child: const Padding(
                                    padding: EdgeInsets.symmetric(
                                        horizontal: 12.0, vertical: 8.0),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: [
                                        Text('Add Waste',
                                            style:
                                                TextStyle(color: Colors.white)),
                                        SizedBox(width: 6.0),
                                        Icon(Icons.arrow_forward,
                                            color: Colors.white, size: 16.0),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 10.0),
                    // Provide some spacing between the card and the text
                    Padding(
                      padding: const EdgeInsets.only(left: 20.0),
                      child: Row(
                        children: <Widget>[
                          Container(
                            height: 20.0,
                            width: 4.0,
                            decoration: BoxDecoration(
                              color: primaryColor,
                              borderRadius: BorderRadius.circular(
                                  4.0), // Adjust as needed
                            ),
                          ),
                          const SizedBox(width: 8.0),
                          // Provide some spacing between the line and the text
                          const Text(
                            'Wastes',
                            style: TextStyle(
                              fontSize: 18.0,
                              fontWeight: FontWeight.bold,
                              color: Colors.black,
                            ),
                          ),
                        ],
                      ),
                    ),

                    Column(
                      children: wasteList
                          .map<Widget>(
                            (Waste waste) => WasteDetailsCard(
                              waste: waste,
                              onWasteUpdated: (oldWaste, newWaste) {
                                setState(() {
                                  int index = wasteList.indexOf(oldWaste);
                                  wasteList[index] = newWaste;
                                });
                              },
                            ),
                          )
                          .toList(),
                    ),
                    if (_isCalculated)
                      const Divider(color: primaryColor, thickness: 2.0),
                  ],
                ),
              ),
            ),
            // Pinning the "Calculate" button at the bottom
            Align(
              alignment: Alignment.bottomCenter,
              child: ElevatedButton(
                onPressed: () {
                  setState(() {
                    _isCalculated = true;
                  });
                  calculateRatioForWasteItems();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.transparent,
                  shadowColor: Colors.transparent,
                  padding: EdgeInsets.zero,
                ),
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFF147B4B), Color(0xFF14AF67)],
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                    ),
                    borderRadius: BorderRadius.circular(4.0),
                  ),
                  child: const Padding(
                    padding:
                        EdgeInsets.symmetric(horizontal: 12.0, vertical: 8.0),
                    child: Text(
                      'Calculate',
                      style: TextStyle(color: Colors.white),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class CnRatioCard extends StatelessWidget {
  final String? result;

  const CnRatioCard({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Dialog(
      insetPadding: const EdgeInsets.all(0.0),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16.0),
      ),
      elevation: 0.0,
      backgroundColor: Colors.transparent,
      child: _buildCard(context),
    );
  }

  Widget _buildCard(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double containerWidth = screenWidth * 0.8; // Dynamic padding based on screen width

    return Stack(
      children: <Widget>[
        Container(
          width: screenWidth,
          padding: const EdgeInsets.all(30.0),
          decoration: BoxDecoration(
            color: Colors.white,
            shape: BoxShape.rectangle,
            borderRadius: BorderRadius.circular(16.0),
            boxShadow: const <BoxShadow>[
              BoxShadow(
                color: Colors.black26,
                blurRadius: 10.0,
                offset: Offset(0.0, 10.0),
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              Flexible(
                child: Text(
                  'Net Carbon to Nitrogen Ratio',
                  style: TextStyle(
                    fontSize: 20.0,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              SizedBox(height: 16.0),
              Flexible(
                child: Text(
                  'Current Ratio: $result:1',
                  style: TextStyle(
                    fontSize: 16.0,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),

              Align(
                alignment: Alignment.bottomCenter,
                child: Container(
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFF147B4B), Color(0xFF14AF67)],
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                    ),
                    borderRadius: BorderRadius.circular(8.0),
                  ),
                  padding: EdgeInsets.symmetric(
                    horizontal: 10.0,
                    vertical: 10.0,
                  ),
                  child: TextButton(
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    child: const Text(
                      "OK",
                      style: TextStyle(
                        fontSize: 16.0,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildDynamicPaddingContainer(String text, double containerWidth) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        width: containerWidth,
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF147B4B), Color(0xFF14AF67)],
            begin: Alignment.centerLeft,
            end: Alignment.centerRight,
          ),
          borderRadius: BorderRadius.circular(8.0),
        ),
        padding: EdgeInsets.symmetric(
          horizontal: 20.0,
          vertical: 20.0,
        ),
        child: Text(
          text,
          style: TextStyle(
            fontSize: 16.0,
            color: Colors.white,
          ),
        ),
      ),
    );
  }
}

class WasteDetailsCard extends StatefulWidget {
  final Waste waste;
  final Function(Waste, Waste) onWasteUpdated;

  const WasteDetailsCard(
      {super.key, required this.waste, required this.onWasteUpdated});

  @override
  _WasteDetailsCardState createState() => _WasteDetailsCardState();
}

class _WasteDetailsCardState extends State<WasteDetailsCard> {
  late Waste waste;

  @override
  void initState() {
    super.initState();
    waste = widget.waste;
  }

  _editWasteDetails() async {
    Waste? updatedWaste = await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => ChangeNotifierProvider(
          create: (context) => WasteData(),
          child: AddWastePage(
              editWaste: waste), // pass the current waste to be edited
        ),
      ),
    );

    if (updatedWaste != null) {
      setState(() {
        waste = updatedWaste; // update local state
      });
      widget.onWasteUpdated(widget.waste, updatedWaste); // notify parent
    }
  }

  @override
  Widget build(BuildContext context) {
    print("Building WasteDetailsCard for waste: ${waste.selectedValue}");
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0),
      child: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10),
              gradient: const LinearGradient(
                colors: [Color(0xFF147B4B), Color(0xFF14AF67)],
                begin: Alignment.centerLeft,
                end: Alignment.centerRight,
              ),
              border: Border.all(color: primaryColor, width: 2.0),
            ),
            child: ListTile(
              title: Text(
                waste.selectedValue == 'Other'
                    ? waste.name
                    : waste.selectedValue,
                style: const TextStyle(color: Colors.white),
              ),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    'Weight: ${waste.weight} Kg',
                    style: const TextStyle(color: Colors.white),
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            top: 8.0,
            right: 8.0,
            child: IconButton(
              icon: const Icon(Icons.edit, color: Colors.white),
              onPressed: _editWasteDetails,
            ),
          ),
        ],
      ),
    );
  }
}
