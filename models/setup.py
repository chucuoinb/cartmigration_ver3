import collections

from libs.base_model import BaseModel
from libs.utils import *


class Setup(BaseModel):
	_table_notice = {
		'table': TABLE_NOTICE,
		'rows': {
			'id': "BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY",
			'license': "VARCHAR(255) NOT NULL",
			'status': "TINYINT(2) NOT NULL DEFAULT 1",
			'notice': "LONGTEXT NOT NULL",
			'thread_name': "VARCHAR(255)",
			'mode': "TINYINT(2) NOT NULL DEFAULT 1"
		},
		'unique': [
			{'license'}
		]

	}

	_table_map = {
		'table': TABLE_MAP,
		'rows': {
			'license': "VARCHAR(255) NOT NULL",
			'id_src': "BIGINT",
			'id_desc': "BIGINT",
			'code_src': "TEXT",
			'code_desc': "TEXT",
			'value': "LONGTEXT",
		}
	}

	_table_recent = {
		'table': TABLE_RECENT,
		'rows': {
			'license': "VARCHAR(255) NOT NULL",
			'notice': "LONGTEXT"
		},
		'unique': [
			{'license'}
		]
	}

	_table_setting = {
		'table': TABLE_SETTING,
		'rows': {
			'license': "VARCHAR(255) NOT NULL",
			'setting': "LONGTEXT"
		},
		'unique': [
			{'license'}
		]
	}

	def __init__(self):
		super().__init__()
		self.tables = [self._table_notice, self._table_map, self._table_recent, self._table_setting]

	def run(self):

		for table in self.tables:
			query = self.dict_to_create_table_sql(table)
			if query['result'] != 'success':
				return False
			res = self.query_raw(query['query'])
			if res['result'] != 'success':
				return False
		return True
