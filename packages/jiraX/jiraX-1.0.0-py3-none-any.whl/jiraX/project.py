import logging
logging.basicConfig(level=logging.INFO)
from .base import Base


class Project(Base):
	"""
	Class responsable for documentation projects in Jira
	"""
	ERROR = "OS error: {0}"
	
	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
	
	def find_all(self): 
		"""
		Responsible for retreving information about projects

		Returns:
		
			List -- Lits of projects
		"""
		try:
			logging.info("Start function: find_all")
			return self.jira.projects()	
			self.jira.__init__
			logging.info("End function: find_all")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_by_key(self, project_key):
		"""Function responsible for finding all project's roles  that user has access"""
		try:
			logging.info("Start function: find_by_key")
			return self.jira.project(project_key)
			logging.info("End funcion: find_by_key")
		except Exception as e:
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)
	

