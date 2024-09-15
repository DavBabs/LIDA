function plot_csv_data_day_by_day(csv_file)
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

    % Get unique days within the filtered date range
    unique_days = unique(dateshift(data.time_stamp, 'start', 'day'));
    num_days = length(unique_days);
    current_day_index = 1;

    % Create the figure
    fig = figure('Name', 'Day-by-Day Data Plot', 'KeyPressFcn', @key_press);

    % Plot the first day's data
    plot_day_data(current_day_index);

    % Key press callback function to navigate between days
    function key_press(~, event)
        if strcmp(event.Key, 'rightarrow')
            current_day_index = min(current_day_index + 1, num_days);
            plot_day_data(current_day_index);
        elseif strcmp(event.Key, 'leftarrow')
            current_day_index = max(current_day_index - 1, 1);
            plot_day_data(current_day_index);
        end
    end

    % Function to plot the data for a specific day
    function plot_day_data(day_index)
        clf; % Clear the current figure
        day = unique_days(day_index);
        
        % Extract data for the current day
        mask = (dateshift(data.time_stamp, 'start', 'day') == day);
        day_time = data.time_stamp(mask);
        
        % Extract temperature data (1, 2, 3, 4)
        temp1 = data.temperature_active1(mask);
        temp2 = data.temperature_active2(mask);
        temp3 = data.temperature_active3(mask);
        temp4 = data.temperature_active4(mask);

        % Extract moisture data (1, 2)
        moisture1 = data.moisture_active1(mask);
        moisture2 = data.moisture_active2(mask);

        % Extract CO2, Methane, and Oxygen
        co2 = data.co2(mask);
        methane = data.methane(mask);
        oxygen = data.oxygen(mask);  % Oxygen now has values between 10-15

        % Plot Temperature 1, 2, 3, 4 in separate subplots
        subplot(4, 1, 1);
        plot(day_time, temp1, '-r', 'LineWidth', 2); hold on;
        plot(day_time, temp2, '-b', 'LineWidth', 2);
        plot(day_time, temp3, '-g', 'LineWidth', 2);
        plot(day_time, temp4, '-k', 'LineWidth', 2);
        title(['Day: ', datestr(day, 'yyyy-mm-dd')]);
        ylabel('Temperature (°C)');
        legend('Temp 1', 'Temp 2', 'Temp 3', 'Temp 4');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;

        % Plot Active moisture 1 and 2
        subplot(4, 1, 2);
        plot(day_time, moisture1, '-m', 'LineWidth', 2); hold on;
        plot(day_time, moisture2, '-c', 'LineWidth', 2);
        ylabel('Moisture');
        legend('Moisture 1', 'Moisture 2');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;

        % Plot CO2 and Methane with oxygen in its own subplot for clarity
        subplot(4, 1, 3);
        plot(day_time, co2, '-r', 'LineWidth', 2); hold on;
        plot(day_time, methane, '-b', 'LineWidth', 2);
        ylabel('CO2 / Methane');
        legend('CO2', 'Methane');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;

        % Plot Oxygen in a separate subplot
        subplot(4, 1, 4);
        plot(day_time, oxygen, '-g', 'LineWidth', 2);
        ylabel('Oxygen (%)');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;
    end
end
