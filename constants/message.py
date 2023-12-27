
class Message:
	"""
  メッセージ定数クラス
	"""
	MSG_OK = "OK."
	MSG_NOVALIDATION = "－"
	MSG_ERR_EMPTY = "NG：未入力です。"
	MSG_INVALID = "NG：{0}で入力してください。"
	MSG_DAY_AFTER = "NG：本日より未来の日付は入力できません。"
	MSG_DATEFORMAT_FAILURE = "NG：日付変換に失敗しました。"
	MSG_WARN_EMPTY = "WARN：未入力です。"
	MSG_WARN_LENGTH = "WARN：最大文字数({0}文字)を超えている部位は切り取られます。"

class DialogMessage:
	"""
	ダイアログ定数クラス
	"""
	DIALOG_TEST = ("info","TEST","【メッセージ未実装】\nこれはテストメッセージです。")
	DIALOG_EDIT_ERROR = ("error","編集中にエラー発生","編集中にエラーが発生しました。\n詳細はコンソールログを参照してください。")
	DIALOG_OUTPUT_ERROR = ("error","出力失敗","ファイル出力に失敗しました。\n詳細はコンソールログを参照してください。")
	DIALOG_INPUT_ERROR = ("error","読込失敗","ファイル読込に失敗しました。\n詳細はコンソールログを参照してください。")
	DIALOG_CANT_DELETE = ("error","もう消せませんよ","これ以上経歴データ削除が出来ません。")
	DIALOG_UNSELECT_ERROR = ("error","未選択項目あり","未選択の項目があります。\n確認してください。")
	DIALOG_ASK_FORCE_OUTPUT = ("yesno","強制出力","入力項目にエラーもしくは警告がありますが、強制的に出力してもよろしいですか？")
	DIALOG_ASK_EDIT_PERSONALDATA = ("yesno","個人基本情報再編集","本当に全項目を再編集しますか？")
	DIALOG_ASK_DELETE_CAREERDATA = ("yesno", "経歴データ削除","この経歴データを削除してしまってもよろしいですか？")
	DIALOG_SUCCESS_READ_CAREERDATA = ("info", "職務経歴情報読込成功","職務経歴情報を読み込みました。")
	DIALOG_SUCCESS_OUTPUT_EXCEL = ("info", "EXCELエクスポート","EXCELファイルを書き出しました。\n※指摘事項が残っている場合は手動で修正してください。")
	DIALOG_ERROR_NO_PERSONAL_DATA = ("error", "個人基本情報未読込","個人基本情報の読込を行ってください。")
	DIALOG_WARN_KEYINVALID = ("yesno", "キー不一致","読込ファイル内のキーが個人基本情報と一致していません。\nそれでも読み込みますか？")
	DIALOG_ERROR_KEYINVALID = ("error", "キー不一致","読込ファイル内のキーが個人基本情報と一致していないため、読み込みできません。")