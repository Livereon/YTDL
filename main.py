import warnings
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import os, sys
from kivy.resources import resource_add_path, resource_find
from yt_dlp import YoutubeDL

try:
    class UI(BoxLayout):

        def  ydl_opt(self, PATH):
            ydl_opts = {
                'format': 'best',
                'paths': {'home': PATH}
            }
            return ydl_opts

        def process(self):
            LINK = self.ids.link.text
            return LINK

        def down_button(self):
            with YoutubeDL(self.ydl_opt(self.ids.path.text)) as ydl:
                if self.process() == "":
                    warnings.warn("There is no link BAKA!")
                    return
                elif str(self.process()).startswith("https://www.youtube.com"):
                    ydl.download([self.process()])
                else:
                    warnings.warn("Ara ara! Use a youtube link!")
                    return
            pass


    class YTDLApp(App):
        pass


    if __name__ == '__main__':
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        YTDLApp().run()

except warnings.catch_warnings as e:
    print("Uh Oh!", e)
pass


