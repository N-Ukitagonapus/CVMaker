'''
開発環境データ
'''
import copy
from constants.const import ENV_SET
from utils.Utilities import Utilities as util
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
		ret = copy.deepcopy(ENV_SET)
		ret["srv"] = self.server
		ret["os"] = self.os
		ret["db"] = self.db
		ret["lang"] = self.lang
		ret["fw"] = self.fw
		ret["mw"] = self.mw
		ret["tools"] = self.tools
		ret["pkg"] = self.pkg
		return ret
  
	def extend(self, input):
		self.server.extend(input.server)
		self.server = util.tidy_list(self.server)
		self.os.extend(input.os)
		self.os = util.tidy_list(self.os)
		self.db.extend(input.db)
		self.db = util.tidy_list(self.db)
		self.lang.extend(input.lang)
		self.lang = util.tidy_list(self.lang)
		self.fw.extend(input.fw)
		self.fw = util.tidy_list(self.fw)
		self.mw.extend(input.mw)
		self.mw = util.tidy_list(self.mw)
		self.tools.extend(input.tools)
		self.tools = util.tidy_list(self.tools)
		self.pkg.extend(input.pkg)
		self.pkg = util.tidy_list(self.pkg)
		