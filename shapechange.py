# https://stackoverflow.com/questions/72496870/window-shape-change-not-working-properly-in-kivy
#this just shows u a shaped window as per ^

from kivy.config import Config
Config.set('graphics', 'shaped', 1)

from kivy.resources import resource_find
alpha_shape = resource_find('100x100.png')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock


Builder.load_string('''
<Root>:
    orientation: 'vertical'
    Button:
        text: 'alpha_shape'
        on_release: app.shape_image(self)
        opacity: .5
''')


class Root(BoxLayout):
    pass


class ShapedWindowApp(App):
    shape_image = StringProperty('', force_dispatch=True)

    def build(self):
        Window.size = (100, 100)
        # Clock.schedule_once(self.set_shape)
        return Root()

    def set_shape(self, *args):   
        # Window.shape_image = alpha_shape
        Window.borderless = True
        Window.shape_mode = 'default'
        Window.shape_cutoff = True

    def shape_image(self,*args):
        print("on_release()")
        

if __name__ == '__main__':
    ShapedWindowApp().run()