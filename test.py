import vlc
import time 

media_player = vlc.MediaPlayer()

media_player.toggle_fullscreen()


media = vlc.Media("video.mp4")

media_player.set_media(media)

media_player.play()

time.sleep(30)