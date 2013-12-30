import kivy
kivy.require('1.4.0')
 
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.logger import Logger
from PIL import Image, ImageStat
import os
 
class MyApp(App):
          # Function to take a screenshot
          def doscreenshot(self,*largs):
                Logger.info('Progress: Made it to screenshot')
                Window.screenshot(name='top04d.jpg')
                
          def simplify(self, data, num):
                Logger.info('Progress: Simplifying')
                datafile = open(num, "w")
                datafile.write("R\n")
                ave=sum(data)/len(data)
                incval=0
                cnt=False
                for i in xrange(0, len(data)):
                    datafile.write(str(data[i])+"\n")
                for j in xrange(0, len(data)):
                    if data[j]<(ave):
                        data[j]=0
                        if cnt==True:
                            incval+=1
                            data[j]=10000
                    if data[j]>(ave):
                        cnt=True
                        data[j]=10000
                    if incval>400:
                        for k in xrange(0,400):
                            data[j-k]=0
                        cnt=False
                        incval=0
                        
                datafile = open("new" + num, "w")
                datafile.write("R\n")
                for l in xrange(0, len(data)):
                    datafile.write(str(data[l])+"\n")
                return data
                
          def show_variance(self, src):
            Logger.info('Progress: Made it to Variance Function')
            im = Image.open(src)
            im_rgb = im.convert("RGB")
            imx, imy = im.size
            iteratx = imx
            iteraty = imy
            dcutoff = 100
            varfactoru = 0
            varfactord = 0
            varfactorroofu = 0
            varfactorroofd = 0
            rdata = []
            finlist = []
            deriv = []
            poper = []
            xboundup = []*20
            xbounddown = []*20
            yboundup = []*20
            ybounddown = []*20
            filebufferx = [0]*iteratx
            filebuffery = [0]*iteraty
            pix = im_rgb.load()
            for z in xrange(1, iteratx):
                rdata[:] = [pix[i, j][0] for j in xrange(0,imy) for i in xrange(z-1,z)]
                mean = sum(rdata)/len(rdata)
                finlist[:] = [(rdata[i]-mean)**2 for i in xrange(len(rdata))]
                varianr = sum(finlist)/len(finlist)
                filebufferx[z-1] = varianr
                rdata[:] = []
            filebufferx = self.simplify(filebufferx, "xfile.txt")
            deriv[:] = [filebufferx[h]-filebufferx[h-1] for h in xrange(1, len(filebufferx))]
            for l in xrange(300, len(deriv) - 500):
                if deriv[l]>dcutoff:
                    xboundup.append(l)
            k = 1
            Logger.info('Data: XboundUp Pre Popper' + str(xboundup))
            while k<len(xboundup):
                if xboundup[k]-xboundup[k-1]<180:
                    poper.append(k)
                k+=1
            inc = 0
            for u in xrange(0, len(poper)):
                xboundup.pop(poper[u]-inc)
                inc+=1
            poper[:] = []
            Logger.info('Debug: XboundUp ' + str(xboundup))
            for m in xrange(300, len(deriv)-500):
                if deriv[m]<-dcutoff:
                    xbounddown.append(m)
            n = 1
            while n<len(xbounddown):
                if xbounddown[n-1]-xbounddown[n]>(-180):
                    poper.append(n)
                n+=1
            inc = 1
            for u in xrange(0, len(poper)):
                xbounddown.pop(poper[u]-inc)
                inc+=1
            Logger.info('Debug: XboundDown ' + str(xbounddown))
            dxcard = xbounddown[-1]-xboundup[-1]
            dxbowl = xbounddown[0]-xboundup[0]
            lengthobj = dxbowl*2.15/dxcard
            objmid = xboundup[-1]-((xboundup[-1]-xbounddown[0])/2)
            poper[:] = []
        
            for d in xrange(1, iteraty):
                rdata[:] = [pix[i, j][0] for j in xrange(d-1,d) for i in xrange(0,objmid)]
                mean = sum(rdata)/len(rdata)
                finlist[:] = [(rdata[i]-mean)**2 for i in xrange(len(rdata))]
                varianr = sum(finlist)/len(finlist)
                filebuffery[d-1] = varianr
                rdata[:] = []
            filebuffery = self.simplify(filebuffery, "yfile.txt")
            deriv[:] = [filebuffery[h]-filebuffery[h-1] for h in xrange(1, len(filebuffery))]
            for l in xrange(300, len(deriv)-300):
                if deriv[l]>dcutoff:
                    yboundup.append(l)
            k = 1
            while k<len(yboundup):
                if yboundup[k]-yboundup[k-1]<150:
                    poper.append(k)
                k+=1
            inc = 0
            for u in xrange(0, len(poper)):
                yboundup.pop(poper[u]-inc)
                inc+=1
            poper[:] = []
            Logger.info('Debug: YboundUp ' + str(yboundup))
            for m in xrange(300, len(deriv)-300):
                if deriv[m]<-dcutoff:
                    ybounddown.append(m)
            g = 1
        
            while g<len(ybounddown):
                if ybounddown[g-1]-ybounddown[g]>(-150):
                    poper.append(g)
                g+=1
            inc = 1
            for u in xrange(0, len(poper)):
                ybounddown.pop(poper[u]-inc)
                inc+=1
            Logger.info('Debug: YboundDown ' + str(ybounddown))
            dybowl = ybounddown[-1]-yboundup[0]
            heightobj = dybowl*2.15/dxcard
            vartuple=(lengthobj, heightobj)
            return vartuple
        
        
          def analyze(self, cam, layout):
                self.doscreenshot()
                Logger.info('Progress: Have we made it this far')
                cam.play=False
                vartuple=self.show_variance("shoe top.jpg")
                varlbl=Label(text="Here are the dimensions" + str(vartuple))
                layout.add_widget(varlbl)
                
          def build(self):
                layout = AnchorLayout(anchor_x="center", anchor_y="bottom")  #Create a camera Widget
                butlayout = AnchorLayout(anchor_x="center", anchor_y="top")
                cam = Camera()        #Get the camera
                cam=Camera(resolution=(640, 480))
                cam.play=True         #Start the camera
                layout.add_widget(cam)
 
                button=Button(text='screenshot',size_hint=(0.12,0.12))
                button.bind(on_press=lambda widget: self.analyze(cam, layout))
                butlayout.add_widget(button)    #Add button to Camera Widget
                layout.add_widget(butlayout)
                 
                return layout
          def on_stop(self):
                os.remove("top04d.jpg")
             
if __name__ == '__main__':
    MyApp().run()            