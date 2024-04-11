class ShodoSetting:
	def __init__(self):
		self.org_name = ""
		self.project_name = ""
		self.token = ""
		self.flg_able = False
		self.use = False

	def set_preference(self, org_name, project_name, token):
		if org_name != "" and project_name != "" and token != "":
			self.org_name = org_name
			self.project_name = project_name
			self.token = token

	def is_active(self):
		return self.flg_able and self.use

	def deactivate(self):
		self.flg_able = False
		self.use = False