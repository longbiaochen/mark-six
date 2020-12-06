// Common libraries =========================================================
var util = require('util');
var path = require('path');
var os = require('os');
var fs = require('fs');
var csv = require('csv-load-sync');


// Module header ==================================================
data_layer = {};
data_layer.param = {};
module.exports = data_layer;
util.log('Loading module: ' + path.parse(__filename).name);


// Module body ==================================================
data_layer.init = function() {}

data_layer.load_grid = function() {
	util.log('load_grid');
	require('../../data/grid.geojson');
}

data_layer.load_base_station = function() {
	util.log('load_base_station');
	data_layer.base_station = csv('data/base_station.csv');
	data_layer.base_station.forEach(function(bs) { bs.traffic = parseFloat(bs.traffic); });
}

data_layer.load_traffic = function() {
	util.log('load_traffic');
	var bin = fs.readFileSync('data/traffic.bin');
	var arr = Array.prototype.slice.call(new Float64Array(bin.buffer));
	data_layer.traffic = [];
	while (arr.length) data_layer.traffic.push(arr.splice(0, time_layer.ticks.length));
}

data_layer.load_prediction = function() {
	util.log('load_prediction');
	var bin = fs.readFileSync('data/prediction.bin');
	var arr = Array.prototype.slice.call(new Float32Array(bin.buffer));
	data_layer.prediction = [];
	while (arr.length) data_layer.prediction.push(arr.splice(0, time_layer.ticks.length));
}
