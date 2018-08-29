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


init();

//On startup
function init(){
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


  render_chart(time_list,min_price_list,avg_price_list)
}


function get_dates_and_val(JSON){
  for (i = 0; i < JSON.length; i++){
    print(price_list = ''+JSON[i].val + ' ,')
    time_list = ',"'+JSON[i].time + '" '
  //update graph
    print(JSON[i])
    addData(myLineChart,JSON[i].time_checked,JSON[i].fish_value)
  }
  

}


function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
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
          pointHoverBackgroundColor: "rgba(2,117,216,1)",
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
}
