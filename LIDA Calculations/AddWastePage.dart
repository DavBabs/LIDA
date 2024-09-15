import 'package:flutter/material.dart';
import 'package:lida/utilities/custom_color.dart';
import 'package:dropdown_search/dropdown_search.dart';
import 'package:provider/provider.dart';
import 'package:lida/screens/calculation/Calculation.dart'; // Update the path as needed

class Waste {
  final String selectedValue;
  final String weight;
  final String name;
  final String carbon;
  final String nitrogen;
  final String moisture;

  Waste({
    required this.selectedValue,
    required this.weight,
    required this.name,
    required this.carbon,
    required this.nitrogen,
    required this.moisture,

  });
}

class WasteData extends ChangeNotifier {
  final List<Waste> wastes = [];

  void addWaste(Waste waste) {
    wastes.add(waste);
    notifyListeners();
  }
}

class AddWastePage extends StatefulWidget {
  @override
  _AddWastePageState createState() => _AddWastePageState();
  final Waste? editWaste; // Add this line for the property

  const AddWastePage({super.key, this.editWaste});
}

class _AddWastePageState extends State<AddWastePage> {
  /*var cnDetails = {
    'Coffee Grounds': {'Carbon': 47.10,'Nitrogen': 2.70,'pH': 5.66,'Moisture': 58},
    'Vegetables': {'Carbon': 37.50,'Nitrogen': 2.50,'pH': 4.98,'Moisture': 92},
    'Fruits': {'Carbon': 56.00, 'Nitrogen': 1.40, 'pH': 4.53, 'Moisture': 89},
    'Food Waste': {'Carbon': 46.40,'Nitrogen': 2.90,'pH': 5.74,'Moisture': 69},
    'Sawdust': {'Carbon': 106.10, 'Nitrogen': 0.20, 'pH': 4.63, 'Moisture': 5},
    'Other':{}
  };*/
  var cnDetails = ['Coffee Grounds','Vegetables','Fruits','Food Waste', 'Sawdust'];

  String? selectedValue;
  final TextEditingController _weightController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _carbonController = TextEditingController();
  final TextEditingController _nitrogenController = TextEditingController();
  final TextEditingController _moistureController = TextEditingController();
  bool _showKgSuffix = false;
  bool _showRatioSuffix = false;

  @override
  void initState() {
    super.initState();

    if (widget.editWaste != null) {
      selectedValue = widget.editWaste!.selectedValue;
      _weightController.text = widget.editWaste!.weight;
      _nameController.text = widget.editWaste!.name;
      _carbonController.text = widget.editWaste!.carbon;
      _carbonController.text = widget.editWaste!.nitrogen;
      _carbonController.text = widget.editWaste!.moisture;

    }
  }

  @override
  void dispose() {
    _weightController.dispose();
    _nameController.dispose();
    _carbonController.dispose();
    _nitrogenController.dispose();
    _moistureController.dispose();

    super.dispose();
  }

  bool _isKeyboardOpen(BuildContext context) {
    return MediaQuery.of(context).viewInsets.bottom != 0;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text(
            widget.editWaste == null ? 'Add Waste' : 'Edit Waste',
            style: TextStyle(color: Colors.black),
          ),
          backgroundColor: Colors.white,
          iconTheme: IconThemeData(color: primaryColor),
          centerTitle: true,
          leading: IconButton(
            icon: Icon(Icons.arrow_back),
            onPressed: () => Navigator.of(context).pop(),
          ),
          elevation: 0.0,
        ),
        body: Padding(
          padding: const EdgeInsets.only(left: 5.0, right: 5.0, top: 10.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              cardDropdown(),
              if (selectedValue == 'Other') ...[
                cardNameEntry(),
                Row(
                  children: [
                    Expanded(child: cardCarbonEntry()), // First column
                    Expanded(child: cardNitrogenEntry()), // Second column
                    Expanded(child: cardMoistureEntry()), // Third column
                  ],
                ),
              ],
              SizedBox(height: 2),
              cardWeightEntry(),
              Spacer(),
              if (!_isKeyboardOpen(context)) buttonsRow(),
            ],
          ),
        ),
      ),
    );
  }

  Widget cardDropdown() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        const Padding(
          padding: EdgeInsets.only(left: 16.0),
          child: Text('Type',
              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold)),
        ),
        const SizedBox(height: 5.0),
        Padding(
          padding: const EdgeInsets.all(5.0),
          child: Container(
            //padding: EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: primaryColor, width: 1),
              borderRadius: BorderRadius.circular(8.0),
              boxShadow: [
                BoxShadow(
                  color: Colors.grey.withOpacity(0.5),
                  spreadRadius: 1,
                  blurRadius: 1,
                  offset: const Offset(0, 1), // changes position of shadow
                ),
              ],
            ),
            child: Stack(
              children: [
                DropdownSearch<String>(
                  popupProps: const PopupProps.menu(
                    showSelectedItems: true,
                    showSearchBox: true,
                  ),
                  items: cnDetails,
                  dropdownDecoratorProps: const DropDownDecoratorProps(
                    dropdownSearchDecoration: InputDecoration(
                      contentPadding: EdgeInsets.symmetric(vertical: 15.0),
                      hintText: 'Select',
                      suffixIcon: Icon(Icons.clear),
                      prefixIcon:
                          Icon(Icons.arrow_drop_down, color: Colors.black),
                      border: InputBorder.none,
                    ),
                  ),
                  onChanged: (newValue) {
                    setState(() {
                      selectedValue = newValue;
                    });
                      //if (selectedValue != 'Other') {
                      //  _cnRatioController.text =
                      //      cnDetails[selectedValue] ?? '';
                  },
                  selectedItem: selectedValue,
                ),
                Positioned(
                  right: 10,
                  top: 15,
                  child: Container(
                    width: 24,
                    height: 24,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget cardNameEntry() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        const Padding(
          padding: EdgeInsets.only(left: 16.0, top: 16.0),
          child: Text('Name',
              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold)),
        ),
        const SizedBox(height: 5.0),
        Card(
          shape: cardShape(),
          child: Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0),
            child: TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.symmetric(vertical: 15.0),
                hintText: 'Enter name',
                border: InputBorder.none,
                prefixIcon:
                    Icon(Icons.add, color: primaryColor), // Added this line
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget cardCarbonEntry() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        const Padding(
          padding: EdgeInsets.only(left: 16.0, top: 16.0),
          child: Text('Carbon',
              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold)),
        ),
        const SizedBox(height: 5.0),
        Card(
          shape: cardShape(),
          child: Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0),
            child: Stack(
              alignment: Alignment.centerRight,
              children: [
                TextField(
                  controller: _carbonController,
                  keyboardType: TextInputType.number,
                  onChanged: (value) {
                    setState(() {
                    });
                  },
                  decoration: const InputDecoration(
                    contentPadding: EdgeInsets.symmetric(vertical: 15.0),
                    hintText: '%',
                    border: InputBorder.none,
                    prefixIcon: Icon(Icons.add, color: primaryColor),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget cardNitrogenEntry() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        const Padding(
          padding: EdgeInsets.only(left: 16.0, top: 16.0),
          child: Text('Nitrogen',
              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold)),
        ),
        const SizedBox(height: 5.0),
        Card(
          shape: cardShape(),
          child: Container(
            padding:
            const EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0),
            child: Stack(
              alignment: Alignment.centerRight,
              children: [
                TextField(
                  controller: _nitrogenController,
                  keyboardType: TextInputType.number,
                  onChanged: (value) {
                    setState(() {
                                          });
                  },
                  decoration: const InputDecoration(
                    contentPadding: EdgeInsets.symmetric(vertical: 15.0),
                    hintText: '%',
                    border: InputBorder.none,
                    prefixIcon: Icon(Icons.add, color: primaryColor),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget cardMoistureEntry() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        const Padding(
          padding: EdgeInsets.only(left: 16.0, top: 16.0),
          child: Text('Moisture',
              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold)),
        ),
        const SizedBox(height: 5.0),
        Card(
          shape: cardShape(),
          child: Container(
            padding:
            const EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0),
            child: Stack(
              alignment: Alignment.centerRight,
              children: [
                TextField(
                  controller: _moistureController,
                  keyboardType: TextInputType.number,
                  onChanged: (value) {
                    setState(() {

                    });
                  },
                  decoration: const InputDecoration(
                    contentPadding: EdgeInsets.symmetric(vertical: 15.0),
                    hintText: '%',
                    border: InputBorder.none,
                    prefixIcon: Icon(Icons.add, color: primaryColor),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget cardWeightEntry() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        const Padding(
          padding: EdgeInsets.only(left: 16.0, top: 16.0),
          child: Text('Quantity',
              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold)),
        ),
        const SizedBox(height: 5.0),
        Card(
          shape: cardShape(),
          child: Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0),
            child: Stack(
              alignment: Alignment.centerRight,
              children: [
                TextField(
                  controller: _weightController,
                  keyboardType: TextInputType.number,
                  onChanged: (value) {
                    setState(() {
                      _showKgSuffix = value
                          .isNotEmpty; // You can rename this to _showKgSuffix
                    });
                  },
                  decoration: const InputDecoration(
                    contentPadding: EdgeInsets.symmetric(vertical: 15.0),
                    hintText: 'Enter Quantity',
                    border: InputBorder.none,
                    prefixIcon: Icon(Icons.add, color: primaryColor),
                  ),
                ),
                if (_showKgSuffix)
                  Padding(
                    padding: EdgeInsets.only(
                      right: MediaQuery.of(context).size.width * 0.65, // 'factor' is a fraction of the screen width
                    ),
                    child: Text("kg", style: TextStyle(fontSize: 16.0)),
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget buttonsRow() {
    // Get the screen width
    double screenWidth = MediaQuery.of(context).size.width;

    // Calculate the horizontal padding based on the screen width
    double horizontalPadding = screenWidth * 0.05; // for example, 5% of screen width

    return Padding(
      padding: EdgeInsets.only(bottom: 30.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center, // Center the buttons in the row
        children: <Widget>[
          Padding(
            padding: EdgeInsets.only(right: horizontalPadding / 2), // Half of the calculated padding
            child: ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              style: ElevatedButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: const Color(0xFFC31818),
                padding: const EdgeInsets.symmetric(horizontal: 32.0, vertical: 8.0),
                textStyle: const TextStyle(fontSize: 18.0),
              ),
              child: const Text('Cancel'),
            ),
          ),
          Padding(
            padding: EdgeInsets.only(left: horizontalPadding / 2), // Half of the calculated padding
            child: ElevatedButton(
              onPressed: _handleAddButton,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.transparent,
                shadowColor: Colors.transparent,
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
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 40.0, vertical: 8.0),
                  child: Text(widget.editWaste == null ? 'Add' : 'Update',
                      style: const TextStyle(color: Colors.white, fontSize: 18.0)),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }


  void _handleAddButton() {
    if (_weightController.text.isEmpty ||
        (selectedValue == 'Other' && _nameController.text.isEmpty) ||
        (selectedValue == 'Other' && _carbonController.text.isEmpty) ||
        (selectedValue == 'Other' && _nitrogenController.text.isEmpty) ||
        (selectedValue == 'Other' && _moistureController.text.isEmpty)) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Error'),
          content: const Text('Please fill in all required fields.'),
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
    } else {
      Waste newOrEditedWaste = Waste(
        selectedValue: selectedValue!,
        weight: _weightController.text,
        name: _nameController.text,
        carbon: _carbonController.text,
        nitrogen: _nitrogenController.text,
        moisture: _moistureController.text,
      );

      if (widget.editWaste != null) {
        // If it's an edit operation, update the existing waste
        // Here, you'll need to define the logic on how you want to update
        // the waste in your data source.
        // This could involve finding the matching waste in your 'wastes' list
        // and updating it.

        int index = Provider.of<WasteData>(context, listen: false)
            .wastes
            .indexWhere((waste) => waste == widget.editWaste);
        if (index != -1) {
          Provider.of<WasteData>(context, listen: false).wastes[index] =
              newOrEditedWaste;
        }

        // Inform listeners about the change
        Provider.of<WasteData>(context, listen: false).notifyListeners();

        print("Updating waste with name: ${newOrEditedWaste.selectedValue}");
      } else {
        // If it's an add operation, then add a new waste
        Provider.of<WasteData>(context, listen: false)
            .addWaste(newOrEditedWaste);
        print("Adding waste with name: ${newOrEditedWaste.selectedValue}");
      }

      // Finally, pop the screen and optionally return the new/edited waste
      Navigator.of(context).pop(newOrEditedWaste);
    }
  }

  RoundedRectangleBorder cardShape() {
    return RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8.0),
        side: const BorderSide(color: primaryColor, width: 1));
  }
}
