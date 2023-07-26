# https://stackoverflow.com/questions/58386411/rounded-corners-with-kivy-using-python-only
from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

Config.set("graphics", "width", "500")
Config.set("graphics", "height", "300")

kvString = '''
#:import C kivy.utils.get_color_from_hex
<RoundedButton@Button>:
    canvas.before:
        # Use a Stencil instruction to create the rounded shape
        StencilPush
        Ellipse:
            pos: self.pos
            size: self.size
        StencilUse

        # Draw a clear background
        Color:
            rgba: 0, 0, 0, 0
        Rectangle:
            # texture: self.background_normal.texture
            size: self.size
            pos: self.pos

    canvas.after:
        StencilUnUse
        Ellipse:
            pos: self.pos
            size: self.size
        StencilPop


FloatLayout:
    # RoundedButton:
    RTextInput:
        size_hint: 0.5,0.5
        text: "Hello world!"
        canvas.before:
            # Use a Stencil instruction to create the rounded shape
            StencilPush
            Ellipse:
                pos: self.pos
                size: self.size
            StencilUse

            # Draw a clear background
            Color:
                rgba: 0, 0, 0, 0
            Rectangle:
                # texture: self.background_normal.texture
                size: self.size
                pos: self.pos

        canvas.after:
            StencilUnUse
            Ellipse:
                pos: self.pos
                size: self.size
            StencilPop
    
        # foreground_color: (1,0,0,1)
        # # canvas.before:
        # canvas.after:
        #     Color:
        #         rgba: 0, 1, 0, 1
        #     # Ellipse:
        #     #     pos: self.pos
        #     #     size: self.size
        #     RoundedRectangle:
        #         pos: self.pos
        #         size: self.size
        #         radius: [50, ]  # Adjust the radius to make the corners rounded
        #     StencilPush
        #     RoundedRectangle:
        #         pos: self.pos
        #         size: self.size
        #         radius: [50, ]  # Same radius as before
        #     StencilUse
        #     StencilUnUse
        #     # StencilPop




        # canvas.before:
        #     Color:
        #         rgba: 0, 1, 0, 0.5
        # canvas.after:
        #     Color:
        #         rgba: 1, 0, 0, 0.5
        
        #     # StencilPush
        # #     # create a rectangular mask with a pos of (100, 100) and a (100, 100) size.
        # #     # Rectangle:
        #     RoundedRectangle:
        #         pos: self.pos
        #         size: 50,50
        #         radius: [30, ]
        #     # StencilUse


        # canvas.before:
        #     Color:
        #         rgba: 0, 0, 0, 1
        #     # StencilPush
        #     RoundedRectangle:
        #         pos: self.pos
        #         size: self.size
        #         radius: [30, ]  # Adjust the radius to make the corners rounded
        #     # StencilUse
        #     Color:
        #         rgba: 1, 1, 1, 1  # Set the color for the text (white in this case)
        #     Rectangle:
        #         pos: self.pos
        #         size: self.size
        #     StencilPop
        # # canvas.before:
        # #     RoundedRectangle:
        # #         pos: self.pos
        # #         size: self.size
        # #         radius: [20, ]
        # canvas.before:
        #     Color:
        #         rgba: 0.5, 0.5, 1, 0  #clear bg color
        #         # rgba: root.current_color
        #     # Ellipse:
        #     #     pos: self.pos
        #     #     size: self.size
        # # https://kivy.org/doc/stable/api-kivy.graphics.stencil_instructions.html
        #     # StencilPush
        #     RoundedRectangle:
        #         pos: self.pos
        #         size: self.size
        #         radius: [20, ]
        #     # StencilUse

'''

kvString1 = '''
RoundedCornerLayout:
'''

class RTextInput(TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape_color = Color(rgba=(0.5, .5, .5, .5))
        self.shape = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

class RoundedCornerLayout(FloatLayout):
    def __init__(self):
        super().__init__()

        with self.canvas.before:
            Color(0.4, 0.4, 0.4, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[(40, 40), (40, 40), (20, 20), (20, 20)],
            )
        self.bind(pos=lambda obj, pos: setattr(self.rect, "pos", pos))
        self.bind(size=lambda obj, size: setattr(self.rect, "size", size))

        self.size_hint = (None, None)
        self.size = (400, 200)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.background_color = 0, 0, 0, 1


class MainApp(App):
    def build(self):
        builderAns = Builder.load_string(kvString)
        return builderAns


if __name__ == "__main__":
    MainApp().run()
