google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);

//AP Comment: added parameter to drawchart function to pass the predicted interest rate
function drawChart(rate) {

  var data = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    /* Add the Script value here - Might need a new route on app.py */
    //AP Comment: remoed hard coded rate and using predicted rate variable
    // ['Rate', 32.0],
    ['Rate', rate],
  ]);

  var options = {
    width: 600, height: 540,
    redFrom: 25, redTo: 40,
    yellowFrom:10, yellowTo: 25,
    greenFrom: 0, greenTo: 10,
    min: 0, max: 40,
    minorTicks: 4, majorTicks: 3
  };

  var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

  chart.draw(data, options);
};