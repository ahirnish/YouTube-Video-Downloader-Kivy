#!/usr/local/bin/python3

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import pytube
import subprocess
import sys

songs_repo = '/Users/ahirnishpareek/Desktop/songs/'

class DownloadAudio(GridLayout):

    def __init__(self, **kwargs):
        super(DownloadAudio, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Enter YouTube URL here'))
        self.url = TextInput(multiline=False)
        self.add_widget(self.url)

        self.button = Button(text="DOWNLOAD")
        self.button.bind(on_press=self.buttonClicked)
        self.add_widget(self.button)

        self.title = Label()
        self.add_widget( self.title )

    def buttonClicked(self, button):
        try:
            button.background_color = (0,1,0,1)
            yt = pytube.YouTube(self.url.text)

            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').all()[0]
            filename = audio_stream.default_filename[0:-4] + '.mp3'
            
            audio_stream.download( output_path = songs_repo )

            subprocess.check_output( [ "/usr/local/bin/ffmpeg", "-i", songs_repo + audio_stream.default_filename, "-ab", "128k", songs_repo + filename] )
            subprocess.check_output( [ "rm", songs_repo + audio_stream.default_filename ] )

        except KeyboardInterrupt:
            pass
        except Exception as err:
            self.title.text = err.__str__()
        else:
            self.title.text = yt.title + " has been downloaded!"
            

class YouTubeAudioDownloaderApp(App):

    def build(self):
        return DownloadAudio()


if __name__ == '__main__':
    YouTubeAudioDownloaderApp().run()
