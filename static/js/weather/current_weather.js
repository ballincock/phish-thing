async function dispatchWeatherQuery(event) {
    event.preventDefault();
    
    const inputVal = document.getElementById('targetLocationInput').value;
    const spinner = document.getElementById('weatherSpinner');
    const errorBox = document.getElementById('errorBroadcastBox');
    const outputFrame = document.getElementById('weatherDataPresentationFrame');
    const submitBtn = document.getElementById('submitQueryBtn');

    errorBox.style.display = 'none';
    outputFrame.style.display = 'none';
    spinner.style.display = 'block';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/api/weather/fetch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location: inputVal })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Server processed an unrecognized parsing exception.');
        }

        document.getElementById('resolvedAddressHeader').innerText = `📍 Location Resolved: ${data.resolvedAddress}`;
        document.getElementById('liveTempDisplay').innerText = `${data.currentConditions.temp}°C`;
        document.getElementById('liveConditionsText').innerText = data.currentConditions.conditions;
        document.getElementById('liveOverviewParagraph').innerText = data.description || '';
        document.getElementById('metricFeelsLike').innerText = `${data.currentConditions.feelslike}°C`;
        document.getElementById('metricHumidity').innerText = `${data.currentConditions.humidity}%`;
        document.getElementById('metricWind').innerText = `${data.currentConditions.windspeed} km/h`;
        document.getElementById('metricUV').innerText = data.currentConditions.uvindex;

        const trendsContainer = document.getElementById('trendsForecastContainer');
        trendsContainer.innerHTML = ''; 

        data.days.slice(0, 3).forEach(day => {
            const dayRow = document.createElement('div');
            dayRow.style = "background: #252525; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #333;";
            dayRow.innerHTML = `
                <div style="max-width: 70%;">
                    <strong style="color: var(--primary); font-size: 1.05rem;">${day.datetime}</strong>
                    <div style="font-size: 0.85rem; color: #bbb; margin-top: 4px;">${day.description}</div>
                </div>
                <div style="text-align: right; white-space: nowrap; font-weight: 700; font-size: 1rem;">
                    <span style="color: #ff6b6b;">↑ ${day.tempmax}°</span>
                    <span style="color: #444; margin: 0 5px;">|</span>
                    <span style="color: #4dadff;">↓ ${day.tempmin}°</span>
                </div>
            `;
            trendsContainer.appendChild(dayRow);
        });

        outputFrame.style.display = 'block';

    } catch (err) {
        errorBox.innerText = `⚠️ Error: ${err.message}`;
        errorBox.style.display = 'block';
    } finally {
        spinner.style.display = 'none';
        submitBtn.disabled = false;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const defaultRegion = document.getElementById('targetLocationInput').value;
    if(defaultRegion) {
        document.getElementById('weatherQueryForm').requestSubmit();
    }
});
