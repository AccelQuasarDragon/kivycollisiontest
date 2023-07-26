# https://stackoverflow.com/questions/35802203/how-do-i-mask-an-image-in-kivy-using-python
from kivy.graphics import *
#^^^^^^ all imports you need for that to work + App()/runTouchApp()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class Root(Widget):
    def __init__(self, **kw):
        super(Root, self).__init__()
        with self.canvas:
            Color(1,0,0,0.5)
            Rectangle(pos=self.pos, size=Window.size)

        bx=BoxLayout(width=Window.width)
        but1=Button(text="mask it!")
        but1.bind(on_release=self.mask)
        but2=Button(text="clear it!")
        but2.bind(on_release=self.clear)

        bx.add_widget(but1)
        bx.add_widget(but2)
        self.add_widget(bx)
        #after few hundred lines of code you'll hate to type even ".add_"
        #binding on_release and other is a way more shorter
        #learn kv, have less troubles :)

    def mask(self, *args):
        with self.canvas:
            #you have to "push" the stencil instructions
            #imagine StencilPush and StencilPop as { and }
            StencilPush()

            #set mask
            Rectangle(pos=[self.pos[0],self.pos[1]+200], size=[100,100])

            #use mask
            StencilUse()

            #draw something and mask will be placed on it
            #Color(1,1,1) for full color, otherwise it tints image
            Color(0,1,0)
            Rectangle(source='<your picture>',\
            pos=[0,0], size=[Window.width-200,Window.height-200])

            #disable Stencil or mask will take effect on everything
            #until StencilPop()
            StencilPop()

            #here it doesn't take effect
            Color(0,1,1)
            Rectangle(pos=[self.pos[0]+200,self.pos[1]+200],\
            size=[Window.width-200,Window.height-200])

            #However here, when StencilPop() and StencilUse()
            #are again, mask is still in the memory
            StencilPush()
            StencilUse()

            #mask is applied... and draws nothing
            #because it's not in the mask's area
            Color(1,1,0)
            Rectangle(pos=[self.pos[0]+200,self.pos[1]+200],\
            size=[Window.width-200,Window.height-200])

            #I think UnUse() is optional
            StencilUnUse()

            #and of course Pop() it
            StencilPop()

    def clear(self, *args):
        self.canvas.clear()
        self.__init__()

class My(App):
    def build(self):
        return Root()

My().run()