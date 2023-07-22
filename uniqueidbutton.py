# https://stackoverflow.com/a/69063413
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class MainScreen(GridLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.cols = 1
        MainScreenLayout = GridLayout()
        MainScreenLayout.cols = 3

        # for loop creating buttons with varying IDs

        NumberToCreate = 4
        for x in range(int(NumberToCreate)):
            aButton = Button(text='button text ' + str(x), on_press=self.press_auth)
            MainScreenLayout.add_widget(aButton)
            # let us make the id similar to the text to simplify the searching
            self.ids['button text ' + str(x)] = aButton

        self.add_widget(MainScreenLayout)

    # function for when button is pressed
    def press_auth(self, instance):
        # here we can accuses the button id using button text 
        print(self.ids[instance.text])


class MyApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
