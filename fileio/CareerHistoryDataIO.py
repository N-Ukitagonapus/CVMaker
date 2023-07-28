from constants.const import ENV_SET, TASKS
from data_structure.EnvironmentData import EnvironmentData
from data_structure.CareerHistoryData import CareerHistoryData
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, filedialog as fd
import datetime
import xml.etree.ElementTree as et
import xml.dom.minidom as md

FILE_TYPES = [("XMLファイル", ".xml")]
INITIAL_DIR = "./"
DEFAULT_EXT = "xml"
BORDER = "-------------------------------------------------"

class CareerHistoryOutValidation():

  # 初期化
	def __init__(self):
		self.result_txt = []
		self.has_pointout = False
	# データチェック
	def validation(self,input:CareerHistoryData):
		result = []
		err_total,warn_total = 0, 0
		i = 1
		# 経歴データごとに参照。
		for data in input.history_list:
			err, warn = 0, 0
			result.append("【経歴データ：{0}】".format(i))
			# 業務開始日が今日より未来の場合はエラー
			if data.term_start > datetime.date.today():
				result.append("[エラー]業務開始日に未来日付は入力できません。")
				err += 1
			# 業務開始日 ＜ 業務終了日の場合はエラー
			if data.term_start > data.term_end:
				result.append("[エラー]業務開始日に業務終了日以降の日付は入力できません。")
				err += 1
			# 業界、プロジェクト概要、システム概要は入力推奨(未入力の場合は警告)
			if str.strip(data.description_gyokai) == "":
				result.append("[警告]業界が未入力です。")
				warn += 1
			if str.strip(data.description_project_overview) == "":
				result.append("[警告]プロジェクト概要が未入力です。")
				warn += 1
			if str.strip(data.description_project_overview) == "":
				result.append("[警告]システム概要が未入力です。")
				warn += 1
			# 作業内容「その他」にチェックがついているのに未入力の場合はエラー
			if TASKS["ETC"] in data.tasks and str.strip(data.tasks_etc) == "":
				result.append("[エラー]作業内容の「その他」を入力してください。")
				err += 1
			# 職位が「その他」で未入力の場合はエラー
			if data.position == "その他" and str.strip(data.position_etc) == "":
				result.append("[エラー]職位が「その他」の場合は職位名を入力してください。")
				err += 1
			# 総メンバー数　＜　自社メンバー数の場合はエラー。
			if data.members < data.members_internal:
				result.append("[エラー]自社メンバー数が総メンバー数よりも多いです。確認してください。")
				err += 1
			#エラー総数
			if err == 0 and warn == 0:
				result.append("指摘なし")
			else:
				result.append("エラー：{0}　警告：{1}".format(err if err > 0 else "なし", warn if warn > 0 else "なし"))
			err_total += err
			warn_total += warn 
			i += 1
			result.append(BORDER)
		# 指摘総数出力
		result.append("【指摘総数】")
		if err_total == 0 and warn_total == 0:
			result.append("指摘なし")
		else:
			result.append("エラー：{0}　警告：{1}".format(err_total if err_total > 0 else "なし", warn_total if warn_total > 0 else "なし"))
		self.result_txt = result
		self.has_pointout = err_total > 0 or warn_total > 0

	#入力チェック画面
	def check_input(self,target:tk.LabelFrame,input:CareerHistoryData):
		self.validation(input)
		subwindow = tk.Toplevel(target)
		subwindow.title("開発規模編集")
		subwindow.geometry("640x480")
		subwindow.resizable(False,False)
		subwindow.grab_set()
		frame_title = tk.Frame(subwindow,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="開発規模編集", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
		btn_ok = ttk.Button(btn_frame,text="OK")
		btn_cancel = ttk.Button(btn_frame,text="キャンセル")
		btn_ok.pack(side=tk.LEFT,padx=10,pady=5)
		btn_cancel.pack(side=tk.RIGHT,padx=10,pady=5)
		btn_frame.pack(side=tk.BOTTOM,padx=20,pady=5)

		text_result=ScrolledText(subwindow,wrap=tk.WORD)
		text_result.pack(side=tk.TOP,expand=True,padx=10,pady=5)
		text_result.insert('1.0',"\n".join(self.result_txt))
		text_result["state"]=tk.DISABLED
		btn_frame = tk.Frame(subwindow,borderwidth=2,relief="groove")
	
		btn_ok["command"] = lambda: output(input)
		btn_cancel["command"] = lambda: cancel()

		def output(input:CareerHistoryData):
			subwindow.destroy()
			del self
		def cancel():
			subwindow.destroy()
			del self
    
class CareerHistoryDataOutput():

	def __init__(self,data:CareerHistoryData):
		self.data = data
		self.filename = fd.asksaveasfilename(
			title = "職務経歴データ保存",
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
   
		tree.write(self.filename, encoding="utf-8", xml_declaration=True)