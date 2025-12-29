# Advanced QR Code Generator 📱

![GitHub release (latest by date)](https://img.shields.io/github/v/release/IHR_USERNAME/IHR_REPO_NAME)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

A powerful, user-friendly desktop application to generate customizable QR codes. Built with Python and Tkinter, featuring advanced styling options, custom colors, and transparency support.

**[Download Latest Windows Version (.exe)](https://github.com/IHR_USERNAME/IHR_REPO_NAME/releases/latest)**

---

## ✨ Features

* **Custom Designs:** Choose between different module styles (Square, Rounded, Circles, Gapped, Bars).
* **Color Customization:** Pick any foreground and background color using a color picker.
* **Transparency Support:** Generate QR codes with transparent backgrounds (perfect for overlays).
* **High Reliability:** Uses high error correction (Level H) by default.
* **Instant Preview:** Live preview of your QR code within the app.
* **Standalone:** Available as a single `.exe` file – no Python installation required.

---

## 🚀 Usage

### Option 1: Run the Executable (Recommended for Users)
1.  Go to the **[Releases Page](https://github.com/IHR_USERNAME/IHR_REPO_NAME/releases)**.
2.  Download the latest `QRCodeGen.exe`.
3.  Double-click to run. No installation needed.

### Option 2: Run from Source (For Developers)
If you want to modify the code or run it on Linux/Mac:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/IHR_USERNAME/IHR_REPO_NAME.git](https://github.com/IHR_USERNAME/IHR_REPO_NAME.git)
    cd IHR_REPO_NAME
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python qr_generator.py
    ```

---

## 🛠 Building the EXE manually

This project uses **PyInstaller** to create the Windows executable.

```bash
pyinstaller --noconsole --onefile --name "QRCodeGen" qr_generator.py