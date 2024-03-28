from data_structure.CareerData import CareerData
class CareerHistoryData:
	"""
	職務経歴情報データ
	"""
	def __init__(self):
		self.last_name_kanji = "" #氏(キー)
		self.first_name_kanji = "" #名(キー)
		self.history_list=[]
		self.history_list.append(CareerData())

	def get_descriptions(self) -> tuple:
		proj_ov = []
		sys_ov = []
		work = []

		for history in self.history_list:
			proj_ov.append("EMPTY" if len(history.description_project_overview) == 0 else history.description_project_overview)
			sys_ov.append("EMPTY" if len(history.description_system_overview) == 0 else history.description_system_overview)
			work.append("EMPTY" if len(history.description_work) == 0 else history.description_work)

		return (proj_ov, sys_ov, work)