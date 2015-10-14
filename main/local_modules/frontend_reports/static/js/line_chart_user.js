function str_to_date(list) {
    var with_date = [];
    for (var i = 0; i < list.length; i++) {
        var date = list[i][0];
        with_date.push([new Date(date[0], date[1] - 1, date[2]), list[i][1]]);
    }
    return with_date
}

function line_chart(points, target, title) {
    google.load('visualization', '1', {packages: ['corechart', 'line']});
    points = str_to_date(points);

    google.setOnLoadCallback(function () {
        drawBackgroundColor(points, target);
    });

    function drawBackgroundColor(points, target, title) {
        var data = new google.visualization.DataTable();
        data.addColumn('date', 'X');
        data.addColumn('number', title);

        data.addRows(points);

        var options = {
            hAxis: {
                title: 'Time'
            },
            vAxis: {
                title: '# ' + title
            },
            backgroundColor: '#f1f8e9'
        };

        var chart = new google.visualization.LineChart(document.getElementById(target));
        chart.draw(data, options);
    }
}

function line_chart_users(points, target) {
    return line_chart(points, target, 'User Account Created')
}

function line_chart_companies(points, target) {
    return line_chart(points, target, 'Companies Added')
}