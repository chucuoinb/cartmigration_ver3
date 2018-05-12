from libs.database import Database


class Cart:
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
		self._db = None
		self._notice = None
		self._cart_url = None
		self._type = None

	# TODO: INIT

