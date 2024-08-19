import tkinter as tk
from tkinter import font
from PIL import ImageGrab, ImageTk

class AreaSelector:
    def __init__(self, root):
        self.root = root
        self.record_area = None
        self.rect = None
        self.guide_lines = []
        self.background_image = None

    def select_area(self, callback):
        self.callback = callback
        self.root.withdraw()
        
        screenshot = ImageGrab.grab()
        
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)
        
        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.background_image = ImageTk.PhotoImage(screenshot)
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)
        
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        self.selection_window.bind('<Escape>', self.cancel_selection)
        
        self.coord_font = font.Font(size=16)
        self.coord_label = tk.Label(self.selection_window, text="", bg='black', fg='white', font=self.coord_font)
        self.coord_label.place(x=10, y=10)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = None

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        for line in self.guide_lines:
            self.canvas.delete(line)
        
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red', width=4)
        
        self.guide_lines = [
            self.canvas.create_line(event.x, 0, event.x, self.canvas.winfo_height(), fill='blue', width=4, dash=(4, 4)),
            self.canvas.create_line(0, event.y, self.canvas.winfo_width(), event.y, fill='blue', width=4, dash=(4, 4))
        ]
        
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.coord_label.config(text=f"Size: {width}x{height} - Position: ({min(self.start_x, event.x)}, {min(self.start_y, event.y)})")

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        if self.start_x != end_x and self.start_y != end_y:
            x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
            x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
            self.record_area = (x1, y1, x2, y2)
        else:
            self.record_area = None
        self.cleanup_and_close()

    def cancel_selection(self, event):
        self.record_area = None
        self.cleanup_and_close()

    def cleanup_and_close(self):
        if self.rect:
            self.canvas.delete(self.rect)
        for line in self.guide_lines:
            self.canvas.delete(line)
        self.selection_window.destroy()
        self.root.deiconify()
        self.callback(self.record_area)