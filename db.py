import sys
from loguru import logger
import psycopg2

class Database:
	"""Postgres Database class"""

	def __init__(self,config):
		self.host = config.DATABASE_HOST
		self.username = config.DATABASE_USERNAME
		self.password = config.DATABASE_PASSWORD
		self.port = config.DATABASE_PORT
		self.dbname = config.DATABASE_NAME
		self.conn = None

	def connect(self):
		"""Connect to a Postgres Database"""
		if self.conn is None:
			try:
				self.conn = pyscopg2.connect(host = self.host, username = self.username, password = self.password , port = self.port,dbname = self.dbname)	
			except pyscopg2.DatabaseError as e:
				logger.error(e)
				sys.exit()
			finally:
				logger.info("Connection Opened Successfully")


con = Database(self, "localhost","tiffymuchaya","tiffymuchaya","5432","cmsreplica")
prints(con)