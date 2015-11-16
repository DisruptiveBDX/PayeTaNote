'use strict';

var spawn = require('child_process').spawn;
var exec = require('child_process').exec;
var readline = require('readline');

var NOTE_FOLDER = './piano';
var NOTE_FILETYPE = 'wav';

function getNote (screenPercentage) {
	return "gabcdef"[Math.floor(screenPercentage * 7)];
}

var pyCam = spawn('python cam.py');

var rl = readline.createInterface({
  input: pyCam.stdout
});



exec('sox piano/a.wav -d');
