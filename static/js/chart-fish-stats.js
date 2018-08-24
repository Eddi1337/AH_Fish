// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';


// Area Chart Example
//VARS

var time_list = ""
var price_list = "Test_date,"
var price_list_array =[06,]
var ctx = document.getElementById("myAreaChart");

//On startup
$.getJSON("test.json", function(json) {

    console.log(json); // this will show the info it in firebug console
    get_dates_and_val(json)
    addData(myLineChart,time_list,price_list)
    
});

function init(){
  console.log(time_list);
  console.log(price);
  
}


function get_dates_and_val(JSON){

  for (i = 0; i < JSON.length; i++){
  //price_list = ''+JSON[i].val + ' ,'
  //time_list = ',"'+JSON[i].time + '" '
  //update graph
    addData(myLineChart,JSON[i].time,JSON[i].val)
  }
  

}


function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}


var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [time_list],
      datasets: [{
        label: "Avg_price",
        lineTension: 0.3,
        backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: [price_list_array],
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
            max: 500,
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