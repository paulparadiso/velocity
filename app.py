from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from velocitycore import VelocityCore
import json
import os
import sys


if getattr(sys, 'frozen', False):                                                                                                                                     
      template_folder = os.path.join(sys.executable, '..','templates')                                                                                                  
      static_folder = os.path.join(sys.executable, '..','static')                                                                                                       
      app = Flask(__name__, template_folder = template_folder,                                                                                                  
                              static_folder = static_folder)
else:
	app = Flask(__name__, static_url_path='/static')

velocity_core = VelocityCore()

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def main_page():
	return redirect(url_for('index'))

@app.route('/')
def index():
	status = velocity_core.get_status()
	return render_template('sync.html', status=status)

@app.route('/current_config')
def current_config():
	return velocity_core.get_current_config(format='json')


###########################################
# Original endpoints to add and remove 
# break points. Have been replaced with
# generic clip API.
###########################################

@app.route('/add_break', methods=['POST'])
def add_break():
	velocity_core.add_range()
	return redirect(url_for('index'))

@app.route('/delete_break', methods=['POST'])
def delete_break():
	velocity_core.remove_range(int(request.form['break']))
	return redirect(url_for('index'))

@app.route('/update_break', methods=['POST'])
def update_break():
	b_id = request.form['id']
	clip = request.form['clip']
	start = request.form['start']
	stop = request.form['stop']
	velocity_core.update_range(b_id, clip, start, stop)
	return redirect(url_for('index'))

#############################################
# Generic clip API.
#############################################

@app.route('/set_mode', methods=['POST', 'GET'])
def set_mode():
	velocity_core.set_mode(request.form['mode'])
	return main_page()

@app.route('/add_clip', methods=['POST'])
def add_clip():
	velocity_core.add_clip()
	return main_page()

@app.route('/remove_clip', methods=['POST'])
def remove_clip():
	clip = request.form['clip']
	velocity_core.remove_clip(clip)
	return main_page()

@app.route('/update_clip', methods=['POST'])	
def update_clip():
	clip = {}
	clip['num'] = request.form['clip']
	clip['id'] = request.form['id']
	velocity_core.update_clip(clip)
	return main_page()

@app.route('/delete_clip', methods=['POST'])
def delete_clip():
	clip = request.form['id']
	velocity_core.delete_clip(clip)
	return main_page()

@app.route('/load_config', methods=['POST'])
def load_config():
	name = request.form['config']
	velocity_core.load_config(name)
	return main_page()

@app.route('/add_arena_instance', methods=['POST'])
def add_arena_instance():
	#arena_instance = request.form['instance']
	velocity_core.add_arena_instance()
	return main_page()

@app.route('/remove_arena_instance', methods=['POST'])
def remove_arena_instance():
	arene_instance = request.form['instance']
	velocity_core.remove_arena_instance(instance)
	return main_page()

@app.route('/update_arena_instance', methods=['POST'])
def update_arena_instance():
	instance = {'id':request.form['id'], 
				'ip': request.form['ip'], 
				'is_master': False, 
				'arena_version': request.form['arena_version']}
	if 'master' in request.form.to_dict().keys():
		instance['is_master'] = True
	velocity_core.update_arena_instance(instance)
	return main_page()

@app.route('/save_config', methods=['POST'])
def save_config():
	name = request.form['config']
	velocity_core.save_config(name)
	return main_page()

@app.route('/new_config', methods=['POST'])
def new_config():
	velocity_core.new_config()
	return main_page()

@app.route('/get_speed')
def get_speed():
	speed = velocity_core.get_speed()
	return json.dumps({'status': 'success', 'data':{'speed': speed}})

@app.route('/play', methods=['POST'])
def play():
	velocity_core.play()
	return redirect(url_for('index'))

@app.route('/pause', methods=['POST'])
def pause():
	velocity_core.pause()
	return redirect(url_for('index'))

@app.route('/set_playback_speed', methods=['POST'])
def set_playback_speed():
	speed = request.form['speed']
	velocity_core.set_playback_speed(speed)
	return json.dumps({'status': 'success'})

@app.route('/update')
def update():
	mph = velocity_core.get_speed()
	return json.dumps({'status': 'success', 'data': {'mph': mph}})

@app.route('/set_arena_version', methods=['POST'])
def set_arena_version():
	version = request.form['version']
	velocity_core.set_arena_version(version)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(host='0.0.0.0')
