from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import Graph, LinePlot
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import numpy as np


def show_popup_window(x_domain, y_min, y_max, root_values, cross_value):
    content = BoxLayout()
    content.add_widget(Label(text=f"Domain of a function: {x_domain} \n"
                                  f"Minimal value of function: {y_min} \n"
                                  f"Maximal value of function: {y_max} \n"
                                  f"Root values: {root_values} \n"
                                  f"Cross with Y line: {cross_value}", size_hint_y=1.0, font_size="22sp"))
    popup_window = Popup(title="Function Analyzer", content=content, size_hint=(None, None), size=(400, 240))
    popup_window.open()


class MainApp(App):
    def build(self):
        return MainGrid()


class MainGrid(BoxLayout):
    math_function = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.function = "1*x**2"
        self.x_min = -1
        self.x_max = 1
        self.y_min = -5
        self.y_max = 5
        self.maxes = 5
        self.step = 0.1
        self.samples = int((self.x_max + abs(self.x_min)) / self.step) + 1
        self.graph = Graph(y_ticks_major=2,
                           x_ticks_major=1,
                           border_color=[1, 1, 0.9, 1],
                           tick_color=[1, 1, 1, 0.7],
                           x_grid=True, y_grid=True,
                           xmin=self.x_min, xmax=self.x_max,
                           ymin=self.y_min, ymax=self.y_max,
                           draw_border=False,
                           x_grid_label=True, y_grid_label=True)

        self.ids.modulation.add_widget(self.graph)
        self.plot_x = np.linspace(self.x_min, self.x_max, self.samples)
        self.plot_y = np.zeros(self.samples)
        self.plot = LinePlot(color=[1, 1, 0, 1], line_width=1.5)
        self.graph.add_plot(self.plot)
        self.update_plot()

    def update_function(self, text):
        self.function = text
        self.update_y_values()
        self.update_graph()

    def update_graph(self):
        self.ids.modulation.remove_widget(self.graph)
        self.samples = int((self.x_max + abs(self.x_min)) / self.step) + 1
        if self.x_max > 30:
            x_ticks = 2
        else:
            x_ticks = 1
        self.graph = Graph(y_ticks_major=round(self.y_max / 5),
                           x_ticks_major=x_ticks,
                           border_color=[1, 1, 0.9, 1],
                           tick_color=[1, 1, 1, 0.7],
                           x_grid=True, y_grid=True,
                           xmin=self.x_min, xmax=self.x_max,
                           ymin=self.y_min, ymax=self.y_max,
                           draw_border=False,
                           x_grid_label=True, y_grid_label=True)

        self.ids.modulation.add_widget(self.graph)
        self.plot = LinePlot(color=[1, 1, 0, 1], line_width=1.5)
        self.graph.add_plot(self.plot)
        self.update_plot()

    def update_plot(self):
        self.plot_x = np.linspace(self.x_min, self.x_max, self.samples)
        self.plot.points = [(x, eval(self.function)) for x in self.plot_x]

    def update_y_values(self):
        self.update_samples()
        self.plot_x = np.linspace(self.x_min, self.x_max, self.samples)
        self.maxes = [(x, eval(self.function)) for x in self.plot_x]

        list_max = []
        for vector in self.maxes:
            list_max.append(vector[1])
        self.y_max = int(max(list_max))

        list_min = []
        for vector in self.maxes:
            list_min.append(vector[1])
        self.y_min = int(min(list_min))

    def update_x_min(self, x_min):
        self.x_min = x_min
        self.update_y_values()
        self.update_graph()

    def update_x_max(self, x_max):
        self.x_max = x_max
        self.update_y_values()
        self.update_graph()

    def update_step_x(self, step):
        self.step = step
        self.update_graph()

    def update_samples(self):
        self.samples = int((self.x_max + abs(self.x_min)) / self.step) + 1

    def show_analysis(self):
        x = 0
        cross_value = [x, eval(self.function)]
        root_values = []
        for value in self.plot.points:
            if 0.00001 > value[1] > -0.00001:
                new_value = (round(value[0], 2), 0)
                root_values.extend(new_value)

        domain = f"<{self.x_min} ; {self.x_max}>"
        show_popup_window(domain, self.y_min, self.y_max, root_values, cross_value)


if __name__ == "__main__":
    MainApp().run()
