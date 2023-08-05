import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class SprintBacklog(Base):

	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_sprint(self, sprint_id): 
		try:
			logging.info("Start function: find_by_sprint")
			return self.jira.search_issues(f'Sprint={sprint_id}')
			logging.info("End function: find_by_sprint")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 