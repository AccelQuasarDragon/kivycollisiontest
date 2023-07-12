__author__ = 'bunkus'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import time

class CamApp(App):

    def build(self):
        self.img1=Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        #opencv2 stuffs
        # self.capture = cv2.VideoCapture(0)
        self.capture = cv2.VideoCapture("COSTA RICA IN 4K 60fps HDR (ULTRA HD).mp4")
        ret, testframe = self.capture.read()
        print("ret?", ret)
        # self.capture = cv2.VideoCapture("Elephants Dream charstart2FULL_265.mp4")
        # cv2.namedWindow("CV2 Image")
        # Clock.schedule_interval(self.update, 1.0/60.0)
        return layout

    def update(self, dt):
        ogtime = time.time()
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        if ret:
            # cv2.imshow("CV2 Image", frame)
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.img1.texture = texture1
        print("totaltime", time.time() - ogtime)

if __name__ == '__main__':
    CamApp().run()