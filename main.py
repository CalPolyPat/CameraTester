import kivy
kivy.require('1.4.0')
 
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.core.window import Window
 
class MyApp(App):
          # Function to take a screenshot
          def doscreenshot(self,*largs):
                Window.screenshot(name='screenshot%(counter)04d.jpg')
     
          def build(self):
                layout = AnchorLayout(anchor_x='center', anchor_y='center')
                cam = Camera()        #Get the camera
                cam=Camera(resolution=(640,480), size=(1200,1200))
                cam.play=True         #Start the camera
                layout.add_widget(cam)
 
                button=Button(text='screenshot',size_hint=(0.12,0.12))
                button.bind(on_press=self.doscreenshot)
                layout.add_widget(button)    #Add button to Camera Widget
                 
                return layout
             
if __name__ == '__main__':
    MyApp().run()            