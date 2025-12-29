import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser, ttk
import qrcode
from PIL import Image, ImageTk, ImageColor
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask

# Standardfarben
current_fill_color = "#000000"  # Schwarz
current_back_color = "#FFFFFF"  # Weiß

# Mapping der Design-Namen zu den Klassen
STYLES = {
    "Standard (Quadrat)": SquareModuleDrawer(),
    "Abgerundet": RoundedModuleDrawer(),
    "Kreise": CircleModuleDrawer(),
    "Gapped (Lücken)": GappedSquareModuleDrawer(),
    "Vertikale Balken": VerticalBarsDrawer(),
    "Horizontale Balken": HorizontalBarsDrawer()
}

def choose_fill_color():
    global current_fill_color
    color = colorchooser.askcolor(title="Vordergrundfarbe wählen")[1]
    if color:
        current_fill_color = color
        btn_fill_color.config(bg=color)

def choose_back_color():
    global current_back_color
    color = colorchooser.askcolor(title="Hintergrundfarbe wählen")[1]
    if color:
        current_back_color = color
        btn_back_color.config(bg=color)

def hex_to_rgb(hex_color):
    """Konvertiert Hex (#FFFFFF) zu RGB Tuple (255, 255, 255)"""
    return ImageColor.getrgb(hex_color)

def generate_qr():
    input_text = entry_data.get()
    
    if not input_text:
        messagebox.showwarning("Fehler", "Bitte Text eingeben.")
        return

    try:
        # 1. Basis QR Code erstellen
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(input_text)
        qr.make(fit=True)

        # 2. Design auswählen
        selected_style_name = combo_style.get()
        module_drawer = STYLES.get(selected_style_name, SquareModuleDrawer())

        # 3. Farben vorbereiten
        # Vordergrund
        front_rgb = hex_to_rgb(current_fill_color)
        
        # Hintergrund (Logik für Transparenz)
        if var_transparent.get():
            # (R, G, B, Alpha) -> Alpha 0 = Transparent
            back_rgba = (255, 255, 255, 0) 
        else:
            back_rgb = hex_to_rgb(current_back_color)
            back_rgba = (back_rgb[0], back_rgb[1], back_rgb[2], 255)

        # 4. Bild mit Styles generieren
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=SolidFillColorMask(
                front_color=(front_rgb[0], front_rgb[1], front_rgb[2]), 
                back_color=back_rgba
            )
        )

        # 5. Vorschau anzeigen
        # Wir müssen das Bild für die Anzeige in RGBA konvertieren (falls transparent)
        # und auf einen weißen Hintergrund legen, damit man es in der GUI sieht
        preview_img = img.resize((250, 250)).convert("RGBA")
        
        # Für die GUI-Vorschau einen Schachbrett- oder weißen Hintergrund simulieren, 
        # falls transparent gewählt wurde, sonst sieht es komisch aus.
        # Hier nehmen wir einfach weiß für die Vorschau:
        background = Image.new("RGBA", preview_img.size, (240, 240, 240, 255))
        composite = Image.alpha_composite(background, preview_img)
        
        tk_img = ImageTk.PhotoImage(composite)
        label_preview.config(image=tk_img)
        label_preview.image = tk_img 
        
        # 6. Speichern Dialog
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Dateien", "*.png")],
            title="QR Code speichern"
        )
        
        if save_path:
            img.save(save_path)
            messagebox.showinfo("Erfolg", f"Gespeichert unter:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler: {e}")

# --- GUI Aufbau ---
root = tk.Tk()
root.title("QR Code Generator Pro V2")
root.geometry("450x650")
root.resizable(False, False)

# Style (für schönere Widgets)
style = ttk.Style()
style.theme_use('clam')

# Frame für Eingabe
frame_input = ttk.LabelFrame(root, text="1. Daten eingeben")
frame_input.pack(pady=10, padx=10, fill="x")

entry_data = ttk.Entry(frame_input, font=("Arial", 10))
entry_data.pack(pady=10, padx=10, fill="x")

# Frame für Design
frame_design = ttk.LabelFrame(root, text="2. Design & Farben")
frame_design.pack(pady=5, padx=10, fill="x")

# Design Auswahl
lbl_style = ttk.Label(frame_design, text="Form:")
lbl_style.grid(row=0, column=0, padx=5, pady=5, sticky="w")
combo_style = ttk.Combobox(frame_design, values=list(STYLES.keys()), state="readonly")
combo_style.current(0) # Erstes Element auswählen
combo_style.grid(row=0, column=1, padx=5, pady=5)

# Farbwahl Buttons
btn_fill_color = tk.Button(frame_design, text="Vordergrundfarbe", bg=current_fill_color, fg="white", command=choose_fill_color)
btn_fill_color.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

btn_back_color = tk.Button(frame_design, text="Hintergrundfarbe", bg=current_back_color, command=choose_back_color)
btn_back_color.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Checkbox Transparenz
var_transparent = tk.BooleanVar()
chk_transparent = ttk.Checkbutton(frame_design, text="Hintergrund Transparent", variable=var_transparent)
chk_transparent.grid(row=2, column=0, columnspan=2, pady=5)

# Generate Button
btn_generate = tk.Button(root, text="QR Code Erstellen & Speichern", command=generate_qr, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
btn_generate.pack(pady=15)

# Vorschau Bereich
label_preview = tk.Label(root, text="Vorschau", bg="#f0f0f0", width=30, height=15)
label_preview.pack(pady=5)

root.mainloop()