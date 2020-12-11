#!/usr/local/bin/python3
import psycopg2
import os
import datetime
import json 

def patient_menu(conn):
    choice = 0
    continu = True
    while(continu):
        os.system("clear")
        print("\n\t\tGestion des patients")
        print("\n\t### Que voulez-vous faire ? ###")
        print("\t0\tRevenir au menu principal\n")
        print("\t1\tVoir les patients")
        print("\t2\tAjouter un patient")
        print("\t3\tModifier un patient")
        print("\t4\tRechercher un patient par numero de puce ou passeport")
        print("\t5\tVoir le détail du dossier médical d'un patient")
        choice = int(input("\n> "))
        os.system("clear")

        if(choice == 0):
            continu = False
            print("\n\tRetour au menu")
        elif(choice == 1):
            voir_patients(conn)
        elif(choice==2):
            ajouter_patient(conn)
        elif(choice==3):
            modifier_patient(conn)
        elif(choice==4):
            rechercher_patient(conn)
        elif(choice==5):
            detail_patient(conn)


def voir_patients(conn):
    cur = conn.cursor()
    sql = "SELECT * FROM PATIENT ORDER BY ID ASC;"
    cur.execute(sql)
    res = cur.fetchall()
    print("\tVoici les patients :")
    print("\t#ID")
    for raw in res:
        print("\t#%s\t%s" % (raw[0], raw[1]))
    input()
    cur.close()

def ajouter_patient(conn):  
    cur = conn.cursor()
    print("\tInsertion d'un nouveau patient :")
    nom = quote(input("\tIndiquez le nom\n\t> "))   
    annee_bd = int(input("\tIndiquez l'annee de naissance\n\t> "))
    mois_bd = int(input("\tIndiquez le mois de naissance\n\t> "))
    jour_bd= int(input("\tIndiquez le jour de naissance\n\t> "))
    date_de_naissance= quote(datetime.date(annee_bd, mois_bd, jour_bd))
    taille = quote(input("\tIndiquez la taille (Petite, Moyenne)\n\t> "))   
    puceID = quote(input("\tIndiquez le numéro de puce\n\t> "))   
    passeportID = quote(input("\tIndiquez le numéro de passeport\n\t> "))   
    print("\n\tEspèces possibles :")
    sql = "SELECT * FROM ESPECE ORDER BY ESPECE ASC"
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print("\t- %s" % (result[0]))
    espece = quote(input("\tIndiquez l'espèce\n\t> "))   
    try: 
        sql = "INSERT INTO PATIENT (Nom, DateDeNaissance, Taille, NumeroPuceID, NumeroPasseport, Espece) VALUES (%s, %s, %s, %s, %s, %s);" % (nom, date_de_naissance, taille, puceID, passeportID, espece)
        cur.execute(sql)
        conn.commit()
        print("\tCommande exécutée")
    except psycopg2.IntegrityError as e: 
        conn.rollback()
        print(e)
    cur.close()

def modifier_patient(conn):
    print("\tVeuillez indiquer l'ID du client à modifier :")
    id = int(input("\n> "))
    print("\n\tVeuillez indiquer l'information que vous voulez modifier :")
    print("\tnom")
    print("\tnumeroPuceID")
    print("\tnumeroPasseport")
    column = str(input("\n> "))
    cur = conn.cursor()
    print("\n\tVeuillez indiquer la nouvelle valeur :")
    value = quote(input("\n> "))
    try:
        sql = "UPDATE PATIENT SET %s = %s WHERE ID=%i;" % (column,value,id)
        cur.execute(sql)
        print("\tCommande exécutée")
        conn.commit()
        cur.close()
    except psycopg2.Error:
        print("Erreur lors de la mise à jour, merci de réessayer.")

def rechercher_patient(conn):
    print("\tVeuillez indiquer le numéro de puce ou de passeport du patient :")
    string = quote(input("\n> "))
    cur = conn.cursor()
    sql = "SELECT * FROM PATIENT WHERE strpos(numeroPuceID,%s)>0 OR strpos(numeroPasseport,%s)>0 ORDER BY ID ASC;" % (string,string)
    cur.execute(sql)
    res = cur.fetchall()
    print("\tVoici les patients trouvés pour votre requête :")
    print("\t#ID")
    for raw in res:
        print("\t#%s\t%s" % (raw[0], raw[1]))
    input()
    cur.close()

def detail_patient(conn):
    print("\tVeuillez indiquer l'ID du patient:")
    ID = int(input("\n> "))
    cur = conn.cursor()
    sql = "SELECT * FROM PATIENT WHERE id=%i;" % (ID)
    cur.execute(sql)
    res = cur.fetchall()
    print("\t#ID : %i" % (ID))
    for raw in res:
        print("\t%s (né le %s)" % (raw[1],raw[2]))
        print("\tEspèce : %s" % raw[6])
        print("\tTaille : %s" % raw[3])
        print("\tNuméro de puce : %s" % raw[4])
        print("\tNuméro de passeport : %s" % raw[5])

    sql = "SELECT * FROM PROPRIETAIRE_ACTUEL WHERE ID_Patient=%i" % (ID)
    cur.execute(sql)
    res = cur.fetchall()
    print("\n\tPropriétaire actuel")
    for raw in res:
        print("\t  - #%s\t%s %s (depuis le %s)" % (raw[2],raw[3],raw[4],raw[5]))
   
    sql = "SELECT * FROM PROPRIETAIRE_PASSE WHERE ID_Patient=%i" % (ID)
    cur.execute(sql)
    res = cur.fetchall()
    print("\n\tAnciens propriétaires")
    for raw in res:
        print("\t  - #%s\t%s %s (du %s au %s)" % (raw[2],raw[3],raw[4],raw[5],raw[6]))

    sql = "SELECT * FROM SOIGNANT_ACTUEL WHERE ID_Patient=%i" % (ID)
    cur.execute(sql)
    res = cur.fetchall()
    print("\n\tSoignants actuels")
    for raw in res:
        print("\t  - #%s\t%s %s (depuis le %s)" % (raw[2],raw[3],raw[4],raw[5]))
   
    sql = "SELECT * FROM SOIGNANT_PASSE WHERE ID_Patient=%i" % (ID)
    cur.execute(sql)
    res = cur.fetchall()
    print("\n\tAnciens soignants")
    for raw in res:
        print("\t  - #%s\t%s %s (du %s au %s)" % (raw[2],raw[3],raw[4],raw[5],raw[6]))
    print('\n')
    input()
    cur.close()

def quote(s):
    if s:
        return '\'%s\'' % s
    else:
        return 'NULL'
