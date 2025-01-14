import customtkinter

from models import PoetryAnalyzer

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Poetry Analysis Tool")
        self.geometry("1080x720")

        self.container = customtkinter.CTkFrame(self)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frames = {}

        for F in (StartUpFrame, LoadFrame, GenerationFrame, ResultFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
            

        self.change_frame(StartUpFrame)
        self.poetry_analyzer = None

    def change_frame(self, f):
        frame = self.frames[f]
        frame.tkraise()
        self.update()

class GenerationFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.frame = customtkinter.CTkFrame(self)
        self.title_text = customtkinter.CTkLabel(self.frame, text="Poem Generator", font=("Arial", 35))
        self.info_text = customtkinter.CTkLabel(self.frame, text="If you wish to generate a poem in the style of an author, enter the name below. \nIf you wish for the poem to be about a certain theme you can enter the theme below.", fg_color="gray30", corner_radius=6)
        self.inputs = customtkinter.CTkFrame(self.frame)
        self.generate_button = customtkinter.CTkButton(self.frame, text="Generate Poem", command=self.on_click_generate_button)
        self.author_entry = customtkinter.CTkEntry(self.inputs, placeholder_text="author")
        self.theme_entry = customtkinter.CTkEntry(self.inputs, placeholder_text="theme")
        
        self.title_text.grid(row=0, column=0, padx=10, pady=10)
        self.author_entry.grid(row=0, column=0, padx=10, pady=10)
        self.theme_entry.grid(row=0, column=1, padx=10, pady=10)
        self.info_text.grid(row=1, column=0, padx=10, pady=10)
        self.inputs.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.generate_button.grid(row=3, column=0, padx=20, pady=20, columnspan=2)
        self.grid_columnconfigure(0, weight=1)
        self.inputs.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid(column=0, row=0)
        self.grid_rowconfigure(0, weight=1)

    def on_click_generate_button(self):
        author = self.author_entry.get()
        theme = self.theme_entry.get()
        if not author:
            author = None
        if not theme:
            theme = None
        self.master.change_frame(LoadFrame)
        poem, analysis = self.master.poetry_analyzer(author, theme)
        self.master.frames[ResultFrame].update_data(poem, analysis)
        self.master.change_frame(ResultFrame)

class ResultFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.frame = customtkinter.CTkFrame(self)
        self.content_frame = customtkinter.CTkFrame(self.frame)
        self.poem_label = customtkinter.CTkLabel(self.content_frame, text="", padx=10, pady=10)
        self.analysis_label = customtkinter.CTkLabel(self.content_frame, text="", padx=10, pady=10)
        self.new_poem_button = customtkinter.CTkButton(self.frame, text="New Poem", command=self.on_click_new_poem_button)
        self.title_label = customtkinter.CTkLabel(self.frame, text="Poem Analysis", font=("Arial", 35))
        
        self.frame.grid(row=0, column=0)
        self.title_label.grid(column=0, row=0)
        self.poem_label.grid(column=0, row=0)
        self.analysis_label.grid(column=1, row=0)
        self.content_frame.grid(row=1, column=0)
        self.new_poem_button.grid(row=2, column=0, padx=10, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure((0, 1), weight=1)

    def update_data(self, poem, analysis):
        self.poem_label.configure(text=poem)
        analysis_labels = list(map(lambda x: x["label"], analysis))
        analysis_string = f"The poem most strongly corresponds with the following emotions: \n{analysis_labels[0]}, {analysis_labels[1]} and {analysis_labels[2]}."
        self.analysis_label.configure(text=analysis_string)

    def on_click_new_poem_button(self):
        self.master.change_frame(GenerationFrame)


class LoadFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = customtkinter.CTkLabel(self, text="Now loading model, please wait.", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.master = master

class StartUpFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.load_model_button = customtkinter.CTkButton(self, text="Load Model", command=self.on_click_load_model_button)
        self.load_model_button.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.master = master

    def on_click_load_model_button(self):
        self.master.change_frame(LoadFrame)
        self.master.poetry_analyzer = PoetryAnalyzer()
        self.master.change_frame(GenerationFrame)

app = App()
app.mainloop()