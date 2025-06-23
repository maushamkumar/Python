import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
import time

# Set minimum Kivy version
kivy.require('2.0.0')

class MessageBubble(Widget):
    def __init__(self, text, is_sent=True, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.is_sent = is_sent
        
        # Create label for message text
        self.label = Label(
            text=text,
            text_size=(None, None),
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1) if is_sent else (0, 0, 0, 1),
            font_size='15sp'
        )
        
        # Calculate text size
        self.label.bind(texture_size=self.update_size)
        self.add_widget(self.label)
        
        # Draw bubble background
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
    def update_size(self, instance, size):
        # Set bubble size based on text
        max_width = Window.width * 0.7
        text_width = min(size[0] + dp(24), max_width)
        text_height = size[1] + dp(20)
        
        self.size = (text_width, text_height)
        self.label.text_size = (text_width - dp(24), None)
        
        # Position label inside bubble - center it properly
        self.label.pos = (self.x + dp(12), self.y + dp(10))
        self.label.size = (text_width - dp(24), text_height - dp(20))
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_sent:
                Color(0.25, 0.7, 0.25, 1)  # Better green for sent messages
            else:
                Color(0.95, 0.95, 0.95, 1)  # Light grey for received messages
            
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )
        
        # Update label position when graphics update
        if hasattr(self, 'label'):
            self.label.pos = (self.x + dp(12), self.y + dp(10))

class ChatArea(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create main layout for messages
        self.messages_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            padding=[dp(10), dp(10)]
        )
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        
        self.add_widget(self.messages_layout)
        
        # Auto-scroll to bottom
        self.bind(size=self.update_scroll)
        
    def add_message(self, text, is_sent=True):
        # Create message bubble
        bubble = MessageBubble(text, is_sent)
        
        # Create container for alignment
        container = BoxLayout(
            size_hint_y=None,
            height=dp(60),  # Will be updated based on bubble size
            padding=[dp(15), dp(5)]
        )
        
        if is_sent:
            # Right align for sent messages
            container.add_widget(Widget())  # Spacer
            container.add_widget(bubble)
        else:
            # Left align for received messages
            container.add_widget(bubble)
            container.add_widget(Widget())  # Spacer
        
        # Update container height based on bubble
        def update_container_height(*args):
            container.height = bubble.height + dp(10)
        
        bubble.bind(size=update_container_height)
        Clock.schedule_once(update_container_height, 0.1)
        
        self.messages_layout.add_widget(container)
        
        # Scroll to bottom
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
        
    def scroll_to_bottom(self, *args):
        self.scroll_y = 0
        
    def update_scroll(self, *args):
        Clock.schedule_once(self.scroll_to_bottom, 0.1)

class ChatApp(App):
    def build(self):
        # Set window background color
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(10), dp(5)]
        )
        
        with header.canvas.before:
            Color(0.1, 0.6, 0.1, 1)  # Dark green header
            RoundedRectangle(
                pos=header.pos,
                size=header.size,
                radius=[0]
            )
        
        header_label = Label(
            text='WhatsApp Clone',
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        header.add_widget(header_label)
        header.bind(pos=self.update_header_bg, size=self.update_header_bg)
        
        # Chat area
        self.chat_area = ChatArea()
        
        # Input area
        input_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(10), dp(5)],
            spacing=dp(10)
        )
        
        with input_layout.canvas.before:
            Color(1, 1, 1, 1)  # White background
            RoundedRectangle(
                pos=input_layout.pos,
                size=input_layout.size,
                radius=[0]
            )
        
        # Text input
        self.text_input = TextInput(
            multiline=False,
            hint_text='Type a message...',
            size_hint_x=0.8,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='16sp'
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        # Send button
        send_button = Button(
            text='Send',
            size_hint_x=0.2,
            background_color=(0.1, 0.6, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        send_button.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_button)
        input_layout.bind(pos=self.update_input_bg, size=self.update_input_bg)
        
        # Add all components to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(self.chat_area)
        main_layout.add_widget(input_layout)
        
        # Add some sample messages
        self.add_sample_messages()
        
        return main_layout
    
    def update_header_bg(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.1, 0.6, 0.1, 1)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[0]
            )
    
    def update_input_bg(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[0]
            )
    
    def send_message(self, instance):
        message_text = self.text_input.text.strip()
        if message_text:
            # Add user message (sent)
            self.chat_area.add_message(message_text, is_sent=True)
            self.text_input.text = ''
            
            # Simulate received message after 2 seconds
            Clock.schedule_once(lambda dt: self.simulate_received_message(message_text), 2)
    
    def simulate_received_message(self, original_message):
        # Simple auto-reply logic
        responses = [
            "That's interesting! 🤔",
            "I see what you mean 👍",
            "Thanks for sharing! 😊",
            "Got it! 👌",
            "Haha, that's funny! 😄",
            "Really? Tell me more! 🤗"
        ]
        
        import random
        response = random.choice(responses)
        self.chat_area.add_message(response, is_sent=False)
    
    def add_sample_messages(self):
        # Add some sample messages to show the UI
        sample_messages = [
            ("Hey! How are you doing?", False),
            ("I'm doing great! Just working on some projects 😊", True),
            ("That sounds awesome! What kind of projects?", False),
            ("I'm building a WhatsApp clone using Kivy! It's pretty cool 🚀", True),
            ("Wow, that's amazing! Can you show me how it works?", False),
        ]
        
        for text, is_sent in sample_messages:
            self.chat_area.add_message(text, is_sent)

if __name__ == '__main__':
    ChatApp().run()