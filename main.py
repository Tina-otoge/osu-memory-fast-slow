import time
import requests
import tkinter as tk

GOSU_URL = 'http://127.0.0.1:24050/json'
TRESHOLD = 18
FONT_SIZE = 24
FONT_NAME = 'Segoe UI'

height = FONT_SIZE * 2
width = int(FONT_SIZE * 4)
root = tk.Tk()
root.iconify()
window = tk.Toplevel(root)
window.geometry(f'{width}x{height}+470+480')
window.attributes('-topmost', True)
window.wm_attributes('-transparentcolor', 'white')
window.overrideredirect(1)
text = tk.Text(window, font=(FONT_NAME, FONT_SIZE))
text.tag_configure('RED', foreground='red')
text.tag_configure('BLUE', foreground='cyan')
text.pack()
session = requests.Session()

def update():
    response = session.get(GOSU_URL)
    data = response.json()
    hit_errors = data['gameplay']['hits']['hitErrorArray']
    if not hit_errors:
        print('Waiting for gameplay...')
        text.insert('1.0', '    ')
        root.after(50, update)
        return
    last_error = hit_errors[-1]
    text.tag_remove('RED', '1.0', 'end')
    text.tag_remove('BLUE', '1.0', 'end')
    if last_error < -TRESHOLD:
        text.insert('1.0', 'FAST    ')
        text.tag_add('BLUE', '1.0', 'end')
    elif last_error > TRESHOLD:
        text.insert('1.0', 'SLOW    ')
        text.tag_add('RED', '1.0', 'end')
    else:
        text.insert('1.0', '    ')
    root.after(1, update)

def main():
    root.after(1000, update)
    window.mainloop()

if __name__ == '__main__':
    main()