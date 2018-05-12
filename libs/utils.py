import importlib
import time

def get_value_by_key_in_dict(dictionary, key, default = None):
	return dictionary[key] if key in dictionary else default


def get_controller(controller_name,buffer):
	module_class = importlib.import_module('controllers.' + controller_name)
	my_class = getattr(module_class, controller_name.capitalize())
	my_instance = my_class(buffer)
	# print(my_instance)
	return my_instance


def print_time(thread_name):
	time.sleep(10)
	print("%s: %s" % (thread_name, time.ctime(time.time())))
