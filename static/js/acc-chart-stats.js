// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

//VARS
var time_list = []
var avg_price_list = []
var min_price_list = []
var price_list_array =[]

var item_list_array = []
var chart_array = []
var imported_json = {}

function init(passed_item_id){
  item_list_array = passed_item_id
  console.log(item_list_array)
  $.getJSON("monitored.json", function(JSON) {
  imported_json = JSON   
  for (i = 0; i < item_list_array.length; i++){ 
    var ctx = document.getElementById(passed_item_id[i].toString());
    //console.log
    chart = create_charts(passed_item_id[i],ctx)
    chart_array.push(chart)
    console.log("adding item "+passed_item_id[i])
    console.log(chart)
    if (chart){
          chart.data.labels.pop();
    chart.data.datasets[0].data.pop();
    chart.data.datasets[1].data.pop();
    }

    //add_items(passed_item_id[i],chart,JSON)
    for (var x in JSON){
      //console.log("itteration " + x);
      if (JSON[x].item_id == passed_item_id[i]){
        console.log("adding to "+ chart.id + " With " + JSON[x].avg_val + " from " + passed_item_id[i])
        //console.log(chart.id);
        //console.log("with data " + JSON[x].time + " "+ JSON[x].avg_val + " "+ JSON[x].min_val)
        chart.data.labels.push(JSON[i].time);
        chart.data.datasets[0].data.push(JSON[i].avg_val);
        chart.data.datasets[1].data.push(JSON[i].min_val);
        chart.update()
      } 
    }

    }
  });
}
/*
function add_items(item,chart,JSON){
    for (var x in JSON){
      console.log(x)
      if (JSON[x].item_id == item){
        console.log("itteration " + x);
        console.log("item " +JSON[x].item_id);
        chart.data.labels.push(JSON[x].time);
        chart.data.datasets[0].data[x] = JSON[x].avg_val;
        chart.data.datasets[1].data[x] = JSON[x].min_val;
        chart.update();
      }
    }
}
/* nope
function add_items(item,chart,JSON){
    list_of_times = []
    list_of_val_min = []
    list_of_val_avg = []
    for (e = 0; e < JSON.length; e++){
      console.log(item)
      if (JSON[e].item_id == item){
        
        list_of_times.unshift(JSON[e].time)
        list_of_val_min.unshift(JSON[e].min_val)
        list_of_val_avg.unshift(JSON[e].avg_val)
        }
    }
    console.log(list_of_times)
    for (var i = list_of_times.length - 1; i >= 0; i--) {
      chart.data.labels.push(list_of_times[i])
    }
    chart.data.labels.push(list_of_times)
    //console.log("Average item val " + JSON[e].avg_val + " for item " + JSON[e].item_id)
    chart.data.datasets[0].data[i] = list_of_val_avg
    chart.data.datasets[1].data[i] = list_of_val_min
    //}
    //}
    //charts.data.labels.data[i] = (JSON[a].time);
    chart.update()
}

*/
function create_charts(item_id, chart_id){
  var item_id = new Chart(chart_id, {
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
  return(item_id)
}