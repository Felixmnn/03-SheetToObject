#This script extracts the source of the information from the usefulpages and prepare the data for further processing
#Data gets save ind the GPTPreparedData folder

import fitz  # PyMuPDF
from tkinter import Tk, Canvas, Button
from PIL import Image, ImageTk
import re
import json
import os

class PDFSummarizer:
    def __init__(self,pdf_path,save_data_path,file):
        pdf_path = pdf_path
        pdf_document = fitz.open(pdf_path)
        for i in range(1, len(pdf_document)):
            text = self.extract_text_from_page( i, pdf_document)
            object = self.format_text(text,pdf_path,file)
            self.save_Output(object,save_data_path)
        pdf_document.close()

    def extract_text_from_page(self, page_number, pdf_document):
        
        # Überprüfen, ob die angegebene Seite existiert
        if page_number < 0 or page_number >= len(pdf_document):
            print("Ungültige Seitenzahl.")
            return None            
        # Entsprechende Seite laden
        page = pdf_document.load_page(page_number)
        
        # Text von der Seite extrahieren
        text = page.get_text()
                
        return text
    
    def format_text(self,text,pdf_path,file):
        # Zeilenumbrüche entfernen
        seite = re.search(r"Seite[^\n]*", text)
        seite = seite.group(0)

        sitzung = re.search(r"Sitzung[^\n]*", text)
        sitzung = sitzung.group(0)

        prof = re.search(r"Prof[^\n]*", text)
        prof = prof.group(0)

        text = text.replace(seite,"")
        text = text.replace(prof,"")
        text = text.replace(sitzung,"")

        lectureName = pdf_path.replace(".json","")

        object = {"extractedText":f"{text}","extractedPage":f"{seite}","extractedSession":f"{sitzung}","extractedProf":f"{prof}","extractedLecture":f"{lectureName}","ectractLectureName":f"{file}","verarbeitet":False}
        return object
    #Auzugebender Text: { Text: text; Seite: seite; Sitzung: sitzung; Prof: prof}    

    def insertJSONObject (self,json_path,json_object):
        try:
            with open (json_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}
        new_question = json_object
        if "questions" in data:
            data["questions"].append(new_question)
        else:
            data["questions"] = [new_question]
        with open(json_path,"w",encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print("Der Eintrag wurde erfolgreich gespeichert")
        

    def save_Output(self,object,save_text_path):
        if not os.path.exists(save_text_path):
            with open (save_text_path, "w", encoding="utf-8") as json_file:
                json.dump({}, json_file, ensure_ascii=False, indent=4)
            self.insertJSONObject(save_text_path,object)
        else:
            self.insertJSONObject(save_text_path,object)

            