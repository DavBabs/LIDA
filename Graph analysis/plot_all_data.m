function plot_all_data(csv_file)
    % Read the CSV file
    data = readtable(csv_file);

    % Convert the timestamp to datetime (assuming it's already in AEST format)
    data.time_stamp = datetime(data.time_stamp, 'InputFormat', 'yyyy-MM-dd HH:mm:ss', 'TimeZone', 'Australia/Sydney');

    % Define the date range (28/06 to 18/07)
    start_date = datetime(2024, 6, 28, 'TimeZone', 'Australia/Sydney');
    end_date = datetime(2024, 7, 18, 'TimeZone', 'Australia/Sydney');
    
    % Filter the data to only include entries within the date range
    mask_date_range = (data.time_stamp >= start_date) & (data.time_stamp <= end_date);
    data = data(mask_date_range, :);

    % Extract timestamps for the entire range
    time = data.time_stamp;

    % Extract temperature data (1, 2, 3, 4)
    temp1 = data.temperature_active1;
    temp2 = data.temperature_active2;
    temp3 = data.temperature_active3;
    temp4 = data.temperature_active4;

    % Extract moisture data (1, 2)
    moisture1 = data.moisture_active1;
    moisture2 = data.moisture_active2;

    % Extract CO2, Methane, and Oxygen
    co2 = data.co2;
    methane = data.methane;
    oxygen = data.oxygen;  % Oxygen has values between 10-15

    % Create the figure
    figure('Name', 'All Data Plot');

    % Plot Temperature 1, 2, 3, 4 in the first row (overlayed)
    subplot(3, 1, 1);
    plot(time, temp1, '-r', 'LineWidth', 2); hold on;
    plot(time, temp2, '-b', 'LineWidth', 2);
    plot(time, temp3, '-g', 'LineWidth', 2);
    plot(time, temp4, '-k', 'LineWidth', 2);
    title('Temperature Data (28/06 - 18/07)');
    ylabel('Temperature (°C)');
    legend('Temp 1', 'Temp 2', 'Temp 3', 'Temp 4');
    datetick('x', 'dd-mmm HH:MM', 'keeplimits');
    grid on;

    % Plot Active moisture 1 and 2 in the second row (overlayed)
    subplot(3, 1, 2);
    plot(time, moisture1, '-m', 'LineWidth', 2); hold on;
    plot(time, moisture2, '-c', 'LineWidth', 2);
    ylabel('Moisture');
    legend('Moisture 1', 'Moisture 2');
    datetick('x', 'dd-mmm HH:MM', 'keeplimits');
    grid on;

    % Plot CO2, Methane, and Oxygen on a shared graph with dual y-axes in the third row
    subplot(3, 1, 3);
    yyaxis left;
    plot(time, co2, '-r', 'LineWidth', 2); hold on;
    ylabel('CO2 (ppm)');
    yyaxis right;
    plot(time, methane, '-b', 'LineWidth', 2); hold on;
    plot(time, oxygen, '-g', 'LineWidth', 2);
    ylabel('Methane / Oxygen');
    legend('CO2', 'Methane', 'Oxygen');
    datetick('x', 'dd-mmm HH:MM', 'keeplimits');
    grid on;

    % Set x-axis label for the entire figure
    xlabel('Time');
end
