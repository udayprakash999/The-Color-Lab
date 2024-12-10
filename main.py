import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import random
from PIL import Image  


def generate_palette(base_color=None):
    def random_color():
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def adjust_color(hex_color, factor):
        hex_color = hex_color.lstrip('#')
        rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        adjusted = [max(0, min(255, int(c * factor))) for c in rgb]
        return f"#{adjusted[0]:02x}{adjusted[1]:02x}{adjusted[2]:02x}"

    def complement_color(hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        complement = [255 - c for c in rgb]
        return f"#{complement[0]:02x}{complement[1]:02x}{complement[2]:02x}"

    if base_color is None:
        base_color = random_color()
    
    palette_colors = [
        base_color,
        adjust_color(base_color, 0.8),
        adjust_color(base_color, 1.2),
        complement_color(base_color),
        random_color(),
    ]

    return palette_colors


def update_palette(base_color=None):
    colors = generate_palette(base_color)
    for i, color in enumerate(colors):
        color_boxes[i].config(bg=color, text=color, fg='white' if i != 2 else 'black')
        color_boxes[i].bind("<Button-1>", lambda e, color=color: copy_to_clipboard(color))


def copy_to_clipboard(color):
    root.clipboard_clear()
    root.clipboard_append(color)
    root.update()
    show_copy_message(color)


def show_copy_message(color):
    copy_label.config(text=f"Copied {color} to clipboard!", fg="#2ecc71")
    copy_label.after(2000, lambda: copy_label.config(text=""))


def save_palette_as_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        image_width = 500
        image_height = 100
        image = Image.new("RGB", (image_width, image_height))
        color_width = image_width // len(color_boxes)
        
        for i, color_box in enumerate(color_boxes):
            color = color_box.cget("bg").lstrip("#")
            rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            for x in range(i * color_width, (i + 1) * color_width):
                for y in range(image_height):
                    image.putpixel((x, y), rgb_color)
        
        image.save(file_path)
        messagebox.showinfo("Success", f"Palette saved as {file_path}")


def save_palette_as_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            for color_box in color_boxes:
                file.write(f"{color_box.cget('text')}\n")
        messagebox.showinfo("Success", f"Palette saved as {file_path}")


def clear_palette():
    for color_box in color_boxes:
        color_box.config(bg="#FFFFFF", text="#FFFFFF")


root = tk.Tk()
root.title("🎉 Advanced Color Palette Generator")
root.geometry("700x600")
root.configure(bg="#2c3e50")

# Header
title_label = tk.Label(root, text="🎨 The Color Lab", font=("Arial", 28, "bold"), bg="#2c3e50", fg="white", pady=10)
title_label.pack()


button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=10)

buttons = [
    ("🎉 Random Palette", lambda: update_palette(None), "#3498db"),
    ("🎨 Select Base Color", lambda: update_palette(colorchooser.askcolor()[1]), "#9b59b6"),
    ("💾 Save as Image", save_palette_as_image, "#2ecc71"),
    ("📄 Save as Text", save_palette_as_text, "#f1c40f"),
    ("❌ Clear Palette", clear_palette, "#e74c3c"),
]

for text, command, color in buttons:
    button = tk.Button(
        button_frame, 
        text=text, 
        command=command, 
        font=("Arial", 12, "bold"), 
        width=15, 
        height=2, 
        bg=color, 
        fg="white", 
        bd=0, 
        highlightthickness=0, 
        relief="flat"
    )
    button.pack(side="left", padx=10, pady=10)
    button.config(
        highlightbackground=color,
        activebackground="#ecf0f1", 
        activeforeground="#2c3e50"
    )

# Color boxes palette
color_boxes = []
for i in range(5):
    label = tk.Label(root, text="#FFFFFF", font=("Arial", 12, "bold"), width=20, height=2, bg="#FFFFFF", relief="solid", borderwidth=2, cursor="hand2")
    label.pack(pady=5)
    color_boxes.append(label)

# Copy message 
copy_label = tk.Label(root, text="", font=("Arial", 12), bg="#2c3e50", fg="white", pady=10)
copy_label.pack()

footer_label = tk.Label(root, text="Designed for Color Dreamers 🎨💫", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1", pady=10)
footer_label.pack()

root.mainloop()