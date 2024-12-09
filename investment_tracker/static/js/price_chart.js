document.addEventListener("DOMContentLoaded", function () {

    // retrieving historical data from the HTML element
    const historicalData = JSON.parse(document.getElementById("historicalPrices").textContent);

    // extracting labels (dates) and data (prices) for the graph
    const labels = Object.keys(historicalData.Close);
    const prices = Object.values(historicalData.Close);

    // creating the line chart
    const ctx = document.getElementById("priceChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Price Over Time",
                    data: prices,
                    borderColor: "rgba(75, 192, 192, 1)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderWidth: 2,
                    pointRadius: 2,
                    tension: 0.2, // Smooth curve
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
                y: { title: { display: true, text: "Price ($)" }, beginAtZero: false },
            },
        },
    });
});