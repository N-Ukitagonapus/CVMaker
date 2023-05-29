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

		et.SubElement(base,"expr_start").text = self.data.expr_start.strftime("%Y%m")
		et.SubElement(base,"absense_year").text = 0 if self.data.period_absense_year.get() == "" else self.data.period_absense_year.get()
		et.SubElement(base,"absense_month").text = 0 if self.data.period_absense_month.get() == "" else self.data.period_absense_month.get()
		create_list(base,self.data.qualifications,"qualifications")
		create_env(base,self.data.expr_env)
		if self.data.pr != "":
			et.SubElement(base,"pr").text = self.data.pr
   
		tree.write(self.filename, encoding="utf-8", xml_declaration=True)

class PersonalDataInput():
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
  
	def read(self):
		vals = {
			"shain_num":{"label":"社員番号"},
			"last_name_kanji":{"label":"氏(漢字)"},
			"first_name_kanji":{"label":"名(漢字)"},
			"last_name_romaji":{"label":"氏(ローマ字)"},
			"first_name_romaji":{"label":"名(ローマ字)"},
			"gender":{"label":"性別"},
			"birthday":{"label":"誕生日"},
			"current_address":{"label":"現住所"},
			"nearest_station":{"label":"最寄り駅"},
			"gakureki":{"label":"最終学歴"}
			}
		keys = list(vals.keys())
		for key in keys:
			text = self.root.find(key)
			if text is not None:
				vals[key]["value"] = text.text
			else:
				vals[key]["value"] = None
		print(vals)
		return vals