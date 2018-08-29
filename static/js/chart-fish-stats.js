// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';


// Area Chart Example
//VARS

var time_list = []
var avg_price_list = []
var min_price_list = []
var price_list_array =[]
var ctx = document.getElementById("myAreaChart");
//var var myLineChart = {}
//init();
//myLineChart.update();
//On startup

$(document).ready(function () {

    load_json();
    lineChart = render_chart(time_list,min_price_list,avg_price_list);
    lineChart.resize();
    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        console.log("tab changed");
    });
});

/*
function init(){
  load_json();

  //Render
  render_chart(time_list,min_price_list,avg_price_list);
  //myLineChart.update();
  //chart.update();
  //myLineChart.update();
}
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    var ev = document.createEvent('Event');
    ev.initEvent('resize', true, true);
    window.dispatchEvent(ev);
  });
*/



function load_json(){
  $.getJSON("fish_min.json", function(JSON) {
    console.log(JSON); // this will show the info it in firebug console
    //get_dates_and_val(json2)
    //addData(myLineChart,time_list,price_list)
    for (i = 0; i < JSON.length; i++){
      min_price_list.push(JSON[i].val)
      time_list.push(JSON[i].time)
      //update graph
    }
  });
  //Get AVG fish items
  $.getJSON("fish_avg.json", function(JSON) {
    console.log(JSON); // this will show the info it in firebug console
    //get_dates_and_val(json1)
    //addData(myLineChart,time_list,price_list)
    for (i = 0; i < JSON.length; i++){
      avg_price_list.push(JSON[i].val)
      //time_list.push(JSON[i].time)
      //update graph
    }
  });
}

function render_chart(time_l,min_l,avg_l){
  var myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: time_l,
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
          data: avg_l,
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
          data: min_l,
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
          }],
          yAxes: [{
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
  return myLineChart;
}
