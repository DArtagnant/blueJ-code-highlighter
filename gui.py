import tkinter as tk
from tkinter import filedialog
from os import path
import webbrowser
import sys
from traceback import print_exception

from highlight import from_file as highlight_from_file

def open_in_browser(url):
    webbrowser.open_new_tab(url)

def read_only_except_ctrlca(event):
    if event.state == 12 and event.keysym in ('c', 'a'):
        return
    else:
        return "break"

class MainGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("BlueJ-code-highlighter")
        self.geometry("400x400")
        container = tk.Frame(self, height=400, width=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.source_file = None
        self.output_dir = None

        self.frames = {}
        for cls_frame in (MainPage,):
            frame = cls_frame(container, self)
            self.frames[cls_frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)

    def show_frame(self, cls):
        frame = self.frames[cls]
        frame.tkraise()

    @property
    def ready_to_convert(self):
        return self.source_file is not None and self.output_dir is not None
    
    def select_source_file(self, *, then_rebuild):
        given_path = filedialog.askopenfilename(title="Choisir un fichier source")
        if given_path != "" and path.exists(given_path):
            self.source_file = given_path
            print(f"fichier source sélectionné : '{self.source_file}'")
        else:
            self.source_file = None
            print("fichier incorrect.")
        for frame in then_rebuild:
            frame.build()
    
    def select_output_dir(self, *, then_rebuild):
        given_path = filedialog.askdirectory(title="Choisir un dossier destination")
        if given_path != "" and path.exists(given_path):
            self.output_dir = given_path
            print(f"dossier de sortie sélectionné : '{self.output_dir}'")
        else:
            self.output_dir = None
            print("dossier incorrect.")
        for frame in then_rebuild:
            frame.build()
    
    def convert_file(self, *, then_rebuild):
        if self.ready_to_convert:
            output_file = path.join(self.output_dir, f"{path.splitext(path.basename(self.source_file))[0]}.html") # type: ignore
            print(f"début de la conversion, le fichier html créé se trouvera à : '{output_file}'")
            try:
                highlight_from_file(self.source_file, output_file)
            except Exception as e:
                print("Une erreur s'est produite lors de la conversion. N'hésitez pas à ouvrir une issue github.")
                print_exception(e)
                print("N'hésitez pas à ouvrir une issue github, voir ci-dessous")
            else:
                open_in_browser(output_file)


class MainPage(tk.Frame):
    def __init__(self, parent, controller: MainGui):
        super().__init__(parent)
        self.controller = controller

        label_bienvenue = tk.Label(self, text="Bienvenue sur BlueJ-code-highlighter")
        label_bienvenue.pack(padx=10, pady=10)

        label_issue = tk.Label(
            self,
            text="en cas d'erreur, cliquer ici pour ouvrir une issue",
            cursor='hand2',
        )
        label_issue.bind('<Button-1>', lambda _: open_in_browser("https://github.com/DArtagnant/blueJ-code-highlighter/issues/new"))
        label_issue.pack(side='bottom', padx=10, pady=(0, 10))

        label_thanks_to = tk.Label(
            self,
            text="mis en forme grâce à blueJ-code-highlighter de DArtagnant",
            cursor='hand2',
        )
        label_thanks_to.bind('<Button-1>', lambda _: open_in_browser("https://github.com/DArtagnant/blueJ-code-highlighter"))
        label_thanks_to.pack(side='bottom', padx=10, pady=(10, 0))

        self.button_line = ButtonLine(
            self,
            self.controller,
        )
        self.button_line.pack(side='top', fill='x')

        self.convert_file_button = tk.Button(
            self,
            text= "Convertir",
            command=lambda: controller.convert_file(then_rebuild=(self, self.button_line)),
        )
        self.convert_file_button.pack(side='top', fill='x')

        self.text_console = tk.Text(self, wrap='word', height=20, width=80)
        self.text_console.bind("<Key>", lambda e: read_only_except_ctrlca(e))
        self.text_console.pack(expand=True, fill='both')
        sys.stdout = RedirectText(self.text_console)
        sys.stderr = RedirectText(self.text_console)

        self.build()
    
    def build(self):
        self.convert_file_button.config(state= 'normal' if self.controller.ready_to_convert else 'disabled')

class ButtonLine(tk.Frame):
    def __init__(self, parent, controller: MainGui):
        super().__init__(parent)
        self.controller = controller

        self.select_file_button = tk.Button(
            self,
            command=lambda: controller.select_source_file(then_rebuild=(self, parent)),
        )
        self.select_file_button.pack(side='left', fill='both')

        self.arrow_label = tk.Label(
            self,
            text="⇨",
            font=("Arial", 30),
        )
        self.arrow_label.pack(
            side='left',
            fill='both',
            expand=True,    
        )

        self.select_output_button = tk.Button(
            self,
            command=lambda: controller.select_output_dir(then_rebuild=(self, parent)),
        )
        self.select_output_button.pack(side='right', fill='both')

        self.build()
    
    def build(self):
        if self.controller.source_file is not None:
            text = f"Changer de fichier :\n'{path.basename(self.controller.source_file)}'"
        else:
            text = "Sélectionner un fichier java"
        self.select_file_button.config(text=text)

        if self.controller.output_dir is not None:
            text = f"Changer de dossier :\n'{path.basename(self.controller.output_dir)}'"
        else:
            text = "Sélectionner un dossier d'export"
        self.select_output_button.config(text=text)


class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        if string != "\n":
            string = f">>> {string}"
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass
    



if __name__ == "__main__":
    testObj = MainGui()
    testObj.mainloop()