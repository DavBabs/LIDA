function plot_csv_data_day_by_day(csv_file)
    % Read the CSV file
    data = readtable(csv_file);

    % Convert the timestamp to datetime (since it's already in AEST format)
    data.time_stamp = datetime(data.time_stamp, 'InputFormat', 'yyyy-MM-dd HH:mm:ss', 'TimeZone', 'Australia/Sydney');

    % Get unique days
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
        day_data = data(dateshift(data.time_stamp, 'start', 'day') == day, :);

        % Calculate the average temperature_active for each timestamp
        avg_temperature_active = mean([day_data.temperature_active1, ...
                                       day_data.temperature_active2, ...
                                       day_data.temperature_active3, ...
                                       day_data.temperature_active4], 2);
        
        % Normalize temperature using a smoothing function (remove dips)
        normalized_temperature_active = movmean(avg_temperature_active, 5); % Adjust window size as needed

        % Create a 3-row subplot for temperature, methane, and oxygen
        subplot(3, 1, 1); % Temperature plot
        plot(day_data.time_stamp, normalized_temperature_active, '-b', 'LineWidth', 2);
        title(['Day: ', datestr(day, 'yyyy-mm-dd')]);
        ylabel('Normalized Avg Temperature (°C)');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;

        % Methane plot in a separate subplot
        subplot(3, 1, 2);
        plot(day_data.time_stamp, day_data.methane, '-r', 'LineWidth', 2);
        ylabel('Methane (ppm)');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;

        % Oxygen plot in a separate subplot
        subplot(3, 1, 3);
        plot(day_data.time_stamp, day_data.oxygen, '-g', 'LineWidth', 2);
        ylabel('Oxygen (%)');
        xlabel('Time');
        datetick('x', 'HH:MM');
        grid on;
    end
end
