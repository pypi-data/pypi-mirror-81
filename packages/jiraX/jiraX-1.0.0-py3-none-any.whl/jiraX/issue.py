import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Issue(Base):

	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_id(self, issue_id): 
		try:
			logging.info("Start function: find_by_id")
			return self.jira.issue(issue_id)
			logging.info("End function: find_by_id")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_by_sprint(self, sprint_id):
		try:
			logging.info("Start function: find_by_sprint")
			return self.jira.search_issues(f"Sprint={sprint_id}")
			logging.info("End function: find_by_sprint")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_by_project(self, project_key):
		"""
		Responsible for retreving all issue from a projects
		
		Arguments:

			project_key {String} -- project_key of Jira
		
		Returns:

			List -- Lits of issues
		
		"""
		try:
			logging.info("Start function: find_by_project")
			return self.jira.search_issues('project='+project_key)
			logging.info("End function: find_by_project")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_epic_by_project(self, project_key):
		"""Function responsible for finding all project's epics that user has access"""
		try:
			logging.info("Start function: find_epic")
			return self.jira.search_issues(f'project = {project_key} AND issuetype = Epic')
			logging.info("End function: find_epic")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_story_by_project(self, project_key):
		try:
			logging.info("Start function: find_story")
			return self.jira.search_issues(f'project = {project_key} AND issuetype = Story')
			logging.info("End function: find_story")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_task_by_project(self, project_key):
		try:
			logging.info("Start function: find_task")
			return self.jira.search_issues(f'project = {project_key} AND issuetype = Task')
			logging.info("End function: find_task")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

