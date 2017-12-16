// Initialization =========================================================
var $ = require('jquery');
var request = require('request');
var cheerio = require('cheerio');
var fs = require('fs');
var os = require('os');
var iconv = require('iconv-lite');
var math = require('mathjs');
var array_to_csv = require('array-to-csv')

// Application entry =========================================================
$(function() {
    crawl(1976);
});

function crawl(year) {
    var fn = year.toString() + '.html';
    var path = 'data/' + fn;
    var url = 'http://www.kj001.com/kj/' + fn;
    var regular = [],
        special = [];

    console.log('downloading file: ' + fn);
    request({
        encoding: null,
        url: url
    }, function(error, response, html) {
        var html = iconv.decode(html, 'gb2312');
        var $ = cheerio.load(html);
        $('div.sortDown.clearfix>div.p').filter(function(_, el) {
            var data = $(el).children().first().text();
            regular.push(parseInt(data));
        });
        regular = math.reshape(regular, [regular.length / 6, 6]);
        regular = regular.reverse();
        fs.appendFileSync('data/regular.csv', array_to_csv(regular) + os.EOL);

        $('td.bg-high2>div.p').filter(function(i, el) {
            var data = $(el).children().first().text();
            special.push(parseInt(data));
        });
        special = math.reshape(special, [special.length, 1]);
        special = special.reverse();
        fs.appendFileSync('data/special.csv', array_to_csv(special) + os.EOL);

        // console.log('data saved: ' + fn);
        if (year < 2017) {
            crawl(year + 1);
        }
    });
}