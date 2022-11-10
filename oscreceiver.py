from oscpy.server import OSCThreadServer
import time

class OSCReceiver:

	def __init__(self):
		self.osc = OSCThreadServer()
		self.sock = self.osc.listen(address='0.0.0.0', port=7001, default=True)
		self.listeners = []

	def add_listener(self, address, callback):
		self.osc.bind(str.encode(address), callback)

	def get_sender(self):
		return self.osc.get_sender()

previous_position = -1.0
def test_callback(values, sender):
	global previous_position
	sender_address = sender[0]
	current_position = values
	if current_position < previous_position:
		print("Trigger next clip.")
	previous_position = current_position
	#print("got values: {} from {}".format(value, sender_address))


if __name__ == "__main__":
	osc_rec = OSCReceiver()
	osc_rec.add_listener('/composition/selectedclip/transport/position', test_callback)
	print("previous_position = {}".format(previous_position))
	while 1:
		pass
		#print("Listening...")
		#time.sleep(0.01)