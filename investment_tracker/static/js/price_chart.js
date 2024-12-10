document.addEventListener("DOMContentLoaded", function () {

    // retrieving historical data for all time periods
    const timePeriodData = {
        "1d": JSON.parse(document.getElementById("dayHistoricalPrices").textContent),
        "5d": JSON.parse(document.getElementById("fiveDaysHistoricalPrices").textContent),
        "1mo": JSON.parse(document.getElementById("monthHistoricalPrices").textContent),
        "3mo": JSON.parse(document.getElementById("threeMonthsHistoricalPrices").textContent),
        "6mo": JSON.parse(document.getElementById("sixMonthsHistoricalPrices").textContent),
        "1y": JSON.parse(document.getElementById("yearHistoricalPrices").textContent),
        "2y": JSON.parse(document.getElementById("twoYearsHistoricalPrices").textContent),
        "5y": JSON.parse(document.getElementById("fiveYearsHistoricalPrices").textContent),
    };

    // function to format dates
    function formatDates(data, period) {
        const dates = Object.keys(data.Close).map(date => new Date(date));
        if (["1d", "5d"].includes(period)) {
            return dates.map(date => date.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" }));
        }
        return dates.map(date => date.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" }));
    }

    // function to get prices
    function getPrices(data) {
        return Object.values(data.Close);
    }

    // initializing the chart with 1-month data
    const ctx = document.getElementById("priceChart").getContext("2d");
    const initialData = timePeriodData["1mo"];
    const initialDates = formatDates(initialData, "1mo");
    const initialPrices = getPrices(initialData);

    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: initialDates,
            datasets: [
                {
                    label: "Price Over Time (1 Month)",
                    data: initialPrices,
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
                legend: { display: false },
                tooltip: { enabled: true },
            },
            scales: {
                x: { title: { display: true, text: "Date" } },
                y: {
                    title: { display: true, text: "Price ($)" },
                    ticks: {
                        callback: function (value) {
                            return `$${value.toFixed(2)}`;
                        },
                    },
                },
            },
        },
    });

    // updating chart based on selected period
    document.getElementById("timePeriod").addEventListener("change", function () {
        const selectedPeriod = this.value;
        const selectedData = timePeriodData[selectedPeriod];
        const formattedDates = formatDates(selectedData, selectedPeriod);
        const prices = getPrices(selectedData);

        chart.data.labels = formattedDates;
        chart.data.datasets[0].data = prices;
        chart.data.datasets[0].label = `Price Over Time (${this.options[this.selectedIndex].text})`;
        chart.update();
    });
});
