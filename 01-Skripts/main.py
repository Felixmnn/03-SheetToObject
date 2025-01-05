#Programm Ablauf:

# Nutzer wählt Seiten die Irrelevant sind
# 

from extractUsefulPages import PDFViewer
from extractPageSourceAndData import PDFSummarizer
from sendGPTSummaryRequest import createOpenAiRequest
 

import os
import re
import json

def checkIfProcessedDirExists(target_directory,root,save_directory):
    if(os.path.isdir(f"{target_directory}/{root}")):
        if (os.path.isdir(f"{save_directory}/{root}")):
            print(f"Directory {root} exists")
        else:
            print(f"Directory {root} does not exist")
            os.makedirs(f"{save_directory}/{root}")
            print("Created new Directory")
    

def checkIfFilteredPDFExists(file,currentDirectory,save_directory):
    if (os.path.isfile(f"{save_directory}/{currentDirectory}/{file}")):
        print("File exists")
        return True
    return False

def reduceAllPDFs(target_directory,save_directory):
    for root, dirs, files in os.walk(target_directory):
        if not dirs:
            currentDirectory = os.path.basename(root)
            checkIfProcessedDirExists(target_directory,currentDirectory,save_directory)
            for file in files:
                if checkIfFilteredPDFExists(file,currentDirectory,save_directory):
                    print(f"Die Datei {file} wurde bereits bearbeitet. Gehe zur nächsten Datei.")
                else:
                    try:
                        #Methode Ruft PDF auf speichert dieses Datei in einem neuen Ordner
                        PDFViewer(f"{target_directory}/{currentDirectory}/{file}",f"{save_directory}/{currentDirectory}/{file}")
                    except Exception as e:
                        print("Error",e)
                    else:
                        print("Successfully moved the folder.")
    print("All files have been processed.")



def transformAllPDFs(target_directory,save_directory):
    for root, dirs, files in os.walk(target_directory):
        if not dirs:
            currentDirectory = os.path.basename(root)
            for file in files:
                try:
                    PDFSummarizer(f"{target_directory}/{currentDirectory}/{file}",f"{save_directory}/{currentDirectory}.json",file)
                    
                except Exception as e:
                    print("Error",e)
                else:
                    print("Successfully moved the folder.")

def trasformStringToQuestions(target_directory,save_directory):
    for dateiname in os.listdir(target_directory):
        dateipfad = os.path.join(target_directory, dateiname)
        # Überprüfen, ob es sich um eine Datei handelt
        if os.path.isfile(dateipfad):
            try:
                print(f"Öffne Datei: {dateiname}")
                with open (dateipfad, 'r', encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    if "questions" in data and isinstance(data["questions"],list):
                        new_data = []

                        try:
                            for obj in data["questions"]:
                                if obj.get("verarbeitet",False) == False:
                                    api_response = "Ich bin die Antwort auf deine Frage"
                                    #Hier kommt dann eine Funktion die die API Response Verarbeitet
                                    response_obj = {"frage":"Frage","antworten":["antwort1","antwort2"],"correctAnswers":[0], "extractedText":obj.get("extractedText"),"extractedPage":obj.get("extractedPage"),"extractedSession":obj.get("extractedSession"),"extractedPro":obj.get("extractedPro"),"extractedLecture":obj.get("extractedLecture"),"ectractLectureName":obj.get("ectractLectureName")}
                                    new_data.append(response_obj)
                                    obj["verarbeitet"] = True
                                else:
                                    print("Diese Folie wurde bereits bearbeitet")

                        except Exception as e:
                            print(f"Fehler augetreten: {e}")
                        finally:
                            with open(dateipfad, 'w', encoding='utf-8') as file:
                                json.dump(data, file, ensure_ascii=False, indent=4)
                            print("Daten wurden gespeichert")
                            neuer_pfad = f"{save_directory}/{dateiname}"
                            if not os.path.isfile(neuer_pfad):
                                with open(neuer_pfad, 'w', encoding='utf-8') as json_file:
                                    json.dump(new_data, json_file, ensure_ascii=False, indent=4)
                            else:
                                with open(neuer_pfad, 'r', encoding='utf-8') as json_file:
                                    existing_data = json.load(json_file)
                                if isinstance(existing_data, list):
                                    existing_data.extend(new_data)
                                else:
                                    print("Fehler: Erwartet ein JSON-Array.")

                                # Schreibe die aktualisierten Daten zurück in die Datei
                                with open(neuer_pfad, 'w', encoding='utf-8') as json_file:
                                    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                                

                    else:
                        print("Die JSON Datei war im falschen Format")
            except Exception as e:
                print(f"Fehler beim bearbeiten von {dateipfad} , der Fehler ist {e}")
            

def main():
    #Step 1 -> löschen der irrelevanten Folien
    #target_directory = "../02-BasePDFs"
    #save_directory = "../03-FilteredData"
    #reduceAllPDFs(target_directory,save_directory)

    #Step 2 -> extrahieren des Textes aus relevanten Folien
    #target_directory = "../03-FilteredData"
    #save_directory = "../04-FolieToString"
    #transformAllPDFs(target_directory,save_directory)

    target_directory = "../04-FolieToString"
    save_directory = "../05-Antworten"
    trasformStringToQuestions(target_directory,save_directory)

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
