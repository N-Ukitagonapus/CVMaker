from functools import partial
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import constants.const
from data_structure.SkillSheetDataStructure import SkillSheetDataStructure
from frames.PersonalDataFrame import PersonalDataFrame
from frames.SkillDataFrame import SkillDataFrame

class Application(tk.Frame):

	def __init__(self, master = None):
		super().__init__(master)

		self.data = SkillSheetDataStructure()
  
		#ウィンドウ設定
		self.master.title("スキルシート生成ソフト")
		self.master.geometry("1000x800")

		#タイトル設定
		self.frame_title = tk.Frame(self.master,width=600,borderwidth=5,relief="groove")
		self.label_title = tk.Label(self.frame_title, text="スキルシート生成ソフト", font=("ＭＳ　ゴシック",20,"bold","italic"))
		self.label_title.pack(side=tk.TOP, padx=10, pady=10)
		self.frame_title.pack(side=tk.TOP, pady=10, fill=tk.X, padx=20)

		self.frame_personal = PersonalDataFrame(self.master)
		self.frame_personal.pack()
		self.frame_personal.btn_load["command"] = lambda: msg.showinfo("Message", "Load Button Has been pushed.")
		self.frame_personal.btn_save["command"] = lambda: msg.showinfo("Message", "Save Button Has been pushed.")

		self.frame_skill = SkillDataFrame(self.master)
		self.frame_skill.pack()

if __name__ == "__main__":
	root = tk.Tk()
	root.resizable(False,False)
	app = Application(master = root)
	app.mainloop()