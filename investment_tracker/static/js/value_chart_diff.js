document.addEventListener("DOMContentLoaded", function () {

    // retrieving historical data for all time periods
    const timePeriodData = {
        "1d": JSON.parse(document.getElementById("dayHistoricalPricesDifferences").textContent),
        "5d": JSON.parse(document.getElementById("fiveDaysHistoricalPricesDifferences").textContent),
        "1mo": JSON.parse(document.getElementById("monthHistoricalPricesDifferences").textContent),
        "3mo": JSON.parse(document.getElementById("threeMonthsHistoricalPricesDifferences").textContent),
        "6mo": JSON.parse(document.getElementById("sixMonthsHistoricalPricesDifferences").textContent),
        "1y": JSON.parse(document.getElementById("yearHistoricalPricesDifferences").textContent),
        "2y": JSON.parse(document.getElementById("twoYearsHistoricalPricesDifferences").textContent),
        "5y": JSON.parse(document.getElementById("fiveYearsHistoricalPricesDifferences").textContent),
    };

    // retrieving portfolio creation date
    const rawCreationDate = document.getElementById("portfolioCreationDate").textContent.trim();
    const portfolioCreationDate = new Date(rawCreationDate.replace(" ", "T"));
    console.log("Parsed portfolio creation date:", portfolioCreationDate);

    // retrieving portfolio initial cost
    const rawMoneyInvested = document.getElementById("portfolioMoneyInvested").textContent.trim();
    const portfolioMoneyInvested = parseFloat(rawMoneyInvested);
    console.log("Initial portfolio cost:", portfolioMoneyInvested);

    // function to format dates
    function formatDates(data) {
        return Object.keys(data.Close).map(date => new Date(date));
    }

    // function to get prices
    function getPrices(data) {
        return Object.values(data.Close);
    }

    // initializing the chart with 1-month data
    const ctx = document.getElementById("differenceChart").getContext("2d");
    const initialData = timePeriodData["1mo"];
    const initialDates = formatDates(initialData);
    const initialPrices = getPrices(initialData);

    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: initialDates,
            datasets: [
                {
                    data: initialPrices,
                    borderColor: "rgba(75, 192, 192, 1)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderWidth: 2,
                    pointRadius: 2,
                    tension: 0.2,
                    fill: false,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true },
                annotation: {
                    annotations: {
                        horizontalLine: {
                            type: "line",
                            yMin: 0,
                            yMax: 0,
                            borderColor: "#E74C3C",
                            borderDash: [5, 5],
                            borderWidth: 2,
                            label: {
                                display: true,
                                position: "start",
                                backgroundColor: "#E74C3C",
                                color: "white",
                                font: {
                                    size: 12,
                                },
                                padding: 6,
                            },
                        },
                        verticalLine: {
                            type: "line",
                            xMin: portfolioCreationDate.getTime(),
                            xMax: portfolioCreationDate.getTime(),
                            borderColor: "#28B463",
                            borderDash: [5, 5],
                            borderWidth: 2,
                            label: {
                                display: true,
                                content: `Portfolio Created on ${portfolioCreationDate.toLocaleDateString()}`,
                                position: "start",
                                backgroundColor: "#28B463",
                                color: "white",
                                font: {
                                    size: 12,
                                },
                                padding: 6,
                            },
                        },
                    },
                },
            },
            scales: {
                x: {
                    type: "time",
                    time: { unit: "day", tooltipFormat: "Pp" },
                    title: { display: true, text: "Date" },
                },
                y: {
                    title: { display: true, text: "Portfolio Value Change ($)" },
                    ticks: {
                        callback: function (value) {
                            return `${value < 0 ? '-' : ''}$${Math.abs(value).toFixed(2)}`;
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
        const formattedDates = formatDates(selectedData);
        const prices = getPrices(selectedData);

        chart.data.labels = formattedDates;
        chart.data.datasets[0].data = prices;
        chart.update();
    });
});
