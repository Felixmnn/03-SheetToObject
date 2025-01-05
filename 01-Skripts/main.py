#Programm Ablauf:

# Nutzer wählt Seiten die Irrelevant sind
# 

from extractUsefulPages import PDFViewer
from extractPageSourceAndData import PDFSummarizer
from sendGPTSummaryRequest import createOpenAiRequest
 

import os
import re

def checkIfProcessedDirExists(root):
    if(os.path.isdir(f"../02-BasePDFs/{root}")):
        if (os.path.isdir(f"../03-FilteredData/{root}")):
            print(f"Directory {root} exists")
        else:
            print(f"Directory {root} does not exist")
            os.makedirs(f"../03-FilteredData/{root}")
            print("Created new Directory")
    

def checkIfFilteredPDFExists(file,currentDirectory):
    if (os.path.isfile(f"../03-FilteredData/{currentDirectory}/{file}")):
        print("File exists")
        return True
    return False

def reduceAllPDFs(target_directory):
    for root, dirs, files in os.walk(target_directory):
        if not dirs:
            currentDirectory = os.path.basename(root)
            checkIfProcessedDirExists(currentDirectory)
            for file in files:
                if checkIfFilteredPDFExists(file,currentDirectory):
                    print(f"Die Datei {file} wurde bereits bearbeitet. Gehe zur nächsten Datei.")
                else:
                    try:
                        #Methode Ruft PDF auf speichert dieses Datei in einem neuen Ordner
                        PDFViewer(f"../02-BasePDFs/{currentDirectory}/{file}",f"../03-FilteredData/{currentDirectory}/{file}")
                    except Exception as e:
                        print("Error",e)
                    else:
                        print("Successfully moved the folder.")
    print("All files have been processed.")



def transformAllPDFs(target_directory):
    for root, dirs, files in os.walk(target_directory):
        if not dirs:
            currentDirectory = os.path.basename(root)
            for file in files:
                try:
                    PDFSummarizer(f"{target_directory}/{currentDirectory}/{file}",f"../04-FolieToString/{currentDirectory}.txt")
                    
                except Exception as e:
                    print("Error",e)
                else:
                    print("Successfully moved the folder.")

def zeileFormatieren(zeile):
    pass   

def trasformStringToQuestions(target_directory):
    for dateiname in os.listdir(target_directory):
        dateipfad = os.path.join(target_directory, dateiname)
        # Überprüfen, ob es sich um eine Datei handelt
        if os.path.isfile(dateipfad):
            try:
                print(f"Öffne Datei: {dateiname}")

                with open(dateipfad, "r+") as datei:
                    for zeile in datei:
                        if "BEARBEITET" not in zeile:
                            print("Übergebe Zeile")
                            original_zeile = zeile.strip()
                            info_match = re.search(r"Text:\s*(.*?);", original_zeile)
                            
                            if info_match:
                                info = info_match.group(1)
                                # API-Request oder Verarbeitung
                                questions = createOpenAiRequest(f"Erstelle 3 singlechoice und 3 multiplechoice antworten auf basis dieser Daten wenn es sinn ergibt{info}")  # Annahme: Funktion existiert
                                print("Wieso kommt er hier nicht an?")
                                # Neue Zeile erstellen
                                neue_zeile = original_zeile.replace(info, questions).strip() + " BEARBEITET\n"

                                # In Antwortendatei speichern
                                antwort_dateipfad = os.path.join("../05-Antworten/", "antworten.txt")
                                with open(antwort_dateipfad, "a", encoding="utf-8") as antwort_datei:
                                    antwort_datei.write(f"{neue_zeile}\n")

                                # Geänderte Zeile in die Datei schreiben
                                datei.write(neue_zeile)
                            else:
                                print("Kein gültiges Muster gefunden.")
                                datei.write(original_zeile + "\n")
                        else:
                            print("Zeile wurde bereits erfolgreich bearbeitet.")
            except Exception as e:
                print(f"Fehler beim Öffnen von {dateiname}: {e}")
            finally:print("Datei wurde abgeschlossen.")

    pass

def main():
    #target_directory = "../02-BasePDFs"
    #reduceAllPDFs(target_directory)
    #target_directory = "../03-FilteredData"
    #transformAllPDFs(target_directory)
    target_directory = "../04-FolieToString"
    trasformStringToQuestions(target_directory)

    """
    original_pdf = "../02-BasePDFs/Einführungsvorlesung Das Politische System Deutschlands/Sitzung_4_Legislative.pdf"
    filered_pdf = "../03-FilteredData/Einführungsvorlesung Das Politische System Deutschlands/gefiltert_Sitzung_2_Verfassungssystem.pdf"
    save_text_path = '../04-GPTPreparedData/output.txt'
    #ermöglicht es dem Nutzer folien zu entfernen zu denen er keine Fragen stellen möchte
    PDFViewer(original_pdf,filered_pdf)
    original_pdf = "../02-BasePDFs/Einführungsvorlesung Das Politische System Deutschlands/Sitzung_4_Legislative.pdf"
    filered_pdf = "../03-FilteredData/Einführungsvorlesung Das Politische System Deutschlands/gefiltert_Sitzung_2_Verfassungssystem.pdf"
    save_text_path = '../04-GPTPreparedData/output.txt'
    #ermöglicht es dem Nutzer folien zu entfernen zu denen er keine Fragen stellen möchte
    PDFViewer(original_pdf,filered_pdf)
    #Speichert die PDF in einem Txt dokumen als Objekt
    PDFSummarizer(original_pdf,25,save_text_path)
    #Nutzt die GPT API um Fragen zu generieren
    antwort = FolieToQuizQuestions("Welcher ist der Beste Film?")
    """


main()
