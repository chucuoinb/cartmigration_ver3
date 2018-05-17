import _thread
import importlib
import configparser
import os
import socket
import sys
import json
from models.setup import Setup
from libs.utils import *


class Server:
	CONFIG_FILE = 'etc/config.ini'

	def __init__(self):
		self.host = None
		self.port = None
		self.content_dir = None
		self.socket = None
		self.all_thread = dict()

	def start(self, port = 8080):
		if not (self.is_config()):
			if not self.setup():
				return
		self.host = socket.gethostbyname(socket.gethostname())  # Default to any avialable network interface
		self.port = port
		self.content_dir = 'web'  # Directory where webpage files are stored
		self.socket = None
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock = ssl.wrap_socket(self.socket)
		print("Starting server on {host}:{port}".format(host = self.host, port = self.port))
		self.socket.bind((self.host, self.port))
		while True:
			self.socket.listen(1)
			conn, addr = self.socket.accept()

			text = ''
			while True:
				data = conn.recv(200)
				data = data.decode("utf-8")
				if not data:
					# Unreliable
					break
				else:
					text += data
			self.solve_buffer(conn, text)
		try:
			pass
			# print("Starting server on {host}:{port}".format(host = self.host, port = self.port))
			# self.socket.bind((self.host, self.port))
			# while True:
			# 	self.socket.listen(1)
			# 	conn, addr = self.socket.accept()
			#
			# 	text = ''
			# 	while True:
			# 		data = conn.recv(200)
			# 		data = data.decode("utf-8")
			# 		if not data:
			# 			# Unreliable
			# 			break
			# 		else:
			# 			text += data
			# 	self.solve_buffer(conn, text)
		except Exception as e:
			print(e)
			self.shutdown()
			sys.exit(1)
		finally:
			pass

	def stop(self):
		pass

	def solve_buffer(self, conn, buffer):
		buffer = json.loads(buffer)
		if (not ('controller' in buffer)) or (not ('action' in buffer)):
			return
		controller_name = buffer['controller']
		action_name = buffer['action']
		data = buffer['data']
		if controller_name == 'migration':
			data_license = data['license'] if 'license' in data else None
			if not data_license:
				return
			if data_license in self.all_thread:
				controller = self.all_thread[data_license]
				getattr(controller, action_name)()
			else:
				controller = get_controller(controller_name, data)
				self.all_thread[data_license] = controller
				controller.start()
		else:
			controller = get_controller(controller_name, data)
			getattr(controller, action_name)(data, conn)

	def shutdown(self):
		try:
			self.socket.shutdown(socket.SHUT_RDWR)
		except Exception as e:
			pass

	def is_config(self):
		return os.path.isfile(self.CONFIG_FILE)

	def setup(self):
		host = input('Enter database host: \n')
		username = input('Enter database username: \n')
		password = input('Enter database password: \n')
		name = input('Enter database name: \n')
		prefix = input('Enter database prefix: \n')
		config = configparser.ConfigParser()
		config.add_section('mysql')
		config['mysql']['db_host'] = host
		config['mysql']['db_username'] = username
		config['mysql']['db_password'] = password
		config['mysql']['db_name'] = name
		config['mysql']['db_prefix'] = prefix
		with open(self.CONFIG_FILE, 'w') as configfile:  # save
			config.write(configfile)
		setup = Setup()
		setup.run()
		return True
