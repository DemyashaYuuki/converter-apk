# ============================================================
# RU: Импортируем и настраиваем окно приложения ДО загрузки Kivy.
# EN: Import and configure the app window BEFORE Kivy fully loads.
# PT: Importamos e configuramos a janela da app ANTES do carregamento completo do Kivy.
# ============================================================

from kivy.config import Config

# RU: Фиксируем размер окна, чтобы интерфейс выглядел как "мобильный".
# EN: Lock the window size so the UI looks like a "mobile" screen.
# PT: Fixamos o tamanho da janela para que a interface pareça um ecrã "móvel".
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")
Config.set("graphics", "resizable", "0")

# ============================================================
# RU: Основные импорты Kivy и стандартной библиотеки Python.
# EN: Main Kivy imports and Python standard library imports.
# PT: Importações principais do Kivy e da biblioteca padrão do Python.
# ============================================================

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

# RU: Задаём тёмный цвет фона самого окна приложения.
# EN: Set the dark background color for the application window itself.
# PT: Definimos a cor escura do fundo da própria janela da aplicação.
Window.clearcolor = (0.129, 0.129, 0.129, 1)  # #212121

# ============================================================
# RU: KV-разметка интерфейса. Здесь описывается внешний вид виджетов.
# EN: KV layout definition. This is where widget appearance is described.
# PT: Definição KV da interface. Aqui descrevemos o aspeto dos widgets.
# ============================================================

KV = """
#:import dp kivy.metrics.dp

# ============================================================
# RU: Поле ввода числа. Это обычный TextInput, упрощённый и стилизованный.
# EN: Numeric input field. This is a simplified and styled TextInput.
# PT: Campo de entrada numérica. É um TextInput simplificado e estilizado.
# ============================================================
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

# ============================================================
# RU: Общий стиль для выпадающих списков валют и языка.
# EN: Shared style for the language and currency dropdown lists.
# PT: Estilo comum para as listas suspensas de idioma e moedas.
# ============================================================
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

# ============================================================
# RU: Стиль элементов внутри раскрытого списка Spinner.
# EN: Style for items inside the opened Spinner dropdown.
# PT: Estilo dos itens dentro da lista aberta do Spinner.
# ============================================================
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

# ============================================================
# RU: Главная яркая кнопка "Конвертировать".
# EN: Main accent "Convert" button.
# PT: Botão principal em destaque "Converter".
# ============================================================
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

# ============================================================
# RU: Кнопка для обмена валют местами.
# EN: Button for swapping the selected currencies.
# PT: Botão para trocar as moedas selecionadas.
# ============================================================
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

# ============================================================
# RU: Корневой макет приложения.
# EN: Root layout of the application.
# PT: Layout principal da aplicação.
# ============================================================
<ConverterLayout>:
    orientation: "vertical"
    padding: dp(20)
    spacing: dp(12)

    # RU: Рисуем сплошной фон всего экрана.
    # EN: Draw a solid background for the whole screen.
    # PT: Desenhamos um fundo sólido para todo o ecrã.
    canvas.before:
        Color:
            rgba: 0.129, 0.129, 0.129, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # RU: Заголовок приложения.
    # EN: Application title.
    # PT: Título da aplicação.
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

    # RU: Строка выбора языка интерфейса.
    # EN: Row for choosing the interface language.
    # PT: Linha para escolher o idioma da interface.
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

    # RU: Контейнер для поля ввода суммы.
    # EN: Container for the amount input field.
    # PT: Contentor do campo de introdução do valor.
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

    # RU: Подпись для блока валют.
    # EN: Label for the currency selection block.
    # PT: Texto do bloco de seleção de moedas.
    Label:
        text: root.currency_row_text
        color: 0.82, 0.82, 0.82, 1
        font_size: "15sp"
        size_hint_y: None
        height: dp(22)
        halign: "left"
        valign: "middle"
        text_size: self.size

    # RU: Одна строка: валюта "из", кнопка обмена, валюта "в".
    # EN: One row: "from" currency, swap button, "to" currency.
    # PT: Uma linha: moeda de origem, botão de troca, moeda de destino.
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

    # RU: Кнопка запуска конвертации вручную.
    # EN: Button for manually triggering conversion.
    # PT: Botão para iniciar manualmente a conversão.
    AccentButton:
        text: root.convert_button_text
        size_hint_y: None
        height: dp(54)
        on_release: root.convert_currency()

    # RU: Карточка с результатом.
    # EN: Card that shows the conversion result.
    # PT: Cartão onde é mostrado o resultado da conversão.
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

    # RU: Подпись состояния: загружены ли живые курсы или используется запасной вариант.
    # EN: Status label: whether live rates are loaded or fallback rates are used.
    # PT: Etiqueta de estado: se as taxas em tempo real foram carregadas ou se está a usar fallback.
    Label:
        text: root.status_text
        color: 0.68, 0.68, 0.68, 1
        font_size: "13sp"
        size_hint_y: None
        height: dp(34)
        halign: "center"
        valign: "middle"
        text_size: self.size

    # RU: Ссылка на источник курсов.
    # EN: Link to the rates source.
    # PT: Ligação para a fonte das taxas.
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

    # RU: Пустой заполнитель внизу, чтобы интерфейс "дышал".
    # EN: Empty spacer at the bottom for breathing room.
    # PT: Espaçador vazio em baixo para dar mais respiro à interface.
    Widget:
"""

# ============================================================
# RU: Класс поля ввода числа.
# EN: Numeric input field class.
# PT: Classe do campo de entrada numérica.
# ============================================================
class PlainNumericInput(TextInput):
    # ------------------------------------------------------------
    # RU: Ограничиваем ввод только цифрами, точкой и запятой.
    # EN: Restrict input to digits, dot and comma.
    # PT: Limitamos a entrada a dígitos, ponto e vírgula.
    # ------------------------------------------------------------
    def insert_text(self, substring, from_undo=False):
        # RU: Разрешённые символы.
        # EN: Allowed characters.
        # PT: Caracteres permitidos.
        allowed = "0123456789.,"

        # RU: Оставляем только разрешённые символы.
        # EN: Keep only the allowed characters.
        # PT: Mantemos apenas os caracteres permitidos.
        filtered = "".join(ch for ch in substring if ch in allowed)

        # RU: Запятую сразу превращаем в точку.
        # EN: Convert comma to dot immediately.
        # PT: Convertimos a vírgula em ponto imediatamente.
        filtered = filtered.replace(",", ".")

        # RU: Не даём пользователю ввести вторую точку.
        # EN: Prevent entering a second dot.
        # PT: Impedimos a introdução de um segundo ponto.
        if "." in self.text and "." in filtered:
            filtered = filtered.replace(".", "")

        # RU: Передаём уже очищенный текст обычному TextInput.
        # EN: Pass the cleaned text to the normal TextInput handler.
        # PT: Passamos o texto limpo para o tratamento normal do TextInput.
        return super().insert_text(filtered, from_undo=from_undo)


# ============================================================
# RU: Кастомный Spinner с дополнительными свойствами цвета и скругления.
# EN: Custom Spinner with extra color and rounding properties.
# PT: Spinner personalizado com propriedades extra de cor e arredondamento.
# ============================================================
class RoundedSpinner(Spinner):
    bg_color = ListProperty([0.2, 0.2, 0.2, 1])
    border_color = ListProperty([0.28, 0.28, 0.28, 1])
    radius = NumericProperty(16)


# ============================================================
# RU: Класс элемента выпадающего списка.
# EN: Dropdown item class.
# PT: Classe de item da lista suspensa.
# ============================================================
class DarkSpinnerOption(SpinnerOption):
    pass


# ============================================================
# RU: Яркая кнопка "Конвертировать" с эффектом нажатия.
# EN: Accent "Convert" button with press effect.
# PT: Botão em destaque "Converter" com efeito ao pressionar.
# ============================================================
class AccentButton(Button):
    radius = NumericProperty(16)
    normal_color = ListProperty([1.0, 0.341, 0.133, 1])
    pressed_color = ListProperty([0.90, 0.28, 0.10, 1])
    current_color = ListProperty([1.0, 0.341, 0.133, 1])

    # RU: При нажатии делаем кнопку темнее.
    # EN: Make the button darker when pressed.
    # PT: Tornamos o botão mais escuro ao pressionar.
    def on_press(self):
        self.current_color = self.pressed_color

    # RU: После отпускания возвращаем обычный цвет.
    # EN: Restore the normal color on release.
    # PT: Restauramos a cor normal ao largar o botão.
    def on_release(self):
        self.current_color = self.normal_color


# ============================================================
# RU: Кнопка обмена валют местами.
# EN: Currency swap button.
# PT: Botão de troca de moedas.
# ============================================================
class SwapButton(Button):
    radius = NumericProperty(16)
    border_color = ListProperty([0.40, 0.40, 0.40, 1])
    normal_color = ListProperty([0.24, 0.24, 0.24, 1])
    pressed_color = ListProperty([0.32, 0.32, 0.32, 1])
    current_color = ListProperty([0.24, 0.24, 0.24, 1])

    # RU: Эффект нажатия.
    # EN: Press effect.
    # PT: Efeito ao pressionar.
    def on_press(self):
        self.current_color = self.pressed_color

    # RU: Возвращаем цвет после отпускания.
    # EN: Restore color after release.
    # PT: Restauramos a cor depois de largar.
    def on_release(self):
        self.current_color = self.normal_color


# ============================================================
# RU: Главный класс приложения. Здесь находится логика интерфейса,
#     тексты, курсы валют, конвертация и обновление данных из интернета.
# EN: Main application class. It contains UI logic, texts, currency rates,
#     conversion logic and online rate updates.
# PT: Classe principal da aplicação. Contém a lógica da interface, textos,
#     taxas de câmbio, lógica de conversão e atualização online das taxas.
# ============================================================
class ConverterLayout(BoxLayout):
    # ------------------------------------------------------------
    # RU: Текстовые свойства, привязанные к Label и Button в интерфейсе.
    # EN: Text properties bound to Labels and Buttons in the interface.
    # PT: Propriedades de texto ligadas aos Labels e Buttons na interface.
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # RU: Список языков, доступных в выпадающем меню.
    # EN: List of languages available in the dropdown menu.
    # PT: Lista de idiomas disponíveis no menu suspenso.
    # ------------------------------------------------------------
    language_values = ListProperty(["Русский", "English", "Português (PT)"])

    # ------------------------------------------------------------
    # RU: Список валют, который видит пользователь.
    # EN: Currency list shown to the user.
    # PT: Lista de moedas mostrada ao utilizador.
    # ------------------------------------------------------------
    currency_values = ListProperty(["$ USD", "€ EUR", "₽ RUB", "Br BYN", "₸ KZT"])

    # ------------------------------------------------------------
    # RU: Символы валют для красивого отображения результата.
    # EN: Currency symbols used for prettier result display.
    # PT: Símbolos das moedas usados para mostrar o resultado de forma mais bonita.
    # ------------------------------------------------------------
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "RUB": "₽",
        "BYN": "Br",
        "KZT": "₸",
    }

    # ------------------------------------------------------------
    # RU: Запасные статические курсы на случай, если интернет недоступен.
    # EN: Fallback static rates used when the internet is unavailable.
    # PT: Taxas estáticas de reserva usadas quando a internet não está disponível.
    # ------------------------------------------------------------
    fallback_rates = {
        "USD": 1.0,
        "EUR": 0.92,
        "RUB": 90.0,
        "BYN": 3.27,
        "KZT": 495.0,
    }

    # ------------------------------------------------------------
    # RU: Все тексты интерфейса на 3 языках.
    # EN: All UI texts in 3 languages.
    # PT: Todos os textos da interface em 3 idiomas.
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # RU: Связываем отображаемое название языка с его внутренним кодом.
    # EN: Map the visible language name to its internal language code.
    # PT: Mapeamos o nome visível do idioma para o seu código interno.
    # ------------------------------------------------------------
    lang_map = {
        "Русский": "ru",
        "English": "en",
        "Português (PT)": "pt",
    }

    # ------------------------------------------------------------
    # RU: Конструктор класса.
    #     Здесь мы загружаем запасные курсы до получения живых.
    # EN: Class constructor.
    #     Here we load fallback rates before live rates are fetched.
    # PT: Construtor da classe.
    #     Aqui carregamos as taxas de reserva antes de obter as taxas reais.
    # ------------------------------------------------------------
    def __init__(self, **kwargs):
        self.rates = self.fallback_rates.copy()
        super().__init__(**kwargs)

    # ------------------------------------------------------------
    # RU: Этот метод вызывается после того, как KV-интерфейс полностью создан.
    #     Здесь мы:
    #     1) подставляем тексты,
    #     2) привязываем пересчёт к вводу текста,
    #     3) запускаем первое обновление курсов,
    #     4) ставим таймер повторного обновления.
    #
    # EN: This method is called after the KV interface is fully created.
    #     Here we:
    #     1) fill UI texts,
    #     2) bind recalculation to text input,
    #     3) start the first rate update,
    #     4) schedule repeated updates.
    #
    # PT: Este método é chamado depois de a interface KV estar totalmente criada.
    #     Aqui:
    #     1) aplicamos os textos da interface,
    #     2) ligamos o recálculo à escrita do utilizador,
    #     3) iniciamos a primeira atualização das taxas,
    #     4) agendamos atualizações periódicas.
    # ------------------------------------------------------------
    def on_kv_post(self, *args):
        self.refresh_texts()
        self.ids.amount_input.bind(text=lambda *_: self.convert_currency())
        Clock.schedule_once(lambda dt: self.refresh_rates(), 0.2)
        Clock.schedule_interval(lambda dt: self.refresh_rates(), 300)

    # ------------------------------------------------------------
    # RU: Удобная функция-помощник: возвращает текст по ключу
    #     в текущем выбранном языке.
    # EN: Helper function: returns text by key in the currently selected language.
    # PT: Função auxiliar: devolve o texto pela chave no idioma atualmente selecionado.
    # ------------------------------------------------------------
    def tr(self, key):
        return self.texts[self.current_lang][key]

    # ------------------------------------------------------------
    # RU: Обновляем все тексты интерфейса при старте и при смене языка.
    # EN: Refresh all interface texts on startup and when the language changes.
    # PT: Atualizamos todos os textos da interface no arranque e ao mudar o idioma.
    # ------------------------------------------------------------
    def refresh_texts(self):
        self.title_text = self.tr("title")
        self.language_text = self.tr("language")
        self.amount_hint_text = self.tr("amount_hint")
        self.currency_row_text = self.tr("currencies")
        self.convert_button_text = self.tr("convert")
        self.swap_button_text = self.tr("swap")
        self.result_title_text = self.tr("result_title")
        self.attribution_text = self.tr("source")

        # RU: Если результат ещё пустой, показываем плейсхолдер.
        # EN: If the result is still empty, show a placeholder.
        # PT: Se o resultado ainda estiver vazio, mostramos um valor placeholder.
        if not self.result_text:
            self.result_text = self.tr("result_placeholder")

        self.update_status_label()

    # ------------------------------------------------------------
    # RU: Обновляем нижний статус в зависимости от состояния курсов:
    #     loading / live / fallback.
    # EN: Update the bottom status depending on rate state:
    #     loading / live / fallback.
    # PT: Atualiza o estado inferior conforme o estado das taxas:
    #     loading / live / fallback.
    # ------------------------------------------------------------
    def update_status_label(self):
        if self.last_status_kind == "live":
            self.status_text = self.tr("live")
        elif self.last_status_kind == "fallback":
            self.status_text = self.tr("fallback")
        else:
            self.status_text = self.tr("loading")

    # ------------------------------------------------------------
    # RU: Обработчик выбора языка.
    #     Меняет внутренний код языка, обновляет интерфейс и пересчитывает результат.
    # EN: Language selection handler.
    #     Changes the internal language code, refreshes the UI and recalculates the result.
    # PT: Manipulador da escolha do idioma.
    #     Altera o código interno do idioma, atualiza a interface e recalcula o resultado.
    # ------------------------------------------------------------
    def on_language_selected(self, spinner_text):
        self.current_lang = self.lang_map.get(spinner_text, "ru")
        self.refresh_texts()
        self.convert_currency()

    # ------------------------------------------------------------
    # RU: Из строки вида "$ USD" получаем только код валюты: "USD".
    # EN: Extract the currency code from a string like "$ USD".
    # PT: Extrai o código da moeda de uma string como "$ USD".
    # ------------------------------------------------------------
    def parse_currency_code(self, spinner_text):
        parts = spinner_text.split()
        return parts[-1] if parts else "USD"

    # ------------------------------------------------------------
    # RU: Главная функция конвертации.
    #     Шаги:
    #     1) читаем текст из поля ввода,
    #     2) проверяем, что он не пустой,
    #     3) пытаемся превратить его в число,
    #     4) узнаём выбранные валюты,
    #     5) переводим сумму в USD,
    #     6) переводим USD в целевую валюту,
    #     7) показываем результат.
    #
    # EN: Main conversion function.
    #     Steps:
    #     1) read text from the input field,
    #     2) check that it is not empty,
    #     3) try to convert it to a number,
    #     4) get selected currencies,
    #     5) convert the amount to USD,
    #     6) convert USD to the target currency,
    #     7) display the result.
    #
    # PT: Função principal de conversão.
    #     Passos:
    #     1) ler o texto do campo,
    #     2) verificar se não está vazio,
    #     3) tentar convertê-lo para número,
    #     4) obter as moedas selecionadas,
    #     5) converter o valor para USD,
    #     6) converter USD para a moeda de destino,
    #     7) mostrar o resultado.
    # ------------------------------------------------------------
    def convert_currency(self):
        text = self.ids.amount_input.text.strip()

        # RU: Если поле пустое — показываем стандартное значение.
        # EN: If the field is empty, show the default placeholder value.
        # PT: Se o campo estiver vazio, mostramos o valor placeholder.
        if not text:
            self.result_text = self.tr("result_placeholder")
            return

        # RU: Пробуем превратить ввод в число.
        # EN: Try converting user input into a number.
        # PT: Tentamos converter a entrada do utilizador para número.
        try:
            amount = float(text)
        except ValueError:
            # RU: Если ввод сломан — показываем ошибку.
            # EN: If input is invalid, show an error.
            # PT: Se a entrada for inválida, mostramos um erro.
            self.result_text = self.tr("invalid")
            return

        # RU: Определяем исходную и целевую валюту.
        # EN: Determine source and target currencies.
        # PT: Determinar a moeda de origem e a de destino.
        from_code = self.parse_currency_code(self.ids.from_currency.text)
        to_code = self.parse_currency_code(self.ids.to_currency.text)

        # RU: Если валюты одинаковые — ничего считать не надо.
        # EN: If both currencies are the same, no conversion is needed.
        # PT: Se ambas as moedas forem iguais, não é necessário converter.
        if from_code == to_code:
            converted = amount
        else:
            # RU: Сначала переводим исходную сумму в USD.
            # EN: First convert the source amount to USD.
            # PT: Primeiro convertemos o valor de origem para USD.
            amount_in_usd = amount / self.rates[from_code]

            # RU: Потом из USD — в целевую валюту.
            # EN: Then convert from USD to the target currency.
            # PT: Depois convertemos de USD para a moeda de destino.
            converted = amount_in_usd * self.rates[to_code]

        # RU: Форматируем результат с двумя знаками после запятой.
        # EN: Format the result with two decimal places.
        # PT: Formatamos o resultado com duas casas decimais.
        self.result_text = f"{converted:.2f} {self.currency_symbols[to_code]}"

    # ------------------------------------------------------------
    # RU: Меняем выбранные валюты местами и сразу пересчитываем результат.
    # EN: Swap selected currencies and immediately recalculate the result.
    # PT: Trocamos as moedas selecionadas e recalculamos o resultado imediatamente.
    # ------------------------------------------------------------
    def swap_currencies(self):
        from_text = self.ids.from_currency.text
        to_text = self.ids.to_currency.text
        self.ids.from_currency.text = to_text
        self.ids.to_currency.text = from_text
        self.convert_currency()

    # ------------------------------------------------------------
    # RU: Запускаем загрузку живых курсов из интернета.
    #     Если запрос пройдёт успешно — вызовется on_rates_success.
    #     Если нет — on_rates_error.
    #
    # EN: Start loading live exchange rates from the internet.
    #     If the request succeeds, on_rates_success is called.
    #     Otherwise, on_rates_error is called.
    #
    # PT: Iniciamos o carregamento das taxas em tempo real da internet.
    #     Se o pedido resultar, será chamado on_rates_success.
    #     Caso contrário, será chamado on_rates_error.
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # RU: Обработчик успешного ответа от API курсов.
    #     Здесь мы:
    #     1) приводим ответ к словарю Python,
    #     2) проверяем, что ответ успешный,
    #     3) достаём нужные валюты,
    #     4) обновляем self.rates,
    #     5) обновляем статус и пересчитываем результат.
    #
    # EN: Handler for a successful rates API response.
    #     Here we:
    #     1) convert the response into a Python dictionary,
    #     2) check that the response is successful,
    #     3) extract required currencies,
    #     4) update self.rates,
    #     5) refresh status and recalculate the result.
    #
    # PT: Manipulador de resposta bem-sucedida da API de taxas.
    #     Aqui:
    #     1) convertemos a resposta para dicionário Python,
    #     2) verificamos se a resposta foi bem-sucedida,
    #     3) extraímos as moedas necessárias,
    #     4) atualizamos self.rates,
    #     5) atualizamos o estado e recalculamos o resultado.
    # ------------------------------------------------------------
    def on_rates_success(self, request, result):
        # RU: Иногда ответ приходит как bytes или str — приводим к dict.
        # EN: Sometimes the response arrives as bytes or str — convert it to dict.
        # PT: Por vezes a resposta chega como bytes ou str — convertemos para dict.
        try:
            if isinstance(result, (bytes, bytearray)):
                result = json.loads(result.decode("utf-8"))
            elif isinstance(result, str):
                result = json.loads(result)
        except Exception:
            self.on_rates_error(request, "json parse error")
            return

        # RU: Проверяем, что API действительно ответил успехом.
        # EN: Check that the API actually returned success.
        # PT: Verificamos se a API respondeu realmente com sucesso.
        if not isinstance(result, dict) or result.get("result") != "success":
            self.on_rates_error(request, "invalid response")
            return

        # RU: Достаём таблицу курсов.
        # EN: Extract the rates table.
        # PT: Extraímos a tabela de taxas.
        raw_rates = result.get("rates", {})
        updated = {"USD": 1.0}

        # RU: Забираем только нужные нам валюты.
        # EN: Keep only the currencies we need.
        # PT: Mantemos apenas as moedas de que precisamos.
        for code in ("EUR", "RUB", "BYN", "KZT"):
            value = raw_rates.get(code)
            if isinstance(value, (int, float)):
                updated[code] = float(value)

        # RU: Если все нужные курсы получены — используем их.
        #     Иначе возвращаемся к запасным.
        # EN: If all required rates are available, use them.
        #     Otherwise, fall back to built-in rates.
        # PT: Se todas as taxas necessárias estiverem disponíveis, usamos essas.
        #     Caso contrário, usamos as taxas internas.
        if len(updated) == 5:
            self.rates = updated
            self.last_status_kind = "live"
        else:
            self.rates = self.fallback_rates.copy()
            self.last_status_kind = "fallback"

        self.update_status_label()
        self.convert_currency()

    # ------------------------------------------------------------
    # RU: Обработчик ошибки при запросе курсов.
    #     Используем запасные курсы и показываем статус fallback.
    # EN: Error handler for rate requests.
    #     Use fallback rates and show fallback status.
    # PT: Manipulador de erro para pedidos de taxas.
    #     Usa taxas de reserva e mostra o estado fallback.
    # ------------------------------------------------------------
    def on_rates_error(self, request, error):
        self.rates = self.fallback_rates.copy()
        self.last_status_kind = "fallback"
        self.update_status_label()
        self.convert_currency()

    # ------------------------------------------------------------
    # RU: Открываем сайт-источник курсов в браузере.
    # EN: Open the rate source website in the browser.
    # PT: Abrimos o site da fonte das taxas no navegador.
    # ------------------------------------------------------------
    def open_attribution(self):
        webbrowser.open("https://www.exchangerate-api.com")


# ============================================================
# RU: Класс самого приложения.
#     Метод build():
#     1) загружает KV-разметку,
#     2) создаёт и возвращает корневой виджет ConverterLayout.
#
# EN: Main application class.
#     The build() method:
#     1) loads the KV layout,
#     2) creates and returns the root ConverterLayout widget.
#
# PT: Classe principal da aplicação.
#     O método build():
#     1) carrega a interface KV,
#     2) cria e devolve o widget principal ConverterLayout.
# ============================================================
class SmartCurrencyConverterApp(App):
    def build(self):
        Builder.load_string(KV)
        return ConverterLayout()


# ============================================================
# RU: Точка входа в программу.
# EN: Program entry point.
# PT: Ponto de entrada do programa.
# ============================================================
if __name__ == "__main__":
    SmartCurrencyConverterApp().run()
