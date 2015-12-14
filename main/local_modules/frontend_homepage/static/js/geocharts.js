function geo_chart(companies, target) {
	window.onresize = function () {
		drawRegionsMap();
	};

	window.onload = function () {
		drawRegionsMap();
	};

    google.load('visualization', '1', {packages: ['geochart']});
    google.setOnLoadCallback(drawRegionsMap);

    function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable(companies);
        var options = {
			legend: 'none',
            colorAxis: {colors: ['#E8CFF7', '#B86BE5']},
            backgroundColor: 'transparent',
            keepAspectRatio: true,
 			width:100 + "%",
 			height:100 + '%',
 			tooltip: { 
				isHtml: true,
				textStyle: { fontName: 'cgsm-regular',fontSize: 16,color: '#ffffff',showColorCode: true}
			}
        };
        var chart = new google.visualization.GeoChart(
            document.getElementById(target)
        );
        chart.draw(data, options);
    }

}





 