// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

//VARS
var time_list = []
var avg_price_list = []
var min_price_list = []
var price_list_array =[]
var ctx = document.getElementById("myAreaChart");

init()

//On startup
function init(){
  load_json();
}

function load_json(){
  //Get Min fish items and add them to line graph
  $.getJSON("fish_min.json", function(JSON) {
    console.log(JSON); // this will show the info it in firebug console
    for (i = 0; i < JSON.length; i++){
      
      time_list.push(JSON[i].time)
      myLineChart.data.datasets[1].data[i] = JSON[i].val
      //update graph
      myLineChart.update()
    }
  });
  //Get AVG fish items and add them to line graph
  $.getJSON("fish_avg.json", function(JSON) {
    console.log(JSON);     
    for (i = 0; i < JSON.length; i++){
      avg_price_list.push(JSON[i].val)
      myLineChart.data.datasets[0].data[i] = JSON[i].val
      //update graph
      myLineChart.update()
    }
  });
}

var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: time_list,
      datasets: [{
        label: "Avg Gold Price",
        lineTension: 0.3,
        //backgroundColor: "rgba(0,255,0,0.3)",
        borderColor: "rgb(127, 191, 63)",
        pointRadius: 5,
        pointBackgroundColor: "rgb(127, 191, 63)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        //pointHoverBackgroundColor: "rgb(127, 191, 63)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: avg_price_list,
      },
      {
        label: "Min Gold Price",
        lineTension: 0.3,
        //backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        //pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: min_price_list,
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)",
          }
        }],
      },
      legend: {
        display: false
      }
    }
});