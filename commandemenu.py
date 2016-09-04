#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
import pickle

def ecritureConfig():
    with open('donnees', 'wb') as fichier:
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(config) 

with open('donnees', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    config_recupere = mon_depickler.load()

    config = {
        "USER" : config_recupere["USER"],
        "WIT_AI_KEY" : config_recupere["WIT_AI_KEY"],
        "RECORD_DURATION" : config_recupere["RECORD_DURATION"],
        "SENSIBILITE_SNOWBOY" : config_recupere["SENSIBILITE_SNOWBOY"],
        "NIVEAU_CONFIDENCE" : config_recupere["NIVEAU_CONFIDENCE"],
        "ECHANTILLON_SILENCE" : config_recupere["ECHANTILLON_SILENCE"]
    }
    
if sys.argv[1] == "wit":
    print ""
    print ""
    print "Nouvelle clé WIT"
    print ""
    config["WIT_AI_KEY"] = raw_input("Clé WIT : ")
    ecritureConfig()
elif sys.argv[1] == "user":
    print ""
    print ""
    print "Nouveau nom utilisateur"
    print ""
    config["USER"] = raw_input("Nom utilisateur : ")
    ecritureConfig()
elif sys.argv[1] == "record":
    print ""
    print ""
    print "Nouvelle durée d'enregistrement en seconde"
    print ""
    config["RECORD_DURATION"] = int(raw_input("Durée enregistrement : "))
    ecritureConfig() 
elif sys.argv[1] == "snowboy":
    print ""
    print ""
    print "Nouvelle sensibilité de SnowBoy entre 0 et 1"
    print ""
    config["SENSIBILITE_SNOWBOY"] = float(raw_input("Sensibilité SnowBoy : "))
    ecritureConfig()  
elif sys.argv[1] == "confidence":
    print ""
    print ""
    print "Nouveau niveau de confidence entre 0 et 1"
    print ""
    config["NIVEAU_CONFIDENCE"] = float(raw_input("Niveau de confidence : "))
    ecritureConfig() 
elif sys.argv[1] == "silence":
    print ""
    print ""
    print "Nouveau temps d'échantillon du silence en seconde"
    print ""
    config["ECHANTILLON_SILENCE"] = float(raw_input("Temps échantillon silence : "))
    ecritureConfig()     