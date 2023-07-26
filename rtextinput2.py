# https://stackoverflow.com/questions/47639548/kivy-textinput-border-radius
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, RoundedRectangle

kvstring = '''
#:import C kivy.utils.get_color_from_hex

<MyTextInput@TextInput>:
    font_size: '14dp'
    background_color: 0,0,0,0
    # background_color:  0.5, 0.5, 1, 0
    cursor_color: C('#ffffff')
    # canvas.before:
    canvas.after:
        # Color:
        #     rgba: 0.5, 0.5, 1, 0  #clear bg color
            # rgba: root.current_color
        # Ellipse:
        #     pos: self.pos
        #     size: self.size
    # https://kivy.org/doc/stable/api-kivy.graphics.stencil_instructions.html
        # StencilPush
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20, ]
        # StencilUse

    # canvas.before:
    #     Color:
    #         rgba: C('#ffffff')
    # canvas.after:
    #     Color:
    #         rgb: C('#0f192e')
    #     Ellipse:
    #         angle_start:180
    #         angle_end:360
    #         pos:(self.pos[0] - self.size[1]/2.0, self.pos[1])
    #         size: (self.size[1], self.size[1])
    #     Ellipse:
    #         angle_start:360
    #         angle_end:540
    #         pos: (self.size[0] + self.pos[0] - self.size[1]/2.0, self.pos[1])
    #         size: (self.size[1], self.size[1])
    #     Color:
    #         rgba: C('#3f92db')
    #     Line:
    #         points: self.pos[0] , self.pos[1], self.pos[0] + self.size[0], self.pos[1]
    #     Line:
    #         points: self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]
    #     Line:
    #         ellipse: self.pos[0] - self.size[1]/2.0, self.pos[1], self.size[1], self.size[1], 180, 360
    #     Line:
    #         ellipse: self.size[0] + self.pos[0] - self.size[1]/2.0, self.pos[1], self.size[1], self.size[1], 360, 540

BoxLayout:
    orientation:'vertical'
    BoxLayout:
        size_hint_y: 20
        canvas.before:
            Color:
                rgba: C('#3f92db')
            Rectangle:
                pos:self.pos
                size:self.size
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 80
        canvas:
            Color:
                rgba: C('#18294a')
            Rectangle:
                pos:self.pos
                size:self.size
        BoxLayout:
            size_hint_y: 10
        BoxLayout:
            size_hint_y: 20
            orientation:'vertical'
            Label:
                size_hint_y: 8
                text: 'Password'
                color: C('#ffffff')
                font_size:'20dp'
                padding: 5,5
                text_size: self.size
                halign: 'center'
                valign: 'center'
            BoxLayout:
                size_hint_y: 8
                BoxLayout:
                    size_hint_x: 25
                BoxLayout:
                    size_hint_x: 50
                    canvas.before:
                        Color:
                            rgba: C('#0f192e')
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    MyTextInput:
                BoxLayout:
                    size_hint_x: 25
        BoxLayout:
            size_hint_y: 10
        BoxLayout:
            size_hint_y: 20
            orientation:'vertical'
            Label:
                size_hint_y: 8
                text: 'Confirm'
                color: C('#ffffff')
                font_size:'20dp'
                padding: 5,5
                text_size: self.size
                halign: 'center'
                valign: 'center'
            BoxLayout:
                size_hint_y: 8
                BoxLayout:
                    size_hint_x: 25
                BoxLayout:
                    size_hint_x: 50
                    canvas.before:
                        Color:
                            rgba: C('#0f192e')
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    MyTextInput:
                BoxLayout:
                    size_hint_x: 25
        BoxLayout:
            size_hint_y: 40
'''

class TestApp(App):
    def build(self):
        builderAns = Builder.load_string(kvstring)
        return builderAns

if __name__ == '__main__':
    TestApp().run()