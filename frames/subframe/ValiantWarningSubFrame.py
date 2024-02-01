import tkinter as tk

class ValiantWarningSubFrame:
  @staticmethod
  def warn(target, result):
        dlg_modeless = tk.Toplevel(target)
        dlg_modeless.title("表記ゆれ警告")   # ウィンドウタイトル
        dlg_modeless.geometry("300x240")        # ウィンドウサイズ(幅x高さ)
