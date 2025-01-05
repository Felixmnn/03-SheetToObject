
import fitz  # PyMuPDF
from tkinter import Tk, Canvas, Button
from PIL import Image, ImageTk

class PDFViewer:
    def __init__(self, pdf_path, save_path):
        self.pdf_document = fitz.open(pdf_path)
        self.current_page = 0
        self.pdf_path = pdf_path
        self.save_path = save_path  # Neuer Speicherpfad

        # Tkinter-Fenster erstellen
        self.window = Tk()
        self.window.title("PDF Viewer")
        self.canvas = None
        self.image_tk = None

        # Buttons hinzufügen
        self.button_frame = Canvas(self.window, height=50)
        self.button_frame.pack()

        self.green_button = Button(self.button_frame, text="Grün (Nächste Seite)", bg="green", fg="white", width=20, height=2, command=self.next_page)
        self.green_button.pack(side="left", padx=20, pady=5)

        self.red_button = Button(self.button_frame, text="Rot (Seite löschen)", bg="red", fg="white", width=20, height=2, command=self.delete_page)
        self.red_button.pack(side="right", padx=20, pady=5)
        
        self.exit_button = Button(self.button_frame, text="Beenden", bg="blue", fg="white", width=20, height=2, command=self.close_application)
        self.exit_button.pack(side="left", padx=20, pady=5)

        self.load_page()
        self.window.mainloop()

    def close_application(self):
        # Geänderte PDF speichern, bevor das Programm geschlossen wird
        self.save_pdf()
        self.window.destroy()

    def load_page(self):
        # PDF-Seite rendern und anzeigen
        if self.canvas:
            self.canvas.destroy()  # Alte Canvas entfernen
        page = self.pdf_document.load_page(self.current_page)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        self.canvas = Canvas(self.window, width=pix.width, height=pix.height)
        self.canvas.pack()
        self.image_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

    def next_page(self):
        if self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.load_page()
        else:
            print("Du bist auf der letzten Seite.")

    def delete_page(self):
        if len(self.pdf_document) > 1:
            # Seite löschen
            self.pdf_document.delete_page(self.current_page)
            print(f"Seite {self.current_page + 1} wurde gelöscht.")
            
            # Falls wir uns nicht auf der letzten Seite befinden
            if self.current_page >= len(self.pdf_document):
                self.current_page = len(self.pdf_document) - 1

            self.load_page()

            # Geänderte PDF speichern
            self.save_pdf()
        else:
            print("Die letzte Seite kann nicht gelöscht werden.")

    def save_pdf(self):
        # Geänderte PDF-Datei unter dem angegebenen Pfad speichern
        self.pdf_document.save(self.save_path)
        print(f"PDF gespeichert als '{self.save_path}'.")



