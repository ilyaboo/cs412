document.addEventListener("DOMContentLoaded", function () {
    // Retrieve historical data from the hidden HTML element
    const historicalData = JSON.parse(document.getElementById("historicalPrices").textContent);

    // Extract all dates and prices
    const allDates = Object.keys(historicalData.Close).map(date => new Date(date));
    const allPrices = Object.values(historicalData.Close);

    // Format dates for display
    const formattedDates = allDates.map(date =>
        date.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })
    );

    // Initialize Chart.js
    const ctx = document.getElementById("priceChart").getContext("2d");
    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: formattedDates,
            datasets: [
                {
                    label: "Price Over Time",
                    data: allPrices,
                    borderColor: "rgba(75, 192, 192, 1)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderWidth: 2,
                    pointRadius: 2,
                    tension: 0.2,
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                tooltip: { enabled: true },
            },
            scales: {
                x: { title: { display: true, text: "Date" } },
                y: {
                    title: { display: true, text: "Price ($)" },
                    ticks: {
                        callback: function (value) {
                            return value.toFixed(2); // Ensure 2 decimal digits
                        },
                    },
                },
            },
        },
    });

    // Update chart based on selected period
    document.getElementById("timePeriod").addEventListener("change", function () {
        const days = parseInt(this.value);
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - days);

        // Filter data based on the selected time period
        const filteredDates = [];
        const filteredPrices = [];
        allDates.forEach((date, index) => {
            if (date >= cutoffDate) {
                filteredDates.push(formattedDates[index]);
                filteredPrices.push(allPrices[index]);
            }
        });

        // Update chart data
        chart.data.labels = filteredDates;
        chart.data.datasets[0].data = filteredPrices;
        chart.update();
    });
});
