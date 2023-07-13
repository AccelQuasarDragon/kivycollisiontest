# https://stackoverflow.com/questions/58800955/kivy-dragbehavior-dragging-more-than-one-widget
from kivy.config import Config

Config.set('graphics', 'multisamples', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
import copy
import numpy as np
from kivy.graphics.texture import Texture
import time
kv = """

<FileBox>:
    size_hint: None, None
    size: 100, 100
    bcolor: (.5,.5,.5,1)
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)  if self.bcolor is None else self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size    

<FileSpace>
    orientation: 'lr-tb'
    spacing: 2


FileSpace:
    #need to add alpha channel to images btw
    FileBox:
        id: sportsball
        # source: "sportspersonMASK.jpg"
        opacity: 0.8
        source: "sportspersonMASK3.jpg"
    FileBox:
        id: frigate
        source: "ranxfrigate.jpg"
        # source: "ranxfrigateinverse.jpg"
        opacity: 0.8
    FileBox:
        id: bomber
        source: "sportspersonMASK2.jpg"
        # source: "ranxbomber.jpg"
        # source: "ranxbomberinverse.jpg"
        opacity: 0.8
    FileBox:
        id: collisionspace
        size: 200, 200
        source: "sportspersonMASK.jpg"
"""
from kivy.clock import Clock

# class FileBox(DragBehavior, BoxLayout):
class FileBox(DragBehavior, Image):

    def __init__(self,**kwargs):
        super(FileBox, self).__init__(**kwargs)
        #save the original image so repeated grayconversion doesn't nuke the image out of existence when i observe it
        Clock.schedule_once(self.originalsave, 2) #0 is too fast, 1 is too fast, 2 works (widget needs to be init before saving an image): https://stackoverflow.com/a/62435605
    def originalsave(self, *args):
        # # print("og self?", dir(self), self.__dict__)
        # try:
        #     # self.originalguy = self.export_as_image()
        #     # self.originalguy = np.full((200,200,3), [255,255,255], dtype=np.uint8) 
        # except Exception as e:
        #     print("blitting died!", e, flush=True)
        #     import traceback
        #     print("full exception", "".join(traceback.format_exception(*sys.exc_info())))
        self.originalguy = self.export_as_image()
        self.originalbuf = self.export_as_image()._texture.pixels


class FileSpace(StackLayout):
    def __init__(self,**kwargs):
        super(FileSpace, self).__init__(**kwargs)
        self.touch_count = 0
        self.files = set()
        self.move_files = False

    def on_touch_up(self, touch):
        # remove rectangle if exists
        try:
            touch.ud['rectangle'].size = (0,0)
        except Exception:
            pass
        self.touch_count = 0
        if self.move_files:
            self.move_files = False
            for file in self.files:
                file.bcolor = (.5,.5,.5,1)
            self.files = set()
        return super(FileSpace, self).on_touch_up(touch)

    def on_touch_down(self, touch):
        if len(self.files) > 0:
            self.move_files = True
        return super(FileSpace, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        # print("fileguy", self.files)
        if self.move_files:
            for file in self.files:
                if not file.collide_point(*touch.pos):  # avoid double move if touch is on one of the chosen files
                    file.pos = (file.x + touch.dx, file.y + touch.dy)
                    print("???")
        else:
            if self.touch_count == 0:
                print('TOUCH Move on', self, touch)
                # copy of the point of rectangle
                self.touch_down_pos = copy.deepcopy(touch)
                self.touch_count += 1

                with self.canvas:
                    touch.ud['rectangle'] = Rectangle(pos=(touch.x, touch.y), size = (0,0))
            # draw a rectangle
            # touch.ud['rectangle'].size = (touch.x - self.touch_down_pos.x, touch.y - self.touch_down_pos.y)
            for child in self.children:
                x = False
                y = False

                # # center of a widget
                # center = [child.pos[0] + child.width/2, child.pos[1] + child.height/2]
                # if (touch.x > center[0] and self.touch_down_pos.x < center[0]) or (touch.x < center[0] and self.touch_down_pos.x > center[0]):
                #     x = True
                # if (touch.y > center[1] and self.touch_down_pos.y < center[1]) or (touch.y < center[1] and self.touch_down_pos.y > center[1]):
                #     y = True
                #center is too strict, I want the entire bounding box
                bbox_id = [child.pos[0], child.pos[1]] #left x and bottom y
                # print("x vs down", touch.x, self.touch_down_pos.x) #touch.x is current pos, touch_down_pos is original pos
                #just check touchdownpos on the bounding box of child widget...
                if bbox_id[0] < self.touch_down_pos.x < bbox_id[0] + child.width:
                    x = True
                if bbox_id[1] < self.touch_down_pos.y < bbox_id[1] + child.height:
                    y = True

                if x and y:
                    child.bcolor = (255/255, 153/255, 51/255, 1)
                    self.files.add(child)
                else:
                    child.bcolor = (.5,.5,.5,1)
                    try:
                        self.files.remove(child)
                    except Exception:
                        pass
            #just be lazy and check for collision amongst all "files" in self.files:
            # print("files?", self.files, )
            for file in self.children: #works because FileSpace is the parent of all the file images/FileBox
                # https://stackoverflow.com/questions/27368483/kivy-checking-if-two-widgets-overlap-after-rotation
                #confirmed widget collision working, now if widgets collide we need to check pixel collision
                if child != file and child.collide_widget(file):

                    def grayConversion(image):
                        ## https://stackoverflow.com/questions/51285593/converting-an-image-to-grayscale-using-numpy
                        grayValue = 0.07 * image[:,:,2] + 0.72 * image[:,:,1] + 0.21 * image[:,:,0]
                        gray_img = grayValue.astype(np.uint8)
                        return gray_img

                    def widgettomask(*args):
                        widgetVAR = args[0]
                        #can't do this as repeated grayconversion nukes the image
                        imageguy = widgetVAR.originalguy
                        bytesformat = imageguy._texture.pixels
                        # imageguy = widgetVAR.export_as_image()
                        # bytesformat = imageguy._texture.pixels
                        # print(type(bytesformat), imageguy.width, imageguy.height,imageguy.__dict__, dir(imageguy)) #, imageguy.colorfmt > confirmed rgba for sportsperson
                        image_array = np.frombuffer(bytesformat, np.uint8).copy().reshape(imageguy.width, imageguy.height, 4) #u need to know ur image format. this is assuming rgba/bgra. if u have no alpha channel then it's just rgb/bgr and so pick 3
                        # print("og shape", image_array.shape)
                        #FOR SOME REASON IMAGEDATA FLIPS VERTICAL TRUE
                        image_array = np.flip(image_array, 0)
                        #use numpy thresholding: https://www.python-engineer.com/posts/image-thresholding/
                        #to make mask, go grayscale then apply thresholding:
                        # https://stackoverflow.com/questions/51285593/converting-an-image-to-grayscale-using-numpy
                        # img_np = image_array
                        img_np = grayConversion(image_array)
                        
                        # img_np = np.stack((img_np,)*4, axis=-1) #just needed to get to rgba format to look at mask in kivy
                        # print("np shape?", img_np.shape)
                        # return img_np

                        # now to B&W from grayscale:
                        # https://stackoverflow.com/a/18778280
                        # white is background, so anything less than 255 should be set to 0 (black)
                        bw = img_np.copy()
                        # print("bw og", bw)
                        bw[bw < 128] = 0    # Black
                        bw[bw >= 128] = 255 # White
                        #back to dim of 4:
                        # https://stackoverflow.com/a/40119878
                        # bw = np.stack((bw,)*4, axis=-1) #just needed to get to rgba format to look at mask in kivy
                        # print("bw shape after", bw.shape, bw)
                        return bw
                    
                    def pixelcollider(*args):
                        # print("argssss",args)
                        widget1VAR = args[0]
                        widget2VAR = args[1]
                        widget1VARmask = widgettomask(widget1VAR)
                        widget2VARmask = widgettomask(widget2VAR)
                        #PLAN:
                        #u know the locations relative to each other
                        #place the masks in a large numpy array that contains both at the correct spot, doing a bitwise AND operation
                        #if the large numpy array is nonzero then they collided somewhere
                        
                        
                        #large numpy array has this size: (minimal x, maximal y, 4)
                        #to normalize against this array, subtract the startlocation (bottom left) of each widget by the startlocation of the large numpy array (minx, miny):
                        minx = int(min(widget1VAR.pos[0], widget2VAR.pos[0]))
                        maxx = int(max(widget1VAR.pos[0] + widget1VAR.width, widget2VAR.pos[0] + widget2VAR.width))
                        miny = int(min(widget1VAR.pos[1], widget2VAR.pos[1]))
                        maxy = int(max(widget1VAR.pos[1] + widget1VAR.height, widget2VAR.pos[1]+ widget2VAR.height))

                        # print("maxx",maxx-minx)
                        #I kinda mixed up x y kinda not, it's because numpy and kivy have different orientations. numpy is an array: top>down, L>R. kivy is down>up, L>R.... smth like that 
                        testarea1 = np.full((maxy-miny,maxx-minx), 0) #black image
                        
                        testarea2 = np.full((maxy-miny,maxx-minx), 0) #black image
                        # testarea2 = np.full((maxx-minx,maxy-miny), 0) #black image
                        # print("testareashape", testarea1.shape, widget1VARmask.shape)

                        #now to update testarea1 with respect to the widget location:
                        #place widget 1 respecting the offsets
                        widget1xoffset = int(widget1VAR.pos[0]- minx)
                        widget1yoffset = int(widget1VAR.pos[1]- miny)
                        #reminder y and x are reversed
                        testarea1[widget1yoffset:widget1yoffset+widget1VAR.height,widget1xoffset:widget1xoffset+widget1VAR.width] = widget1VARmask
                        # print("offsets and dim", 
                        #       testarea1.shape,
                        #       widget1VARmask.shape, 

                        #       widget1VAR.pos, 
                        #       minx, miny,
                        #       widget1xoffset, 
                        #       widget1yoffset, 
                        #       widget1xoffset,
                        #       widget1xoffset+widget1VAR.width,
                        #       widget1yoffset,
                        #       widget1yoffset+widget1VAR.height)

                        #now to update testarea2 with respect to the widget location:
                        #place widget 2 respecting the offsets
                        widget2xoffset = int(widget2VAR.pos[0]-minx)
                        widget2yoffset = int(widget2VAR.pos[1]-miny)
                        # print("offsets and dim2", 
                        #       testarea2.shape, 
                        #       widget2VARmask.shape,
                        #       widget2VAR.pos, 
                        #       minx, miny,
                        #       widget2xoffset,
                        #       widget2xoffset,
                        #       widget2xoffset,
                        #       widget2yoffset,
                        #       widget2xoffset+widget2VAR.width,
                        #       widget2yoffset+widget2VAR.height
                        #       )
                        #reminder y and x are reversed
                        testarea2[widget2yoffset:widget2yoffset+widget2VAR.height,widget2xoffset:widget2xoffset+widget2VAR.width] = widget2VARmask

                        # #show testarea1 and testarea2:
                        # finaltest = np.add(testarea1, testarea2) #add is if black is the bg

                        # finaltest = np.subtract(testarea1, testarea2) 
                        #clip to stop negative numbers:
                        # https://stackoverflow.com/a/21460603
                        # finaltest = np.clip(finaltest, 0, 255, out=finaltest)

                        # finaltest as per: https://stackoverflow.com/a/23655364 
                        finaltest = testarea1 & testarea2
                        finalverdict = np.count_nonzero(finaltest)
                        # print("finalverdict", finalverdict)
                        
                        #just needed to get to rgba format to look at mask in kivy
                        # #back to dim of 4:
                        # # https://stackoverflow.com/a/40119878
                        finaltest = np.stack((finaltest,)*4, axis=-1).astype(np.uint8) 
                        # finaltest
                        #blit to collisionspace:
                        newtexture = Texture.create(size=(finaltest.shape[1],finaltest.shape[0]), colorfmt='rgba') 
                        newtexture.blit_buffer(finaltest.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                        # print("root", self.ids, self.ids["collisionspace"])
                        self.ids["collisionspace"].texture = newtexture

                        # testarea2
                        # #blit to collisionspace:
                        # testarea2 = np.stack((testarea2,)*4, axis=-1).astype(np.uint8) 
                        # newtexture = Texture.create(size=(testarea2.shape[1],testarea2.shape[0]), colorfmt='rgba') 
                        # newtexture.blit_buffer(testarea2.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                        # # print("root", self.ids, self.ids["collisionspace"])
                        # self.ids["collisionspace"].texture = newtexture

                        # testara1
                        # #blit to collisionspace:
                        # testarea1 = np.stack((testarea1,)*4, axis=-1).astype(np.uint8) 
                        # newtexture = Texture.create(size=(testarea1.shape[1],testarea1.shape[0]), colorfmt='rgba') 
                        # newtexture.blit_buffer(testarea1.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                        # # print("root", self.ids, self.ids["collisionspace"])
                        # self.ids["collisionspace"].texture = newtexture
                        
                        # widget2 mask works #confirmed after turning on bw = np.stack((bw,)*4, axis=-1)
                        # #blit to collisionspace:
                        # newtexture = Texture.create(size=(widget2VARmask.shape[1],widget2VARmask.shape[0]), colorfmt='rgba') 
                        # newtexture.blit_buffer(widget2VARmask.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                        # # print("root", self.ids, self.ids["collisionspace"])
                        # self.ids["collisionspace"].texture = newtexture

                        # # widget1 mask works #confirmed after turning on bw = np.stack((bw,)*4, axis=-1)
                        # #blit to collisionspace:
                        # # widget1VARmask = np.stack((widget1VARmask,)*4, axis=-1).astype(np.uint8) 
                        # newtexture = Texture.create(size=(widget1VARmask.shape[1],widget1VARmask.shape[0]), colorfmt='rgba') 
                        # newtexture.blit_buffer(widget1VARmask.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                        # # print("root", self.ids, self.ids["collisionspace"])
                        # self.ids["collisionspace"].texture = newtexture

                        #testarea1 works
                        # #blit to collisionspace:
                        # testarea1 = np.stack((testarea1,)*4, axis=-1).astype(np.uint8) 
                        # newtexture = Texture.create(size=(testarea1.shape[1],testarea1.shape[0]), colorfmt='rgba') 
                        # newtexture.blit_buffer(testarea1.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                        # # print("root", self.ids, self.ids["collisionspace"])
                        # self.ids["collisionspace"].texture = newtexture
                        
                        
                        # #show testarea1 and testarea2:
                        # finaltest = np.add(testarea1, testarea2)
                        # #back to dim of 4:
                        # # https://stackoverflow.com/a/40119878
                        # finaltest = np.stack((finaltest,)*4, axis=-1).astype(np.uint8) #just needed to get to rgba format to look at mask in kivy
                        # # finaltest = np.stack((widget1VARmask,)*4, axis=-1).astype(np.uint8) #just needed to get to rgba format to look at mask in kivy
                        # # finaltest = np.full((200,200,3), [255,255,255], dtype=np.uint8) 
                        # #blit to collisionspace:
                        # newtexture = Texture.create(size=(finaltest.shape[1],finaltest.shape[0]), colorfmt='rgba') 
                        # newtexture.blit_buffer(finaltest.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                        # # print("root", self.ids, self.ids["collisionspace"])
                        # self.ids["collisionspace"].texture = newtexture


                        #check for collision as such:
                        # collision = np.array_equal(testarea1, testarea2)
                        if finalverdict: 
                            return True
                        else:
                            return False
                        #  np.count_nonzero(subtraction_array)
                    # print(child.pos, file.pos)

                    if pixelcollider(child, file):
                        print("collision!")
                    else:
                        print("no collision")

                    #THIS BLOCK CONFIRMS THAT THE MASK WORKS
                    # '''
                    # maskimage_whitebg = widgettomask(child) 
                    # # print("???", maskimage_whitebg.shape)
                    # #FOR SOME REASON IMAGEDATA FLIPS VERTICAL TRUE
                    # # maskimage_whitebg = np.flip(maskimage_whitebg, 0)
                      
                    # newtexture = Texture.create(size=(maskimage_whitebg.shape[1],maskimage_whitebg.shape[0]), colorfmt='rgba') 
                    
                    # newtexture.blit_buffer(maskimage_whitebg.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                    # child.texture = newtexture
                    # print("checking collision between:", child.__class__, file.__class__)
                    # print("checking collision between:", dir(child))
                    '''

                    #THIS BLOCK CONFIRMED THAT IMAGEDATA FLIPS IMAGES VERTICALLY
                    # '''
                    # imageguy = child.export_as_image()
                    # bytesformat = imageguy._texture.pixels
                    # maskimage_whitebg = np.frombuffer(bytesformat, np.uint8).reshape(imageguy.height, imageguy.width, 4) 
                    # #FOR SOME REASON IMAGEDATA FLIPS VERTICAL TRUE
                    # maskimage_whitebg = np.flip(maskimage_whitebg, 0)
                    
                    # newtexture = Texture.create(size=(maskimage_whitebg.shape[1],maskimage_whitebg.shape[0]), colorfmt='rgba') 
                    
                    # newtexture.blit_buffer(maskimage_whitebg.tobytes(), colorfmt="rgba", bufferfmt='ubyte')
                    # child.texture = newtexture
                    # '''
        return super(FileSpace, self).on_touch_move(touch)

sm = Builder.load_string(kv)

class SFTP(App):

    def build(self):
        self.title = 'SFTP'

        return sm

if __name__ == '__main__':
    SFTP().run()