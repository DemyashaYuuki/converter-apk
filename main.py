from kivy.config import Config

Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.textinput import TextInput
import json
import webbrowser

Window.clearcolor = (0.129, 0.129, 0.129, 1)  # #212121

KV = """
#:import dp kivy.metrics.dp

<PlainNumericInput>:
    background_normal: ""
    background_active: ""
    background_color: 0, 0, 0, 0
    foreground_color: 1, 1, 1, 1
    disabled_foreground_color: 1, 1, 1, 1
    hint_text_color: 0.65, 0.65, 0.65, 1
    cursor_color: 1, 1, 1, 1
    selection_color: 0.35, 0.35, 0.35, 0.8
    multiline: False
    write_tab: False
    font_size: "22sp"
    padding: [0, 0, 0, 0]
    size_hint_y: None
    height: dp(30)
    pos_hint: {"center_y": 0.5}

<RoundedSpinner>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    font_size: "17sp"
    sync_height: True
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.radius, self.radius, self.radius, self.radius]
    canvas.after:
        Color:
            rgba: self.border_color
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, self.radius)
            width: 1.1

<DarkSpinnerOption>:
    background_normal: ""
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    font_size: "16sp"
    canvas.before:
        Color:
            rgba: 0.2, 0.2, 0.2, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10), dp(10), dp(10), dp(10)]

<AccentButton>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    bold: True
    font_size: "19sp"
    canvas.before:
        Color:
            rgba: self.current_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.radius, self.radius, self.radius, self.radius]

<SwapButton>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    bold: True
    font_size: "14sp"
    canvas.before:
        Color:
            rgba: self.current_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.radius, self.radius, self.radius, self.radius]
    canvas.after:
        Color:
            rgba: self.border_color
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, self.radius)
            width: 1.1

<ConverterLayout>:
    orientation: "vertical"
    padding: dp(20)
    spacing: dp(12)

    canvas.before:
        Color:
            rgba: 0.129, 0.129, 0.129, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: root.title_text
        color: 1, 1, 1, 1
        bold: True
        font_size: "23sp"
        size_hint_y: None
        height: dp(38)
        halign: "center"
        valign: "middle"
        text_size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(46)
        spacing: dp(10)

        Label:
            text: root.language_text
            color: 0.82, 0.82, 0.82, 1
            font_size: "15sp"
            size_hint_x: 0.35
            halign: "left"
            valign: "middle"
            text_size: self.size

        RoundedSpinner:
            id: language_spinner
            text: "Русский"
            values: root.language_values
            option_cls: "DarkSpinnerOption"
            size_hint_x: 0.65
            on_text: root.on_language_selected(self.text)

    BoxLayout:
        size_hint_y: None
        height: dp(58)
        padding: dp(16), 0, dp(16), 0

        canvas.before:
            Color:
                rgba: 0.2, 0.2, 0.2, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(16), dp(16), dp(16), dp(16)]
        canvas.after:
            Color:
                rgba: 0.28, 0.28, 0.28, 1
            Line:
                rounded_rectangle: (self.x, self.y, self.width, self.height, dp(16))
                width: 1.1

        PlainNumericInput:
            id: amount_input
            hint_text: root.amount_hint_text

    Label:
        text: root.currency_row_text
        color: 0.82, 0.82, 0.82, 1
        font_size: "15sp"
        size_hint_y: None
        height: dp(22)
        halign: "left"
        valign: "middle"
        text_size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(54)
        spacing: dp(8)

        RoundedSpinner:
            id: from_currency
            text: "$ USD"
            values: root.currency_values
            option_cls: "DarkSpinnerOption"
            on_text: root.convert_currency()

        SwapButton:
            text: root.swap_button_text
            size_hint_x: None
            width: dp(58)
            on_release: root.swap_currencies()

        RoundedSpinner:
            id: to_currency
            text: "€ EUR"
            values: root.currency_values
            option_cls: "DarkSpinnerOption"
            on_text: root.convert_currency()

    AccentButton:
        text: root.convert_button_text
        size_hint_y: None
        height: dp(54)
        on_release: root.convert_currency()

    BoxLayout:
        orientation: "vertical"
        size_hint_y: None
        height: dp(112)
        padding: dp(14)
        spacing: dp(6)

        canvas.before:
            Color:
                rgba: 0.2, 0.2, 0.2, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(16), dp(16), dp(16), dp(16)]
        canvas.after:
            Color:
                rgba: 0.28, 0.28, 0.28, 1
            Line:
                rounded_rectangle: (self.x, self.y, self.width, self.height, dp(16))
                width: 1.1

        Label:
            text: root.result_title_text
            color: 0.72, 0.72, 0.72, 1
            font_size: "14sp"
            size_hint_y: None
            height: dp(18)
            halign: "left"
            valign: "middle"
            text_size: self.size

        Label:
            text: root.result_text
            color: 1, 1, 1, 1
            bold: True
            font_size: "27sp"
            halign: "center"
            valign: "middle"
            text_size: self.size

    Label:
        text: root.status_text
        color: 0.68, 0.68, 0.68, 1
        font_size: "13sp"
        size_hint_y: None
        height: dp(34)
        halign: "center"
        valign: "middle"
        text_size: self.size

    Label:
        markup: True
        text: root.attribution_text
        color: 0.55, 0.55, 0.55, 1
        font_size: "12sp"
        size_hint_y: None
        height: dp(20)
        halign: "center"
        valign: "middle"
        text_size: self.size
        on_ref_press: root.open_attribution()

    Widget:
"""


class PlainNumericInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        allowed = "0123456789.,"
        filtered = "".join(ch for ch in substring if ch in allowed)
        filtered = filtered.replace(",", ".")
        if "." in self.text and "." in filtered:
            filtered = filtered.replace(".", "")
        return super().insert_text(filtered, from_undo=from_undo)


class RoundedSpinner(Spinner):
    bg_color = ListProperty([0.2, 0.2, 0.2, 1])
    border_color = ListProperty([0.28, 0.28, 0.28, 1])
    radius = NumericProperty(16)


class DarkSpinnerOption(SpinnerOption):
    pass


class AccentButton(Button):
    radius = NumericProperty(16)
    normal_color = ListProperty([1.0, 0.341, 0.133, 1])
    pressed_color = ListProperty([0.90, 0.28, 0.10, 1])
    current_color = ListProperty([1.0, 0.341, 0.133, 1])

    def on_press(self):
        self.current_color = self.pressed_color

    def on_release(self):
        self.current_color = self.normal_color


class SwapButton(Button):
    radius = NumericProperty(16)
    border_color = ListProperty([0.40, 0.40, 0.40, 1])
    normal_color = ListProperty([0.24, 0.24, 0.24, 1])
    pressed_color = ListProperty([0.32, 0.32, 0.32, 1])
    current_color = ListProperty([0.24, 0.24, 0.24, 1])

    def on_press(self):
        self.current_color = self.pressed_color

    def on_release(self):
        self.current_color = self.normal_color


class ConverterLayout(BoxLayout):
    title_text = StringProperty("")
    language_text = StringProperty("")
    amount_hint_text = StringProperty("")
    currency_row_text = StringProperty("")
    convert_button_text = StringProperty("")
    swap_button_text = StringProperty("")
    result_title_text = StringProperty("")
    result_text = StringProperty("")
    status_text = StringProperty("")
    attribution_text = StringProperty("")
    current_lang = StringProperty("ru")
    last_status_kind = StringProperty("loading")

    language_values = ListProperty(["Русский", "English", "Português (PT)"])
    currency_values = ListProperty(["$ USD", "€ EUR", "₽ RUB", "Br BYN", "₸ KZT"])

    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "RUB": "₽",
        "BYN": "Br",
        "KZT": "₸",
    }

    fallback_rates = {
        "USD": 1.0,
        "EUR": 0.92,
        "RUB": 90.0,
        "BYN": 3.27,
        "KZT": 495.0,
    }

    texts = {
        "ru": {
            "title": "Умный конвертер валют",
            "language": "Язык",
            "amount_hint": "Введите сумму",
            "currencies": "Валюты",
            "convert": "Конвертировать",
            "swap": "SWAP",
            "result_title": "Результат",
            "result_placeholder": "0.00",
            "invalid": "Некорректный ввод",
            "live": "Живые курсы загружены",
            "loading": "Обновление курсов…",
            "fallback": "Нет сети: используются встроенные курсы",
            "source": '[ref=src]Источник курсов[/ref]',
        },
        "en": {
            "title": "Smart Currency Converter",
            "language": "Language",
            "amount_hint": "Enter amount",
            "currencies": "Currencies",
            "convert": "Convert",
            "swap": "SWAP",
            "result_title": "Result",
            "result_placeholder": "0.00",
            "invalid": "Invalid input",
            "live": "Live rates loaded",
            "loading": "Updating rates…",
            "fallback": "Offline: built-in rates are used",
            "source": '[ref=src]Rates source[/ref]',
        },
        "pt": {
            "title": "Conversor Inteligente de Moedas",
            "language": "Idioma",
            "amount_hint": "Introduza o montante",
            "currencies": "Moedas",
            "convert": "Converter",
            "swap": "SWAP",
            "result_title": "Resultado",
            "result_placeholder": "0.00",
            "invalid": "Entrada inválida",
            "live": "Taxas atualizadas carregadas",
            "loading": "A atualizar taxas…",
            "fallback": "Sem internet: a usar taxas internas",
            "source": '[ref=src]Fonte das taxas[/ref]',
        },
    }

    lang_map = {
        "Русский": "ru",
        "English": "en",
        "Português (PT)": "pt",
    }

    def __init__(self, **kwargs):
        self.rates = self.fallback_rates.copy()
        super().__init__(**kwargs)

    def on_kv_post(self, *args):
        self.refresh_texts()
        self.ids.amount_input.bind(text=lambda *_: self.convert_currency())
        Clock.schedule_once(lambda dt: self.refresh_rates(), 0.2)
        Clock.schedule_interval(lambda dt: self.refresh_rates(), 300)

    def tr(self, key):
        return self.texts[self.current_lang][key]

    def refresh_texts(self):
        self.title_text = self.tr("title")
        self.language_text = self.tr("language")
        self.amount_hint_text = self.tr("amount_hint")
        self.currency_row_text = self.tr("currencies")
        self.convert_button_text = self.tr("convert")
        self.swap_button_text = self.tr("swap")
        self.result_title_text = self.tr("result_title")
        self.attribution_text = self.tr("source")

        if not self.result_text:
            self.result_text = self.tr("result_placeholder")

        self.update_status_label()

    def update_status_label(self):
        if self.last_status_kind == "live":
            self.status_text = self.tr("live")
        elif self.last_status_kind == "fallback":
            self.status_text = self.tr("fallback")
        else:
            self.status_text = self.tr("loading")

    def on_language_selected(self, spinner_text):
        self.current_lang = self.lang_map.get(spinner_text, "ru")
        self.refresh_texts()
        self.convert_currency()

    def parse_currency_code(self, spinner_text):
        parts = spinner_text.split()
        return parts[-1] if parts else "USD"

    def convert_currency(self):
        text = self.ids.amount_input.text.strip()

        if not text:
            self.result_text = self.tr("result_placeholder")
            return

        try:
            amount = float(text)
        except ValueError:
            self.result_text = self.tr("invalid")
            return

        from_code = self.parse_currency_code(self.ids.from_currency.text)
        to_code = self.parse_currency_code(self.ids.to_currency.text)

        if from_code == to_code:
            converted = amount
        else:
            amount_in_usd = amount / self.rates[from_code]
            converted = amount_in_usd * self.rates[to_code]

        self.result_text = f"{converted:.2f} {self.currency_symbols[to_code]}"

    def swap_currencies(self):
        from_text = self.ids.from_currency.text
        to_text = self.ids.to_currency.text
        self.ids.from_currency.text = to_text
        self.ids.to_currency.text = from_text
        self.convert_currency()

    def refresh_rates(self):
        self.last_status_kind = "loading"
        self.update_status_label()

        UrlRequest(
            "https://open.er-api.com/v6/latest/USD",
            on_success=self.on_rates_success,
            on_failure=self.on_rates_error,
            on_error=self.on_rates_error,
            timeout=10,
        )

    def on_rates_success(self, request, result):
        try:
            if isinstance(result, (bytes, bytearray)):
                result = json.loads(result.decode("utf-8"))
            elif isinstance(result, str):
                result = json.loads(result)
        except Exception:
            self.on_rates_error(request, "json parse error")
            return

        if not isinstance(result, dict) or result.get("result") != "success":
            self.on_rates_error(request, "invalid response")
            return

        raw_rates = result.get("rates", {})
        updated = {"USD": 1.0}

        for code in ("EUR", "RUB", "BYN", "KZT"):
            value = raw_rates.get(code)
            if isinstance(value, (int, float)):
                updated[code] = float(value)

        if len(updated) == 5:
            self.rates = updated
            self.last_status_kind = "live"
        else:
            self.rates = self.fallback_rates.copy()
            self.last_status_kind = "fallback"

        self.update_status_label()
        self.convert_currency()

    def on_rates_error(self, request, error):
        self.rates = self.fallback_rates.copy()
        self.last_status_kind = "fallback"
        self.update_status_label()
        self.convert_currency()

    def open_attribution(self):
        webbrowser.open("https://www.exchangerate-api.com")


class SmartCurrencyConverterApp(App):
    def build(self):
        Builder.load_string(KV)
        return ConverterLayout()


if __name__ == "__main__":
    SmartCurrencyConverterApp().run()