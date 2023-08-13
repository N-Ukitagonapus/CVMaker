import datetime
from tkinter import filedialog as fd
import jaconv

import openpyxl as pyxl
from monthdelta import monthmod 

from data_structure.CareerHistoryData import CareerHistoryData
from data_structure.ExcelOutputData import ExcelOutputData
from data_structure.PersonalData import PersonalData
from data_structure.SkillData import SkillData

from utils.Utilities import Utilities as util

FILE_TYPES = [("EXCELファイル", ".xlsx")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xlsx"
SHEET_NAME = "技術経歴書"

#単項セル
CELLS = {
	"氏名":"B8",
	"性別":"X8",
	"年齢":"AC8",
	"自宅最寄駅":"AH8",
	"住所":"BA8",
	"最終学歴":"B10",
	"業界経験":"X10",
	"保有資格":"AH10",
	"得意分野":"D13",
	"サーバ":"O15",
	"OS":"O16",
	"DB":"O17",
	"言語":"O18",
	"フレームワーク":"O19",
	"ミドルウェア":"O20",
	"ツール":"O21",
	"パッケージ":"O22",
	"自己PR":"D25"
}

class ExcelOutput():
	def __init__(self):
		self.wb = pyxl.load_workbook('template/ExcelTemplate.xlsx')

	def export(self, personal:PersonalData, skill:SkillData, career:CareerHistoryData):
		out_data = self.create_excel_data(personal, skill, career)
		self.write_excel(out_data)
		filename = "{0}_{1}技術経歴書_{2}".format(datetime.date.today().strftime("%Y%m"),out_data.number,out_data.fullname)
		self.save(filename)

	def create_excel_data(self, personal:PersonalData, skill:SkillData, career:CareerHistoryData) -> ExcelOutputData:
		def get_initial(sei:str, mei:str):
			initial_sei = jaconv.han2zen(sei[0:1],'',False,True,False)
			initial_mei = jaconv.han2zen(mei[0:1],'',False,True,False)
			return "{0}．{1}".format(initial_sei, initial_mei)

		def get_gyokaikeiken(start, absense_year, absense_month):
			periods = monthmod(start, datetime.date.today())[0].months
			periods -= ((0 if absense_year == "" else int(absense_year)) * 12) + (0 if absense_month == "" else int(absense_month))
			return "{0}ヶ月".format(periods) if periods < 12 else "{0}年{1}ヶ月".format(periods // 12, periods % 12)

		ret = ExcelOutputData()
		ret.number = personal.shain_num.get()
		ret.fullname = personal.name_last_kanji.get() + personal.name_first_kanji.get()
		ret.name_initial = get_initial(personal.name_last_romaji.get(),personal.name_first_romaji.get())
		ret.gender = personal.gender.get()
		ret.age = "{0}歳".format(util.get_years_sub(personal.birthday,datetime.date.today())[0])
		ret.moyori_station = personal.nearest_station.get()
		ret.address = personal.current_address.get()
		ret.gakureki = personal.gakureki.get()
		ret.gyokai_keiken = get_gyokaikeiken(skill.expr_start,skill.period_absense_year.get(),skill.period_absense_month.get())
		ret.qualifications = ",".join(skill.qualifications)
		ret.tokui_bunya = skill.specialty.get()
		ret.siyoukeiken = skill.expr_env
		ret.pr = skill.pr
		return ret

	def write_excel(self, data:ExcelOutputData):
		sheet = self.wb[SHEET_NAME]
		#単項セル書込
		sheet[CELLS["氏名"]] = data.name_initial
		sheet[CELLS["性別"]] = data.gender
		sheet[CELLS["年齢"]] = data.age
		sheet[CELLS["自宅最寄駅"]] = data.moyori_station
		sheet[CELLS["住所"]] = data.address
		sheet[CELLS["最終学歴"]] = data.gakureki
		sheet[CELLS["業界経験"]] = data.gyokai_keiken
		sheet[CELLS["保有資格"]] = data.qualifications
		sheet[CELLS["得意分野"]] = data.tokui_bunya
		sheet[CELLS["サーバ"]] = ",".join(data.siyoukeiken.server)
		sheet[CELLS["OS"]] = ",".join(data.siyoukeiken.os)
		sheet[CELLS["DB"]] = ",".join(data.siyoukeiken.db)
		sheet[CELLS["言語"]] = ",".join(data.siyoukeiken.lang)
		sheet[CELLS["フレームワーク"]] = ",".join(data.siyoukeiken.fw)
		sheet[CELLS["ミドルウェア"]] = ",".join(data.siyoukeiken.mw)
		sheet[CELLS["ツール"]] = ",".join(data.siyoukeiken.tools)
		sheet[CELLS["パッケージ"]] = ",".join(data.siyoukeiken.pkg)
		sheet[CELLS["自己PR"]] = data.pr
		
	def save(self, filename):
		exportfile = fd.asksaveasfilename(
			title = "EXCEL保存",
			filetypes = FILE_TYPES,
			initialdir = INITIAL_DIR,
			initialfile = filename,
			defaultextension = DEFAULT_EXT
		)
		self.wb.save(exportfile)
