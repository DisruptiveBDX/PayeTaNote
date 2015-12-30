'use strict';

var spawn = require('child_process').spawn;
var exec = require('child_process').exec;
var readline = require('readline');

var NOTE_FOLDER = './piano/';
var NOTE_FILETYPE = 'wav';

function getNote (screenPercentage) {
	return "gabcdef"[Math.floor(screenPercentage * 7)];
}

var pyCam = spawn('python', ['-u', 'cam.py']);


pyCam.stderr.on('data', function (data) {
	console.error(data.toString());
});

pyCam.stdout.on('data', function (data) {
	console.log('STDOUT', data.toString());
});


var rl = readline.createInterface({
  input: pyCam.stdout
});

rl.on('line', function (line) {
	var nb = parseFloat(line, 10);

	if (!Number.isNaN(nb)) {

		console.log('SUCCESS:', nb);
		exec('sox ' + NOTE_FOLDER + getNote(nb) + '.' + NOTE_FILETYPE + ' -d');
	}
	else {
		console.error('ERROR:', line);
	}
});
