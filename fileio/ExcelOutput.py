import copy
import datetime
from functools import partial
import tkinter as tk
from tkinter import StringVar, ttk, filedialog as fd
import jaconv

import openpyxl as pyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.styles import Alignment

from monthdelta import monthmod

from data_structure.CareerData import CareerData 
from data_structure.CareerHistoryData import CareerHistoryData
from data_structure.ExcelOutputData import ExcelOutputData, KeirekiSubData, KeirekiSubDataTypeA, KeirekiSubDataTypeB
from data_structure.PersonalData import PersonalData
from data_structure.SkillData import SkillData

from utils.Utilities import Utilities as util, resource_path
from constants.message import DialogMessage as diag

#####################################
###　定数
#####################################

RADIO_MODE_NAME ={
	"MASKING":("マスキング:","名前はイニシャルでマスキングされます。\n(更新作業の場合はこのモードを選択)"),
	"FULLNAME":("フルネーム:","名前をフルネームで設定します。\n(採用時の再提出の場合はこのモードを選択)")
}

RADIO_MODE_EXCEL = {
	"A":("Aタイプ:","作業区分はすべて列挙されます。"),
	"B":("Bタイプ:","作業区分はマーク表示されます。")
}

FILE_TYPES = [("EXCELファイル", ".xlsx")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xlsx"
SHEET_NAME = "技術経歴書"
CAREER_START_ROW = {"A":34, "B":35}
PRINT_AREA = "A1:CD{0}"
BOX = Border(
	top=Side(style='thin', color='000000'),
	bottom=Side(style='thin', color='000000'),
	left=Side(style='thin', color='000000'),
	right=Side(style='thin', color='000000')
)
STYLE_NUM = (Font(size = 11) ,Alignment(horizontal="center",vertical="center",wrapText=True))
STYLE_KEIREKI = (Font(size = 9) , Alignment(horizontal="left",vertical="top",wrapText=True))
STYLE_MARK = (Font(size = 9) , Alignment(horizontal="left",vertical="center",wrapText=True))

#単項セル
SINGLE_CELLS = {
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
# 経歴セル Aタイプ
# 0:書き込みセル
# 1:結合セル
LIST_CELLS ={
  "A":{
		"No":("B{0}","B{0}:C{0}"),
		"期間":("D{0}","D{0}:L{0}"),
		"業務内容":("M{0}","M{0}:AG{0}"),
		"開発環境":("AH{0}","AH{0}:AW{0}"),
		"作業区分":("AX{0}","AX{0}:BE{0}"),
		"作業規模":("BF{0}","BF{0}:BP{0}"),
		"職位":("BQ{0}","BQ{0}:BV{0}"),
		"体制":("BW{0}","BW{0}:CC{0}")
	},
  "B":{
		"No":("B{0}","B{0}:C{0}"),
		"期間":("D{0}","D{0}:L{0}"),
		"業務内容":("M{0}","M{0}:AG{0}"),
		"開発環境":("AH{0}","AH{0}:AT{0}"),
		"作業区分":[("AU{0}","AU{0}:AU{0}"),("AV{0}","AV{0}:AV{0}"),("AW{0}","AW{0}:AW{0}"),("AX{0}","AX{0}:AX{0}"),("AY{0}","AY{0}:AY{0}"),("AZ{0}","AZ{0}:AZ{0}"),("BA{0}","BA{0}:BA{0}"),("BB{0}","BB{0}:BB{0}"),("BC{0}","BC{0}:BC{0}"),("BD{0}","BD{0}:BD{0}")],
		"作業規模":("BE{0}","BE{0}:BP{0}"),
		"職位":("BQ{0}","BQ{0}:BV{0}"),
		"体制":("BW{0}","BW{0}:CC{0}")
	}
}

####################################
###　定数ここまで
####################################
class ExcelOutput():
	"""
	EXCEL出力クラス
	"""
	def __init__(self, personal:PersonalData, skill:SkillData, career:CareerHistoryData):
		"""
		EXCEL出力クラス
		Args:
				mode (str): 出力テンプレートモード
		"""
		self.personal = personal
		self.skill = skill
		self.career = career
		self.mode_name = None
		self.mode_excel = None
	
	def subframe_modeselect(self, tgt):
		"""
		出力モード選択画面

		Args:
				tgt (tk.Frame): 表示元
		"""

		subwindow = tk.Toplevel(tgt)
		subwindow.title("項目再活性")
		subwindow.geometry("300x320")
		subwindow.resizable(False,False)
		subwindow.grab_set()

		frame_button = tk.Frame(subwindow,borderwidth=1,relief=tk.RAISED)
		frame_button_inner = tk.Frame(frame_button)
		button_ok = ttk.Button(frame_button_inner,width=10,text="OK")
		button_cancel = ttk.Button(frame_button_inner,width=10,text="キャンセル")
		frame_button.pack(side=tk.BOTTOM,fill=tk.X,padx=5,pady=5)
		frame_button_inner.pack(pady=5)
		button_cancel.grid(row=0,column=0,padx=15)
		button_ok.grid(row=0,column=1,padx=15)

		frame_name = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "名前設定モード")
		frame_name.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=5,pady=5)
		frame_name_inner=tk.Frame(frame_name)
		frame_name_inner.pack(fill=tk.BOTH,padx=2,pady=2)
		mode_name = StringVar()
		for i in RADIO_MODE_NAME.keys():
			ttk.Radiobutton(frame_name_inner,text=RADIO_MODE_NAME[i][0],value=i,variable=mode_name).pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=2,pady=2)
			tk.Label(frame_name_inner,justify="left",text=RADIO_MODE_NAME[i][1]).pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=2,pady=2)

		frame_excel = tk.LabelFrame(subwindow,relief=tk.RAISED,text = "EXCELスタイル設定モード")
		frame_excel.pack(side=tk.TOP,fill=tk.X,padx=5,pady=5)
		frame_excel_inner=tk.Frame(frame_excel)
		frame_excel_inner.pack(side=tk.TOP,fill=tk.X,padx=2,pady=2)
		mode_excel = StringVar()
		for i in RADIO_MODE_EXCEL.keys():
			ttk.Radiobutton(frame_excel_inner,text=RADIO_MODE_EXCEL[i],value=i,variable=mode_excel).pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=2,pady=2)

		button_ok["command"] = lambda: do_output()
		button_cancel["command"] = lambda: cancel()

		def do_output():
			"""
			出力処理実行
			"""
			if mode_name.get() == "" or mode_excel.get() == "":
					util.msgbox_showmsg(diag.DIALOG_UNSELECT_ERROR)
			else:
				self.mode_name = mode_name.get()
				self.mode_excel = mode_excel.get()
				try:
					self.export()
					util.msgbox_showmsg(diag.DIALOG_SUCCESS_OUTPUT_EXCEL)
				except Exception as e:
					print(e)
					util.msgbox_showmsg(diag.DIALOG_OUTPUT_ERROR)
				finally:
					subwindow.destroy()
		def cancel():
			"""
			キャンセル
			"""
			subwindow.destroy()

	def export(self):
		"""
		EXCELファイルエクスポート

		Parameters
		----------
		personal : PersonalData
				個人基本情報
		skill : SkillData
				技術情報
		career : CareerHistoryData
				職務経歴情報
		"""
		self.wb = pyxl.load_workbook(resource_path("template/ExcelTemplate_{0}.xlsx".format(self.mode_excel)))
		out_data = self.create_excel_data(self.personal, self.skill, self.career)
		self.write_excel(out_data)
		filename = "{0}_{1}技術経歴書_{2}".format(datetime.date.today().strftime("%Y%m"),out_data.number,out_data.fullname)
		self.save(filename)


	def create_excel_data(self, personal:PersonalData, skill:SkillData, career:CareerHistoryData) -> ExcelOutputData:
		"""
		EXCELデータ作成

		Parameters
		----------
		personal : PersonalData
				個人基本情報
		skill : SkillData
				技術情報
		career : CareerHistoryData
				職務経歴情報

		Returns
		-------
		ExcelOutputData
				EXCEL出力データ
		"""
		# 氏名イニシャル取得
		def get_initial(sei:str, mei:str):
			initial_sei = jaconv.han2zen(sei[0:1],'',False,True,False)
			initial_mei = jaconv.han2zen(mei[0:1],'',False,True,False)
			return "{0}．{1}".format(initial_sei, initial_mei)

		# 業界経験取得
		def get_gyokaikeiken(start, absense_year, absense_month):
			periods = monthmod(start, datetime.date.today())[0].months
			periods -= ((0 if absense_year == "" else int(absense_year)) * 12) + (0 if absense_month == "" else int(absense_month))
			return "{0}ヶ月".format(periods) if periods < 12 else "{0}年".format(periods // 12) if periods % 12 == 0 else "{0}年{1}ヶ月".format(periods // 12, periods % 12)

		# 経歴作成
		def create_keireki(cdata:CareerData):
			ret = KeirekiSubData()
			if self.mode_excel == "A":
				ret = KeirekiSubDataTypeA()
				ret.set_work_kbn(cdata.tasks, cdata.tasks_etc)	# 作業区分
			elif self.mode_excel == "B":
				ret = KeirekiSubDataTypeB()
				ret.set_work_kbn(cdata.tasks)										# 作業区分
			ret.set_kikan(cdata.term_start, cdata.term_end)																	# 作業期間
			ret.set_gyomu(cdata.description_gyokai, cdata.description_project_overview,
										cdata.description_system_overview, cdata.description_work)				# 業務内容
			ret.set_kankyo(cdata.environment)																								# 開発環境
			ret.set_sagyo_kibo(cdata.scale)																									# 作業規模
			ret.set_shokui(cdata.position, cdata.position_etc, cdata.flg_internal_leader)		# 職位
			ret.set_taisei(cdata.members, cdata.members_internal)														# 体制
			return ret


		ret = ExcelOutputData()
		ret.number = personal.shain_num.get()
		ret.fullname = personal.name_last_kanji.get() + personal.name_first_kanji.get()
		ret.name_initial = get_initial(personal.name_last_romaji.get(),personal.name_first_romaji.get())
		ret.gender = personal.gender.get()
		ret.age = "{0}歳".format(util.get_years_sub(personal.birthday,util.get_first_date(datetime.date.today()))[0])
		ret.moyori_station = personal.nearest_station.get()
		ret.address = personal.current_address.get()
		ret.gakureki = personal.gakureki.get()
		ret.gyokai_keiken = get_gyokaikeiken(skill.expr_start,skill.period_absense_year.get(),skill.period_absense_month.get())
		ret.qualifications = ",".join(skill.qualifications)
		ret.tokui_bunya = skill.specialty.get()
		ret.siyoukeiken = copy.deepcopy(skill.expr_env)
		ret.pr = skill.pr

		for cdata in career.history_list:
			ret.keireki.append(create_keireki(cdata))
			ret.siyoukeiken.extend(cdata.environment)
		return ret

	def write_excel(self, data:ExcelOutputData):
		"""
		EXCEL書き込み
		EXCEL出力データの内容を実際に書き込む

		Parameters
		----------
		data : ExcelOutputData
				EXCEL出力データ
		"""

		def prepare_cells(sheet, cell_define, row, text, style):
			"""
			セル書込
			Args:
					sheet (Worksheet): シート
					cell_define (dict[str, Any]): セル定義
					row (int): 行番号
					text (int): テキスト
					style (_type_): セルの書式設定
			"""
			cell_start = cell_define[0].format(row)
			cells_merge = cell_define[1].format(row)
			for cell in sheet[cells_merge][0]:
				cell.border = BOX
			sheet.merge_cells(cells_merge)
			sheet[cell_start].value = text
			sheet[cell_start].font = style[0]
			sheet[cell_start].alignment = style[1]

		sheet = self.wb[SHEET_NAME]
		#単項セル書込
		sheet[SINGLE_CELLS["氏名"]].value = data.name_initial  if self.mode_name == "MASKING" else data.fullname
		sheet[SINGLE_CELLS["性別"]].value = data.gender
		sheet[SINGLE_CELLS["年齢"]].value = data.age
		sheet[SINGLE_CELLS["自宅最寄駅"]].value = data.moyori_station
		sheet[SINGLE_CELLS["住所"]].value = data.address
		sheet[SINGLE_CELLS["最終学歴"]].value = data.gakureki
		sheet[SINGLE_CELLS["業界経験"]].value = data.gyokai_keiken
		sheet[SINGLE_CELLS["保有資格"]].value = data.qualifications
		sheet[SINGLE_CELLS["得意分野"]].value = data.tokui_bunya
		sheet[SINGLE_CELLS["サーバ"]].value = ",".join(data.siyoukeiken.server)
		sheet[SINGLE_CELLS["OS"]].value = ",".join(data.siyoukeiken.os)
		sheet[SINGLE_CELLS["DB"]].value = ",".join(data.siyoukeiken.db)
		sheet[SINGLE_CELLS["言語"]].value = ",".join(data.siyoukeiken.lang)
		sheet[SINGLE_CELLS["フレームワーク"]].value = ",".join(data.siyoukeiken.fw)
		sheet[SINGLE_CELLS["ミドルウェア"]].value = ",".join(data.siyoukeiken.mw)
		sheet[SINGLE_CELLS["ツール"]].value = ",".join(data.siyoukeiken.tools)
		sheet[SINGLE_CELLS["パッケージ"]].value = ",".join(data.siyoukeiken.pkg)
		sheet[SINGLE_CELLS["自己PR"]].value = data.pr

		#経歴行書込
		cell_list = LIST_CELLS[self.mode_excel]
		row = CAREER_START_ROW[self.mode_excel]
		for i in range (len(data.keireki)):
			cur = data.keireki[i]
			sheet.row_dimensions[row].height = 180
			prepare_cells(sheet, cell_list["No"], row, str(i+1), STYLE_NUM)
			prepare_cells(sheet, cell_list["期間"], row, cur.text_kikan, STYLE_KEIREKI)
			prepare_cells(sheet, cell_list["業務内容"], row, cur.text_gyomu, STYLE_KEIREKI)
			prepare_cells(sheet, cell_list["開発環境"], row, cur.text_kankyo, STYLE_KEIREKI)
			prepare_cells(sheet, cell_list["作業規模"], row, cur.text_sagyokibo, STYLE_KEIREKI)
			prepare_cells(sheet, cell_list["職位"], row, cur.text_shokui, STYLE_KEIREKI)
			prepare_cells(sheet, cell_list["体制"], row, cur.text_taisei, STYLE_KEIREKI)
			if self.mode_excel == "A":
				prepare_cells(sheet, cell_list["作業区分"], row, cur.text_work_kbn, STYLE_KEIREKI)
			elif self.mode_excel == "B":
				for i in range(len(cell_list["作業区分"])):
					prepare_cells(sheet, cell_list["作業区分"][i], row, "●" if cur.list_work_kbn[i] else "", STYLE_MARK)
			sheet.print_area = PRINT_AREA.format(row+1)
			row += 1

	def save(self, filename):
		exportfile = fd.asksaveasfilename(
			title = "EXCEL保存",
			filetypes = FILE_TYPES,
			initialdir = INITIAL_DIR,
			initialfile = filename,
			defaultextension = DEFAULT_EXT
		)
		self.wb.save(exportfile)
