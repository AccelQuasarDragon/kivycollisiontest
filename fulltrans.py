# https://stackoverflow.com/questions/59223007/how-to-make-transparent-screen-on-desktopapp-in-kivy

import win32api
import win32gui
import win32con

from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
#https://stackoverflow.com/questions/36762664/how-to-change-the-colours-of-the-background-of-the-screen-in-kivy-app-module-of
# Window.clearcolor = (.9, .9, .9, 1) #white
Window.clearcolor = (.9, .9, .9, 0.1) #white
from kivy.lang.builder import Builder

class AddWarning(BoxLayout):
    pass

kvstring = '''
AddWarning:
    id: warningID
    Button:
        id: buttonid
        size: 100, 200
        text: "sayonara"
        opacity: 100
'''
# https://stackoverflow.com/questions/66732164/kivy-transparent-canvas-background

class WarningApp(App):
    def build(self):
        Window.set_title("ht")
        # Window.clearcolor = (0, 0, 0, 0.1)
        self.HWND = win32gui.FindWindow(None, 'ht')
        win32gui.SetWindowLong(self.HWND, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.HWND, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # win32gui.SetLayeredWindowAttributes(HWND, win32api.RGB(0,0,0), 230, win32con.LWA_ALPHA) #less transparent
        win32gui.SetLayeredWindowAttributes(self.HWND, win32api.RGB(0,0,0), 50, win32con.LWA_ALPHA) #more transparent
        # bind example: https://stackoverflow.com/questions/61409361/how-to-implement-mouse-over-animation-in-kivy
        Window.bind(mouse_pos=self.on_motion)
        # return AddWarning()
        loadedkv = Builder.load_string(kvstring)
        return loadedkv
    
    #https://stackoverflow.com/questions/29640745/kivy-how-to-separate-background-touch-from-a-widget-touch

    #https://stackoverflow.com/questions/61409361/how-to-implement-mouse-over-animation-in-kivy
    def on_motion(self, src, mouse_pos):
        root_widget = AppInstance.get_running_app()
        print("motion...", root_widget.root.ids['buttonid'], self.root.collide_point(*mouse_pos), root_widget.root.ids['buttonid'].collide_point(*mouse_pos))
        if self.root.collide_point(*mouse_pos):
            win32gui.SetLayeredWindowAttributes(self.HWND, win32api.RGB(0,0,0), 230, win32con.LWA_ALPHA) #less transparent
        else:
            win32gui.SetLayeredWindowAttributes(self.HWND, win32api.RGB(0,0,0), 50, win32con.LWA_ALPHA) #more transparent
        pass
        # 
        # if self.root.ids.butt.collide_point(*mouse_pos):
        #     print('over Button at', mouse_pos, 'Do animation')

if __name__ == '__main__':
    AppInstance = WarningApp()
    AppInstance.run()