from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

# Define the KV language string for the custom TextInput
Builder.load_string('''
<RoundedTextInput>:
    canvas.before:
        Color:
            rgba: 0.8, 0.8, 0.8, 1  # Set the background color (light gray in this case)
        StencilPush
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10, ]  # Adjust the radius to make the corners rounded
        StencilUse
        Color:
            rgba: 1, 1, 1, 1  # Set the color for the text (white in this case)
        Rectangle:
            pos: self.pos
            size: self.size
        StencilPop
''')

class RoundedTextInput(TextInput):
    pass

class MyApp(App):
    def build(self):
        return RoundedTextInput(multiline=False, size_hint=(None, None), size=(200, 50))

if __name__ == '__main__':
    MyApp().run()