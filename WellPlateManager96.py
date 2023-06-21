from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex

from kivymd.uix.button import MDFlatButton

from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.toolbar import MDToolbar 
from kivymd.uix.filemanager import MDFileManager 
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel


class RoundButtonGrid(GridLayout):

    def __init__(self, button_colors, **kwargs):
        super(RoundButtonGrid, self).__init__(**kwargs)
        self.cols = 12
        self.spacing = 10
        self.button_colors = button_colors

        for i, color_index in enumerate(self.button_colors):
            button = Button(text=str(i+1),
                            background_normal="",
                            background_color=self.get_color_from_index(color_index),
                            on_release=self.button_pressed)

            self.add_widget(button)


    def get_color_from_index(self, color_index):
        self.colors = [
                get_color_from_hex("#000000"), # black
                get_color_from_hex("#FF0000"), # red
                get_color_from_hex("#00FF00"), # green
                get_color_from_hex("#0000FF"), # blue
        ]
        return self.colors[color_index]


    def button_pressed(self, button):
        button_index = int(button.text)-1
        self.button_colors[button_index] = (self.button_colors[button_index] + 1) % len(self.colors)
        button.background_color = self.colors[self.button_colors[button_index]]
        print(f"button {button.text} pressed!")


class MyApp(MDApp):
    button_colors = None
    spreadsheet = None

    def build(self):

        self.title = "WellPlateManager96"
        self.theme_cls.primary_palette = "Blue"
        
        layout = GridLayout(cols=1)
        toolbar = MDToolbar(title="96-Well Plate")
        toolbar.right_action_items = [
                ["file", lambda x: self.open_file_manager()],
                ["content-save", lambda x: self.show_save_dialog()],
                ["information", lambda x: self.show_explanation_dialog()],
                ["group", lambda x: self.group_samples()],
        ]
        layout.add_widget(toolbar)
        
        if self.button_colors is None:
            self.button_colors = [0 for _ in range(96)]
        layout.add_widget(RoundButtonGrid(button_colors=self.button_colors))


        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.load_file
        )
        
        return layout
    
    def open_file_manager(self):
        self.file_manager.show("./")

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def load_file(self, path):
        print("Selected file:", path)

        if path.endswith(".txt"):
            with open(path) as template:
                button_colors = template.read().split(",")
                button_colors = [int(color) for color in button_colors]

            self.file_manager.close()
            self.button_colors = button_colors
            self.root.clear_widgets()
            self.root.add_widget(self.build())

        
        elif path.endswith(".xlsx"):
            spreadsheet = pd.read_excel(path)
            self.spreadsheet = np.asarray(spreadsheet, order="K") # C, F, A

        else:
            print("not a supported file format")


    def group_samples(self):
        print(self.button_colors)
        if self.spreadsheet is None:
            print("No data loaded")
        else:
            print(self.spreadsheet)

    def show_save_dialog(self):
        content = MDTextField()
        self.dialog = MDDialog(
                title="Save File",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=self.dismiss_save_dialog),
                    MDFlatButton(text="SAVE", on_release=lambda x: self.save_file(content.text))
                ],
        )
        self.dialog.open()


    def dismiss_save_dialog(self, *args):
        self.dialog.dismiss()


    def save_file(self, file_name):
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        self.file_path = file_name

        button_colors_str = ",".join(str(color) for color in self.button_colors)
        with open(self.file_path, "w") as file:
            file.write(button_colors_str)
        print("File saved:", self.file_path)
        self.dialog.dismiss()


    def show_explanation_dialog(self):
        self.dialog = MDDialog(
            title="Color Explanations",
            text="Blank is RED\nQC is GREEN\nSample is BLACK\nSubgroup sample is BLUE",
        )
        self.dialog.open()

if __name__ == '__main__':
    MyApp().run()

