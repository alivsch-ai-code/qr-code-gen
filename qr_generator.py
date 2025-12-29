import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk # Benötigt: pip install pillow

def generate_qr():
    # 1. Daten aus dem Eingabefeld holen
    input_text = entry_data.get()
    
    if not input_text:
        messagebox.showwarning("Fehler", "Bitte geben Sie einen Text oder eine URL ein.")
        return

    try:
        # 2. QR Code Konfiguration
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(input_text)
        qr.make(fit=True)

        # 3. Bild erstellen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 4. Bild für die GUI konvertieren und anzeigen
        # Wir müssen das Bild verkleinern, damit es in die Vorschau passt
        preview_img = img.resize((250, 250)) 
        tk_img = ImageTk.PhotoImage(preview_img)
        
        label_preview.config(image=tk_img)
        label_preview.image = tk_img # Referenz behalten (Wichtig für Garbage Collector!)
        
        # 5. Speichern Dialog anbieten
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Dateien", "*.png"), ("Alle Dateien", "*.*")],
            title="QR Code speichern"
        )
        
        if save_path:
            img.save(save_path)
            messagebox.showinfo("Erfolg", f"QR Code gespeichert unter:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# --- GUI Aufbau ---
root = tk.Tk()
root.title("QR Code Generator Pro")
root.geometry("400x450")
root.resizable(False, False)

# Überschrift
label_instruction = tk.Label(root, text="URL oder Text eingeben:", font=("Arial", 12))
label_instruction.pack(pady=10)

# Eingabefeld
entry_data = tk.Entry(root, width=40, font=("Arial", 10))
entry_data.pack(pady=5)

# Button
btn_generate = tk.Button(root, text="QR Code Generieren & Speichern", command=generate_qr, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_generate.pack(pady=20)

# Vorschau-Label (Platzhalter)
label_preview = tk.Label(root, text="Vorschau erscheint hier", bg="#f0f0f0", width=35, height=15)
label_preview.pack(pady=10)

# Hauptschleife starten
root.mainloop()