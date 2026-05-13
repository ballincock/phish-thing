async function dispatchHistoricalQuery(event) {
    event.preventDefault();
    
    const locationVal = document.getElementById('histLocationInput').value;
    const startDateVal = document.getElementById('histStartDate').value;
    const endDateVal = document.getElementById('histEndDate').value;
    
    const spinner = document.getElementById('historicalSpinner');
    const errorBox = document.getElementById('histErrorBox');
    const displayArea = document.getElementById('historicalPresentationArea');
    const submitBtn = document.getElementById('submitHistBtn');

    if (new Date(startDateVal) > new Date(endDateVal)) {
        errorBox.innerText = "⚠️ Error: The selection timeline is invalid. Start Date must fall before or on the End Date.";
        errorBox.style.display = 'block';
        return;
    }

    errorBox.style.display = 'none';
    displayArea.style.display = 'none';
    spinner.style.display = 'block';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/api/historical/fetch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                location: locationVal,
                start_date: startDateVal,
                end_date: endDateVal
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Server processed an unrecognized parsing exception.');
        }

        document.getElementById('resolvedHistLocationHeader').innerText = `📍 Region Profile: ${data.resolvedAddress}`;
        document.getElementById('resolvedHistTimezone').innerText = `Timezone: ${data.timezone}`;
        document.getElementById('rangeOverviewParagraph').innerText = data.description || 'Historical time-range meteorological records parsed successfully.';

        const daysContainer = document.getElementById('historicalDaysContainer');
        daysContainer.innerHTML = '';

        if(data.days && data.days.length > 0) {
            data.days.forEach(day => {
                const row = document.createElement('div');
                row.style = "background: #252525; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #333;";
                row.innerHTML = `
                    <div style="max-width: 70%;">
                        <strong style="color: var(--primary); font-size: 1.05rem;">${day.datetime}</strong>
                        <div style="font-size: 0.85rem; color: #ccc; margin-top: 3px;">${day.conditions || 'Conditions Data Unmapped'}</div>
                        <div style="font-size: 0.75rem; color: #888; margin-top: 2px;">Humidity: ${day.humidity}% | Wind: ${day.windspeed} km/h</div>
                    </div>
                    <div style="text-align: right; white-space: nowrap; font-weight: 700; font-size: 1rem;">
                        <span style="color: #ff6b6b;">↑ ${day.tempmax}°C</span>
                        <span style="color: #444; margin: 0 5px;">|</span>
                        <span style="color: #4dadff;">↓ ${day.tempmin}°C</span>
                    </div>
                `;
                daysContainer.appendChild(row);
            });
        } else {
            daysContainer.innerHTML = '<div style="color:#aaa; text-align:center; padding:10px;">No diagnostic entries mapped inside the provided range parameters.</div>';
        }

        displayArea.style.display = 'block';

    } catch (err) {
        errorBox.innerText = `⚠️ Error: ${err.message}`;
        errorBox.style.display = 'block';
    } finally {
        spinner.style.display = 'none';
        submitBtn.disabled = false;
    }
}
