from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import numpy as np


class MathFunctionAnalysis(App):
    def build(self):
        self.title = 'Math Functions Analyzer'
        self.root = AppLayout()
        return self.root


class AppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AppLayout, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 20

        self.text = {'background_color': (1, 1, 1, 0.9), 'font_size': '12sp', 'border': (0, 10, 10, 10),
                     'font_name': 'Arial'}

        self.button = {'size_hint_y': None, 'height': '32sp', 'font_size': '14sp',
                       'background_color': (0, 0, 0.9, 1), 'padding': [10, 10], 'font_name': 'Arial'}

        self.header_label = Label(text='Math Function Analyzer', height=50, size_hint=(1, None), font_size='28sp',
                                  color=(1, 1, 1, 0.9))
        self.blank = Label(height=50, color=(1, 1, 1, 0.9))
        self.add_widget(self.blank)

        self.function_input = TextInput(hint_text='Enter your math function', **self.text)
        self.samples_input = TextInput(hint_text='Enter samples', **self.text)
        self.x_min = TextInput(hint_text='Enter x_min', **self.text)
        self.x_max = TextInput(hint_text='Enter x_max', **self.text)

        self.add_widget(self.header_label)
        self.add_widget(self.function_input)
        self.add_widget(self.samples_input)
        self.add_widget(self.x_min)
        self.add_widget(self.x_max)

        self.blank = Label(height=50, color=(1, 1, 1, 0.9))
        self.add_widget(self.blank)

        self.check_button = self.create_button('Calculate your function', self.check_math_function)
        self.add_widget(self.check_button)

        self.blank = Label(height=50, color=(1, 1, 1, 0.9))
        self.add_widget(self.blank)

        self.result_domain = TextInput(hint_text='Domain of function:', **self.text)
        self.result_set_of_values = TextInput(hint_text='Set of values:', **self.text)
        self.result_roots = TextInput(hint_text='Roots:', **self.text)
        self.result_max_min = TextInput(hint_text='Max: Min:', **self.text)
        self.result_multivalued = TextInput(hint_text="Is function multivalued?", **self.text)
        self.result_derivative = TextInput(hint_text="Derivative in x_min: and x_max:", **self.text)
        self.result_internal = TextInput(hint_text="Definite integral in the interval x_min;x_max: ", **self.text)

        self.add_widget(self.result_domain)
        self.add_widget(self.result_set_of_values)
        self.add_widget(self.result_roots)
        self.add_widget(self.result_max_min)
        self.add_widget(self.result_multivalued)
        self.add_widget(self.result_derivative)
        self.add_widget(self.result_internal)

        self.blank = Label(height=50, color=(1, 1, 1, 0.9))
        self.add_widget(self.blank)

    def create_button(self, text, on_press_handler):
        return Button(text=text, on_press=on_press_handler, **self.button)

    def check_fields(self):
        function = self.function_input.text.strip()
        samples = self.samples_input.text.strip()
        x_min = self.x_min.text.strip()
        x_max = self.x_max.text.strip()

        if not function:
            self.function_input.hint_text = 'Please enter a function.'
            return 0, 0, 0, 0

        if not samples:
            self.samples_input.hint_text = 'Please enter samples.'
            return 0, 0, 0, 0

        if not x_min:
            self.x_min.hint_text = 'Please enter x_min.'
            return 0, 0, 0, 0

        if not x_max:
            self.x_max.hint_text = 'Please enter x_max.'
            return 0, 0, 0, 0

        return str(function), int(samples), float(x_min), float(x_max)

    def check_math_function(self, instance):
        function, samples, x_min, x_max = self.check_fields()
        if function == 0 or samples == 0:
            return 0
        function_2 = lambda x: eval(function)

        domain_of_function = self.find_domain_of_function(x_min, x_max)
        self.result_domain.text = "Domain of function is: " + domain_of_function

        set_of_values = self.find_set_of_values(function_2, x_min, x_max, samples)
        if len(set_of_values) > 6:
            middle_len = int(len(set_of_values) / 2)
            self.result_set_of_values.text = (f"Set of values is (too many values to show all): [{set_of_values[0]}, "
                                              f"{set_of_values[middle_len - 1]}, "
                                              f"{set_of_values[middle_len + 1]}, "
                                              f"{set_of_values[-1]}]")
        else:
            self.result_set_of_values.text = f"Set of values is: {set_of_values}"

        roots = self.find_roots(function_2, x_min, x_max, samples)
        self.result_roots.text = f"Roots of function are: {roots}"

        maximum, minimum = self.find_maximum_and_minimum_of_function(function_2, x_min, x_max, samples)
        self.result_max_min.text = f"Maximum of function: {maximum}, Minimum of function: {minimum}"

        multivalued = self.check_multivalued(function_2, x_min, x_max)
        self.result_multivalued.text = multivalued

        derivative_min = self.calculate_derivative(function_2, x_min)
        derivative_max = self.calculate_derivative(function_2, x_max)
        self.result_derivative.text = f"Derivative in x_min: {derivative_min} and x_max: {derivative_max}"

        integral = self.calculate_integral(function_2, x_min, x_max)
        self.result_internal.text = f"Definite integral in the interval x_min;x_max: {integral}"

    @staticmethod
    def find_domain_of_function(x_min, x_max):
        return f"<{x_min}: {x_max}>"

    @staticmethod
    def find_set_of_values(equation, x_min, x_max, samples):
        list_of_x = np.linspace(x_min, x_max, samples)
        set_of_values = []
        for x in list_of_x:
            x = round(x, 2)
            y = equation(x)
            y = round(y, 2)
            value = f"({x}:{y})"
            set_of_values.append(value)
        return set_of_values

    @staticmethod
    def find_roots(equation, x_min, x_max, samples):
        roots = []
        list_of_x = np.linspace(x_min, x_max, samples)

        for x in list_of_x:
            x_val = round(x, 2)
            if equation(x_val) == 0:
                roots.append(x_val)

        if not roots:
            roots = "No roots"
        return roots

    @staticmethod
    def find_maximum_and_minimum_of_function(equation, x_min, x_max, samples):
        list_of_x = np.linspace(x_min, x_max, samples)
        list_of_y = []
        for x in list_of_x:
            x = round(x, 2)
            y = equation(x)
            list_of_y.append(y)
        maximum = float(max(list_of_y))
        minimum = float(min(list_of_y))
        return maximum, minimum

    @staticmethod
    def calculate_derivative(equation, x):
        h = 1e-5
        derivative = (equation(x + h) - equation(x)) / h
        return round(derivative, 3)

    @staticmethod
    def calculate_integral(equation, x_min, x_max):
        integral = 0
        step = 1e-5
        x_val = x_min

        while x_val < x_max:
            integral += equation(x_val) * step
            x_val += step

        return round(integral, 3)

    @staticmethod
    def check_multivalued(equation, x_min, x_max):
        h = 0.1
        values = set()
        x = x_min
        while x <= x_max:
            values.add(equation(x))
            x += h

        if len(values) == (x_max - x_min) / h + 1:
            result = f"Function is multivalued in interval: ({x_min}, {x_max})"
        else:
            result = f"Function is not multivalued in interval: ({x_min}, {x_max})"

        return result


if __name__ == '__main__':
    MathFunctionAnalysis().run()
