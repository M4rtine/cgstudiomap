function geo_chart(companies, target) {

    google.load('visualization', '1', {packages: ['geochart']});
    google.setOnLoadCallback(drawRegionsMap);

    function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable(companies);
        var options = {
            colorAxis: {colors: ['#E8CFF7', '#B86BE5']},
            backgroundColor: '#F2F2F2',
            width: '100%'
        };
        var chart = new google.visualization.GeoChart(
            document.getElementById(target)
        );
        chart.draw(data, options);
    }
}
