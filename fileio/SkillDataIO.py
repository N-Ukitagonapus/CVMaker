from constants.const import ENV_SET
from data_structure.EnvironmentData import EnvironmentData
from data_structure.SkillData import SkillData
from tkinter import filedialog as fd
import xml.etree.ElementTree as et
import xml.dom.minidom as md

FILE_TYPES = [("XMLファイル", ".xml")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xml"
class SkillDataOutput():

	def __init__(self,data:SkillData):
		self.data = data
		self.filename = fd.asksaveasfilename(
			title = "技術情報保存",
			filetypes = FILE_TYPES,
			initialdir = INITIAL_DIR,
			defaultextension = DEFAULT_EXT
    )

	def output(self):
		def create_list(tgt, list:list, base_title):
			if len(self.data.qualifications) > 0 :
				inner = et.SubElement(tgt,base_title)
				for val in list:
					et.SubElement(inner,"value").text = val

		def create_env(tgt, envs:EnvironmentData):
			trunk = et.SubElement(tgt,"environments")
			create_list(trunk,envs.server,"servers")
			create_list(trunk,envs.os,"os")
			create_list(trunk,envs.db,"databases")
			create_list(trunk,envs.lang,"languages")
			create_list(trunk,envs.fw,"frameworks")
			create_list(trunk,envs.mw,"middlewares")
			create_list(trunk,envs.tools,"tools")
			create_list(trunk,envs.pkg,"packages")

		base = et.Element("SkillData")
		tree = et.ElementTree(element=base)

		et.SubElement(base,"shain_num").text = self.data.shain_num
		et.SubElement(base,"expr_start").text = self.data.expr_start.strftime("%Y%m")
		et.SubElement(base,"absense_year").text = "0" if self.data.period_absense_year.get() == "" else self.data.period_absense_year.get()
		et.SubElement(base,"absense_month").text = "0" if self.data.period_absense_month.get() == "" else self.data.period_absense_month.get()
		if self.data.specialty != "":
			et.SubElement(base,"specialty").text = self.data.specialty.get()
		create_list(base,self.data.qualifications,"qualifications")
		create_env(base,self.data.expr_env)
		if self.data.pr != "":
			et.SubElement(base,"pr").text = self.data.pr
		et.indent(tree,"\t")
		
		tree.write(self.filename, encoding="utf-8", xml_declaration=True)

class SkillDataInput():

	def __init__(self):
		filename = fd.askopenfilename(
		title = "個人基本情報読込",
		filetypes = FILE_TYPES,
		initialdir = INITIAL_DIR,
		defaultextension = DEFAULT_EXT
    )
		tree = et.parse(filename) 

		# XMLを取得
		self.root = tree.getroot()
  
	#XML読込
	def read(self):

		def read_env(tree):
			keys=[
				("servers","srv"),
				("os","os"),
				("databases","db"),
				("languages","lang"),
				("frameworks","fw"),
				("middlewares","mw"),
				("tools","tools"),
				("packages","pkg")
			]
			ret = ENV_SET
			for key in keys:
				subtree = tree.find(key[0])
				for value in subtree.iter("value"):
					ret[key[1]].append(value.text)
			return ret

		#単体項目を取得
		vals = {
			"expr_start":{"label":"業界開始年月"},
			"absense_year":{"label":"休職期間(年)"},
			"absense_month":{"label":"休職期間(月)"},
			"specialty":{"label":"得意分野"},
			"pr":{"label":"自己PR"}
			}
		keys = list(vals.keys())
		for key in keys:
			text = self.root.find(key)
			if text is not None:
				vals[key]["value"] = text.text if key != "expr_start" else text.text + "01"
			else:
				vals[key]["value"] = ""

		#資格情報を取得
		vals["qualifications"]={"label":"資格情報"}
		list_qual=[]
		sikaku = self.root.find("qualifications")
		for value in sikaku.iter("value"):
			list_qual.append(value.text)
		vals["qualifications"]["value"] = list_qual

		#使用経験環境を取得
		vals["environments"]={"label":"使用経験(業務外)"}
		vals["environments"]["value"] = read_env(self.root.find("environments"))

		print(vals)
		return vals