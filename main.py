import os
import sys

import pyperclip
from kivy.app import App
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from yt_dlp import YoutubeDL


class Logger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class UI(BoxLayout):

    def ydl_opt(self, path, rs, ext, usr, pw):

        ydl_opts = {
            'format': 'best/mp4',
            'username': usr,
            'password': pw,
            'extractor_args': {
                'crunchyroll': {
                    'language': ['jaJp'],
                    'hardsub': ['None', 'enUS']},
            },
            'format_sort_force': {
                f'height: {rs}',
                f'ext: {ext}',
            },
            'paths': {'home': path},
            'ffmpeg_location': './ffmpeg.exe',
            'logger': Logger(),
            'ignoreerrors': 'only_download',
            'check_formats': None
        }

        return ydl_opts

    def audioonly(self,path):
        ydl_optsau = {
            'format': 'ba',
            'paths': {'home': path},
            'postprocessors': [{
                # Embed metadata in video using ffmpeg.
                # ℹ️ See yt_dlp.postprocessor.FFmpegMetadataPP for the arguments it accepts
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }],
            'logger': Logger(),
        }
        return ydl_optsau

    def pastebutton(self):
        pastedlink = pyperclip.paste()
        self.ids.link.text = pastedlink
        pass

    def process(self):
        links = self.ids.link.text
        return links

    def down_button_audio(self):
        path = self.ids.path.text
        link = str(self.process())
        with YoutubeDL(self.audioonly(path)) as ydl:
            if "https://" in link:
                ydl.download([link])
                return
            elif link == "":
                print("There is no link BAKA!")
                return
        pass

    def down_button(self):
        path = self.ids.path.text
        rs = self.ids.rs.text
        usr = self.ids.u.text
        pw = self.ids.p.text
        link = str(self.process())
        with YoutubeDL(self.ydl_opt(path, rs, 'mp4',usr,pw)) as ydl:
            if "https://" in link:
                ydl.download([link])
                return
            elif link == "":
                print("There is no link BAKA!")
                return
        pass


class YTDLApp(App):
    pass


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    YTDLApp().run()
