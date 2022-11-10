import obd
import serial.tools.list_ports

DEFAULT_BAUDRATE = 115200

class OBDController:

	def __init__(self):
		self.connection = None
		self.baudrate = DEFAULT_BAUDRATE
		self._connect()

	def _connect(self):
		ports = serial.tools.list_ports.comports()
		usb_serial_port = None
		for port, desc, hwid in sorted(ports):
			if 'USB' in desc:
				print('USB serial device found on {}'.format(port))
				usb_serial_port = port
				break
		if usb_serial_port == None:
			self.connection = None
		else:
			self.connection = obd.OBD(portstr=usb_serial_port, baudrate = self.baudrate)

	def _create_command(self, cmd):
		return getattr(obd.commands, cmd)

	def _query(self, cmd):
		response = self.connection.query(cmd)
		return response

	def get_speed(self):
		cmd = self._create_command('SPEED')
		response = self._query(cmd)
		return int(response.value.to('mph').magnitude)	