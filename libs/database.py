import configparser
import mysql.connector
from mysql.connector import errorcode
from pathlib import Path
from libs import utils
import re


class Database:
	_db = None
	_conn = None
	_cursor = None
	_db_host = ''
	_db_username = ''
	_db_password = ''
	_db_name = ''
	_db_prefix = ''
	CONFIG_FILE = 'etc/config.ini'
	CONST_MSG_ERR = 'Could not connect database.'

	def __init__(self):
		self.set_config()

	def default_config(self):
		default_config = dict()
		default_config['db_host'] = ''
		default_config['db_username'] = ''
		default_config['db_password'] = ''
		default_config['db_name'] = ''
		default_config['db_prefix'] = ''
		return default_config

	def get_db_host(self):
		if self._db_host:
			return self._db_host
		default_config = self.default_config()
		return default_config['db_host']

	def get_db_username(self):
		if self._db_username:
			return self._db_username
		default_config = self.default_config()
		return default_config['db_username']

	def get_db_password(self):
		if self._db_password:
			return self._db_password
		default_config = self.default_config()
		return default_config['db_password']

	def get_db_name(self):
		if self._db_name:
			return self._db_name
		default_config = self.default_config()
		return default_config['db_name']

	def get_db_prefix(self):
		if self._db_prefix:
			return self._db_prefix
		default_config = self.default_config()
		return default_config['db_prefix']

	def set_db_host(self, host = ''):
		self._db_host = host
		return self

	def set_username(self, username = ''):
		self._db_username = username
		return self

	def set_db_password(self, password = ''):
		self._db_password = password
		return self

	def set_db_name(self, name = ''):
		self._db_name = name
		return self

	def set_db_prefix(self, prefix = ''):
		self._db_prefix = prefix
		return self

	def set_config(self):
		file_config = Path(self.CONFIG_FILE)
		if not file_config.is_file():
			return False
		config = configparser.ConfigParser()
		config.read(self.CONFIG_FILE)
		self.set_db_host(config['mysql']['db_host']).set_username(config['mysql']['db_username']).set_db_password(
				config['mysql']['db_password']).set_db_name(config['mysql']['db_name'])
		return self

	def get_config(self):
		config = dict()
		config['host'] = self.get_db_host()
		config['user'] = self.get_db_username()
		config['password'] = self.get_db_password()
		config['database'] = self.get_db_name()
		config['raise_on_warnings'] = True
		config['charset'] = 'utf8'
		config['use_unicode'] = True
		return config

	# TODO: CONNECT

	def connect(self):
		self.refresh_connect()

	def refresh_connect(self):
		self.close_connect()
		self._conn = self._create_connect()
		return self._conn

	def close_connect(self):
		if self._cursor:
			self._cursor.close()
		if self._conn:
			self._conn.close()
		return True

	def _create_connect(self):
		config = self.get_config()
		try:
			cnx = mysql.connector.connect(**config)
			return cnx
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)

	def get_connect(self):
		if self._conn:
			ping = self._conn.ping()
			if not ping:
				self.refresh_connect()
		else:
			self._conn = self._create_connect()
		return self._conn

	def get_cursor(self):
		conn = self.get_connect()
		if conn:
			self._cursor = conn.cursor()
		return self._cursor

	def get_table_name(self, table):
		return self._db_prefix + table

	def escape(self, value):
		if value is None:
			return 'null'
		if value == '':
			return "''"
		if not value:
			return value
		if isinstance(value, int):
			return value
		if isinstance(value, str):
			value = re.escape(value)
		return "'" + value + "'"

	def dict_to_create_table_sql(self, dictionary):
		if not (isinstance(dictionary, dict)):
			return {'result': 'error', 'msg': "Data not exists."}

		table = dictionary['table']
		row_data = dictionary['rows']
		references_data = utils.get_value_by_key_in_dict(dictionary, 'references', dict())
		unique_data = utils.get_value_by_key_in_dict(dictionary, 'unique', dict())
		rows = list()
		for row_name, construct in row_data.items():
			row = "`" + row_name + "` " + construct
			rows.append(row)

		references = list()
		for row_reference, data_reference in references_data.items():
			references.append("FOREIGN KEY (" + row_reference + ") REFERENCES " + self.get_table_name(
					data_reference['table']) + "(" + data_reference['row'] + ")")
		unique = list()
		if unique_data:
			for row_unique in unique_data:
				name = ''
				fields = list()
				for field in row_unique:
					name += '-' + field.upper() if name else field.upper()
					fields.append("`" + field + "`")
				str_unique = 'UNIQUE `' + name + '` ( '
				str_unique += ','.join(fields) + ' )'
				unique.append(str_unique)
		table_name = self.get_table_name(table)
		query = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
		query += ','.join(rows)
		if references:
			query += ","
			query += ','.join(references)
		if unique:
			query += ","
			query += ",".join(unique)
		query += ' )'
		return {'result': 'success', 'query': query}

	def dict_to_insert_condition(self, dictionary, allow_key = None):
		keys = dictionary.keys()
		data_key = list()
		data_value = list()
		if not allow_key:
			data_key = keys
			values = dictionary.values()
			for value in values:
				data_value.append(self.escape(value))
		else:
			for key in keys:
				if key in allow_key:
					data_key.append(key)
					value = dictionary[key]
					if isinstance(value, int):
						data_value.append(value)
					else:
						data_value.append(self.escape(value))
		if not data_key:
			return False
		data_value = list(map(lambda x: str(x), data_value))
		key_condition = '(`' + '`, `'.join(data_key) + '`)'
		value_condition = '(' + ', '.join(data_value) + ')'
		return key_condition + ' VALUES ' + value_condition

	def dict_to_where_condition(self, dictionary):
		if not dictionary:
			return '1 = 1'
		if isinstance(dictionary, str):
			return dictionary
		data = list()
		for key, value in dictionary.items():
			data.append("`" + key + "` = " + self.escape(value))
		condition = " AND ".join(data)
		return condition

	def dict_to_set_condition(self, dictionary):
		if not dictionary:
			return ''
		data = list()
		for key, value in dictionary.items():
			data.append("`" + key + "` = " + self.escape(value))
		return ','.join(data)

	def list_to_in_condition(self, dictionary):
		if not dictionary:
			return "('null')"
		data = list(map(self.escape, dictionary))
		data = list(map(lambda x: str(x), data))
		return "(" + ",".join(data) + ")"

	# TODO: QUERY
	def select_raw(self, query):
		try:
			cursor = self.get_cursor()
			if not cursor:
				return self.response_error(self.CONST_MSG_ERR)
			cursor.execute(query)
			rows = cursor.fetchall()
			cursor.close()
			return self.response_success(rows)
		except Exception as e:
			return self.response_error(e)

	def select_obj(self, table, where = None, select_field = None):
		table_name = self.get_table_name(table)
		cursor = self.get_cursor()
		if not cursor:
			return self.response_error(self.CONST_MSG_ERR)
		data_select = '*'
		if select_field and isinstance(select_field, list):
			data_select = ','.join(select_field)
		query = "SELECT " + data_select + " FROM `" + table_name + "`"
		if where:
			if isinstance(where, str):
				query += " WHERE " + where
			elif isinstance(where, dict):
				query += " WHERE " + self.dict_to_where_condition(where)
		return self.select_raw(query)

	def insert_raw(self, query, insert_id = False):
		cursor = self.get_cursor()
		if not cursor:
			return self.response_error()
		try:
			cursor.execute(query)
			self._conn.commit()
			data = True
			if insert_id:
				data = cursor.lastrowid
			return self.response_success(data)
		except Exception as e:
			return self.response_error(e)

	def insert_obj(self, table, data, insert_id = False):
		table_name = self.get_table_name(table)
		data_condition = self.dict_to_insert_condition(data)
		query = "INSERT INTO `" + table_name + "` " + data_condition
		return self.insert_raw(query, insert_id)

	def query_raw(self, query):
		cursor = self.get_cursor()
		if not cursor:
			return self.response_error()
		try:
			cursor.execute(query)
			self._conn.commit()
			self._cursor.close()
			return self.response_success()
		except mysql.connector.Error as e:
			if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				return self.response_success()
			return self.response_error(e)

	# response
	def response_error(self, msg = None):
		if not msg:
			msg = self.CONST_MSG_ERR
		return {'result': 'error', 'msg': msg, 'data': None}

	def response_success(self, data = None, msg = None):
		return {
			'result': 'success', 'msg': msg, 'data': data
		}
