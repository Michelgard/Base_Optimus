#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import json
import config
import speech_recognition as sr
import time
import pygame
import subprocess
import os
import signal
import sys

WIT_AI_KEY = config.WIT_AI_KEY
niveauConfidence = config.NIVEAU_CONFIDENCE
echantillonSilence = config.ECHANTILLON_SILENCE
commande = None

#Fonction appelée quand vient l'heure de fermer notre programme
def fermer_programme(signal, frame):
    sys.exit(0)
    
# Connexion du signal à notre fonction
signal.signal(signal.SIGINT, fermer_programme)

#Fonction analyse retour écoute micro en JSON
def texte_json(js, niveauConfidence):
    print js
    if js['_text'] == None:
        play("error.wav")
        play("Je-ne-comprends-pas.wav")
        print "Je-ne-comprends-pas : pas de texte"
        return False
    else:
        if js['outcomes'][0]['entities'] == {}:
            play("error.wav")
            play("Je-ne-trouve-pas-de-correspondance.wav")
            parole(js['_text'])
            print "Je-ne-trouve-pas-de-correspondance a " + js['_text']
            return {'texte':texte, 'entities':"", 'confidence':"", 'intent':""}
        else:
            texte = js['_text']
            for key, value in  js['outcomes'][0]['entities'].iteritems():
                pass
            entities = str(key)
            confidence = value[0]['confidence']
            intent = str(value[0]['value'])
            if confidence < niveauConfidence: #niveau de confidence pour va$
                play("error.wav")
                play("Je-ne-comprends-pas-la-commande.wav")
                parole(texte)
                print "Je-ne-comprends-pas-la-commande confidence < a " + str(niveauConfidence)
                return {'texte':texte, 'entities':entities, 'confidence':confidence, 'intent':intent}
            else:
                return {'texte':texte, 'entities':entities, 'confidence':confidence, 'intent':intent}

def parole(texte):
    tempfile = "temp.wav"
    devnull = open("/dev/null","w")
    subprocess.call(["pico2wave", "-l", "fr-FR", "-w", tempfile, texte],stderr=devnull)
    subprocess.call(["aplay", tempfile],stderr=devnull)
    os.remove(tempfile)

def play(fichier):
    path = os.getcwd() + "/les_sons/" + fichier
    pygame.mixer.init(frequency=16000, channels=1)
    pygame.mixer.Sound(path).play()
    while pygame.mixer.get_busy():
        # lecture en cours
        pass

def callback(r, audio):
    text = r.recognize_wit(audio, WIT_AI_KEY, True)
    global commande 
    commande = texte_json(text, niveauConfidence)
	
def record(duration):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, echantillonSilence)
    
    play("triggered.wav")
    play("Oui.wav")
    
    stop_listening = r.listen_in_background(sr.Microphone(), callback)
    for _ in range(50): time.sleep(0.1) 
    stop_listening()
    
        