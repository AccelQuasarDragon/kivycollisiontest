__author__ = 'bunkus'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import threading
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time

def draw_landmarks_on_image(annotated_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image
   
# with open("pose_landmarker_lite.task", 'rb') as f:
with open("pose_landmarker_full.task", 'rb') as f:
    modelbytes = f.read()
    base_options = python.BaseOptions(model_asset_buffer=modelbytes)
    VisionRunningMode = mp.tasks.vision.RunningMode
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=VisionRunningMode.VIDEO,
        min_pose_detection_confidence=0.5, min_tracking_confidence=0.5,
        )
landmarker = mp.tasks.vision.PoseLandmarker.create_from_options(options)
from collections import deque
import time

class CamApp(App):
    def build(self):
        self.img1=Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        # self.capture = cv2.VideoCapture(0)
        # self.capture = cv2.VideoCapture("Elephants Dream charstart2FULL_265.mp4")
        # self.capture = cv2.VideoCapture("Elephants Dream charstart2FULL.webm")
        Clock.schedule_interval(self.on_frame_data, 1.0/60.0)
        Clock.schedule_once(self.on_start, 0)
        self.index = 0
        self.readindex = 0
        self.canceling_thread = False
        self.frame_data = None
        self.width = 0
        self.height = 0
        self.fps = 30
        return layout

    def on_start(self, *args):
        self.readingdequeE = deque(maxlen=30)
        self.readingdequeO = deque(maxlen=30)
        self.answerdeque = deque(maxlen=30)
        self.capture = cv2.VideoCapture("Elephants Dream charstart2FULL.webm")
        self.readthread = threading.Thread(target=self.reading_thread)
        self.readthread.start()
        import time
        time.sleep(1)

        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()
        time.sleep(1)
        self.thread2 = threading.Thread(target=self.thread_function2)
        self.thread2.start()
    def reading_thread(self):
        while True:
            if len(self.readingdequeE) < 30 and len(self.readingdequeO) < 30:
                ret, testframe = self.capture.read()
                if ret and self.readindex%2 == 0:
                    # self.readingdequeE.append({"framenumber": self.readindex, str("framenumber"+ str(self.readindex)): testframe})
                    self.readingdequeE.append(testframe)
                    print("readeven")
                    self.readindex += 1
                if ret and self.readindex%2 == 1:
                    # self.readingdequeO.append({"framenumber": self.readindex, str("framenumber"+ str(self.readindex)): testframe})
                    self.readingdequeO.append(testframe)
                    print("readodd")
                    self.readindex += 1
            time.sleep(0.01)

    def thread_functionOG(self):
        while not self.canceling_thread:
            timeog = time.time()
            ret, testframe = self.capture.read()
            self.index += 1
            if ret: 
                global landmarker
                image = testframe
                self.height = testframe.shape[0]
                self.width = testframe.shape[1]
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
                results = landmarker.detect_for_video(image, self.index) 
                self.frame_data = draw_landmarks_on_image(testframe, results)
            print("totaltime_MEDIAPIPE", time.time() - timeog, "starttime:", timeog, "endtime:", time.time())
        self.thread = None


    def thread_function(self): #read even frames and start
        #set the starttime
        if not hasattr(self, "starttime"):
            self.starttime = time.time()
        # print("1a, index", self.index)
        while not self.canceling_thread:
            # print("1b, index", self.index, self.index % 2 == 0 and len(self.readingdequeE) >1)
            timeog = time.time()
            if self.index % 2 == 0 and len(self.readingdequeE) >1:
                print("read1a")
                testframe = self.readingdequeE.pop()
                print("read1b",)
                self.index += 1
                
                global landmarker
                image = testframe
                framenumber = self.index
                self.height = testframe.shape[0]
                self.width = testframe.shape[1]
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
                results = landmarker.detect_for_video(image, self.index) 
                if len(self.answerdeque) < 30:
                    self.answerdeque.append({"framenumber": framenumber, str("framedata" + str(framenumber)): draw_landmarks_on_image(testframe, results)})
                    print("appendedEa", framenumber)
                else:
                    time.sleep(0.03)
                    self.answerdeque.append({"framenumber": framenumber, str("framedata" + str(framenumber)): draw_landmarks_on_image(testframe, results)})
                    print("appendedEb", framenumber)
            time.sleep(0.01)
            # print("totaltime", time.time() - timeog)
        self.thread = None

    def thread_function2(self): #read odd frames and continue
        # print("2a, index", self.index)
        while not self.canceling_thread:
            timeog = time.time()
            # print("2b, index", self.index, self.index % 2 == 1 and len(self.readingdequeO) >1)
            if self.index % 2 == 1 and len(self.readingdequeO) >1:
                print("read2a")
                testframe = self.readingdequeO.pop()
                print("read2b")
                self.index += 1
                global landmarker
                image = testframe
                framenumber = self.index
                self.height = testframe.shape[0]
                self.width = testframe.shape[1]
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
                results = landmarker.detect_for_video(image, self.index) 
                if len(self.answerdeque) < 30:
                    self.answerdeque.append({"framenumber": framenumber, str("framedata" + str(framenumber)): draw_landmarks_on_image(testframe, results)})
                    print("appendedOa", framenumber)
                else:
                    time.sleep(0.03)
                    self.answerdeque.append({"framenumber": framenumber, str("framedata" + str(framenumber)): draw_landmarks_on_image(testframe, results)})
                    print("appendedOb", framenumber)
            time.sleep(0.01)
            # print("totaltime", time.time() - timeog)
        self.thread = None

    def on_frame_data(self, *_):
        # if isinstance(self.frame_data,np.ndarray):
        # u can peek at deques: https://stackoverflow.com/questions/48640251/how-to-peek-front-of-deque-without-popping#:~:text=You%20can%20peek%20front%20element,right%20and%20seems%20efficient%20too. , can do it but I thought of a simpler way in the example py file
        #read until u get the correct amt
        #know the correct framenumber
        answerdata = False
        ans_framenumber = (time.time() - self.starttime)/self.fps
        #search the first 5 of the deque
        for x in range(5):
            print("??",x, len(self.answerdeque))
            if x < len(self.answerdeque):
                if self.answerdeque[x]["framenumber"] == ans_framenumber:
                    answerdata = self.answerdeque.popleft()
                else:
                    self.answerdeque.popleft()
        if answerdata: 
            
            buf1 = cv2.flip(answerdata[str("framenumber"+ans_framenumber)], 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(self.width, self.height), colorfmt='bgr') 
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img1.texture = texture1
if __name__ == '__main__':
    CamApp().run()