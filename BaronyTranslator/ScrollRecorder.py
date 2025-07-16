import tkinter as tk
from tkinter import ttk
import json
import os

class RowSection(ttk.Frame):
    def __init__(self, parent, title, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.title = title

        self.label = ttk.Label(self, text=title)
        self.label.pack(side="left", padx=5)

        self.combo = ttk.Combobox(self, values=["Charging", "Repair", "Enchant Weapon", "Enchant Armor", "Remove Curse", "Mapping", "Food", "Identify", "Summon", "Light", "Teleportation", "Fire",  "Destroy Armor", "Arrow" ], width=20)
        self.combo.set("Unknown")
        self.combo.pack(side="left", padx=5)

        self.up_button = ttk.Button(self, text="↑", width=3, command=self.move_up)
        self.up_button.pack(side="right", padx=2)

        self.down_button = ttk.Button(self, text="↓", width=3, command=self.move_down)
        self.down_button.pack(side="right", padx=2)

    def move_up(self):
        self.controller.move_section(self, direction="up")

    def move_down(self):
        self.controller.move_section(self, direction="down")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Barony Scroll Recorder")
        self.geometry("400x900")

        self.section_container = ttk.Frame(self)
        self.section_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.sections = []
        self.create_sections(["ZELGO", "JUYED", "NR 9", "NOBARY", "PRATY", "DAIYEN", "LEP GEX", "PRIRU", "ELBIB", "VERR", "VENZAR", "THARR", "YUM YUM", "ELAM ELBOW", "DUAM", "ANDOVA", "KIRJE", "VE FORBRY", "HACKEM", "VELOX", "FOOBIE", "TEMOV", "GARVEN", "READ ME"])

        reset_button = ttk.Button(self, text="Reset", width=10, command=self.reset)
        reset_button.pack(pady =(5,10))

        save_btn = ttk.Button(self, text="Save", command=self.save_state)
        save_btn.pack(pady=(0, 5))

        self.save_file = "save.json"

        self.load_state()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_sections(self, titles):
        for title in titles:
            section = RowSection(self.section_container, title=title, controller=self)
            self.sections.append(section)
            section.pack(fill="x", pady=5)

    def move_section(self, section, direction):
        idx = self.sections.index(section)
        if direction == "up" and idx > 0:
            self.sections[idx], self.sections[idx - 1] = self.sections[idx - 1], self.sections[idx]
        elif direction == "down" and idx < len(self.sections) - 1:
            self.sections[idx], self.sections[idx + 1] = self.sections[idx + 1], self.sections[idx]
        else:
            return

        #Repack in new order, could optimize
        for sec in self.sections:
            sec.pack_forget()
            sec.pack(fill="x", pady=5)

    def reset(self):
        for section in self.sections:
            section.combo.set("Unkown")

    def save_state(self):
        data = {section.title: section.combo.get() for section in self.sections}
        with open(self.save_file, "w") as f:
            json.dump(data, f)

    def load_state(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                data = json.load(f)
            for section in self.sections:
                if section.title in data:
                    section.combo.set(data[section.title])

    def on_close(self):
        self.save_state()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
