
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("400x300")

        # Variables
        self.image_paths = []
        self.current_image_idx = 0

        # GUI Elements
        self.label_path = tk.Label(self.root, text="Selected Image: None")
        self.label_path.pack()

        self.entry_path = tk.Entry(self.root, width=50)
        self.entry_path.pack()

        self.btn_browse = tk.Button(self.root, text="Browse", command=self.browse_image)
        self.btn_browse.pack()

        self.btn_convert_gray = tk.Button(self.root, text="Convert to Grayscale", command=self.convert_to_grayscale)
        self.btn_convert_gray.pack()

        self.btn_edge_detect = tk.Button(self.root, text="Edge Detection", command=self.edge_detection)
        self.btn_edge_detect.pack()

        self.btn_reset = tk.Button(self.root, text="Reset", command=self.reset)
        self.btn_reset.pack()

        # OpenCV window size
        self.cv_window_width = 600
        self.cv_window_height = 600

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if file_path:
            self.image_paths.append(file_path)
            self.current_image_idx = len(self.image_paths) - 1
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, file_path)
            self.label_path.config(text=f"Selected Image: {os.path.basename(file_path)}")

    def convert_to_grayscale(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select an image first.")
            return
        
        image_path = self.image_paths[self.current_image_idx]
        original = cv2.imread(image_path)
        if original is None:
            messagebox.showerror("Error", f"Could not read image from {image_path}")
            return
        
        gray_image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        
        # Resize images to fit within 600x600 window
        original_resized = self.resize_image(original, self.cv_window_width, self.cv_window_height)
        gray_resized = self.resize_image(gray_image, self.cv_window_width, self.cv_window_height)
        
        cv2.imshow('Original', original_resized)
        cv2.imshow('Grayscale', gray_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def resize_image(self, image, width, height):
        h, w = image.shape[:2]
        aspect_ratio = w / h
        if aspect_ratio > 1:
            new_width = width
            new_height = int(width / aspect_ratio)
        else:
            new_height = height
            new_width = int(height * aspect_ratio)
        resized_image = cv2.resize(image, (new_width, new_height))
        return resized_image

    def edge_detection(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select an image first.")
            return
        
        image_path = self.image_paths[self.current_image_idx]
        original = cv2.imread(image_path)
        if original is None:
            messagebox.showerror("Error", f"Could not read image from {image_path}")
            return
        
        gray_image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 100, 200)
        
        # Resize images to fit within 600x600 window
        original_resized = self.resize_image(original, self.cv_window_width, self.cv_window_height)
        edges_resized = self.resize_image(edges, self.cv_window_width, self.cv_window_height)
        
        cv2.imshow('Original', original_resized)
        cv2.imshow('Edges', edges_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def reset(self):
        self.image_paths = []
        self.current_image_idx = 0
        self.entry_path.delete(0, tk.END)
        self.label_path.config(text="Selected Image: None")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
