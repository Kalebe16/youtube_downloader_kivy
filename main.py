from tkinter import N
from kivymd.app import MDApp
from kivy.lang import Builder   
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window



import re
import pytube
import requests
from pytube import YouTube
import webbrowser

import os, sys
from kivy.resources import resource_add_path, resource_find



# variaveis globais
link_video = ""

youtube = ""

titulo_video = ""

thumbnail_video = ""





class JanelaGerenciadora(ScreenManager):

   pass

class JanelaChecarInternet(Screen):
    pass


class JanelaPrincipal(Screen):

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.eventos_teclado)

        #------------- CÓDIGO IMPORTANTISSIMO ------------------------  --->remove arquivos de video se houver algum na pasta de arquivos de audio
        if os.path.exists("./downloads_mp3"):

            path1 = "./downloads_mp3" 
            for file in os.listdir(path1):                  #For para percorrer dentro da pasta passada anteriormente
                if re.search('mp4', file):                 #If verificando se o arquivo e .MP4                    
                    mp4_path = os.path.join(path1 , file)
                    os.remove(mp4_path)
        #-------------------------------------------------------------

        return super().on_pre_enter(*args)
    


    def eventos_teclado(self, window, key, *args):
        if self.ids.caixa_link.text != "" and key == 13:
            self.pegar_video()
            #print(key) #-  para mostrar qual o codigo de cada tecla pressionada
            return True



    def pegar_video(self):
        global link_video, youtube, titulo_video, thumbnail_video
        self.dialog = MDDialog(title = "ERRO",text="Link inválido!", buttons=[MDFlatButton(text="OK", on_release = self.liberar)])

        try:
            link_video = self.ids.caixa_link.text
            youtube = YouTube(link_video)
            titulo_video = youtube.title
            thumbnail_video = youtube.thumbnail_url
            self.mudar_tela()

        except pytube.exceptions.RegexMatchError:
            # escessao de link incorreto
            self.dialog.open()

        except pytube.exceptions.VideoUnavailable:
            # escessao de link incorreto
            self.dialog.open()

        
        

    def liberar(self, obj):
        self.dialog.dismiss()


    def mudar_tela(self):
        HeartDownloader.get_running_app().root.current = "janelabaixar"
        HeartDownloader.get_running_app().root.transition.direction='left'


    def apagar_caixa_link(self):
        self.ids.caixa_link.text = ""

   
    def abrir_link(self):
        meu_site = "https://kalebeportfolio.netlify.app/"
        webbrowser.open(meu_site)

              

class JanelaBaixar(Screen):
    popup_download = None

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)
        return super().on_pre_enter(*args)


    def voltar(self, window, key, *args):
        if key == 27:
            HeartDownloader.get_running_app().root.current = 'janelaprincipal' 
            HeartDownloader.get_running_app().root.transition.direction='right'
            #Mp3Downloader é a classe que herda de MDApp ou seja, é a classe principal do app, então tanto faz usar Mp3Downloader ou MDApp

        # print(key) -  para mostrar qual o codigo de cada tecla pressionada
            return True
        

    def on_enter(self, *args):
        super().on_enter(*args)
        self.ids.title.text = titulo_video
        self.ids.thumbnail.source = thumbnail_video



           

    def baixar_video(self):
        self.titulo_video = youtube.title
        self.titulo_filtrado = ''.join(filter(str.isalnum, self.titulo_video)) 
        self.filename_mp4 = self.titulo_filtrado + ".mp4"
        self.filename_mp3 = self.titulo_filtrado + ".mp3"

        if os.path.exists("./downloads_mp4/" + self.filename_mp4):
            
            self.mostrar_alert_download()

        
        else:

            path = "./downloads_mp4"                         
            youtube.streams.get_highest_resolution().download(path, filename=self.filename_mp4)
        


    

    def baixar_audio(self):
        self.titulo_video = youtube.title
        self.titulo_filtrado = ''.join(filter(str.isalnum, self.titulo_video)) 
        self.filename_mp4 = self.titulo_filtrado + ".mp4"
        self.filename_mp3 = self.titulo_filtrado + ".mp3"
        
        if os.path.exists("./downloads_mp3/" + self.filename_mp3):
            
            self.mostrar_alert_download()
        
        else:
            
            try:
                path = "./downloads_mp3"                          
                
                my_mp4 = youtube.streams.get_audio_only().download(path, filename=self.filename_mp3)
                base, ext = os.path.splitext(my_mp4)
                my_mp3 = base + '.mp3'
                os.rename(my_mp4, my_mp3)

                #------------- CÓDIGO IMPORTANTISSIMO ------------------------  --->remove arquivos de video se houver algum na pasta de arquivos de audio

                path1 = "./downloads_mp3" 
                for file in os.listdir(path1):                  #For para percorrer dentro da pasta passada anteriormente
                    if re.search('mp4', file):                 #If verificando se o arquivo e .MP4                    
                        mp4_path = os.path.join(path1 , file)
                        os.remove(mp4_path)
                #-------------------------------------------------------------


            except:
                None

    
    def mostrar_alert_download(self):
        self.alert = MDDialog(title = "ERRO",text="Você ja fez o download desse arquivo!", buttons=[MDFlatButton(text="OK", on_release = self.liberar_alert)])
        self.alert.open()
    
    
    def liberar_alert(self, obj):
        self.alert.dismiss()

        

class HeartDownloader(MDApp):

    def on_start(self):
        # função de nome reservado do kivy, é ativada toda vez que a classe é chamada!
        self.test_internet()

        return super().on_start()

    def test_internet(self):
        
        self.dialog = MDDialog(title = "ERRO",text="Sem conexão com a internet! :(", buttons=[MDFlatButton(text="OK", on_release = self.liberar)])

        try:
            url = 'https://www.google.com'
            timeout = 5
            requests.get(url, timeout=timeout)

        except:
            self.dialog.open()


    

    def liberar(self, obj):
        self.dialog.dismiss()
        self.stop()

    

    def voltar(self):
        # ESTA FUNÇÃO É NECESSARIA PORQUE O TOOLBAR NÃO RECONHECE ESSES METODOS NO LAMBDAX :
        HeartDownloader.get_running_app().root.current = "janelaprincipal"
        HeartDownloader.get_running_app().root.transition.direction='right'


    def mudar_cor(self):
        tema = self.theme_cls.theme_style
        if tema == "Dark":
            self.theme_cls.theme_style = 'Light'

            
        else:
            self.theme_cls.theme_style = 'Dark'

       

    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Gray"
        self.title = "Heart Downloader"
        self.icon = 'C:\\projeto_kivy\\logo.png'
        #self.theme_cls.primary_hue = "500"

        return Builder.load_file("main.kv")


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    HeartDownloader().run()

