// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

//VARS
var time_list = []
var avg_price_list = []
var min_price_list = []
var price_list_array =[]

var item_list_array = []
var chart_list = {}
var page_elements = {}
var imported_json = {}

function init(passed_item_id){
  item_list_array = passed_item_id
  console.log(item_list_array)
  $.getJSON("monitored.json", function(JSON) {
  imported_json = JSON   


  for (i = 0; i < item_list_array.length; i++){ 
    page_elements[passed_item_id[i]] = document.getElementById(passed_item_id[i].toString());
    //Create a list of charts for each passed id?
    //chart = create_charts(passed_item_id[i],ctx)
    console.log("creating chart for item "+passed_item_id[i])
    chart_list[passed_item_id[i]] = create_charts(passed_item_id[i],page_elements[passed_item_id[i]])
    for (var x in JSON){    
      
      if (JSON[x].item_id == passed_item_id[i]){

        chart_list[passed_item_id[i]].data.labels.push(JSON[x].time);
        //console.log("Adding time " +JSON[x].time + " for "+ passed_item_id[i]);
        chart_list[passed_item_id[i]].data.datasets[0].data.push(JSON[x].avg_val);
        //console.log("Adding avg " +JSON[x].avg_val);
        chart_list[passed_item_id[i]].data.datasets[1].data.push(JSON[x].min_val);
        //chart_list[passed_item_id[i]].chart.reset();
        chart_list[passed_item_id[i]].chart.update();
        }
      }
    }
  //chart_list[6557].chart.data.datasets[1].data.push(14);
  console.log(chart_list)
  for (var x in chart_list){

    console.log(passed_item_id[i])
    //chart_list[passed_item_id[i]].chart.update();
  }
  });

}

function create_charts(item_id, chart_id){
  var item_id = new Chart(chart_id, {
      type: 'line',
      data: {
        //labels: time_list,
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
          //data: [0],
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
          //data: [0],
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
  return(item_id)
}