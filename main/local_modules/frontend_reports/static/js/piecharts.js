function pie_chart_companies(companies, target) {
    google.load('visualization', '1', {packages: ['corechart']});

    google.setOnLoadCallback(function () {
        drawPiechart(
            companies, target
        );
    });


    function drawPiechart(companies, target) {
        var data = google.visualization.arrayToDataTable(companies);
        var options = {
            backgroundColor: '#f1f8e9',
            title: 'Repartition of companies by countries.',
        };

        var chart = new google.visualization.PieChart(document.getElementById(target));
        chart.draw(data, options);
    }
}

