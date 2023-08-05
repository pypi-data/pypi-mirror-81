import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Sprint(Base):

	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_board(self, board_id):
		"""Function responsible for finding all project's sprints  that user has access"""
		try:
			logging.info("Start function: find_by_board")
			return self.jira.sprints(board_id)
			logging.info("End funcion: find_by_board")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)

    