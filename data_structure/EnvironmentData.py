'''
開発環境データ
'''
from constants.const import ENV_SET


class EnvironmentData:
  #コンストラクタ(のようなもの)
	def __init__(self):
		self.server =[] #使用経験(業務外)・サーバ
		self.os = [] #使用経験(業務外)・OS
		self.db = [] #使用経験(業務外)・DB
		self.lang = [] #使用経験(業務外)・言語
		self.fw = [] #使用経験(業務外)・フレームワーク
		self.mw = [] #使用経験(業務外)・ミドルウェア
		self.tools = [] #使用経験(業務外)・ツール
		self.pkg =[] #使用経験(業務外)・パッケージ

	def set_values(self, entry:dict):
		self.server = entry["srv"]
		self.os = entry["os"]
		self.db = entry["db"]
		self.lang = entry["lang"]
		self.fw = entry["fw"]
		self.mw = entry["mw"]
		self.tools = entry["tools"]
		self.pkg = entry["pkg"]

	def get_values(self):
		ret = ENV_SET
		ret["srv"] = self.server
		ret["os"] = self.os
		ret["db"] = self.db
		ret["lang"] = self.lang
		ret["fw"] = self.fw
		ret["mw"] = self.mw
		ret["tools"] = self.tools
		ret["pkg"] = self.pkg
		return ret
   