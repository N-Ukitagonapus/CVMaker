class _consttype:
	class _ConstTypeError(TypeError):
		pass
	def __setattr__(self, name, value):
		v = self.__dict__.get(name, value)
		if type(v) is not type(value):
			raise self._ConstTypeError(f"Can't rebind {type(v)} to {type(value)}")
		self.__dict__[name] = value
	def __del__(self):
		self.__dict__.clear()

import sys
sys.modules[__name__] = _consttype()

import const
const.POSITIONS = {
  "TE":"テスター",
	"PG":"プログラマ",
	"SE":"システムエンジニア",
	"TL":"チームリーダー",
	"PL":"プロジェクトリーダー",
	"PM":"プロジェクトマネージャ",
	"ETC":"その他"
}

const.TASKS = [
  "企画",
	"要件定義",
	"方式設計",
	"基本設計",
	"詳細設計",
	"プログラム設計",
	"製造",
	"単体テスト",
	"結合テスト",
	"システムテスト",
	"運用テスト",
	"システム移行",
	"運用・保守",
	"その他"
]