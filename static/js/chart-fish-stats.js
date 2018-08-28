// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';


// Area Chart Example
//VARS

var time_list = ""
var price_list = "Test_date,"
var avg_price_list_array =[1]
var min_price_list_array =[1]
var ctx = document.getElementById("myAreaChart");

//Get AVG fish items
$.getJSON("fish_avg.json", function(json1) {

    console.log(json1); // this will show the info it in firebug console
    //get_dates_and_val(json1)
    for (i = 0; i < json1.length; i++){

    //update graph
      addData_avg(myLineChart,json1[i].time,json1[i].val)
    }
    
});

$.getJSON("fish_min.json", function(json2) {

    console.log(json2); // this will show the info it in firebug console
    //get_dates_and_val(json2)
    //addData(myLineChart,time_list,price_list)
    for (i = 0; i < json2.length; i++){

    //update graph
      addData_min(myLineChart,json2[i].time,json2[i].val)
    }
    
});


function get_dates_and_val(JSON){

}

function addData_avg(chart, label, data) {
    console.log("updating avg")
    chart.data.labels.push(label);
    chart.data.datasets[0] => {
        dataset.data.push(data);
    });
    chart.update();
}
function addData_min(chart, label, data) {
    console.log("updating min")    
    chart.data.labels.push(label);
    chart.data.datasets[1] => {
        dataset.data.push(data);
    });
    chart.update();
}


var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [time_list],
      datasets: [{
        label: "Avg Gold Price",
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
        data: [avg_price_list_array],
      },
      {
        label: "Min Gold Price",
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
        data: [min_price_list_array],
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
