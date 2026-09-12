import os
import re
import time
import threading
import img2pdf
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

class IMGToPDFConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IMG to PDF Converter")
        self.geometry("600x350")
        self.configure(bg="#f4f6f9")
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure("Modern.TEntry", padding=5, fieldbackground="white")
        self.style.configure("Modern.Horizontal.TProgressbar", thickness=15, background="#4caf50", troughcolor="#e0e0e0")
        
        self.create_widgets()

    def get_natural_key(self, text):
        return [int(num) if num.isdigit() else num.lower() for num in re.split(r'(\d+)', text)]

    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#f4f6f9", padx=30, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)

        try:
            img = Image.open("assets/folder_icon.png")
            img = img.resize((20, 20), Image.Resampling.LANCZOS)
            self.icon_folder = ImageTk.PhotoImage(img)
        except Exception:
            self.icon_folder = None

        lbl_folder = tk.Label(main_frame, text="Select Images Folder:", bg="#f4f6f9", font=("Segoe UI", 10, "bold"), fg="#333")
        lbl_folder.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.folder_path = tk.StringVar()
        self.entry_folder = ttk.Entry(main_frame, textvariable=self.folder_path, font=("Segoe UI", 10), style="Modern.TEntry", state='readonly')
        self.entry_folder.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        btn_folder = tk.Button(main_frame, image=self.icon_folder, text="Browse" if not self.icon_folder else "", command=self.browse_folder, bg="#ffffff", relief="flat", cursor="hand2", width=30 if not self.icon_folder else None)
        btn_folder.grid(row=1, column=1)
        self.add_hover_effect(btn_folder, "#ffffff", "#e0e0e0")

        lbl_pdf = tk.Label(main_frame, text="Select Output PDF:", bg="#f4f6f9", font=("Segoe UI", 10, "bold"), fg="#333")
        lbl_pdf.grid(row=2, column=0, sticky="w", pady=(15, 5))

        self.output_path = tk.StringVar()
        self.entry_pdf = ttk.Entry(main_frame, textvariable=self.output_path, font=("Segoe UI", 10), style="Modern.TEntry", state='readonly')
        self.entry_pdf.grid(row=3, column=0, sticky="ew", padx=(0, 10))

        btn_pdf = tk.Button(main_frame, image=self.icon_folder, text="Browse" if not self.icon_folder else "", command=self.browse_pdf, bg="#ffffff", relief="flat", cursor="hand2", width=30 if not self.icon_folder else None)
        btn_pdf.grid(row=3, column=1)
        self.add_hover_effect(btn_pdf, "#ffffff", "#e0e0e0")

        self.btn_convert = tk.Button(main_frame, text="Convert to PDF", command=self.start_conversion, bg="#4caf50", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2", pady=8)
        self.btn_convert.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(25, 10))
        self.add_hover_effect(self.btn_convert, "#4caf50", "#45a049")

        self.lbl_progress = tk.Label(main_frame, text="", bg="#f4f6f9", font=("Segoe UI", 9, "bold"), fg="#555")
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate", style="Modern.Horizontal.TProgressbar")

    def add_hover_effect(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Folder")
        if folder_selected:
            self.folder_path.set(folder_selected)

    def browse_pdf(self):
        file_selected = filedialog.asksaveasfilename(title="Save PDF As", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_selected:
            self.output_path.set(file_selected)

    def start_conversion(self):
        folder = self.folder_path.get()
        output = self.output_path.get()

        if not folder or not output:
            messagebox.showerror("Error", "Please select both input folder and output file.")
            return

        self.lbl_progress.grid(row=5, column=0, columnspan=2, pady=(5, 0))
        self.progress.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(2, 0))
        self.btn_convert.config(state="disabled", bg="#9e9e9e")
        self.lbl_progress.config(text="(0/0)", fg="#555")

        threading.Thread(target=self.process_conversion, args=(folder, output), daemon=True).start()

    def process_conversion(self, folder, output):
        try:
            valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")
            files = [f for f in os.listdir(folder) if f.lower().endswith(valid_extensions)]
            files.sort(key=self.get_natural_key)

            if not files:
                self.reset_ui()
                messagebox.showerror("Error", "No valid images found in the selected folder.")
                return

            total_images = len(files)
            self.progress["maximum"] = total_images
            image_paths = []

            for i, f in enumerate(files, 1):
                image_paths.append(os.path.join(folder, f))
                self.progress["value"] = i
                self.lbl_progress.config(text=f"({i}/{total_images})")
                self.update_idletasks()
                time.sleep(0.01) 

            self.lbl_progress.config(text="Generating PDF file...")
            self.update_idletasks()
            
            with open(output, "wb") as f:
                f.write(img2pdf.convert(image_paths))

            self.lbl_progress.config(text="Conversion Completed!", fg="#4caf50")
            self.btn_convert.config(state="normal", bg="#4caf50")
            messagebox.showinfo("Completed", "PDF created successfully!")

        except Exception as e:
            self.reset_ui()
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def reset_ui(self):
        self.lbl_progress.grid_forget()
        self.progress.grid_forget()
        self.btn_convert.config(state="normal", bg="#4caf50")

if __name__ == "__main__":
    app = IMGToPDFConverterApp()
    app.mainloop()