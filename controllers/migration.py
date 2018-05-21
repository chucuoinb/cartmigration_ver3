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
			print(result)
			if result['result'] == 'success':
				self.finish_migration()
				break
			else:
				if 'current' in result:
					self.set_current(result['current'])

		print("Exiting " + self.name)

	def migration(self):
		result = self.default_result_migration()
		current = self.get_current()
		if not current:
			result['result'] = 'success'
			result['msg'] = 'Finish Migration!'
			return result
		cart = get_model('basecart')
		getattr(cart, 'set_license')(self._license)
		self._notice = getattr(cart, 'get_user_notice')(self._license)
		print(self._notice)
		if not self._notice:
			result['result'] = 'success'
			result['msg'] = 'Finish Migration!'
			return result
		result['result'] = 'process'
		result['process']['next'] = current
		self._notice['running'] = True
		self._notice['resume']['type'] = current

		if not (self._notice['config'][current]):
			next_action = self._next_action[current]
			if next_action:
				if self._notice['config'][next_action]:
					source_cart = self.get_source_cart(cart)
					target_cart = self.get_target_cart(cart)
					if (not source_cart) or (not target_cart):
						result['result'] = 'success'
						result['msg'] = 'Finish Migration!'
						return result
					fn_prepare_source = 'prepare_' + next_action + '_export'
					fn_prepare_target = 'prepare_' + next_action + '_import'
					prepare_source = getattr(source_cart, fn_prepare_source)()
					self._notice = getattr(source_cart, 'get_notice')()
					getattr(target_cart, 'set_notice')(self._notice)
					prepare_target = getattr(target_cart, fn_prepare_target)()
					self._notice = getattr(target_cart, 'get_notice')()
				self._notice['process'][next_action]['time_start'] = int(time.time())
				self._notice['resume']['type'] = next_action
				result['process']['next'] = next_action
			else:
				self._notice['running'] = False
				result['result'] = 'success'
				result['msg'] = 'Finish Migration!'
			save_notice = self.save_notice(cart)
			if not save_notice:
				result['result'] = 'error'
				return result
			save_recent = self.save_recent(cart)
			if not save_recent:
				result['result'] = 'error'
				return result
			return result
		total = self._notice['process'][current]['total']
		imported = self._notice['process'][current]['imported']
		imported = int(imported)
		error = self._notice['process'][current]['error']
		error = int(error)
		id_src = self._notice['process'][current]['id_src']
		simple_action = self._simple_action[current]
		next_action = self._next_action[current]
		if imported < total:
			source_cart = self.get_source_cart(cart)
			target_cart = self.get_target_cart(cart)
			if (not source_cart) or (not target_cart):
				if (not source_cart) or (not target_cart):
					result['result'] = 'success'
					result['msg'] = 'Finish Migration!'
					return result
			fn_get_main = getattr(source_cart, 'get_'+current+'_main_export')
			fn_get_ext = getattr(source_cart, 'get_'+current+'_ext_export')
			fn_convert_export = getattr(source_cart, 'convert'+simple_action+'_export')
			fn_get_id = getattr(target_cart, 'get_'+simple_action+'_id_import')
			fn_check_import = getattr(target_cart, 'check_'+simple_action+'_import')
			fn_router_import = getattr(target_cart, 'router_'+simple_action+'_import')
			fn_before_import = getattr(target_cart, 'before_'+simple_action+'_import')
			fn_import = getattr(target_cart, simple_action+'_import')
			fn_after_import = getattr(target_cart, 'after_'+simple_action+'_import')
			fn_addition_import = getattr(target_cart, 'addition_'+simple_action+'_import')
			mains = fn_get_main()
			if mains['result'] != 'success':
				return mains
			ext = fn_get_ext(mains)
			if ext['result'] != 'success':
				return ext
			for main in mains:
				if imported >= total:
					break
				imported += 1
				convert = fn_convert_export(main, ext)
				if convert['result'] == 'error':
					return convert
				if convert['result'] == 'warning':
					error += 1
					result['msg'] += convert['msg']
					if 'id' in convert:
						id_src = convert['id']
						self.log(convert['id'], simple_action)
					continue
				if convert['result'] == 'pass':
					continue
				convert_data = convert['data']
				id_src = fn_get_id(convert_data, main, ext)
				if fn_check_import(convert_data, main, ext):
					continue
				import_data = fn_import(convert_data, main, ext)
				if import_data['result'] == 'error':
					return import_data
				if import_data['result'] != 'warning':
					error += 1
					result['msg'] += import_data['msg']
					continue
				id_desc = import_data['data']
				after_import = fn_after_import(id_desc,convert_data,main,ext)
				if after_import['result'] == 'error':
					return after_import
				if after_import['result'] == 'success' and after_import['msg']:
					result['msg'] += after_import['msg']
			result['process']['type'] = current
		else:
			pass

	def get_current(self):
		return self._current

	def set_current(self,current):
		self._current = current

	def stop(self):
		self._exit_flag = 1

	def set_exit_flag(self, exit_flag):
		self._exit_flag = exit_flag

	def save_notice(self, cart = None):
		if not cart:
			cart = get_model('basecart')
		notice = self._notice
		demo = None
		if 'demo' in notice and notice['demo']:
			demo = 2
		print(cart)
		return getattr(cart, 'save_user_notice')(self._license, notice, demo)

	def save_recent(self, cart = None):
		if not cart:
			cart = get_model('basecart')
		return getattr(cart, 'save_recent')(self._license,self._notice)

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

	def get_source_cart(self, basecart = None):
		if not basecart:
			basecart = get_model('basecart')

		cart_custom_name = getattr(basecart, 'get_source_custom_cart')(self._license)
		source_cart = get_model(cart_custom_name)
		if source_cart:
			return source_cart
		cart_type = self._notice['src']['cart_type']
		cart_version = self._notice['src']['config']['version']
		cart_name = getattr(basecart, 'get_cart')(cart_type,cart_version)
		source_cart = get_model(cart_name)
		if not source_cart:
			return None
		getattr(source_cart, 'set_type')('src')
		getattr(source_cart, 'set_notice')(self._notice)
		return source_cart

	def get_target_cart(self, basecart = None):
		if not basecart:
			basecart = get_model('basecart')

		cart_custom_name = getattr(basecart, 'get_target_custom_cart')(self._license)
		target_cart = get_model(cart_custom_name)
		if target_cart:
			return target_cart
		cart_type = self._notice['target']['cart_type']
		cart_version = self._notice['target']['config']['version']
		cart_name = getattr(basecart, 'get_cart')(cart_type, cart_version)
		target_cart = get_model(cart_name)
		if not target_cart:
			return None
		getattr(target_cart, 'set_type')('src')
		getattr(target_cart, 'set_notice')(self._notice)
		return target_cart

	def log(self, msg, type_log):
		log(msg, self._license, type_log + 'error')
