import json
import os



class JSONConverter():
    def __init__(self,json_path,json_object):
        self.insertJSONObject(json_path,json_object)
        pass

    def createJSONObject (self):
        pass

    def initializeJSON(self,json_path, json_object):
        if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump({}, json_file)

    def insertJSONObject (self,json_path,json_object):
        self.initializeJSON(json_path,json_object)
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
        

json_object = {"question":"Welche der folgenden Ämter werden durch den Bundestag gewählt?","answers":["Bundeskanzler","Präsident des Bundesrechnungshofs","Hälfte der Bundesverfassungsrichter","Bundespräsident"],"correctAnswers":[0,1,2],"themengebiet":"Legislative","vorlesung":"Einführungsvorlesung Das Politische System Deutschlands","offizielleKlausurfrage":False,"erstellDatum":"02.01.2025","autor":"felix","prof":"name","quelleDokument":"Sitzung_4_Legislative","quelleDokumentSeite":10}
JSONConverter("../PolitischeSystemDeutschland.json",json_object)