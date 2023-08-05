import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Board(Base):

	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_project(self, project_key):
		"""Function responsible for finding all project's boards  that user has access"""
		try:
			logging.info("Start function: find_by_project")
			return self.jira.boards(projectKeyOrID=project_key)
			logging.info("End funcion: find_by_project")
		except Exception as e:
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)


    

