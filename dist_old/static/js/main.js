'use strict'

var update = function(){
	$.get('update', function(data){
		//console.log(data.data)
		var resp = JSON.parse(data);
		$('#mph').html(resp.data.mph);
		$('#clip').html(resp.data.clip);
	})
}

$(document).ready(function(){
	console.log('Document ready.');
	$('#speed-range').on("change mousemove", function() {
    	var speed = $('#speed-range').val() / 100.0;
   		//console.log(speed);
   		$('#speed-output').html(speed);
	});
	$('#speed-reset').on('click', function(){
		$('#speed-range').val(100.0);
		$('#speed-output').html(1);
		var speed = $('#speed-range').val() / 100.0;
		$.post('set_playback_speed', {'speed': speed});
	});
	$('#speed-range').on('change', function(){
		var speed = $('#speed-range').val() / 100.0;
		console.log(speed);
		$.post('set_playback_speed', {'speed': speed}); 
	});
	$('#version-select').on('change', function(){
		var version = $('#version-select').val();
		$.post('set_arena_version', {'version': version})
	});
	window.setInterval(update, 500);
});
