from datetime import datetime, timedelta

from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import requests
from kivy.uix.image import Image
import matplotlib.pyplot as plt
from kivy.core.window import Window


class CurrencyConverterApp(App):
    def build(self):
        self.title = 'Currency Converter'
        self.root = ConverterLayout()
        return self.root


class ConverterLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ConverterLayout, self).__init__(**kwargs)


        # Content Layout
        self.orientation = 'vertical'
        self.background_color = (0, 0.5, 0.5, 0.5)
      #  self.spacing = 10
      #  self.padding = 10

        self.cols = 1
        self.spacing = 5  # Odstęp między widgetami wewnątrz GridLayout
        self.padding = [20, 20, 20, 20]

        # Header Label
        header_label = Label(text='Currency Converter', font_size='24sp', color=(0.1, 0.7, 0.3, 1))
        self.add_widget(header_label)

        # Content Layout
      ##  content_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20, 20, 20, 20])

        self.text_input_style = {
            'background_color': (1, 1, 1, 1),  # Granatowe miejsce do wpisywania
            'multiline': False,
            'font_size': '18sp',
            'padding': [10, 10],
            'size_hint_y': None,
            'height': '32sp',  # Zmniejszona wysokość
            'border': (0, 20, 20, 20),
            'font_name': 'DejaVuSans'
        }

        self.label_style = {
            'font_size': '14sp',
            'color': (0.1, 0.7, 0.3, 1),
            'font_name': 'DejaVuSans'
        }

        self.button_style = {
            'size_hint_y': None,
            'height': '32sp',  # Zmniejszona wysokość
            'font_size': '14sp',  # Zmniejszona wielkość czcionki
            'background_color': (0.1, 0.7, 0.3, 1),
            'font_name': 'DejaVuSans'
        }
        self.convert_button = {
            'size_hint_y': None,
           # 'size_hint_x': '5sp',
            'height': '32sp',  # Zmniejszona wysokość
            'font_size': '14sp',  # Zmniejszona wielkość czcionki
            'background_color': (0.1, 0.7, 0.3, 1),
            'padding': [10, 10],
            'font_name': 'DejaVuSans'
        }

        amount_label = Label(text='Amount:', **self.label_style)
        amount_label.size_hint_y = None  # Wymuszamy, aby wysokość etykiety była taka, jak jej zawartość
        amount_label.height = '10sp'
        self.amount_input = TextInput(hint_text='Enter Amount', **self.text_input_style)
        self.add_widget(amount_label)
        self.add_widget(self.amount_input)

        # Add Currency Inputs
        content_layout = BoxLayout(orientation='horizontal', spacing=10)

  ##      self.amount_input = TextInput(hint_text='Enter Amount', **self.text_input_style)

  ##      content_layout.add_widget(self.amount_input)
   ##     self.add_widget(content_layout)



        self.from_currency_input = TextInput(hint_text='From Currency (e.g., USD)', **self.text_input_style)
        self.to_currency_input = TextInput(hint_text='To Currency (e.g., PLN)', **self.text_input_style)

        content_layout.add_widget(self.from_currency_input)
        image = (Image(source='twoarrows.png'))
        image.size_hint = (None, None)
        image.size = (60, 60)
        content_layout.add_widget(image)

        # Zmodyfikuj ścieżkę do własnej grafik
        content_layout.add_widget(self.to_currency_input)
        self.add_widget(content_layout)


        # Add the Content Layout to the Main Layout
        convert_button = Button(text='Convert', on_press=self.convert_currency, **self.convert_button)
        self.add_widget(convert_button)


        self.result_label = Label(text='Converted Amount: ', **self.label_style)
        self.add_widget(self.result_label)



        plot_button = Button(text='Show Trends', on_press=self.show_trends, **self.button_style)
        self.add_widget(plot_button)

        history_button = Button(text='Show History', on_press=self.show_history, **self.button_style)
        self.add_widget(history_button)
        self.conversion_history = []


    def convert_currency(self, instance):
        try:
            amount = float(self.amount_input.text)
            from_currency = self.from_currency_input.text.upper()
            to_currency = self.to_currency_input.text.upper()

            if from_currency == 'PLN':
                amount_in_pln = amount
            else:
                api_url = f'https://api.nbp.pl/api/exchangerates/rates/A/{from_currency}/?format=json'
                response = requests.get(api_url)
                data = response.json()
                exchange_rate = data['rates'][0]['mid']
                amount_in_pln = amount * exchange_rate

            if to_currency == 'PLN':
                converted_amount = amount_in_pln
            else:
                api_url_to_currency = f'https://api.nbp.pl/api/exchangerates/rates/A/{to_currency}/?format=json'
                response_to_currency = requests.get(api_url_to_currency)
                data_to_currency = response_to_currency.json()
                exchange_rate_to_currency = data_to_currency['rates'][0]['mid']
                converted_amount = amount_in_pln / exchange_rate_to_currency

            self.result_label.text = f'Converted Amount: {converted_amount:.2f} {to_currency}'
            conversion_entry = f'{amount:.2f} {from_currency} => {converted_amount:.2f} {to_currency}'
            self.conversion_history.append(conversion_entry)

        except (ValueError, requests.RequestException):
            self.result_label.text = 'Invalid input or unable to fetch exchange rate'

    def show_history(self, instance):
        if not self.conversion_history:
            self.result_label.text = 'No conversion history available.'
            return

        # Display history in a popup
        history_text = '\n'.join(self.conversion_history)
        history_label = Label(text=history_text, **self.label_style)
        history_popup_content = BoxLayout(orientation='vertical')
        history_popup_content.add_widget(history_label)
        history_popup = Popup(title='Conversion History', content=history_popup_content, size_hint=(0.9, 0.9))
        history_popup.open()
    def show_trends(self, instance):
        from_currency = self.from_currency_input.text

        if not from_currency:
            self.result_label.text = 'Please enter valid values.'
            return

        try:
            # Pobierz 30 dni kursów waluty z API NBP
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

            nbp_chart_api_url = f'http://api.nbp.pl/api/exchangerates/rates/a/{from_currency}/{start_date}/{end_date}/?format=json'
            response = requests.get(nbp_chart_api_url)
            data = response.json()

            # Tworzenie wykresu
            dates = [entry['effectiveDate'] for entry in data['rates']]
            rates = [entry['mid'] for entry in data['rates']]

            plt.figure(figsize=(8, 6))
            plt.plot(dates, rates, marker='o')
            plt.title(f'Currency Changes for {from_currency} in the Last 30 Days')
            plt.xlabel('Date')
            plt.ylabel('Mid Rate')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Zapisz wykres do pliku obrazu
            plot_filename = 'currency_changes_plot.png'
            plt.savefig(plot_filename)
            plt.close()

            # Wyświetlenie wykresu jako obrazu
            plot_image = Image(source=plot_filename)
            popup_content = BoxLayout(orientation='vertical')
            popup_content.add_widget(plot_image)
            popup = Popup(title='Currency Changes Plot', content=popup_content, size_hint=(0.9, 0.9))
            popup.open()

        except Exception as e:
            self.result_label.text = f'Failed to retrieve currency data for the plot. Error: {str(e)}'


if __name__ == '__main__':
    CurrencyConverterApp().run()
