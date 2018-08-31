// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

//VARS
var time_list = []
var avg_price_list = []
var min_price_list = []
var price_list_array =[]
var ctx = document.getElementById("myAreaChart");
console.log({{item}});
init()

//On startup
function init(){
  //Get list of monitored items
  $.getJSON("monitored.json", function(JSON) {
    console.log(JSON);     
    for (i = 0; i < JSON.length; i++){
      if (JSON.[i].item_id == {{item}}{
        avg_price_list.push(JSON[i].val)
        {{item}}.data.datasets[0].data[i] = JSON[i].val
        //update graph
        myLineChart.update()
      }
    }
  });
  load_json();
}


var {item} = new Chart(ctx, {
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
{% endfor %}