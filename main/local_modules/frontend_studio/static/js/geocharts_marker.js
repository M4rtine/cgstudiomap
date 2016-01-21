function geo_chart_marker(city_name, latitude, longitude, country_code, target) {
	window.onresize = function () {
		drawRegionsMap();
	};

	window.onload = function () {
		drawRegionsMap();
	};

    google.load('visualization', '1', {packages: ['geochart']});
    google.setOnLoadCallback(drawRegionsMap);

    function drawRegionsMap() {
        var options = {
            legend: 'none',
            colorAxis: {colors: ['#E8CFF7', '#B86BE5']},
            backgroundColor: 'transparent',
            keepAspectRatio: true,
            width:100 + "%",
            height:100 + '%',
            tooltip: 'none',
            region: country_code,
            displayMode: 'markers'
        };

        var data = google.visualization.arrayToDataTable([
          ['City',   'latitude', 'longitude'],
          [city_name,latitude,    longitude]
        ]);


        var chart = new google.visualization.GeoChart(
            document.getElementById(target)
        );
        chart.draw(data, options);

    }

}





 