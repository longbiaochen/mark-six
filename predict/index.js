// Initialization =========================================================
var $ = require('jquery');
var request = require('request');
var cheerio = require('cheerio');
var fs = require('fs');
var iconv = require('iconv-lite');
var math = require('mathjs');
var array_to_csv = require('array-to-csv')


var fn = '2016.html';
var path = 'data/' + fn;
var url = 'http://www.kj001.com/kj/' + fn;

var regular = [],
    special = [];

// Application entry =========================================================
$(function() {

});