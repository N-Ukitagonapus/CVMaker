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

icon = '''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
				7xc+9j5yn+M+4zw33jLeWV/MN8C3yLfLT8Nvnl+F30N/I/9k/3r/0QCngCUBZwOJ
				gUGBWwL7+Hp8Ib+OPzrbZfay2e1BjKC5QRVBj4KtguXBrSFoyOyQrSH355jOkc5p
				DoVQfujW0Adh5mGLw34MJ4WHhVeGP45wiFga0TGXNXfR3ENz30T6RJZE3ptnMU85
				ry1KNSo+qi5qPNo3ujS6P8YuZlnM1VidWElsSxw5LiquNm5svt/87fOH4p3iC+N7
				F5gvyF1weaHOwvSFpxapLhIsOpZATIhOOJTwQRAqqBaMJfITdyWOCnnCHcJnIi/R
				NtGI2ENcKh5O8kgqTXqS7JG8NXkkxTOlLOW5hCepkLxMDUzdmzqeFpp2IG0yPTq9
				MYOSkZBxQqohTZO2Z+pn5mZ2y6xlhbL+xW6Lty8elQfJa7OQrAVZLQq2QqboVFoo
				1yoHsmdlV2a/zYnKOZarnivN7cyzytuQN5zvn//tEsIS4ZK2pYZLVy0dWOa9rGo5
				sjxxedsK4xUFK4ZWBqw8uIq2Km3VT6vtV5eufr0mek1rgV7ByoLBtQFr6wtVCuWF
				fevc1+1dT1gvWd+1YfqGnRs+FYmKrhTbF5cVf9go3HjlG4dvyr+Z3JS0qavEuWTP
				ZtJm6ebeLZ5bDpaql+aXDm4N2dq0Dd9WtO319kXbL5fNKNu7g7ZDuaO/PLi8ZafJ
				zs07P1SkVPRU+lQ27tLdtWHX+G7R7ht7vPY07NXbW7z3/T7JvttVAVVN1WbVZftJ
				+7P3P66Jqun4lvttXa1ObXHtxwPSA/0HIw6217nU1R3SPVRSj9Yr60cOxx++/p3v
				dy0NNg1VjZzG4iNwRHnk6fcJ3/ceDTradox7rOEH0x92HWcdL2pCmvKaRptTmvtb
				Ylu6T8w+0dbq3nr8R9sfD5w0PFl5SvNUyWna6YLTk2fyz4ydlZ19fi753GDborZ7
				52PO32oPb++6EHTh0kX/i+c7vDvOXPK4dPKy2+UTV7hXmq86X23qdOo8/pPTT8e7
				nLuarrlca7nuer21e2b36RueN87d9L158Rb/1tWeOT3dvfN6b/fF9/XfFt1+cif9
				zsu72Xcn7q28T7xf9EDtQdlD3YfVP1v+3Njv3H9qwHeg89HcR/cGhYPP/pH1jw9D
				BY+Zj8uGDYbrnjg+OTniP3L96fynQ89kzyaeF/6i/suuFxYvfvjV69fO0ZjRoZfy
				l5O/bXyl/erA6xmv28bCxh6+yXgzMV70VvvtwXfcdx3vo98PT+R8IH8o/2j5sfVT
				0Kf7kxmTk/8EA5jz/GMzLdsAAAAgY0hSTQAAeiUAAICDAAD5/wAAgOkAAHUwAADq
				YAAAOpgAABdvkl/FRgAAAwBQTFRFAAAA/DEx+1RU/g8P8+PjX8rx9p6e9cHBALHw
				dtDxKrzx+Hx8gNOmC7Pwntu6ALBQHrhkQcLxIrnw/8AA+mNjveTP2+zj/R4ePcF5
				W8mNedGh/EFBl9m1teHJF7ZfBLHwNb5z2+zy1Ore8vLyVMeIcs+c9NDQveTyALDw
				ntvxALDw1Ory9q6uteHx+IyM+XJygNPx+1BQAL//l9nx/M08/gsL/S4uedHx9b29
				W8nx95ubcs/xfNKjPcHxHrjwVMfxG7hiOcB2Nb7wV8iKk9iyseDG/hsbE7VdMb1x
				ALDw8u7uF7bw0Onb7vHv7vHy9MzMUMaGbs6aqt7CyObWZsuU9qqq0Ony+IiI5+/r
				+W5useDx5+/y+0xMyObxfNLx/Soqk9jx/wgIqt7y89vb9bm595eXV8jwbs7x+ltb
				AK1RAK7xOcDx+dZq/Dk5ZsvwUMbx/hcXMb3wj9ewD7Ra8urqAK/vG7jx9MjIruDF
				zOjZ6vDtE7XwLr1vTMWDas2XALBQ6vDyiNWrALLypt2/9qamxOXTCLJVJrppRMJ9
				+Wpq+ISE4+7ozOjy+0hIY8uS4+7yxOXx/SYmruDy+NyI/wQEj9fxALDw89fXpt3x
				9bW1iNXx95OT+ldXas3x/hMTALDwTMXxC7NXY8vx9MTERMLw8+fnjNeuLr3x9qKi
				KrxsSMSAD7TwhNSooty8BLFT+WZmIrlnJrrw+0REweXR3+3lQcJ8X8qQ/SIiueLM
				ALDw1+rgCLLw3+3y/wAA1+rxdtCfweXyotzx9NTUjNfyueLxhNTx+XZ2ALDwm9ry
				ycnJysrKy8vLzMzMzc3Nzs7Oz8/P0NDQ0dHR0tLS09PT1NTU1dXV1tbW19fX2NjY
				2dnZ2tra29vb3Nzc3d3d3t7e39/f4ODg4eHh4uLi4+Pj5OTk5eXl5ubm5+fn6Ojo
				6enp6urq6+vr7Ozs7e3t7u7u7+/v8PDw8fHx8vLy8/Pz9PT09fX19vb29/f3+Pj4
				+fn5+vr6+/v7/Pz8/f39/v7+////B8I1VAAAAAF0Uk5TAEDm2GYAAAC6SURBVHja
				bJCxDcIwEEWfHQZAEWIBJEv0zJQeKSUjMEF2yRoUNwKyhEVBB6JwYp8dX3W65//9
				78wMMN4BGHCkMnPuCyBWA1WC1eCoQCYD8NQqW1hJlii3OBIBcIpMK4vxnMuaBR3S
				i+x2BaDfJIDzlLwqApfGDWLmIW36FsGcYu8BdvusCeU+QXVWSRQKawJfqcL2OnEY
				UmpfopD2+dKKYYEXcKtd6fro9fjUn9rqxJp42tX9FsnG7T8A/iYsvwu//BkAAAAA
				SUVORK5CYII=
			'''