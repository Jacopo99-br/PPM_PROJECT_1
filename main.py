from tkinter import X
import requests
import json
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import TwoLineRightIconListItem
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.screen import MDScreen
from kivy.core.audio import SoundLoader
import os

#from screens_py_.home_page import HomePage

from device_class import Device



class Tab(MDFloatLayout,MDTabsBase):
    pass

class MusicListItem(TwoLineRightIconListItem):
    pass

class HomePage(MDScreen):
    '''Home Page'''




class MyApp(MDApp): 
    music_path='/home/jacopo-bruscaglioni/Musica'
    
    weather_api_key='ac5066adfaa550475ab1b270b52346d3'
    devices_list=[]
    music_tracks_list=os.listdir(music_path)
    
    
    
    
    
    def add_home_widget(self , device_name):
        try:
            if(self.root.ids.home.children[0].text=='Add a device-widget'):
                self.root.ids.home.remove_widget(self.root.ids.home.children[0])
                
        except Exception as e:
            print("error " + str(e))
       
    def build(self):
        Window.size=[400,600]
        self.theme_cls.theme_style='Dark'
        self.load_all_kv_files()
        
        #per mettere il meteo
        self.get_weather("Borgo san Lorenzo")
        
        return HomePage()
    def on_start(self):
        for file in self.music_tracks_list:
            if file.endswith('mp3'):
                required_file=(file)
                self.root.ids.music.ids.tabs.ids.list_track.add_widget(MusicListItem(text=required_file,secondary_text='unknown artst'))
      
    def load_all_kv_files(self):
        Builder.load_file('screens_kv_/home_screen.kv')
        Builder.load_file('screens_kv_/music_screen.kv')
        Builder.load_file('screens_kv_/home_page.kv')
        
    def get_weather(self, city_name):
        
        try:
            coordinates_url=f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},Italy&appid={self.weather_api_key}"
            response = requests.get(coordinates_url)
            x = response.json()[0]
            lat=x["lat"]
            lon=x["lon"]
            
            url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.weather_api_key}"
            response = requests.get(url)
            x1 = response.json()
            
            temperature= int(x1["main"]["temp"] - 273)
            wind=round(x1["wind"]["speed"]*18/5) #per averlo in km/h
            humidity=x1["main"]["humidity"]
            w_description=x1["weather"][0]["description"]
            
        except requests.ConnectionError as ex:
            print(str(ex))

if __name__=="__main__":
    MyApp().run()
    