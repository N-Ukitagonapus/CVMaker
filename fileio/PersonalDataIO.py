from data_structure.PersonalData import PersonalData
from tkinter import filedialog as fd
import xml.etree.ElementTree as et
import xml.dom.minidom as md

class PersonalDataOutput():
	def __init__(self,data:PersonalData):
		self.data = data
		self.filename = fd.asksaveasfilename(
			title = "個人基本情報保存",
			filetypes = [("XMLファイル", ".xml")],
			initialdir = "./",
			defaultextension = "xml"
    )

	def output(self):
		base = et.Element("PersonalData")
		tree = et.ElementTree(element=base)

		if self.data.shain_num.get() != "":
			et.SubElement(base,"shain_num").text = self.data.shain_num.get()
		if self.data.name_last_kanji.get() != "":
			et.SubElement(base,"last_name_kanji").text = self.data.name_last_kanji.get()
		if self.data.name_first_kanji.get() != "":
			et.SubElement(base,"first_name_kanji").text = self.data.name_first_kanji.get()
		if self.data.name_last_romaji.get() != "":
			et.SubElement(base,"last_name_romaji").text = self.data.name_last_romaji.get()
		if self.data.name_first_romaji.get() != "":
			et.SubElement(base,"first_name_romaji").text = self.data.name_first_romaji.get()
		if self.data.gender.get() != "":
			et.SubElement(base,"gender").text = self.data.gender.get()
		et.SubElement(base,"birthday").text = self.data.birthday.strftime("%Y%m%d")
		if self.data.current_address.get() != "":
			et.SubElement(base,"current_address").text = self.data.current_address.get()
		if self.data.nearest_station.get() != "":
			et.SubElement(base,"nearest_station").text = self.data.nearest_station.get()
		if self.data.gakureki.get() != "":
			et.SubElement(base,"gakureki").text = self.data.gakureki.get()
		et.indent(tree,"\t")

		tree.write(self.filename, encoding="utf-8", xml_declaration=True)