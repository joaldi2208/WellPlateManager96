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


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#import seval
import re

class ArithmeticOperation():
    def __init__(self, elementA, elementB):
        self.elementA = elementA
        self.elementB = elementB

    def addition(self):
        return self.elementA + self.elementB

    def subtraction(self):
        return self.elementA - self.elementB

    def multiplication(self):
        return self.elementA * self.elementB

    def division(self):
        return self.elementA / self.elementB



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
                get_color_from_hex("#8B0000"), # red4
                get_color_from_hex("#00FF00"), # green
                get_color_from_hex("#008B00"), # green
                get_color_from_hex("#00008B"), # blue4
                get_color_from_hex("#FFFF00"), # yellow
                get_color_from_hex("#8B8B00"), # yellow4
                get_color_from_hex("#A020F0"), # purple
                get_color_from_hex("#551A8B"), # purple4
                get_color_from_hex("#FF8C00"), # darkOrange
                get_color_from_hex("#8B4500"), # darkOrange4
                get_color_from_hex("#FFC1C1"), # rosyBrown1
                get_color_from_hex("#CD9B9B"), # rosybrown3
                get_color_from_hex("#00FFFF"), # cyan
                get_color_from_hex("#008B8B"), # cyan4
                get_color_from_hex("#800000"), # maroon
                get_color_from_hex("#FFD700"), # gold
                get_color_from_hex("#00FF7F"), # sprintGreen
                get_color_from_hex("#D2691E"), # chocolate
                get_color_from_hex("#8A2BE2"), # blueViolet
                get_color_from_hex("#4B0082"), # indigo
                get_color_from_hex("#FF1493"), # deepPink
                get_color_from_hex("#7FFF00"), # chartreuse
                get_color_from_hex("#FF69B4"), # hotPink
                get_color_from_hex("#FFFFFF"), # white
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
    samples_col = None

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
                ["calculator", lambda x: self.show_arithmetic_dialog()],
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
            self.spreadsheet = pd.read_excel(path, index_col=0)
            n_cols = self.spreadsheet.shape[1]
            self.spreadsheet.columns = [i+1 for i in range(n_cols)]

            self.file_manager.close()
            empty_cols = self.spreadsheet.columns[self.spreadsheet.isna().all()]
            # white color for empty samples
            for empty_col in empty_cols:
                col_index = empty_col - 1
                self.button_colors[col_index] = 25
            self.button_colors[n_cols:] = [25 for _ in range(96-n_cols)]
            
            self.spreadsheet.dropna()
            self.root.clear_widgets()
            self.root.add_widget(self.build())


        else:
            print("not a supported file format")


    def group_samples(self):
        #print(self.button_colors)
        if self.spreadsheet is None:
            print("No data loaded")
        else:
            self.grouped_samples = []
            colors = np.array(self.button_colors)

            self.grouped_samples.append( np.where(colors == 0)[0] )
            self.grouped_samples.append( np.where(colors == 1)[0] )
            self.grouped_samples.append( np.where(colors == 2)[0] )
            self.grouped_samples.append( np.where(colors == 3)[0] )
            self.grouped_samples.append( np.where(colors == 4)[0] )
            self.grouped_samples.append( np.where(colors == 5)[0] )
            self.grouped_samples.append( np.where(colors == 6)[0] )
            self.grouped_samples.append( np.where(colors == 7)[0] )
            self.grouped_samples.append( np.where(colors == 8)[0] )
            self.grouped_samples.append( np.where(colors == 9)[0] )
            self.grouped_samples.append( np.where(colors == 10)[0] )
            self.grouped_samples.append( np.where(colors == 11)[0] )
            self.grouped_samples.append( np.where(colors == 12)[0] )
            self.grouped_samples.append( np.where(colors == 13)[0] )
            self.grouped_samples.append( np.where(colors == 14)[0] )
            self.grouped_samples.append( np.where(colors == 15)[0] )
            self.grouped_samples.append( np.where(colors == 16)[0] )
            self.grouped_samples.append( np.where(colors == 18)[0] )
            self.grouped_samples.append( np.where(colors == 19)[0] )
            self.grouped_samples.append( np.where(colors == 20)[0] )
            self.grouped_samples.append( np.where(colors == 21)[0] )
            self.grouped_samples.append( np.where(colors == 22)[0] )
            self.grouped_samples.append( np.where(colors == 23)[0] )
            self.grouped_samples.append( np.where(colors == 24)[0] )
            self.grouped_samples.append( np.where(colors == 25)[0] )
            
            print(self.spreadsheet)


    def show_arithmetic_dialog(self):
        content = MDTextField()
        self.dialog = MDDialog(
                title="arithmetic",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=self.dismiss_save_dialog),
                    MDFlatButton(text="CALCULATE", on_release=lambda x: self.basic_arithmetic(content.text))
                ],
        )
        self.dialog.open()

    def basic_arithmetic(self, arithmetic_operation):
        """
        until now only two different element can make one arithmetic operation
        """
        def logistic_growth(t, N0, r, K):
            return K / (1 + (K / N0 - 1) * np.exp(-r * t))

        print(arithmetic_operation)

        color_table = {
                "black": 0,
                "lightred": 1,
                "darkred": 2,
                "lightgreen": 3,
                "darkgreen": 4,
                "darkblue": 5,
                "lightyellow": 6,
                "darkyellow": 7,
                "lightpurple": 8,
                "darkpurple": 9,
                "lightorange": 10,
                "darkorange": 11,
                "lightbrown": 12,
                "darkbrown": 13,
                "lightcyan": 14,
                "darkcyan": 15,
                "maroon": 16,
                "gold": 17,
                "sprintGreen": 18,
                "chocolate": 19,
                "blueViolet": 20,
                "indigo": 21,
                "deepPink": 22,
                "chartreuse": 23,
                "hotPink": 24,
                }
        
        allowed_operators = r"[\+\-\*\/]+"
        groups = re.split(allowed_operators, arithmetic_operation)
        used_operators = re.findall(allowed_operators, arithmetic_operation)
        codes = [color_table[color] for color in groups]
    
        print(groups)
        print(codes)
        print(used_operators)
        
        color_locations = []
        for code in codes:
            locations = self.grouped_samples[code]
            # index vs real location
            locations = [location + 1 for location in locations]
            color_locations.append(locations)
        
       #----------------------------mean of groupint---------------# 

        grouped_mean = []
        for locations in color_locations:
           column_mean = self.spreadsheet[locations].mean(axis=1)
           grouped_mean.append(column_mean)


        Calculation = ArithmeticOperation(grouped_mean[0], grouped_mean[1])

        if used_operators[0] == "+":
            Sum = Calculation.addition()
            print(Sum)
        elif used_operators[0] == "-":
            Diff = Calculation.subtraction()
            print(Diff)
            params, _ = curve_fit(logistic_growth, self.spreadsheet.index.to_list(), Diff.to_list())
            N0_fit, r_fit, K_fit = params
            t_fit = np.linspace(0,172800, 10000)

            N_fit = logistic_growth(t_fit, N0_fit, r_fit, K_fit)
            plt.scatter(self.spreadsheet.index, Diff, color="black", label="Data")
            plt.plot(t_fit, N_fit, label="Fit")
            plt.xlabel("Time")
            plt.ylabel("Population Size")
            plt.legend()

            plt.show()
        elif used_operators[0] == "*":
            Prod = Calculation.multiplication()
            print(Prod)
        elif used_operators[0] == "/":
            Quot = Calculation.division()
            print(Quot)


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

