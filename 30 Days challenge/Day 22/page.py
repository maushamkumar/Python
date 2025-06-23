from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle


# 👇 Custom label with background
class ColoredLabel(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.2)
        self.padding = 10

        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 1)  # Background color (blueish)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Add the label inside this BoxLayout
        self.label = Label(text=text, color=(1, 1, 1, 1))  # White text
        self.add_widget(self.label)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


# 🔐 Login form
class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        Window.size = (400, 300)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Username
        self.add_widget(ColoredLabel("Username"))
        self.username = TextInput(hint_text='Enter username', multiline=False, size_hint=(1, 0.2))
        self.add_widget(self.username)

        # Password
        self.add_widget(ColoredLabel("Password"))
        self.password = TextInput(hint_text='Enter password', password=True, multiline=False, size_hint=(1, 0.2))
        self.add_widget(self.password)

        # Login Button
        self.login_btn = Button(text='Login', size_hint=(1, 0.2), background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        self.login_btn.bind(on_press=self.validate_user)
        self.add_widget(self.login_btn)

    def validate_user(self, instance):
        print(f"Username: {self.username.text}")
        print(f"Password: {self.password.text}")


class MyApp(App):
    def build(self):
        self.title = "Login Form"
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
