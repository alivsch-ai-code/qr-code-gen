import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser, ttk
import qrcode
from PIL import Image, ImageTk, ImageColor, ImageOps
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)

# Standard colors
current_fill_color = "#000000"  # Black
current_back_color = "#FFFFFF"  # White

# English Style Names
STYLES = {
    "Standard (Square)": SquareModuleDrawer(),
    "Rounded": RoundedModuleDrawer(),
    "Circles": CircleModuleDrawer(),
    "Gapped": GappedSquareModuleDrawer(),
    "Vertical Bars": VerticalBarsDrawer(),
    "Horizontal Bars": HorizontalBarsDrawer()
}

def choose_fill_color():
    global current_fill_color
    color = colorchooser.askcolor(title="Select Foreground Color")[1]
    if color:
        current_fill_color = color
        btn_fill_color.config(bg=color)

def choose_back_color():
    global current_back_color
    color = colorchooser.askcolor(title="Select Background Color")[1]
    if color:
        current_back_color = color
        btn_back_color.config(bg=color)

def generate_qr():
    input_text = entry_data.get()
    
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter text or URL.")
        return

    try:
        # 1. Setup QR Code Mechanism
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(input_text)
        qr.make(fit=True)

        # 2. Get Selected Style
        selected_style_name = combo_style.get()
        module_drawer = STYLES.get(selected_style_name, SquareModuleDrawer())

        # 3. Generate Basic Image (Black & White ONLY first)
        # We let qrcode generate the shapes in B/W, we handle colors later.
        img_bw = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
        ).convert("RGBA") # Convert to RGBA immediately

        # 4. Custom Coloring Logic (The Fix)
        # We create a new image by using the B/W QR code as a mask.
        
        # Prepare dimensions
        width, height = img_bw.size
        
        # Prepare Background
        if var_transparent.get():
            # Fully transparent background (R, G, B, 0)
            back_color_rgba = (255, 255, 255, 0)
        else:
            # User selected background
            rgb = ImageColor.getrgb(current_back_color)
            back_color_rgba = (rgb[0], rgb[1], rgb[2], 255)
            
        bg_layer = Image.new("RGBA", (width, height), back_color_rgba)
        
        # Prepare Foreground (The QR Pattern)
        fg_rgb = ImageColor.getrgb(current_fill_color)
        fg_layer = Image.new("RGBA", (width, height), (fg_rgb[0], fg_rgb[1], fg_rgb[2], 255))
        
        # Create Mask:
        # The img_bw has Black modules (0) and White background (255).
        # For a mask, we need White (255) where we want the Foreground Color, 
        # and Black (0) where we want the Background Color.
        # So we convert to Grayscale ('L') and Invert it.
        mask = ImageOps.invert(img_bw.convert("L"))

        # Composite: Put FG on top of BG using the Mask
        final_img = Image.composite(fg_layer, bg_layer, mask)

        # 5. Preview for GUI
        preview_img = final_img.resize((250, 250), Image.Resampling.LANCZOS)
        
        # Create a checkerboard or white background specifically for the GUI preview
        # so transparent codes are visible
        gui_bg = Image.new("RGBA", preview_img.size, (240, 240, 240, 255))
        gui_preview = Image.alpha_composite(gui_bg, preview_img)
        
        tk_img = ImageTk.PhotoImage(gui_preview)
        label_preview.config(image=tk_img)
        label_preview.image = tk_img 
        
        # 6. Save Dialog
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")],
            title="Save QR Code"
        )
        
        if save_path:
            final_img.save(save_path)
            messagebox.showinfo("Success", f"Saved to:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("QR Code Generator Pro V3")
root.geometry("450x650")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

# Input Frame
frame_input = ttk.LabelFrame(root, text="1. Enter Data")
frame_input.pack(pady=10, padx=10, fill="x")

entry_data = ttk.Entry(frame_input, font=("Arial", 10))
entry_data.pack(pady=10, padx=10, fill="x")

# Design Frame
frame_design = ttk.LabelFrame(root, text="2. Design & Colors")
frame_design.pack(pady=5, padx=10, fill="x")

# Style Selection
lbl_style = ttk.Label(frame_design, text="Shape:")
lbl_style.grid(row=0, column=0, padx=5, pady=5, sticky="w")
combo_style = ttk.Combobox(frame_design, values=list(STYLES.keys()), state="readonly")
combo_style.current(0)
combo_style.grid(row=0, column=1, padx=5, pady=5)

# Color Buttons
btn_fill_color = tk.Button(frame_design, text="Foreground Color", bg=current_fill_color, fg="white", command=choose_fill_color)
btn_fill_color.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

btn_back_color = tk.Button(frame_design, text="Background Color", bg=current_back_color, command=choose_back_color)
btn_back_color.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Transparency Checkbox
var_transparent = tk.BooleanVar()
chk_transparent = ttk.Checkbutton(frame_design, text="Transparent Background", variable=var_transparent)
chk_transparent.grid(row=2, column=0, columnspan=2, pady=5)

# Generate Button
btn_generate = tk.Button(root, text="Generate & Save QR Code", command=generate_qr, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
btn_generate.pack(pady=15)

# Preview
label_preview = tk.Label(root, text="Preview", bg="#f0f0f0", width=30, height=15)
label_preview.pack(pady=5)

root.mainloop()