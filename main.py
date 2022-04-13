if __name__ == '__main__':
    import pyperclip
    from kivy.app import App
    from kivy.resources import resource_add_path
    from kivy.uix.boxlayout import BoxLayout
    from yt_dlp import YoutubeDL
    import multiprocessing
    import os
    import sys

    pool = multiprocessing.Pool()


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

        def ydl_opt(self, path, rs, ext, usr, pw, thumb, embed, sponsblock):

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
                'ffmpeg_location': 'ffmpeg/ffmpeg.exe',
                'prefer_ffmpeg': True,
                'logger': Logger(),
                'ignoreerrors': 'only_download',
                'check_formats': None,
            }
            if thumb is True:
                ydl_opts['writethumbnail'] = 'True'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegThumbnailsConvertor',
                    'format': 'jpg'
                }, ]
            if sponsblock is True:
                ydl_opts['postprocessors'] = [
                    {
                        'key': 'SponsorBlock',
                        'categories': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview',
                                       'interaction', 'music_offtopic']
                    },
                    {
                        'key': 'ModifyChapters',
                        'remove_sponsor_segments': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview',
                                                    'interaction', 'music_offtopic']
                    }
                ]

            if embed is True:
                ydl_opts['writethumbnail'] = 'True'
                ydl_opts['postprocessors'] = {
                                                 'key': 'EmbedThumbnail',
                                             },

            return ydl_opts

        def audioonly(self, path):
            ydl_optsau = {
                'format': 'ba',
                'paths': {'home': path},
                'ffmpeg_location': 'ffmpeg/ffmpeg.exe',
                'postprocessors': [{
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
                    pool.imap(ydl.download([link]), range(0, 10))
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
            thumb = self.ids.thumbswitch.active
            embed = self.ids.embed.active
            sponsblock = self.ids.sponswitch.active

            link = str(self.process())
            with YoutubeDL(self.ydl_opt(path, rs, 'mp4', usr, pw, thumb, embed, sponsblock)) as ydl:

                if "https://" in link:
                    pool.imap(ydl.download([link]), range(1, 10))

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
