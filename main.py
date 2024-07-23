import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermark App")
        self.root.geometry("600x400")

        # Create main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.main_frame, text="Select an image:", bg="#f0f0f0", font=('Arial', 12))
        self.label.pack(pady=(0, 10))

        self.image_path = tk.StringVar()
        self.button_browse = tk.Button(self.main_frame, text="Browse", command=self.browse_image, bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'), relief=tk.RAISED, padx=10, pady=5)
        self.button_browse.pack(pady=(0, 20))

        self.label_text = tk.Label(self.main_frame, text="Enter watermark text:", bg="#f0f0f0", font=('Arial', 12))
        self.label_text.pack(pady=(0, 10))

        self.entry_text = tk.Entry(self.main_frame, width=40, font=('Arial', 12))
        self.entry_text.pack(pady=(0, 20))

        self.button_watermark = tk.Button(self.main_frame, text="Add Watermark", command=self.add_watermark, bg="#2196F3", fg="white", font=('Arial', 12, 'bold'), relief=tk.RAISED, padx=10, pady=5)
        self.button_watermark.pack(pady=(0, 10))

        self.button_save = tk.Button(self.main_frame, text="Save Image", command=self.save_image, state='disabled', bg="yellow", fg="white", font=('Arial', 12, 'bold'), relief=tk.RAISED, padx=10, pady=5)
        self.button_save.pack(pady=(0, 10))

        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def browse_image(self):
        filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        self.image_path.set(filedialog.askopenfilename(title="Select an image", filetypes=filetypes))

    def add_watermark(self):
        image_path = self.image_path.get()
        if not image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        text = self.entry_text.get()
        if not text:
            messagebox.showerror("Error", "Please enter watermark text.")
            return

        try:
            # Open the image
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            width, height = img.size

            # Add watermark
            spacing_x = 500
            spacing_y = 300
            for y in range(0, height, spacing_y):
                for x in range(0, width, spacing_x):
                    draw.text((x, y), text, font=font, fill=(255, 255, 255, 50))

            # Display image with watermark
            self.display_image(img)

            # Enable save button
            self.button_save.config(state='normal')

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_image(self, img):
        self.canvas_frame.pack_forget()  # Remove previous canvas if it exists
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.imshow(np.array(img))
        ax.axis('off')

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if save_path:
            try:
                img = Image.open(self.image_path.get())
                draw = ImageDraw.Draw(img)
                text = self.entry_text.get()
                font = ImageFont.load_default()
                width, height = img.size

                # Add watermark
                spacing_x = 500
                spacing_y = 300
                for y in range(0, height, spacing_y):
                    for x in range(0, width, spacing_x):
                        draw.text((x, y), text, font=font, fill=(255, 255, 255, 50))

                img.save(save_path)
                messagebox.showinfo("Success", "Image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
