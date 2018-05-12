from libs.utils import *
import threading


class Migration(threading.Thread):
	_db = None

	def __init__(self, buffer):
		super().__init__()
		self._exit_flag = 0
		threading.Thread.__init__(self)
		self.threadID = buffer['data']['license']
		self.name = buffer['data']['license']
		self.license_data = buffer['data']['license']

	def run(self):
		print("Starting " + self.name)
		while not self._exit_flag:
			self.migration()
		print("Exiting " + self.name)

	def migration(self):
		print_time(self.license_data)

	def stop(self):
		self._exit_flag = 1

	def set_exit_flag(self, exit_flag):
		self._exit_flag = exit_flag
