from libs.database import Database
from libs.base_model import BaseModel
from libs.utils import *

class LeBasecart(BaseModel):
	CONNECTOR_SUFFIX = '/litextension_connector/connector.php'
	TYPE_TAX = 'tax'
	TYPE_TAX_PRODUCT = 'tax_product'
	TYPE_TAX_CUSTOMER = 'tax_customer'
	TYPE_TAX_RATE = 'tax_rate'
	TYPE_TAX_CALCULATION = 'tax_calculation'
	TYPE_TAX_ZONE = 'tax_zone'
	TYPE_TAX_ZONE_COUNTRY = 'tax_zone_country'
	TYPE_TAX_ZONE_STATE = 'tax_zone_state'
	TYPE_TAX_ZONE_RATE = 'tax_zone_rate'
	TYPE_MANUFACTURER = 'manufacturer'
	TYPE_CATEGORY = 'category'
	TYPE_PRODUCT = 'product'
	TYPE_CHILD = 'product_child'
	TYPE_ATTR = 'attr'
	TYPE_ATTR_VALUE = 'attr_value'
	TYPE_OPTION = 'option'
	TYPE_OPTION_VALUE = 'option_value'
	TYPE_CUSTOMER = 'customer'
	TYPE_ADDRESS = 'address'
	TYPE_ORDER = 'order'
	TYPE_REVIEW = 'review'
	TYPE_SHIPPING = 'shipping'
	TYPE_PAGE = 'page'
	TYPE_BLOCK = 'block'
	TYPE_WIDGET = 'widget'
	TYPE_POLL = 'poll'
	TYPE_TRANSACTION = 'transaction'
	TYPE_NEWSLETTER = 'newsletter'
	TYPE_USER = 'user'
	TYPE_RULE = 'rule'
	TYPE_CART_RULE = 'cart_rule'
	TYPE_POST = 'post'
	TYPE_FORMAT = 'format'
	TYPE_COMMENT = 'comment'
	TYPE_TAG = 'tag'
	TYPE_BUNDLE_OPTION = "bundle_option"
	TYPE_ORDER_ITEM = "sales_order_item"
	TYPE_CAT_URL = "category_url_key"
	TYPE_PRO_URL = "product_url_key"
	PRODUCT_SIMPLE = 'simple'
	PRODUCT_CONFIG = 'configurable'
	PRODUCT_VIRTUAL = 'virtual'
	PRODUCT_DOWNLOAD = 'download'
	PRODUCT_GROUP = 'grouped'
	PRODUCT_BUNDLE = 'bundle'
	OPTION_FIELD = 'field'
	OPTION_TEXT = 'text'
	OPTION_SELECT = 'select'
	OPTION_DATE = 'date'
	OPTION_DATETIME = 'datetime'
	OPTION_RADIO = 'radio'
	OPTION_CHECKBOX = 'checkbox'
	OPTION_PRICE = 'price'
	OPTION_BOOLEAN = 'boolean'
	OPTION_FILE = 'file'
	OPTION_MULTISELECT = 'multi_select'
	OPTION_FRONTEND = 'frontend'
	OPTION_BACKEND = 'backend'
	GENDER_MALE = 'm'
	GENDER_FEMALE = 'f'
	GENDER_OTHER = 'o'
	PRICE_POSITIVE = '+'
	PRICE_NEGATIVE = '-'

	def __init__(self):
		super().__init__()
		self._db = None
		self._notice = None
		self._cart_url = None
		self._type = None
		self._user_id = None
		self._license = None

	# TODO: INIT
	def get_db(self):
		if not self._db:
			db = Database()
			conn = db.get_connect()
			if not conn:
				return None
			self._db = db
		return self._db


	# TODO: NOTICE
	def set_type(self, cart_type):
		self._type = cart_type

	def get_type(self):
		return self._type

	def get_user_id(self):
		return self._user_id

	def set_user_id(self,user_id):
		self._user_id = user_id

	def set_notice(self, notice):
		self._notice = notice
		cart_type = self.get_type()
		if cart_type:
			self._cart_url = notice[cart_type]['cart_url']
		return self

	def get_notice(self):
		return self._notice

	def get_user_notice(self, user_license):
		if not user_license:
			return None
		db = self.get_db()
		if not db:
			return None
		notice = db.select_obj(TABLE_NOTICE, {'license': user_license})
		if (notice['result'] != 'success') or (not notice['data']):
			return None
		return json.loads(notice['data'])

	def save_notice(self, _license, notice, mode = None, status = None):
		notice = json.dumps(notice)
		if not _license:
			return False
		db = self.get_db()
		exist = db.select_obj(TABLE_NOTICE, {'license': _license})
		if exist['result'] != 'success':
			return False
		if exist['data']:
			result = self.update_obj(TABLE_NOTICE, {'notice': notice}, {'license': _license})
		else:
			data_notice = {
				'license': _license,
				'notice': notice,
			}
			if mode:
				data_notice['mode'] = mode
			if status:
				data_notice['status'] = status
			result = self.insert_obj(TABLE_NOTICE, data_notice)
		return True if (result['result'] == 'success') and result['data'] else False
	# def sync_notice(self, notice):
	# 	notice_server = self.get_user_notice(notice['license'])
	# 	if not notice_server:
	# 		return notice

	def get_license(self):
		return self._license

	def set_license(self, _license):
		self._license = _license

	# TODO: Cart
	def get_cart(self, cart_type, cart_version = None):
		if cart_type == 'magento':
			if ('1.14' in cart_version) or ('1.13' in cart_version):
				return 'cart_magento19'
			magento_version = self.convert_version(cart_version, 2)
			if magento_version > 200:
				return 'cart_magento2'
			elif magento_version > 149:
				return 'cart_magento19'
			elif magento_version > 141:
				return 'cart_magento14'
			else:
				return 'cart_magento13'
		return 'basecart'

	def get_source_cart(self):
		cart_type = self._notice['src']['cart_type']
		cart_version = self._notice['src']['config']['version']
		cart_name = self.get_cart(cart_type, cart_version)
		source_cart = get_model(cart_name)
		return source_cart

	def get_target_cart(self):
		cart_type = self._notice['target']['cart_type']
		cart_version = self._notice['target']['config']['version']
		cart_name = self.get_cart(cart_type, cart_version)
		source_cart = get_model(cart_name)
		return source_cart

	def convert_version(self, v, num):
		digits = v.split('.')
		version = 0
		if isinstance(digits, list):
			for index, val in enumerate(digits):
				if index <= num:
					version += int(val[0]) * pow(10, max(0, num - index))
		return version

	def prepare_import_source(self):
		return {
			'result': 'success'
		}

	def prepare_import_target(self):
		return {
			'result': 'success'
		}

	def prepare_taxes_import(self):
		return {'result': 'success'}

	def prepare_taxes_export(self):
		return {'result': 'success'}

	def get_taxes_main_export(self):
		return response_success()

	def get_taxes_ext_export(self,taxes):
		return response_success()

	def convert_tax_export(self,tax,taxes_ext):
		return response_success()

	def get_tax_id_import(self,convert,tax,taxes_ext):
		return False

	def check_tax_import(self,convert,tax,taxes_ext):
		return False

	def router_tax_import(self,convert,tax,taxes_ext):
		return response_success('tax_import')

	def before_tax_import(self, convert, tax, taxes_ext):
		return response_success()

	def tax_import(self,convert,tax,taxes_ext):
		return response_success(0)

	def after_tax_import(self,convert,tax,taxes_ext):
		return response_success()

	def addition_tax_import(self,convert,tax,taxes_ext):
		return response_success()

