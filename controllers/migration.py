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

	_current = 'taxes'

	def __init__(self, data):
		super().__init__()
		self._exit_flag = 0
		threading.Thread.__init__(self)
		self.threadID = data['license']
		self._name = data['license']
		self._license = data['license']
		self._notice = data

	def start(self):
		self.save_notice()
		super().start()

	def run(self):
		print("Starting " + self.name)
		while not self._exit_flag:
			result = self.migration()
			if result['result'] == 'success':
				self.finish_migration()
				break
			else:
				self.set_current(result['current'])

		print("Exiting " + self.name)

	def migration(self):
		result = self.default_result_migration()
		current = self.get_current()
		if not current:
			result['result'] = 'success'
			result['msg'] = 'Finish Migration'
			return result
		cart = get_model('basecart')
		getattr(cart,'set_license')(self._license)
		self._notice = getattr(cart, 'get_user_notice')
		result['result'] = 'process'
		result['process']['next'] = current
		self._notice['running'] = True
		self._notice['resume']['type'] = current
		if not (self._notice['config'][current]):
			next_action = self._next_action[current]
			if next_action:
				if self._notice['config'][next_action]:
					pass



	def get_current(self):
		return self._current

	def set_current(self,current):
		self._current = current

	def stop(self):
		self._exit_flag = 1

	def set_exit_flag(self, exit_flag):
		self._exit_flag = exit_flag

	def save_notice(self):
		cart = get_model('basecart', self._license)
		print(cart)
		notice = self._notice
		demo = None
		if 'demo' in notice and notice['demo']:
			demo = 2
		getattr(cart, 'save_notice')(self._license, notice, demo)

	def default_result_migration(self):
		return {
			'result': '',
			'msg': '',
			'process': {
				'next': '',
				'total': 0,
				'imported': 0,
				'error': 0,
				'point': 0,
			}
		}
	def finish_migration(self):
		pass