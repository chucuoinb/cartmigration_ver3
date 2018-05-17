from libs.utils import *
import threading


class Migration(threading.Thread):
	_db = None
	_import_action = (
		'taxes', 'manufacturers', 'categories', 'products', 'customers', 'orders', 'reviews', 'pages', 'blocks',
		'rules', 'cartrules')
	_next_action = {
		'taxes': 'manufacturers',
		'manufacturers': 'categories',
		'categories': 'products',
		'products': 'customers',
		'customers': 'orders',
		'orders': 'reviews',
		'reviews': 'pages',
		'pages': 'blocks',
		'blocks': 'rules',
		'rules': 'cartrules',
		'cartrules': False,
	}
	_simple_action = {
		'taxes': 'tax',
		'manufacturers': 'manufacturer',
		'categories': 'category',
		'products': 'product',
		'customers': 'customer',
		'orders': 'order',
		'reviews': 'review',
		'pages': 'page',
		'blocks': 'block',
		'widgets': 'widget',
		'polls': 'poll',
		'newsletters': 'newsletter',
		'users': 'user',
		'rules': 'rule',
		'cartrules': 'cartrule',
	}

	def __init__(self, data):
		super().__init__()
		self._exit_flag = 0
		threading.Thread.__init__(self)
		self.threadID = data['license']
		self._name = data['license']
		self._license = data['license']
		self._notice = data

	def run(self):
		print("Starting " + self.name)
		while not self._exit_flag:
			self.migration()
		print("Exiting " + self.name)

	def migration(self):
		cart = get_model('basecart', self._license)


	def stop(self):
		self._exit_flag = 1

	def set_exit_flag(self, exit_flag):
		self._exit_flag = exit_flag
