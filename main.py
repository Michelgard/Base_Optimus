#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import fonction #l'ensemble des fonctions de l'appli
from snowboy.Snowboy import Snowboy
import os
import signal
import sys
import pickle

#Fonction appelée quand vient l'heure de fermer notre programme
def fermer_programme(signal, frame):
    sys.exit(0)
    
# Connexion du signal à notre fonction
signal.signal(signal.SIGINT, fermer_programme)

config_recupere = fonction.lectureConfig()
sensibiliteSnowboy = config_recupere["SENSIBILITE_SNOWBOY"]
duration = config_recupere["RECORD_DURATION"]

fonction.play("Bonjour-je-suis-Optimus.wav") #message au lancement de l'appli 

fin = False #si fin = True arret de l'appli
while (not fin):
    #attente mot magique
    snow = Snowboy('snowboy/resources/optimus.pmdl', sensibiliteSnowboy)
    snow.detection()
    
    i = 0
    fonction.commande = None
    while fonction.commande == None and i < 3: #ecoute trois fois
        fonction.record(duration)
        i = i + 1

    commande = fonction.commande   
    if commande == None: #si aucune commande micro
        fonction.play("timeout.wav")
        fonction.play("J-ai-pas-entendu-de-commande.wav")
        print "j'ai pas entendu de commande"
    if commande: #fonction retour OK commande validée à traiter  
        print "commande validée"
        print commande['texte'], commande['entities'], commande['confidence'], commande['intent']        
    fin = True
    
