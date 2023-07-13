__author__ = 'bunkus'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import time
import numpy as np

class CamApp(App):

    def build(self):
        self.img1=Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        self.capture = cv2.VideoCapture("Elephants Dream charstart2FULL_265.mp4")
        Clock.schedule_interval(self.update, 1.0/33.0)
        return layout

    def update(self, dt):
        # display image from cam in opencv window
        originaltime = time.time()
        ret, frame = self.capture.read()
        print("5. codeline time:", time.time()-originaltime)
        originaltime = time.time()
        # convert it to texture
        buf1 = np.concatenate((frame, np.full((frame.shape[0],frame.shape[1], 1), 255)), axis=2).astype(frame.dtype)
        buf1 = cv2.flip(buf1, 0)
        print("6. codeline time:", time.time()-originaltime)
        originaltime = time.time()
        buf = buf1.tostring()
        print("7. codeline time:", time.time()-originaltime)
        originaltime = time.time()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgra') 
        print("8. codeline time:", time.time()-originaltime)
        originaltime = time.time()
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgra', bufferfmt='ubyte')
        print("9. codeline time:", time.time()-originaltime)
        # display image from the texture
        originaltime = time.time()
        self.img1.texture = texture1
        print("10. codeline time:", time.time()-originaltime)

if __name__ == '__main__':
    CamApp().run()