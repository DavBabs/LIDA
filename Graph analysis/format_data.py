import csv
from datetime import datetime, timezone, timedelta

# Function to convert timestamp to AEST (Australian Eastern Standard Time)
def convert_timestamp_to_aest(epoch_time):
    # Convert epoch time to datetime object
    dt = datetime.fromtimestamp(epoch_time / 1000, tz=timezone.utc)
    # Convert to AEST (UTC+10)
    aest = dt + timedelta(hours=10)
    return aest.strftime('%Y-%m-%d %H:%M:%S')

# Function to process the input CSV and write to output CSV
def process_csv(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        # Define the output fieldnames
        fieldnames = [
            'moisture_active1', 'moisture_active2', 'oxygen', 'lid', 'co2', 'time_stamp',
            'device_id', 'temperature_curing1', 'temperature_curing2',
            'moisture_curing1', 'moisture_curing2', 'automation_active',
            'methane', 'temperature_active1', 'temperature_active2',
            'temperature_active3', 'temperature_active4'
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Split the list values and map them to the appropriate columns
            moisture_active = eval(row['moisture_active'])  # Convert string to list
            temperature_active = eval(row['temperature_active'])  # Convert string to list
            temperature_curing = eval(row['temperature_curing'])  # Convert string to list
            moisture_curing = eval(row['moisture_curing'])  # Convert string to list

            # Create a new row with the required format
            new_row = {
                'moisture_active1': moisture_active[0],
                'moisture_active2': moisture_active[1],
                'oxygen': row['oxygen'],
                'lid': row['lid'],
                'co2': row['co2'],
                'time_stamp': convert_timestamp_to_aest(int(row['time_stamp'])),
                'device_id': row['device_id'],
                'temperature_curing1': temperature_curing[0],
                'temperature_curing2': temperature_curing[1],
                'moisture_curing1': moisture_curing[0],
                'moisture_curing2': moisture_curing[1],
                'automation_active': row['automation_active'],
                'methane': row['methane'],
                'temperature_active1': temperature_active[0],
                'temperature_active2': temperature_active[1],
                'temperature_active3': temperature_active[2],
                'temperature_active4': temperature_active[3],
            }

            # Write the new row to the output CSV
            writer.writerow(new_row)

# Specify the input and output file paths
input_file = 'lida_table_exportFull.csv'
output_file = 'lida_tableCleaned.csv'

# Call the function to process the CSV
process_csv(input_file, output_file)
