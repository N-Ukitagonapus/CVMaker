'''
職務経歴
'''
class CareerHistoryData:
	#コンストラクタ(のようなもの)
	def __init__(self):
		self.__flg_over = False
		self.__term_start = ""
		self.__term_end = ""
		self.__description_industry = ""
		self.__description_project_overview = ""
		self.__description_system_overview = ""
		self.__description_work = []
		self.__development_srv = []  
		self.__development_os = []
		self.__development_db = []
		self.__development_lang = []
		self.__development_fw = []
		self.__development_mw = []
		self.__development_tools = []
		self.__development_pkg = []
		self.__tasks = []
		self.__scale = ""
		self.__position = ""
		self.__flg_internal_leader = False
		self.__members = 0
		self.__members_internal = 0