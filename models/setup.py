import collections

from libs.base_model import BaseModel
from libs.utils import *


class Setup(BaseModel):
	def __init__(self):
		super().__init__()
		self.tables = list()
		table_thread = dict()
		table_thread['table'] = 'cartmigration_notice'
		table_thread['rows'] = dict()
		table_thread['rows']['id'] = "BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY"
		table_thread['rows']['license'] = "VARCHAR(255) NOT NULL"
		table_thread['rows']['status'] = "TINYINT(2)"
		table_thread['rows']['notice'] = "LONGTEXT NOT NULL"
		table_thread['rows']['thread_name'] = "VARCHAR(255)"
		print(table_thread)
		self.tables.append(table_thread)

	def run(self):

		for table in self.tables:
			query = self.dict_to_create_table_sql(table)
			if query['result'] != 'success':
				print(query)
				return False
			res = self.query_raw(query['query'])
			if res['result'] != 'success':
				print(res)
				return False
		return True
