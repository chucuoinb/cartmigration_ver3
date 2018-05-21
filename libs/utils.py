import base64
import importlib
import json
import time

from pathlib import Path

import os

TABLE_NOTICE = "cartmigration_notice"
TABLE_MAP = "cartmigration_map"
TABLE_RECENT = "cartmigration_recent"
TABLE_SETTING = "cartmigration_setting"


def get_value_by_key_in_dict(dictionary, key, default = None):
	return dictionary[key] if key in dictionary else default


def get_controller(controller_name, data = None):
	module_class = importlib.import_module('controllers.' + controller_name)
	my_class = getattr(module_class, controller_name.capitalize())
	if data:
		my_instance = my_class(data)
	else:
		my_instance = my_class()
	return my_instance


def get_model(name, data = None):
	if not name:
		return None
	name_path = name.replace('_', '/')
	file_path = 'models/' + name_path + '.py'
	file_model = Path(file_path)
	if not file_model.is_file():
		return None
	model_name = "models." + name.replace('_', '.')
	module_class = importlib.import_module(model_name)
	class_name = get_model_class_name(name)

	try:
		model_class = getattr(module_class, class_name)
		if data:
			model = model_class(data)
		else:
			model = model_class()
		return model
	except Exception as e:
		log(e)
		return None


def get_model_class_name(name, char = '_'):
	split = name.split(char)
	upper = map(lambda x: x.capitalize(), split)
	new_name = 'Le' + ''.join(upper)
	return new_name


def print_time(thread_name):
	time.sleep(10)
	print("%s: %s" % (thread_name, time.ctime(time.time())))


def log(msg, _license = None, type_error = 'exception'):
	path = 'log/'
	if _license:
		_license = str(_license)
		path = 'log/' + _license
	if not os.path.exists(path):
		os.makedirs(path)
	log_file = open(path + '/' + type_error + '.log', 'a')
	if isinstance(msg, dict):
		msg = json.dumps(msg)
	msg = str(msg) + '\r\n'
	date_time = time.strftime('%Y/%m/%d %H:%M:%S')
	msg = date_time + ' : ' + msg
	log_file.write(msg)


# response
def response_error(msg = None):
	return {'result': 'error', 'msg': msg, 'data': None}


def response_success(data = None, msg = None):
	return {
		'result': 'success', 'msg': msg, 'data': data
	}


# base64
def string_to_base64(s):
	if not isinstance(s, str):
		s = str(s)
	return base64.b64encode(s.encode('utf-8')).decode('utf-8')


def base64_to_string(b):
	try:
		s = base64.b64decode(b).decode('utf-8')
		return s
	except Exception as e:
		return b
