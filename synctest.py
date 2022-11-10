from oscreceiver import OSCReceiver
from arenacontroller import ArenaController
import time

osc_receiver = OSCReceiver()
arena_controller = ArenaController()
previous_position = -1.0
master_address = '127.0.0.1'
next_clip = 0
num_clips = 1

def trigger_next_clip():
	global next_clip
	global num_clips
	global arena_controller
	arena_controller.set_clip(next_clip + 1)
	next_clip = (next_clip + 1) % num_clips


def position_callback(values, sender):
	global previous_position
	sender_address = sender[0]
	if(sender_address == '127.0.0.1'):
		current_position = values
		if current_position < previous_position:
			previous_position = -1.0
			trigger_next_clip()
		else:
			previous_position = current_position

if __name__ == "__main__":
	arena_controller.add_arena_instance("master", "127.0.0.1", arena_version='6')
	arena_controller.add_arena_instance("slave", "192.168.0.160", arena_version='6')
	osc_receiver.add_listener('/composition/selectedclip/transport/position', position_callback)
	trigger_next_clip()
	while 1:
		time.sleep(0.1)