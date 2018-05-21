from models.basecart import LeBasecart
from libs.utils import *


class LeCartMagento2(LeBasecart):
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
