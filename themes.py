import tkinter as tk
from tkinter import ttk

def set_dark_theme(root):
    root.tk_setPalette(background="#2e2e2e", 
                       foreground="white", activeBackground="#1e1e1e", activeForeground="white")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background="#2e2e2e", foreground="white")
    style.configure("TCombobox", fieldbackground="#1e1e1e", background="#2e2e2e", foreground="white")
    style.map("TCombobox", fieldbackground=[('readonly', '#1e1e1e')])
    style.configure("TButton", background="#1e1e1e", foreground="white")
    style.map("TButton", background=[('active', '#ac151f')], foreground=[('active', 'white')])

def set_light_theme(root):
    root.tk_setPalette(background="#f0f0f0", 
                       foreground="black", activeBackground="#e0e0e0", activeForeground="black")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background="#f0f0f0", foreground="black")
    style.configure("TCombobox", fieldbackground="#ffffff", background="#f0f0f0", foreground="black")
    style.map("TCombobox", fieldbackground=[('readonly', '#ffffff')])
    style.configure("TButton", background="#e0e0e0", foreground="black")
    style.map("TButton", background=[('active', '#c0c0c0')], foreground=[('active', 'black')])

def set_dark_blue_theme(root):
    root.tk_setPalette(background="#2c3e50", foreground="white", 
                       activeBackground="#3498db", activeForeground="white")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background="#2c3e50", foreground="white")
    style.configure("TCombobox", fieldbackground="#34495e", background="#2c3e50", foreground="white")
    style.map("TCombobox", fieldbackground=[('readonly', '#34495e')])
    style.configure("TButton", background="#3498db", foreground="white")
    style.map("TButton", background=[('active', '#2980b9')], foreground=[('active', 'white')])

def set_light_green_theme(root):
    root.tk_setPalette(background="#5b8a57", foreground="white", 
                       activeBackground="#4a7d4a", activeForeground="white")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background="#5b8a57", foreground="white")
    style.configure("TCombobox", fieldbackground="#4a7d4a", background="#6ba07c", foreground="white")
    style.map("TCombobox", fieldbackground=[('readonly', '#4a7d4a')])
    style.configure("TButton", background="#4a7d4a", foreground="white")
    style.map("TButton", background=[('active', '#005700')], foreground=[('active', 'white')])

def set_purple_theme(root):
    root.tk_setPalette(background="#6a0f6a", foreground="white", 
                       activeBackground="#9b4d9b", activeForeground="white")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background="#6a0f6a", foreground="white")
    style.configure("TCombobox", fieldbackground="#8c2b8c", background="#5c0f5c", foreground="white")
    style.map("TCombobox", fieldbackground=[('readonly', '#8c2b8c')])
    style.configure("TButton", background="#8c2b8c", foreground="white")
    style.map("TButton", background=[('active', '#9b4d9b')], foreground=[('active', 'white')])

def set_starry_night_theme(root):
    root.tk_setPalette(background="#2e3a5f", foreground="white", 
                       activeBackground="#1f2a47", activeForeground="white")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background="#2e3a5f", foreground="white")
    style.configure("TCombobox", fieldbackground="#1b263b", background="#2e3a5f", foreground="white")
    style.map("TCombobox", fieldbackground=[('readonly', '#1b263b')])
    style.configure("TButton", background="#3b4e6c", foreground="white")
    style.map("TButton", background=[('active', '#a9ad68')], foreground=[('active', 'white')])