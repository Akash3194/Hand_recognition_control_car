from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
import win32com.client as wincl
from kivy.uix.screenmanager import ScreenManager,Screen
import time
import pyfirmata as p
import cv2
import math
import numpy as np


Builder.load_string('''
<Buttons>:
    FloatLayout:
        id:show
        
        Label:
            id:same
            markup:True
            text:''
            pos_hint:{'center_x':.045,'center_y':.95}
        Label:
            id:change
            markup:True
            text:''
            pos_hint:{'center_x':.2,'center_y':.95}

<front_page>:
    
    BoxLayout:
        orientation:'vertical'
        spacing:40
        padding:[40,20,20,40]
        BoxLayout:
            Label:
                markup:True
                text:"[color=555555][b]Minor Project[/b][/color]"
                
        BoxLayout:
            Button:
                text:"Push This Button"
                background_color:[0.56,0.69,0.79,1]
                on_release:root.manager.current='btn'
       
<hand_control>:
                
        
            
            
            

''')


class Buttons(Screen, FloatLayout, Widget):
    def __init__(self, **kwargs):
        super(Buttons, self).__init__(**kwargs)

        self.port='COM5'
        self.board=p.Arduino(self.port)
        self.f_right_tyre=self.board.get_pin('d:3:p')
        self.b_right_tyre=self.board.get_pin('d:9:p')
        self.f_left_tyre=self.board.get_pin('d:5:p')
        self.b_left_tyre=self.board.get_pin('d:11:p')
        self.speak=True
        self.keyboard = Window.request_keyboard(self.buttonreleased, self, 'text')
        self.keyboard.bind(on_key_down=self.buttondown, on_key_up=self.buttonreleased)

    def buttonreleased(self, keyboard, keycode):
        print ("closed")

        self.f_right_tyre.write(0)
        self.f_left_tyre.write(0)
        self.b_right_tyre.write(0)
        self.b_left_tyre.write(0)
        self.ids.change.text = ""
        self.ids.show.add_widget(Image(source="White.png"))
        self.keyboard = None

    def buttondown(self, keyboard, keycode, text, modifiers):
        j = keycode
        if keycode[1] == 'up':

            self.ids.change.text = "[b][color=4C4646]Moving Forward....[/color][/b]"

            self.ids.same.text = "[b][color=4C4646]Car Status:[/color][/b]"

            self.ids.show.add_widget(Image(source="up.png"))
            self.f_right_tyre.write(1)
            self.f_left_tyre.write(1)





        elif keycode[1] == 'right':
            self.ids.change.text = "[b][color=4C4646]Moving Right....[/color][/b]"
            self.ids.same.text = "[b][color=4C4646]Car Status:[/color][/b]"
            self.ids.show.add_widget(Image(source="Right.png"))
            self.f_right_tyre.write(0.2)
            self.f_left_tyre.write(1)
        elif keycode[1] == 'left':
            self.ids.change.text = "[b][color=4C4646]Moving Left....[/color][/b]"
            self.ids.show.add_widget(Image(source="Left.png"))
            self.ids.same.text = "[b][color=4C4646]Car Status:[/color][/b]"
            self.f_right_tyre.write(1)
            self.f_left_tyre.write(0.2)
        elif keycode[1] == 'down':
            self.ids.change.text = "[b][color=4C4646]Moving Backside....[/color][/b]"
            self.ids.show.add_widget(Image(source="Down.png"))
            self.ids.same.text = "[b][color=4C4646]Car Status:[/color][/b]"
            self.b_right_tyre.write(1)
            self.b_left_tyre.write(1)

        print(j)


class front_page(Screen):
    pass




class StartApp(App):
    def build(self):
        self.sm=ScreenManager()
        self.screen1=front_page(name='f_p')
        self.screen2=Buttons(name='btn')
        self.sm.add_widget(self.screen1)
        self.sm.add_widget(self.screen2)

        Window.clearcolor=1,1,1,1
        return self.sm

StartApp().run()
