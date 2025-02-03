document.getElementById('citySearchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const city = document.getElementById('cityInput').value;
    const resultsDiv = document.getElementById('cityResults');
    
    try {
        const response = await fetch('/search_regions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `city=${encodeURIComponent(city)}`
        });
        
        const data = await response.json();
        
        if (data.length > 0) {
            let html = '<h4>Wine regions found:</h4><ul>';
            data.forEach(region => {
                html += `
                    <li>
                        <strong>${region.name}</strong> (${region.country})
                        <br>
                        Distance: ${region.distance.toFixed(2)} km
                        <br>
                        Features: ${region.features}
                    </li>`;
            });
            html += '</ul>';
            resultsDiv.innerHTML = html;
        } else {
            resultsDiv.innerHTML = `<p>No wine regions found within 100 km of ${city}.</p>`;
        }
    } catch (error) {
        resultsDiv.innerHTML = '<p>Error searching for wine regions. Please try again.</p>';
    }
});

document.getElementById('countrySearchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const country = document.getElementById('countryInput').value;
    const resultsDiv = document.getElementById('countryResults');
    
    try {
        const response = await fetch('/country_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `country=${encodeURIComponent(country)}`
        });
        
        const data = await response.json();
        
        if (data.success) {
            let html = `<h4>${data.count} wine regions found:</h4><ul>`;
            data.regions.forEach(region => {
                html += `
                    <li>
                        <strong>${region.name}</strong>
                        <br>
                        ${region.features}
                    </li>`;
            });
            html += '</ul>';
            resultsDiv.innerHTML = html;
        } else {
            if (data.suggestions.length > 0) {
                let html = `<p>Country not found. Did you mean:</p><ul>`;
                data.suggestions.forEach(suggestion => {
                    html += `<li>${suggestion}</li>`;
                });
                html += '</ul>';
                resultsDiv.innerHTML = html;
            } else {
                resultsDiv.innerHTML = `<p>No wine regions found for this country.</p>`;
            }
        }
    } catch (error) {
        resultsDiv.innerHTML = '<p>Error searching for country information. Please try again.</p>';
    }
}); 