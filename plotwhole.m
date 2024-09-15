function plotwhole(csv_file)
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
        day_temperature = mean([data.temperature_active1(mask), ...
                                data.temperature_active2(mask), ...
                                data.temperature_active3(mask), ...
                                data.temperature_active4(mask)], 2);
        day_oxygen = data.oxygen(mask);
        day_methane = data.methane(mask);

        % Detect dips in temperature and rises in oxygen
        temp_dips = find(diff(day_temperature) < -2); % Temperature dips by more than 2°C
        o2_rises = find(diff(day_oxygen) > 1);        % Oxygen increases by more than 1%

        % Create a 3-row subplot for temperature, methane, and oxygen
        subplot(3, 1, 1); % Temperature plot
        plot(day_time, day_temperature, '-b', 'LineWidth', 2);
        hold on;
        plot(day_time(temp_dips), day_temperature(temp_dips), 'rv', 'MarkerFaceColor', 'r'); % Mark temperature dips
        title(['Day: ', datestr(day, 'yyyy-mm-dd')]);
        ylabel('Avg Temperature (°C)');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;

        % Methane plot in a separate subplot
        subplot(3, 1, 2);
        plot(day_time, day_methane, '-r', 'LineWidth', 2);
        ylabel('Methane (ppm)');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;

        % Oxygen plot in a separate subplot
        subplot(3, 1, 3);
        plot(day_time, day_oxygen, '-g', 'LineWidth', 2);
        hold on;
        plot(day_time(o2_rises), day_oxygen(o2_rises), 'kv', 'MarkerFaceColor', 'k'); % Mark oxygen increases
        ylabel('Oxygen (%)');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;
    end
end
