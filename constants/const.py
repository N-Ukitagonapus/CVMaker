# 環境編集_内容セット
ENV_SET = {
  "srv": [] #サーバ
	,"os" : [] #OS
	,"db" : [] #DB
	,"lang" : [] #言語
	,"fw" : [] #フレームワーク
	,"mw" : [] #ミドルウェア
	,"tools" : [] #ツール
	,"pkg":[]#パッケージ
} 

# 環境編集_タイトル
ENV_GENRE = {
	"srv":"ｻｰﾊﾞ\n※ｸﾗｳﾄﾞ環境時のみ",
	"os":"OS",
	"db":"DB",
	"lang":"言語",
	"fw":"ﾌﾚｰﾑﾜｰｸ",
	"mw":"ﾐﾄﾞﾙｳｪｱ",
	"tools":"ﾂｰﾙ",
	"pkg":"ﾊﾟｯｹｰｼﾞ"
}

# 職位
POSITIONS = {
  "テスター":"TE",
	"プログラマ":"PG",
	"システムエンジニア":"SE",
	"チームリーダー":"TL",
	"プロジェクトリーダー":"PL",
	"プロジェクトマネージャ":"PM",
	"その他":"ETC"
}

# 作業内容
TASKS = {
  "SP":"企画",
	"RD":"要件定義",
	"AD":"方式設計",
	"BD":"基本設計",
	"DD":"詳細設計",
	"PD":"プログラム設計",
	"PG":"製造",
	"UT":"単体テスト",
	"IT":"結合テスト",
	"ST":"システムテスト",
	"OT/UAT":"運用テスト/受入テスト",
	"MG":"システム移行",
	"OP/MA":"運用・保守",
	"SU":"サポート",
	"ETC":"その他"
}

TASKS_MERGE = {
	"RD" :["SP", "RD"],	#要件
	"BD" :["AD", "BD"],	#基本
	"DD" :["DD", "PD"],	#詳細
	"PG" :["PG"],	#実装
	"UT" :["UT"],	#UT
 	"IT" :["IT"],	#IT
  "ST" :["ST","OT/UAT"],	#ST
	"OP" :["MG","OP/MA"],	#運用
	"SU" :["SU"],	#サポート
	"ETC":["ETC"]	#その他
}

# チェック結果
VALID_OK = "OK"
VALID_WARN = "WARN"
VALID_ERR = "ERROR"

# チェック結果_表示背景
COLOR = {
	VALID_OK:"white",
	VALID_WARN:"#ffd700",
	VALID_ERR:"#ff6347"
}