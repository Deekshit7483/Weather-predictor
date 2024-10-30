document.getElementById('fetchWeatherBtn').addEventListener('click', async () => {
    const city = document.getElementById('cityInput').value;
    const currentWeatherDiv = document.getElementById('currentWeather');
    const timeSeriesDiv = document.getElementById('timeSeries');

    if (!city) {
        alert("Please enter a city name.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/weather?city=${city}`);
        const data = await response.json();

        if (data.error) {
            currentWeatherDiv.innerHTML = `<p>${data.error}</p>`;
            timeSeriesDiv.innerHTML = '';
        } else {
            currentWeatherDiv.innerHTML = `
                <h2>Current Weather:</h2>
                <p>Temperature: ${data.current.temperature}°C</p>
                <p>Humidity: ${data.current.humidity}%</p>
                <p>Description: ${data.current.description}</p>
            `;

            // Display time series data
            timeSeriesDiv.innerHTML = '<h2>7-Day Weather Forecast:</h2>';
            data.time_series.forEach(day => {
                timeSeriesDiv.innerHTML += `
                    <p>${day.date}: Temperature: ${day.temperature}°C, Humidity: ${day.humidity}%</p>
                `;
            });
        }
    } catch (error) {
        currentWeatherDiv.innerHTML = `<p>Error fetching weather data.</p>`;
        timeSeriesDiv.innerHTML = '';
    }
});
