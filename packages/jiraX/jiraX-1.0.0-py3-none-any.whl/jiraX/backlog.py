import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Backlog(Base):

	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_project(self, project_key): 
		try:
			logging.info("Start function: find_by_projcet")
			return self.jira.search_issues('project='+project_key)
			logging.info("End function: find_by_project")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

    




