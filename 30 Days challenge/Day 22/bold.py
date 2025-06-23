from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

class BoldStyleGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super(BoldStyleGenerator, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Input field
        self.input_field = TextInput(
            hint_text="Enter your text",
            multiline=False,
            size_hint=(1, 0.1),
            font_size=20
        )
        self.add_widget(self.input_field)

        # Button
        self.generate_button = Button(
            text="Generate Bold Styles",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.generate_button.bind(on_press=self.generate_styles)
        self.add_widget(self.generate_button)

        # Output area (scrollable)
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.output = Label(size_hint_y=None, text_size=(self.width, None), font_size=18)
        self.output.bind(texture_size=self.update_label_height)
        self.scroll.add_widget(self.output)
        self.add_widget(self.scroll)

    def update_label_height(self, instance, size):
        self.output.height = size[1]

    def bold_styles_generator(self, text):
        styles = [
            ("Bold (Sans)", str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                          "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇")),
            ("Bold (Serif)", str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                           "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳")),
            ("Bold Italic", str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                          "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛")),
        ]
        for label, table in styles:
            yield f"{label}:\n{text.translate(table)}\n"

    def generate_styles(self, instance):
        input_text = self.input_field.text
        output_text = ""
        if input_text:
            for styled in self.bold_styles_generator(input_text):
                output_text += styled + "\n"
        else:
            output_text = "Please enter some text."

        self.output.text = output_text

class BoldTextApp(App):
    def build(self):
        self.title = "Bold Text Generator"
        return BoldStyleGenerator()

if __name__ == '__main__':
    BoldTextApp().run()
