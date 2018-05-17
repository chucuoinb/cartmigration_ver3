from libs.database import Database


class BaseModel:
	_db = None

	def __init__(self):
		self._db = Database()

	def get_db(self):
		return self._db

	def query_raw(self, query):
		return self._db.query_raw(query)

	def dict_to_create_table_sql(self, dictionary):
		return self._db.dict_to_create_table_sql(dictionary)

	def dict_to_insert_condition(self, dictionary, allow_key = None):
		return self._db.dict_to_insert_condition(dictionary, allow_key)

	def dict_to_where_condition(self, dictionary):
		return self._db.dict_to_where_condition(dictionary)

	def dict_to_set_condition(self, dictionary):
		return self._db.dict_to_set_condition(dictionary)

	def list_to_in_condition(self, list_data):
		return self._db.list_to_in_condition(list_data)

	def insert_obj(self, table, data, insert_id = False):
		return self._db.insert_obj(table, data, insert_id)

	def insert_raw(self, query, insert_id = False):
		return self._db.insert_raw(query, insert_id)
