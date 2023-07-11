'''
開発規模
'''
class ScaleData:
	def __init__(self):
		## 設計
		self.des_base = 0				#基本設計
		self.des_detail = 0			#詳細設計
		## 製造
		self.gamens = 0					#画面数
		self.batches = 0				#バッチ数
		self.forms = 0					#帳票数
		self.etc1_name = ""			#その他1：名称
		self.etc1_num = 0				#その他1：数
		self.etc2_name = ""			#その他2：名称
		self.etc2_num = 0				#その他2：数
		self.total_steps = 0		#総ステップ
		## テスト
		self.uts = 0						#単体テスト
		self.its = 0						#結合テスト
		self.sts = 0						#総合テスト