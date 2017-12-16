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
    if (fs.existsSync(path)) {
        console.log('File read from cache.')
        var html = fs.readFileSync(path);
        var $ = cheerio.load(html);
        var i = 0;
        $('div.sortDown.clearfix>div.p').filter(function(i, el) {
            var data = $(el).children().first().text();
            regular.push(parseInt(data));
        });
        regular = math.reshape(regular, [151, 6]);
        regular = regular.reverse();
        fs.writeFileSync('data/regular.csv', array_to_csv(regular));

        $('td.bg-high2>div.p').filter(function(i, el) {
            var data = $(el).children().first().text();
            special.push(parseInt(data));
        });
        special = math.reshape(special, [151, 1]);
        special = special.reverse();
        fs.writeFileSync('data/special.csv', array_to_csv(special));

        console.log(regular[0], special[0]);

    } else {
        console.log('Requesting page from website...');
        request({
            encoding: null,
            url: url
        }, function(error, response, html) {
            var html = iconv.decode(html, 'gb2312');
            fs.writeFileSync(path, html);
            console.log('file saved: ' + path)
        });
    }
});