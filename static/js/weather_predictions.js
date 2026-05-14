async function executePredictiveAnalysis(event) {
    event.preventDefault();
    
    const cityValue = document.getElementById('predictCityInput').value.trim();
    const speciesValue = document.getElementById('predictSpeciesInput').value;
    const spinner = document.getElementById('predictSpinner');
    const errorBox = document.getElementById('predictErrorBox');
    const outputBlock = document.getElementById('predictionsOutputBlock');
    const submitBtn = document.getElementById('submitPredictBtn');

    if(!cityValue) {
        errorBox.innerText = "⚠️ Input Error: Please enter a target city name before submitting.";
        errorBox.style.display = 'block';
        return;
    }

    errorBox.style.display = 'none';
    outputBlock.style.display = 'none';
    spinner.style.display = 'block';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/api/predictions/fetch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                city_input: cityValue,
                target_species: speciesValue 
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Predictive framework exception.');
        }

        document.getElementById('resolvedPredictTitle').innerText = `📍 Radar Target: ${data.city}`;
        document.getElementById('speciesDynamicLabel').innerText = data.target_species;
        
        document.getElementById('fishScoreVal').innerText = `${data.angling_forecast.score}%`;
        document.getElementById('fishVerdictLabel').innerText = data.angling_forecast.verdict;
        document.getElementById('fishSeasonText').innerText = data.angling_forecast.season;
        document.getElementById('fishLunarText').innerText = data.angling_forecast.lunar;
        document.getElementById('fishStrategyText').innerText = data.angling_forecast.strategy;

        document.getElementById('predFront').innerText = data.predictions.front;
        document.getElementById('predPrecip').innerText = data.predictions.precip_risk;
        document.getElementById('predWind').innerText = data.predictions.wind;
        document.getElementById('predBaro').innerText = data.predictions.baro_trend;

        document.getElementById('telTemp').innerText = `${data.metrics.temp}°F`;
        document.getElementById('telBaro').innerText = `${data.metrics.pressure} mb`;

        const speedVal = data.metrics.wind_speed !== undefined ? data.metrics.wind_speed : 0;
        const dirVal = data.metrics.wind_dir !== undefined ? data.metrics.wind_dir : 'N';

        document.getElementById('telWind').innerText = `${speedVal} mph ${dirVal}`;
        document.getElementById('telHumid').innerText = `${data.metrics.humidity}%`;

        const historyContainer = document.getElementById('predictHistoryBox');
        historyContainer.innerHTML = '';
        data.history.forEach(log => {
            const line = document.createElement('div');
            line.style.padding = "4px 0";
            line.style.borderBottom = "1px solid #2e2e2e";
            line.innerHTML = `• <span style="color:var(--primary); font-weight:bold;">${log.city}</span>: ${log.temp}°F loaded at [${log.time}]`;
            historyContainer.appendChild(line);
        });

        outputBlock.style.display = 'block';

    } catch (err) {
        errorBox.innerText = `⚠️ Error: ${err.message}`;
        errorBox.style.display = 'block';
    } finally {
        spinner.style.display = 'none';
        submitBtn.disabled = false;
    }
}
