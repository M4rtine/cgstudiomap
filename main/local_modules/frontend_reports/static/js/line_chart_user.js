function str_to_date(list0, list1, list2) {
    var with_date = [];
    for (var i = 0; i < list0.length; i++) {
        var date = list0[i][0];
        with_date.push([new Date(date[0], date[1] - 1, date[2]), list0[i][1], list1[i][1], list2[i][1]]);
    }
    return with_date
}

function line_chart(users, created_companies, updated_companies, target) {
    google.load('visualization', '1', {packages: ['corechart', 'line']});
    points = str_to_date(users, created_companies, updated_companies);

    google.setOnLoadCallback(function () {
        drawBackgroundColor(
            points, target
        );
    });

    function drawBackgroundColor(points, target) {
        var data = new google.visualization.DataTable();
        data.addColumn('date', 'Date');
        data.addColumn('number', '# Users');
        data.addColumn('number', '# Company Created');
        data.addColumn('number', '# Company Updated');

        data.addRows(points);

        var options = {
            hAxis: {
                title: 'Time'
            },
            vAxis: {
                title: 'Number'
            },
            backgroundColor: '#f1f8e9',
            explorer: {
                axis: 'horizontal',
                keepInBounds: true,
                actions: ['dragToZoom', 'rightClickToReset']
            }
        };

        var chart = new google.visualization.LineChart(document.getElementById(target));
        chart.draw(data, options);
    }
}

