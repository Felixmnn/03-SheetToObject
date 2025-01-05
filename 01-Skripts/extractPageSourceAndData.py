#This script extracts the source of the information from the usefulpages and prepare the data for further processing
#Data gets save ind the GPTPreparedData folder

import fitz  # PyMuPDF
from tkinter import Tk, Canvas, Button
from PIL import Image, ImageTk
import re

class PDFSummarizer:
    def __init__(self,pdf_path,save_data_path):
        pdf_path = pdf_path
        pdf_document = fitz.open(pdf_path)
        for i in range(1, len(pdf_document)):
            text = self.extract_text_from_page( i, pdf_document)
            text = self.format_text(text)
            self.save_Output(text,save_data_path)
        pdf_document.close()

    def extract_text_from_page(self, page_number, pdf_document):
        # PDF-Dokument öffnen
        
        # Überprüfen, ob die angegebene Seite existiert
        if page_number < 0 or page_number >= len(pdf_document):
            print("Ungültige Seitenzahl.")
            return None            
        # Entsprechende Seite laden
        page = pdf_document.load_page(page_number)
        
        # Text von der Seite extrahieren
        text = page.get_text()
                
        return text
    
    def format_text(self,text):
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

        text = {f"Text: {text}; Seite: {seite}; Sitzung: {sitzung}; Prof: {prof}"}  
        return text
    #Auzugebender Text: { Text: text; Seite: seite; Sitzung: sitzung; Prof: prof}    

    
    def save_Output(self,text,save_text_path):
        with open(save_text_path,'a',encoding='utf-8') as file:
            file.write(f"{text}\n")
            