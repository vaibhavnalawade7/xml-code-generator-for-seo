import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

class DateTimeDialog(simpledialog.Dialog):
    def body(self, master):
        self.calendar = Calendar(master, date_pattern='yyyy-mm-dd', font=('Sans-serif', 10))
        self.calendar.pack(pady=10)

        tk.Label(master, text="Select time (HH:MM:SS):", font=('Sans-serif', 10)).pack()

        # Entry widgets for hours, minutes, and seconds with labels
        tk.Label(master, text="Hours:", font=('Sans-serif', 10)).pack(side=tk.LEFT)
        self.hour_var = tk.StringVar(value="00")
        tk.Entry(master, textvariable=self.hour_var, validate="key", validatecommand=(master.register(self.validate_input), "%P"), font=('Sans-serif', 10)).pack(side=tk.LEFT)

        tk.Label(master, text="Minutes:", font=('Sans-serif', 10)).pack(side=tk.LEFT)
        self.minute_var = tk.StringVar(value="00")
        tk.Entry(master, textvariable=self.minute_var, validate="key", validatecommand=(master.register(self.validate_input), "%P"), font=('Sans-serif', 10)).pack(side=tk.LEFT)

        tk.Label(master, text="Seconds:", font=('Sans-serif', 10)).pack(side=tk.LEFT)
        self.second_var = tk.StringVar(value="00")
        tk.Entry(master, textvariable=self.second_var, validate="key", validatecommand=(master.register(self.validate_input), "%P"), font=('Sans-serif', 10)).pack(side=tk.LEFT)

        return self.calendar

    def validate_input(self, value):
        return value.isdigit() and 0 <= int(value) <= 59

    def apply(self):
        selected_date = self.calendar.get_date()
        selected_time = f"{self.hour_var.get()}:{self.minute_var.get()}:{self.second_var.get()}"
        self.result = f"{selected_date}T{selected_time}+00:00"

def get_last_mod():
    dialog = DateTimeDialog(window)
    return dialog.result

def generate_xml_code():
    urls = url_text.get("1.0", tk.END).splitlines()
    last_mod = get_last_mod()

    root = Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for url in urls:
        if url.strip():  # Ignore empty lines
            url_element = SubElement(root, "url")
            loc_element = SubElement(url_element, "loc")
            loc_element.text = url
            lastmod_element = SubElement(url_element, "lastmod")
            lastmod_element.text = last_mod

    xml_code = minidom.parseString(tostring(root)).toprettyxml(indent="    ")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, xml_code)

def copy_to_clipboard():
    xml_code = result_text.get("1.0", tk.END)
    window.clipboard_clear()
    window.clipboard_append(xml_code)
    window.update()
    messagebox.showinfo("Copied", "XML code copied to clipboard!")

# Create the main window
window = tk.Tk()
window.title("XML Code Generator")
window.geometry("800x600")
window.configure(bg="#F2F2F2")

# Configure the colors and fonts
bg_color = "#F2F2F2"
entry_bg_color = "#FFFFFF"
button_bg_color = "#4CAF50"
button_fg_color = "white"
blue_button_bg_color = "#2196F3"  # Blue color

window.configure(bg=bg_color)

# Create and place GUI components
tk.Label(window, text="Enter URLs (one per line):", bg=bg_color, fg="#333333", font=('Sans-serif', 12)).pack(pady=5)
url_text = tk.Text(window, height=10, width=60, bg=entry_bg_color, font=('Sans-serif', 10))
url_text.pack(pady=5)

generate_button = tk.Button(window, text="Generate XML Code", command=generate_xml_code, bg=blue_button_bg_color, fg=button_fg_color, font=('Sans-serif', 12))
generate_button.pack(pady=5)

tk.Label(window, text="Generated XML Code:", bg=bg_color, fg="#333333", font=('Sans-serif', 12)).pack(pady=5)

# Create a scrollbar for the result_text
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(window, height=10, width=60, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg=entry_bg_color, font=('Sans-serif', 10))
result_text.pack(pady=5)

# Configure the scrollbar
scrollbar.config(command=result_text.yview)

copy_button = tk.Button(window, text="Copy Code", command=copy_to_clipboard, bg=blue_button_bg_color, fg=button_fg_color, font=('Sans-serif', 12))
copy_button.pack(pady=5)

# Start the Tkinter event loop
window.mainloop()
