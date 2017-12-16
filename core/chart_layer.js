// Common libraries =========================================================
var util = require('util');
var path = require('path');
var plotly = require('plotly.js/dist/plotly.js');


// Module header ==================================================
chart_layer = {};
chart_layer.param = {};
module.exports = chart_layer;
util.log('Loading module: ' + path.parse(__filename).name);


// Module body ==================================================
chart_layer.init = function() {}

chart_layer.plot_traffic = function() {
	util.log('plot_traffic');
	var data = [{
		x: time_layer.ticks,
		y: data_layer.traffic[chart_layer.base_station_id - 1],
		type: "scatter",
		name: "Real Traffic"
	}];
	var layout = {
		title: 'Traffic of Base Station ' + chart_layer.base_station_id,
		xaxis: {
			title: 'Time',
			range: [chart_layer.param.start_range, chart_layer.param.end_range]
		},
		yaxis: {
			title: 'Volume'
		}
	};
	plotly.purge('chart_view');
	plotly.plot('chart_view', data, layout);
}

chart_layer.plot_prediction = function() {
	util.log('plot_prediction');
	var data = [{
		x: time_layer.ticks,
		y: data_layer.prediction[chart_layer.base_station_id - 1],
		type: "scatter",
		name: "Predicted Traffic"
	}];
	var layout = {
		title: 'Prediction of Base Station',
		xaxis: {
			title: 'Time',
			range: [chart_layer.param.start_range, chart_layer.param.end_range]
		},
		yaxis: {
			title: 'Volume'
		}
	};
	plotly.plot('chart_view', data, layout);
}
