import tkinter as tk

from tkinter import filedialog, messagebox, ttk, Label, Entry, IntVar

from scripts.invisible_watermark import encode_invisible_watermark, decode_invisible_watermark
from scripts.visible_watermark import apply_visible_watermark


def apply_watermark():
    watermark_type = watermark_type_combobox.get()
    watermark_text = entry_watermark_detail.get()
    watermark_file = entry_watermark_file.get()
    source_file = entry_source_file.get()

    # Based on the file type and watermark type, call the appropriate functions
    if watermark_type == 'Visible':
        # Perform visible watermarking
        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if output_file_path:
            options = {'opacity': opacity_var.get(), 'font_size': font_size_var.get()}
            apply_visible_watermark(source_file, output_file_path, watermark_text, **options)
            label_feedback.config(text=f"Watermarked image saved as {output_file_path}.")
    elif watermark_type == 'Invisible':
        # Perform invisible watermarking
        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if output_file_path:
            encode_invisible_watermark(source_file, output_file_path, watermark_text, watermark_file if watermark_file is not '' else None)
            label_feedback.config(text=f"Invisible watermark encoded in image saved as {output_file_path}.")
    else:
        messagebox.showerror("Error", "Please select a valid watermark type.")
    pass


# Set up the main application window
app = tk.Tk()
app.title('Advanced Watermarking App')

# File type selection
tk.Label(app, text="~~~ Encode/Decode Image ~~~").pack()

tk.Label(app, text="Select Watermark Type:").pack()
watermark_type_combobox = ttk.Combobox(app, values=["Visible", "Invisible"])
watermark_type_combobox.pack()

# Watermark detail
tk.Label(app, text="Watermark Text:").pack()
entry_watermark_detail = tk.Entry(app)
entry_watermark_detail.pack()

# Source file
tk.Label(app, text="Source File:").pack()
entry_source_file = tk.Entry(app)
entry_source_file.pack()
tk.Button(app, text="Browse", command=lambda: entry_source_file.insert(0, filedialog.askopenfilename())).pack()

# Watermark file
tk.Label(app, text="Source File:").pack()
entry_watermark_file = tk.Entry(app)
entry_watermark_file.pack()
tk.Button(app, text="Browse", command=lambda: entry_watermark_file.insert(0, filedialog.askopenfilename())).pack()

# Image-specific options
opacity_var = IntVar(value=128)  # Default opacity
label_opacity = Label(app, text="Opacity (for visible watermark):")
label_opacity.pack()
slider_opacity = tk.Scale(app, from_=0, to_=255, orient="horizontal", variable=opacity_var)
slider_opacity.pack()

font_size_var = IntVar(value=36)  # Default font size
label_font_size = Label(app, text="Font Size (for visible watermark):")
label_font_size.pack()
entry_font_size = Entry(app, textvariable=font_size_var)
entry_font_size.pack()

# Apply Watermark Button
tk.Button(app, text="Apply Watermark", command=apply_watermark).pack()

# Feedback Label
label_feedback = tk.Label(app, text="")
label_feedback.pack()


def decode_watermark():
    """
    Handles the decoding of an invisible watermark from an image.
    """
    source_file = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if source_file:
        watermark_text = decode_invisible_watermark(source_file)
        label_decoded_watermark.config(text=f"Decoded watermark: {watermark_text}")


# Add a section in the UI for decoding the watermark
tk.Label(app, text="Decode Invisible Watermark").pack()

# Button to choose the image to decode
tk.Button(app, text="Choose Image to Decode", command=decode_watermark).pack()

# Label to display the decoded watermark
label_decoded_watermark = tk.Label(app, text="")
label_decoded_watermark.pack()

app.mainloop()
