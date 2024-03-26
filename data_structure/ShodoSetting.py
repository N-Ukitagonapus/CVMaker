class ShodoSetting:
	def __init__(self):
		self.user_id = ""
		self.project_name = ""
		self.token = ""
		self.flg_able = False
		self.use = False

	def set_preference(self, user_id, project_name, token):
		if user_id != "" and project_name != "" and token != "":
			self.user_id = user_id
			self.project_name = project_name
			self.token = token

	def is_active(self):
		return self.flg_able and self.use

	def deactivate(self):
		self.flg_able = False
		self.use = False