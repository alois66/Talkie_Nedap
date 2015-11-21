#!/usr/bin/env python
import subprocess
import os
import RPi.GPIO as GPIO
import time
import thread
from pydub import AudioSegment
from flask import Flask

talkie = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)


def IsTheRadioFree(threadName):
    global urgenceAck
    print ("Thread " + threadName + " Started.")
    cnt = 0
    while True:
        GPIO.wait_for_edge(17, GPIO.RISING)
        cnt += 1
        timer[cnt] = time.localtime
        if cnt > 3:
            timer[1] = timer[2]
            timer[2] = timer[3]
            timer[3] = timer[4]
            cnt = 3

        if cnt == 3:
            elapsedtime = timer[3] - timer[1]  # time = temps entre les 3 impulsions
            if elapsedtime > 2:
                urgenceAck = 1


def talking(phrase="", lang="FR", jingle=0, urgence=0):
    global urgenceAck

    try:
        repetitions = 1
        if urgence == 1:
            repetitions = 10

        while repetitions > 0:
            language_dict = {"FR": 'fr-FR',
                             "US": 'en-US',
                             "GB": 'en-GB',
                             "DE": 'de-DE',
                             "ES": 'es-ES',
                             "IT": 'it-IT'
            }
            language = language_dict[lang]
            phrase = phrase.encode('utf-8')
            cachepath = os.path.dirname(os.path.dirname(__file__))
            jinglepath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'jingle'))
            file = 'tts'
            filename = os.path.join(cachepath, file + '.wav')
            filenamemp3 = os.path.join(cachepath, file + '.mp3')
            os.system('pico2wave -l ' + language + ' -w ' + filename + ' "' + phrase + '"')
            song = AudioSegment.from_wav(filename)
            if not jingle or jingle == '0':
                songmodified = song
            else:
                jinglename = os.path.join(jinglepath, jingle + '.mp3')
                try:
                    os.stat(jinglename)
                except:
                    return 'Erreur le jingle %s n\'existe pas' % jinglename
                jinglename = os.path.join(jinglepath, jingle + '.mp3')
                jingle = AudioSegment.from_mp3(jinglename)
                songmodified = jingle + song
            songmodified.export(filenamemp3, format="mp3", bitrate="128k",
                                tags={'albumartist': 'Talkie', 'title': 'TTS', 'artist': 'Talkie'},
                                parameters=["-ar", "44100", "-vol", "100"])
            song = AudioSegment.from_mp3(filenamemp3)
            cmd = ['mplayer']
            cmd.append(filenamemp3)
            if GPIO.input(17) != 0:
                print 'GPIO 17 en cours d\'utilisation'
                while GPIO.input(17) != 0:
                    time.sleep(0.5)
            print 'GPIO 17 libre'
            GPIO.output(18, 1)
            print 'GPIO 18 ON et synthese du message'
            with open(os.devnull, 'wb') as nul:
                subprocess.call(cmd, stdout=nul, stderr=subprocess.STDOUT)
            GPIO.output(18, 0)
            print 'Synthese finie GPIO 18 OFF'
            if urgenceAck == 1:
                urgenceAck = 0
                repetitions = 0

            if repetitions > 0:
                time.sleep(5)  # Delai entre deux repetions de messages dans le cas d'urgence

            repetitions -= 1
    except Exception, expt:
        return str(expt)
    return 'Post %s' % phrase


@talkie.route("/")
def index():
    return "Talkie Web Link !! </br> Use /post/phrase=xx&jingle=xx&lang=xxxx </br> For no jingle use jingle=0 </br> Available languages are : </br> DE : deutsch ; GB : english GB; US : english US; ES : spanish; FR : french; IT : italian </br> To check if server is alive : /hello </br> To check state of GPIO 17 : /gpio-read"


@talkie.route("/hello")
def hello():
    return "Hello World!!"


@talkie.route("/gpio-read")
def gpioread():
    try:
        result = GPIO.input(17)
    except Exception, e:
        return str(e)
    return 'Etat Gpio 17 : ' + str(result)


@talkie.route('/post/phrase=<phrase>&jingle=<jingle>&lang=<lang>')
def route1():
    return talking(phrase, lang, jingle, 0)


@talkie.route('/post/phrase=<phrase>&lang=<lang>')
def route2():
    return talking(phrase, lang, 0, 0)


@talkie.route('/post/phrase=<phrase>&lang=<lang>&urgence=<urgence>')
def route3():
    return talking(phrase, "FR", 0, urgence)


@talkie.route('/post/phrase=<phrase>')
def route4():
    return talking(phrase, "FR", 0, 0)


if __name__ == "__main__":
    try:
        thread.start_new_thread(IsTheRadioFree, ("IsTheRadioFree",))
    except ImportError, e:
        print ("Error with Thread IsTheRadioFree")
        quit()
    except KeyboardInterrupt:
        print 'Ctrl+C pressed cleaning'
        quit()

    try:
        talkie.run(host='0.0.0.0',port=4001)
    except KeyboardInterrupt:
        print 'Ctrl+C pressed cleaning'
        GPIO.cleanup()
    except:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
        
        