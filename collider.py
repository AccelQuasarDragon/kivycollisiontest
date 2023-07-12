# https://stackoverflow.com/questions/63617496/draggable-image-in-kivy
# https://kivy.org/doc/stable/api-kivy.uix.behaviors.drag.html
# https://stackoverflow.com/questions/58800955/kivy-dragbehavior-dragging-more-than-one-widget
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder


# class Box_layout(FloatLayout):
#     def __init__(self, **kwargs):
#         super(Box_layout, self).__init__(**kwargs)
#         self.size_hint = (0.50, 0.50)
#         self.orientation = "vertical"
#         self.add_widget(
#             MoveableImage()
#         )  # drag_rectangle = [self.x, self.y, self.width, self.height],source="temp_plot.png"))


class MoveableImage(DragBehavior, Image):

    def __init__(self, **kwargs):
        super(MoveableImage, self).__init__(**kwargs)
        self.drag_timeout = 10000000
        self.drag_distance = 0
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def on_pos(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

    def on_size(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]

class gameApp(App):
    def build(self):
        # wimg = MoveableImage(source="ranxfrigate.jpg")
        # m = Box_layout()
        kv = """
<MoveableImage>:
    # Define the properties for the MoveableImage
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
FloatLayout:
    MoveableImage:
        source: "ranxfrigate.jpg"
    MoveableImage:
        source: "ranxcruiser.jpg"
# Image:
#     source: "ranxfrigate.jpg"
        """
        return Builder.load_string(kv)


if __name__ == "__main__":
    gameApp().run()
