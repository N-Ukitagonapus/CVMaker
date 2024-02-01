import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class ValiantWarningSubFrame:
	@staticmethod
	def warn(target, result):
		def create_text(input:dict)->list:
			ret = []
			for key in input.keys():
				ret.append("【{0}】".format(key))
				ret += input[key]
			return ret
		dlg = tk.Toplevel(target)
		dlg.title("表記ゆれ警告")   # ウィンドウタイトル
		dlg.geometry("320x240")        # ウィンドウサイズ(幅x高さ)
		frame_title = tk.Frame(dlg,borderwidth=5,relief="groove")
		label_title = tk.Label(frame_title, text="表記ゆれ警告", font=("Meiryo UI",14,"bold"))
		label_title.pack(side=tk.TOP,padx=10,pady=5)
		frame_title.pack(side=tk.TOP,fill=tk.X,padx=20,pady=5)

		text_result=ScrolledText(dlg,wrap=tk.WORD)
		text_result.pack(side=tk.TOP,expand=True,padx=10,pady=5)
		text_result.insert('1.0',"\n".join(create_text(result)))
		text_result["state"]=tk.DISABLED