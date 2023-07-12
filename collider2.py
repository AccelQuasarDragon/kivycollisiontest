"""
Basic Pixel Perfect Point Collision in kivy

Overriding the Image's [collide_point] method to use the underlying [core.image.Image]'s
[read_pixel] method and access the alpha information of the colliding pixel.
The [keep_data: True] statement is essential, before assigning (loading) a texture.
A deviation from the [size_hint: None, None] and [size: self.texture_size], along with
the use of [allow_stretch] and other size modifications, could probably be allowed,
by using the [norm_image_size] property, but the scaling and rotation of a ScatterLayout
(as in the current example) works fine as is.
Also note that the image's local [y] coordinate is inverse as far as [read_pixel] is
concerned.
(Could it be the reason why this approach doesn't seem to work with atlases?)

Thanks to niavlys for his 3/14/14 post:
(https://groups.google.com/forum/#!topic/kivy-users/BnjrZT0NkhU)
and to tshirtman for his:
(7/24/14 https://groups.google.com/forum/#!topic/kivy-dev/dpT7yqs_Mq0)

unjuan 2015
"""
# https://groups.google.com/g/kivy-users/c/LBdragxkYDA?pli=1
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_string('''
<RootLayout>:
    CustomImage:
        keep_data: True
        size_hint: None, None
        size: self.texture_size
        pos_hint: {'center_x': .5, 'center_y': .5}
        source: 'sportspersonMASK.jpg'
        opacity: .3
''')


class CustomImage(Image):
    def __init__(self, **kwargs):
        # ################################### un-comment for a python-only version
        # kwargs.setdefault('keep_data', True)
        # kwargs.setdefault('size_hint', (None,None))
        super(CustomImage, self).__init__(**kwargs)
        # self.pos_hint = {'center_x': .5, 'center_y': .5}
        # self.opacity = .3
        #######################################################################

    def collide_point(self, x, y):
        # Do not want to upset the read_pixel method, in case of a bound error
        try:
            color = self._coreimage.read_pixel(x - self.x, self.height - (y - self.y))
        except:
            color = 0, 0, 0, 0
        if color[-1] > 0:
            return True
        return False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 1
        else:
            self.opacity = .3


class RootLayout(ScatterLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
        # ################################### un-comment for python-only version
        # cimage = CustomImage()
        # cimage.source = 'wolf.png'
        # cimage.size = cimage.texture.size
        # self.add_widget(cimage)
        ###########################################################################


class CollTestApp(App):
    def build(self):
        return RootLayout()


if __name__ == '__main__':
    CollTestApp().run()