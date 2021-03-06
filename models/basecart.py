from libs.database import Database
from libs.base_model import BaseModel
from libs.utils import *
import requests
import base64
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
		notice = self.select_obj(TABLE_NOTICE, {'license': user_license})
		if (notice['result'] != 'success') or (not notice['data']):
			return None
		try:
			notice_data = notice['data'][0]['notice']
			notice_data = json.loads(notice_data)
			return notice_data
		except Exception as e:
			return None

	def save_user_notice(self, _license, notice, mode = None, status = None):
		notice = json.dumps(notice)
		if not _license:
			return False
		exist = self.select_obj(TABLE_NOTICE, {'license': _license})
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

	def delete_user_notice(self, _license):
		if not _license:
			return True
		delete = self.delete_obj(TABLE_NOTICE,{'license': _license})
		if delete and delete['result'] == 'success':
			return delete['data']
		return False

	def save_recent(self, _license, notice):
		notice = json.dumps(notice)
		exist = False
		check = self.select_obj(TABLE_RECENT,{'license': _license})
		if check and check['result'] == 'success' and check['data']:
			exist = True
		result = False
		if exist:
			update = self.update_obj(TABLE_RECENT, {'notice': notice}, {'license': _license})
			if update and update['result'] == 'success':
				result = update['data']
		else:
			insert = self.insert_obj(TABLE_RECENT, {'license': _license, 'notice': notice})
			if insert and insert['result'] == 'success':
				result = insert['data']
		return result

	def get_recent(self, _license):
		if not _license:
			return None
		result = self.select_obj(TABLE_RECENT, {'license': _license})
		if 'data' in result and '0' in result['data']:
			return json.loads(result['data'][0]['notice'])
		return None

	def delete_recent(self,_license):
		if not _license:
			return True
		delete = self.delete_obj(TABLE_RECENT,{'license': _license})
		if delete and delete['result'] == 'success':
			return delete['data']
		return False

	def get_license(self):
		return self._license

	def set_license(self, _license):
		db = self.get_db()
		if db:
			db.set_license(_license)
			self._db = db
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

	def get_source_custom_cart(self, _license):
		return 'custom_'+_license+'_source'

	def get_target_custom_cart(self, _license):
		return 'custom_'+_license+'_target'

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


	def get_connector_url(self, action, token=None, cart_type = None):
		if not cart_type:
			cart_type = self.get_type()
		if not token:
			token = self._notice[cart_type]['config']['token']
		url = self.get_url_suffix(self.CONNECTOR_SUFFIX)
		url += '?action='+action+'&token='+token
		return url

	def get_url_suffix(self, suffix):
		url = self._cart_url.rstrip('/') + '/' + suffix.lstrip('/')
		return url

	def get_connector_data(self):
		pass

	def encode_connector_data(self, data):
		encode_data = dict()
		for k, v in data.items():
			encode_data[k] = string_to_base64(v)
		return encode_data

	def add_table_prefix(self, data):
		if 'query' in data:
			cart_type = self.get_type()
			prefix = self._notice[cart_type]['config']['table_prefix']
			queries = json.loads(data['query'])
			if 'multi_query' in data:
				add = dict()
				for table, query in queries.items():
					query['query'] = query['query'].replace('_DBPRF_', prefix)
					add[table] = query
				data['query'] = json.dumps(add)
			else:
				query = queries
				query['query'] = query['query'].replace('_DBPRF_', prefix)
				data['query'] = json.dumps(query)
		return data


	def get_request_by_post(self, url, data):
		try:
			r = requests.post(url,data)
			r.raise_for_status()
			print(r.text)
		except requests.exceptions.HTTPError as errh:
			print("Http Error:", errh)
		except requests.exceptions.ConnectionError as errc:
			print("Error Connecting:", errc)
		except requests.exceptions.Timeout as errt:
			print("Timeout Error:", errt)
		except requests.exceptions.RequestException as err:
			print("OOps: Something Else", err)


	# TODO: MIGRATION
	def prepare_import_source(self):
		return response_success()

	def prepare_import_target(self):
		return response_success()


	# TODO: TAX
	def prepare_taxes_import(self):
		return self

	def prepare_taxes_export(self):
		return self

	def get_taxes_main_export(self):
		return response_success()

	def get_taxes_ext_export(self, taxes):
		return response_success()

	def convert_tax_export(self, tax, taxes_ext):
		return response_success()

	def get_tax_id_import(self, convert, tax, taxes_ext):
		return False

	def check_tax_import(self, convert, tax, taxes_ext):
		return False

	def router_tax_import(self, convert, tax, taxes_ext):
		return response_success('tax_import')

	def before_tax_import(self, convert, tax, taxes_ext):
		return response_success()

	def tax_import(self, convert, tax, taxes_ext):
		return response_success(0)

	def after_tax_import(self, convert, tax, taxes_ext):
		return response_success()

	def addition_tax_import(self, convert, tax, taxes_ext):
		return response_success()


	# TODO: MANUFACTURER
	def prepare_manufacturers_import(self):
		return self

	def prepare_manufacturers_export(self):
		return self

	def get_manufacturers_main_export(self):
		return response_success()

	def get_manufacturers_ext_export(self, manufacturers):
		return response_success()

	def convert_manufacturer_export(self, manufacturer, manufacturers_ext):
		return response_success()

	def get_manufacturer_id_import(self, convert, manufacturer, manufacturers_ext):
		return False

	def check_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return False

	def router_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success('manufacturer_import')

	def before_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success()

	def manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success(0)

	def after_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success()

	def addition_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success()



	# TODO: CATEGORY
	def prepare_categories_import(self):
		return self

	def prepare_categories_export(self):
		return self

	def get_categories_main_export(self):
		return response_success()

	def get_categories_ext_export(self, categories):
		return response_success()

	def convert_category_export(self, category, categories_ext):
		return response_success()

	def get_category_id_import(self, convert, category, categories_ext):
		return False

	def check_category_import(self, convert, category, categories_ext):
		return False

	def router_category_import(self, convert, category, categories_ext):
		return response_success('category_import')

	def before_category_import(self, convert, category, categories_ext):
		return response_success()

	def category_import(self, convert, category, categories_ext):
		return response_success(0)

	def after_category_import(self, convert, category, categories_ext):
		return response_success()

	def addition_category_import(self, convert, category, categories_ext):
		return response_success()


	# TODO: PRODUCT
	def prepare_products_import(self):
		return self

	def prepare_products_export(self):
		return self

	def get_products_main_export(self):
		return response_success()

	def get_products_ext_export(self, products):
		return response_success()

	def convert_product_export(self, product, products_ext):
		return response_success()

	def get_product_id_import(self, convert, product, products_ext):
		return False

	def check_product_import(self, convert, product, products_ext):
		return False

	def router_product_import(self, convert, product, products_ext):
		return response_success('product_import')

	def before_product_import(self, convert, product, products_ext):
		return response_success()

	def product_import(self, convert, product, products_ext):
		return response_success(0)

	def after_product_import(self, convert, product, products_ext):
		return response_success()

	def addition_product_import(self, convert, product, products_ext):
		return response_success()



	# TODO: CUSTOMER
	def prepare_customers_import(self):
		return self

	def prepare_customers_export(self):
		return self

	def get_customers_main_export(self):
		return response_success()

	def get_customers_ext_export(self, customers):
		return response_success()

	def convert_customer_export(self, customer, customers_ext):
		return response_success()

	def get_customer_id_import(self, convert, customer, customers_ext):
		return False

	def check_customer_import(self, convert, customer, customers_ext):
		return False

	def router_customer_import(self, convert, customer, customers_ext):
		return response_success('customer_import')

	def before_customer_import(self, convert, customer, customers_ext):
		return response_success()

	def customer_import(self, convert, customer, customers_ext):
		return response_success(0)

	def after_customer_import(self, convert, customer, customers_ext):
		return response_success()

	def addition_customer_import(self, convert, customer, customers_ext):
		return response_success()



	# TODO: ORDER
	def prepare_orders_import(self):
		return self

	def prepare_orders_export(self):
		return self

	def get_orders_main_export(self):
		return response_success()

	def get_orders_ext_export(self, orders):
		return response_success()

	def convert_order_export(self, order, orders_ext):
		return response_success()

	def get_order_id_import(self, convert, order, orders_ext):
		return False

	def check_order_import(self, convert, order, orders_ext):
		return False

	def router_order_import(self, convert, order, orders_ext):
		return response_success('order_import')

	def before_order_import(self, convert, order, orders_ext):
		return response_success()

	def order_import(self, convert, order, orders_ext):
		return response_success(0)

	def after_order_import(self, convert, order, orders_ext):
		return response_success()

	def addition_order_import(self, convert, order, orders_ext):
		return response_success()


	# TODO: REVIEW
	def prepare_reviews_import(self):
		return self

	def prepare_reviews_export(self):
		return self

	def get_reviews_main_export(self):
		return response_success()

	def get_reviews_ext_export(self, reviews):
		return response_success()

	def convert_review_export(self, review, reviews_ext):
		return response_success()

	def get_review_id_import(self, convert, review, reviews_ext):
		return False

	def check_review_import(self, convert, review, reviews_ext):
		return False

	def router_review_import(self, convert, review, reviews_ext):
		return response_success('review_import')

	def before_review_import(self, convert, review, reviews_ext):
		return response_success()

	def review_import(self, convert, review, reviews_ext):
		return response_success(0)

	def after_review_import(self, convert, review, reviews_ext):
		return response_success()

	def addition_review_import(self, convert, review, reviews_ext):
		return response_success()


	# TODO: PAGE
	def prepare_pages_import(self):
		return self

	def prepare_pages_export(self):
		return self

	def get_pages_main_export(self):
		return response_success()

	def get_pages_ext_export(self, pages):
		return response_success()

	def convert_page_export(self, page, pages_ext):
		return response_success()

	def get_page_id_import(self, convert, page, pages_ext):
		return False

	def check_page_import(self, convert, page, pages_ext):
		return False

	def router_page_import(self, convert, page, pages_ext):
		return response_success('page_import')

	def before_page_import(self, convert, page, pages_ext):
		return response_success()

	def page_import(self, convert, page, pages_ext):
		return response_success(0)

	def after_page_import(self, convert, page, pages_ext):
		return response_success()

	def addition_page_import(self, convert, page, pages_ext):
		return response_success()


	# TODO: BLOCK
	def prepare_blocks_import(self):
		return response_success()

	def prepare_blocks_export(self):
		return self

	def get_blocks_main_export(self):
		return self

	def get_blocks_ext_export(self, blocks):
		return response_success()

	def convert_block_export(self, block, blocks_ext):
		return response_success()

	def get_block_id_import(self, convert, block, blocks_ext):
		return False

	def check_block_import(self, convert, block, blocks_ext):
		return False

	def router_block_import(self, convert, block, blocks_ext):
		return response_success('block_import')

	def before_block_import(self, convert, block, blocks_ext):
		return response_success()

	def block_import(self, convert, block, blocks_ext):
		return response_success(0)

	def after_block_import(self, convert, block, blocks_ext):
		return response_success()

	def addition_block_import(self, convert, block, blocks_ext):
		return response_success()

