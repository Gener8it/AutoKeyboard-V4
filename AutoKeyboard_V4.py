import time
import threading
from pynput.keyboard import Controller, Listener, Key, KeyCode
import tkinter as tk
from tkinter import ttk

keyboard = Controller()
is_running = False
key_to_press = 'space'
interval = 0.01
start_stop_key = Key.f6
press_count = 0
hold_key = False

special_keys = [
    'space', 'enter', 'shift', 'ctrl', 'alt', 'tab', 'esc', 'backspace',
    'caps_lock', 'delete', 'home', 'end', 'page_up', 'page_down', 'arrow_up',
    'arrow_down', 'arrow_left', 'arrow_right', 'insert', 'f1', 'f2', 'f3', 'f4',
    'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
]

def clicker():
    global is_running, press_count, key_to_press
    pressed = 0
    while True:
        if is_running and (press_count == 0 or pressed < press_count):
            try:
                print(f"Clicker: Key to press = {key_to_press}")
                
                if key_to_press in special_keys:
                    if key_to_press == 'space':
                        keyboard.press(Key.space)
                        if not hold_key:
                            keyboard.release(Key.space)
                    else:
                        key = getattr(Key, key_to_press, None)
                        if key:
                            keyboard.press(key)
                            if not hold_key:
                                keyboard.release(key)
                else:
                    keyboard.press(KeyCode.from_char(key_to_press))
                    if not hold_key:
                        keyboard.release(KeyCode.from_char(key_to_press))

                pressed += 1
                time.sleep(interval)
            except AttributeError:
                print(f"Error: Invalid key = {key_to_press}")
                is_running = False
        else:
            time.sleep(0.1)

def toggle_clicker():
    global is_running
    is_running = not is_running
    start_button.config(text="Stop" if is_running else "Start")
    status_label.config(text=f"Autoclicker {'running' if is_running else 'stopped'}")

def on_press(key):
    global is_running
    if key == start_stop_key:
        toggle_clicker()

def start_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def set_speed():
    global interval, press_count
    minutes = int(min_entry.get())
    seconds = int(sec_entry.get())
    milliseconds = int(ms_entry.get())
    interval = (minutes * 60) + seconds + (milliseconds / 1000)
    press_count = int(num_press_entry.get()) if num_press_entry.get() else 0
    status_label.config(text=f"Interval set to {interval} seconds")

def save_key():
    global key_to_press
    selected_key = key_var.get().lower()
    print(f"Saving key: {selected_key}")
    key_to_press = selected_key

def set_hotkey():
    global start_stop_key
    hotkey = hotkey_entry.get().lower()
    if hotkey.startswith('f') and hotkey[1:].isdigit():
        start_stop_key = getattr(Key, hotkey, None)
    elif hotkey == 'space':
        start_stop_key = Key.space
    else:
        start_stop_key = KeyCode.from_char(hotkey)
    status_label.config(text=f"Hotkey set to: {hotkey.upper()}")

root = tk.Tk()
root.title("Auto Keyboard")
root.configure(bg='#1e1e1e')
root.geometry("320x640")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure("Rounded.TButton", foreground="white", background="#3c3c3c", padding=6, relief="flat", borderwidth=10)
style.configure("Rounded.TEntry", foreground="white", fieldbackground="#3c3c3c", padding=4, relief="flat")
style.configure("Rounded.TCombobox", fieldbackground="#3c3c3c", background="#3c3c3c", foreground="white", padding=4)
style.configure("TLabel", foreground="white", background="#1e1e1e")
style.map("Rounded.TButton", background=[('active', '#505050')])

key_var = tk.StringVar(value='space')
key_label = ttk.Label(root, text="Key to press:", font=("Arial", 12))
key_label.pack(pady=10)

key_menu = ttk.Combobox(root, textvariable=key_var, values=[chr(i) for i in range(97, 123)] + special_keys, style="Rounded.TCombobox")
key_menu.pack()

save_key_button = ttk.Button(root, text="Save Key", command=save_key, style="Rounded.TButton")
save_key_button.pack(pady=10)

hotkey_label = ttk.Label(root, text="Set Start/Stop Hotkey:", font=("Segoe UI", 11))
hotkey_label.pack(pady=10)

hotkey_entry = ttk.Entry(root, style="Rounded.TEntry")
hotkey_entry.insert(0, 'f6')
hotkey_entry.pack()

set_hotkey_button = ttk.Button(root, text="Save Hotkey", command=set_hotkey, style="Rounded.TButton")
set_hotkey_button.pack(pady=10)

speed_label = ttk.Label(root, text="Set Delay between Keys:", font=("Segoe UI", 11))
speed_label.pack(pady=10)

min_label = ttk.Label(root, text="Minutes:", font=("Segoe UI", 10))
min_label.pack()
min_entry = ttk.Entry(root, style="Rounded.TEntry", justify="center")
min_entry.insert(0, "0")
min_entry.pack()

sec_label = ttk.Label(root, text="Seconds:", font=("Segoe UI", 10))
sec_label.pack()
sec_entry = ttk.Entry(root, style="Rounded.TEntry", justify="center")
sec_entry.insert(0, "0")
sec_entry.pack()

ms_label = ttk.Label(root, text="Milliseconds:", font=("Segoe UI", 10))
ms_label.pack()
ms_entry = ttk.Entry(root, style="Rounded.TEntry", justify="center")
ms_entry.insert(0, "10")
ms_entry.pack()

num_press_label = ttk.Label(root, text="Number of Keys to Automate (0 = Infinite):", font=("Segoe UI", 11))
num_press_label.pack(pady=10)

num_press_entry = ttk.Entry(root, style="Rounded.TEntry", justify="center")
num_press_entry.insert(0, "10")
num_press_entry.pack()

hold_var = tk.BooleanVar()
hold_check = ttk.Checkbutton(root, text="Hold Key", variable=hold_var, command=lambda: setattr(globals(), 'hold_key', hold_var.get()), style="TCheckbutton")
hold_check.pack()

set_speed_button = ttk.Button(root, text="Set Interval", command=set_speed, style="Rounded.TButton")
set_speed_button.pack(pady=10)

status_label = ttk.Label(root, text="Autoclicker stopped", font=("Segoe UI", 11))
status_label.pack(pady=10)

start_button = ttk.Button(root, text="Start", command=toggle_clicker, style="Rounded.TButton")
start_button.pack(pady=20)

click_thread = threading.Thread(target=clicker)
click_thread.daemon = True
click_thread.start()

listener_thread = threading.Thread(target=start_listener)
listener_thread.daemon = True
listener_thread.start()

root.mainloop()
