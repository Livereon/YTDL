import warnings
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import os, sys
from kivy.resources import resource_add_path, resource_find
from yt_dlp import YoutubeDL
import pyperclip

def format_selector(ctx):

    pass

validURL = {
    "https://www.youtube.com",
    "https://www.tiktok.com",
    "https://www.crunchyroll.com"
}

class UI(BoxLayout):

    def ydl_opt(self, PATH):
        ydl_opts = {
            'format': 'best',
            'paths': {'home': PATH},
            'format_sort': {
                'res': f"{self.ids.resspinner.text[:-1]}",
                'ext': "mp4"

            }
        }
        return ydl_opts

    def pasteButton(self):
        pastedlink = pyperclip.paste()
        self.ids.link.text = pastedlink
        pass

    def process(self):
        links = self.ids.link.text
        return links

    def down_button(self):
        with YoutubeDL(self.ydl_opt(self.ids.path.text)) as ydl:
            link = str(self.process())
            if any(link.startswith(x) for x in validURL):
                ydl.download([self.process()])
                return
            elif link == "":
                print("There is no link BAKA!")
                return
            else:
                print("Ara ara! Use a Youtube,TikTok or Crunchyroll link!")
                return
        pass

##"
class YTDLApp(App):
    pass


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    YTDLApp().run()



