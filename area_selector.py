import tkinter as tk
from tkinter import font

class AreaSelector:
    def __init__(self, root):
        self.root = root
        self.record_area = None
        self.rect = None
        self.guide_lines = []

    def select_area(self, callback):
        self.callback = callback
        self.root.withdraw()
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)
        self.selection_window.configure(bg='black')

        self.canvas = tk.Canvas(self.selection_window, cursor="cross", bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        self.selection_window.bind('<Escape>', self.cancel_selection)

        self.coord_font = font.Font(size=16)
        self.coord_label = tk.Label(self.selection_window, text="", bg='white', fg='green', font=self.coord_font)
        self.coord_label.place(x=10, y=10)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = None

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red', width=2)

        for line in self.guide_lines:
            self.canvas.delete(line)
        self.guide_lines.clear()

        self.guide_lines = [
            self.canvas.create_line(event.x, 0, event.x, self.canvas.winfo_height(), fill='blue', width=2, dash=(2, 2)),
            self.canvas.create_line(0, event.y, self.canvas.winfo_width(), event.y, fill='blue', width=2, dash=(2, 2))
        ]

        self.coord_label.config(text=f"Start: ({self.start_x}, {self.start_y}) - End: ({event.x}, {event.y})")

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        if self.start_x == end_x or self.start_y == end_y:
            self.record_area = None
        else:
            x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
            x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
            self.record_area = (x1, y1, x2, y2)
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
