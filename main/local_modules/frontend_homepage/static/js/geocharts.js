function geo_chart(companies, target) {

    google.load('visualization', '1', {packages: ['geochart']});
    google.setOnLoadCallback(drawRegionsMap);

    function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable(companies);
        var options = {
			legend: 'none',
            colorAxis: {colors: ['#E8CFF7', '#B86BE5']},
            backgroundColor: '#F2F2F2',
            keepAspectRatio: true,
 			width:100 + "%",
 			height:100 + '%',
 			tooltip: {textStyle: {color: '#444444'}, trigger:'focus'}
        };
        var chart = new google.visualization.GeoChart(
            document.getElementById(target)
        );
        chart.draw(data, options);
    }

  go();

  window.addEventListener('resize', go);

  function go() {
  	chart.draw(data, options);
  }
}





 