import tkinter as tk
from tkinter import ttk
from fileio.ExcelOutput import ExcelOutput
from utils.Validation import DynamicValidation as dval
from frames.PersonalDataFrame import PersonalDataFrame
from frames.SkillDataFrame import SkillDataFrame
from frames.CareerHistoryFrame import CareerHistoryFrame
from utils.Utilities import Utilities as util
from constants.message import DialogMessage as diag
class Application(tk.Frame):

	def __init__(self, master = None):
		super().__init__(master)
  
		#ウィンドウ設定
		self.master.title("K.S.A.M")
		self.master.geometry("1200x900")

		self.create_widgets()

	def sync_shain_num(self,event):
		var = self.frame_personal.data.shain_num.get()
		if dval.is_numeric(var,3):
			self.frame_skill.data.shain_num = var
			self.frame_history.data.shain_num = var
			print("[YUM!]Sync Shain Number complete!")
		else:
			print("[OUCH]Failed to sync Shain Number...")

	def create_widgets(self):
		#タイトル設定
		self.frame_title = tk.Frame(self.master,borderwidth=5,relief="groove")
		self.label_title = tk.Label(self.frame_title, text="Kushimsoft Skillsheet Automatic Maker", font=("Meiryo UI",20,"bold","italic"))
		self.label_title.pack(side=tk.TOP,padx=10,pady=10)
		self.frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=10)

		#Exportボタン
		self.frame_bottombutton = tk.Frame(self.master,borderwidth=5,relief="groove")
		self.button_export = ttk.Button(self.frame_bottombutton,width=15,text="Excel書出")
		self.button_export.pack(side=tk.RIGHT,padx=10,pady=5)
		self.frame_bottombutton.pack(side=tk.BOTTOM,fill=tk.X,padx=20,pady=10)

		self.frame_personal = PersonalDataFrame(self.master)
		self.frame_personal.pack()

		self.frame_skill = SkillDataFrame(self.master)
		self.frame_skill.pack()

		self.frame_history = CareerHistoryFrame(self.master)
		self.frame_history.pack()

		self.frame_personal.data.shain_num.trace('w',self.sync_shain_num)
		self.button_export["command"] = lambda: self.export_excel()

	# 社員番号更新イベント
	# argsのnameと内包StringVarの_nameが一致したらイベントを発生させる。
	def sync_shain_num(self, *args):
		tgt = self.frame_personal.data.shain_num
		if args[0] == tgt._name:
			var = tgt.get()
			if dval.is_numeric(var,3):
				self.frame_skill.data.shain_num = var
				self.frame_history.data.shain_num = var

	# EXCEL書き出し
	# 現在の登録内容でExcelファイルを書き出す。
	def export_excel(self):
		out = ExcelOutput()
		try:
			out.export(self.frame_personal.data, self.frame_skill.data, self.frame_history.data)
		except Exception as e:
			print(e)
			util.msgbox_showmsg(diag.DIALOG_INPUT_ERROR)
		finally:
			del out

if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(False,False)
	app = Application(master = root)
	app.mainloop()