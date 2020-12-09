#!/usr/local/bin/python3
import psycopg2
import os
import datetime

def personnel_menu(conn):
    choice = 0
    continu = True
    while(continu):
        print("\n\t\tGestion du personnel")
        print("\n\t### Que voulez-vous faire ? ###")
        print("\t0\tRevenir au menu principal\n")
        print("\t1\tVoir les membres du personnel")
        print("\t2\tAjouter un membre du personnel")
        print("\t3\tModifier un membre du personnel")
        print("\t4\tRechercher un personnel par son nom ou prénom")
        choice = int(input("\n> "))
        os.system("clear")

        if(choice == 0):
            continu = False
            print("\n\tRetour au menu")
        elif(choice == 1):
            voir_membres_personnel(conn)
        elif(choice==2):
            ajouter_member_personnel(conn)
        elif(choice==3):
            modifier_membre_personnel(conn)
        elif(choice==4):
            rechercher_personnel(conn)


def voir_membres_personnel(conn):
    cur = conn.cursor()
    sql = "SELECT * FROM PERSONNEL ORDER BY ID ASC;"
    cur.execute(sql)
    res = cur.fetchall()
    print("\tVoici les membres du personnel :")
    print("\t#ID")
    for raw in res:
        print("\t#%s\tPOSTE : %s\t\t%s %s (né le %s)\t(coordonnées : - tel: %s - adresse %s)" % (raw[0], raw[6], raw[1], raw[2], raw[3], raw[5], raw[4]))
    input()
    cur.close()

def ajouter_member_personnel(conn):  
    cur = conn.cursor()
    print("\tInsertion d'un nouveau membre du personnel :")
    nom = quote(input("\tIndiquez le nom\n\t> "))
    prenom = quote(input("\tIndiquez le prénom\n\t> "))
    adresse = quote(input("\tIndiquez l'adresse\n\t> "))
    numero_tel = quote(input("\tIndiquez le numéro de téléphone\n\t> "))    
    annee_bd = int(input("\tIndiquez l'annee de naissance\n\t> "))
    mois_bd = int(input("\tIndiquez le mois de naissance\n\t> "))
    jour_bd= int(input("\tIndiquez le jour de naissance\n\t> "))
    date_de_naissance= quote(datetime.date(annee_bd, mois_bd, jour_bd))
    poste = quote(input("\tIndiquez le poste (Veto, Assistant)\n\t> "))
    try: 
        sql = "INSERT INTO PERSONNEL (Nom, Prenom, DateDeNaissance, Adresse, NumeroTel, Poste) VALUES (%s, %s, %s, %s, %s, %s);" % (nom, prenom, date_de_naissance, adresse, numero_tel, poste)
        cur.execute(sql)
        conn.commit()
        print("\tCommande exécutée")
    except psycopg2.IntegrityError as e: 
        conn.rollback()
        print(e)
    cur.close()

def modifier_membre_personnel(conn):
    print("\tVeuillez indiquer l'ID du personnel à modifier :")
    id = int(input("\n> "))
    print("\n\tVeuillez indiquer l'information que vous voulez modifier :")
    print("\tnom")
    print("\tprenom")
    print("\tadresse")
    print("\tnumeroTel")
    print("\tposte")
    column = str(input("\n> "))
    print("\n\tVeuillez indiquer la nouvelle valeur :")
    value = quote(input("\n> "))
    try:
        cur = conn.cursor()
        sql = "UPDATE PERSONNEL SET %s = %s WHERE ID=%i;" % (column,value,id)
        cur.execute(sql)
        print("\tCommande exécutée")
        conn.commit()
        cur.close()
    except psycopg2.Error:
        print("Erreur lors de la mise à jour, merci de réessayer.")

def rechercher_personnel(conn):
    print("\tVeuillez indiquer le nom ou prénom du personnel :")
    string = quote(input("\n> "))
    cur = conn.cursor()
    sql = "SELECT * FROM PERSONNEL WHERE strpos(nom,%s)>0 OR strpos(prenom,%s)>0 ORDER BY ID ASC;" % (string,string)
    cur.execute(sql)
    res = cur.fetchall()
    print("\tVoici les membres du personnel trouvés pour votre requête :")
    print("\t#ID")
    for raw in res:
        print("\t#%s\tPOSTE : %s\t\t%s %s (né le %s)\t(coordonnées : - tel: %s - adresse %s)" % (raw[0], raw[6], raw[1], raw[2], raw[3], raw[5], raw[4]))
    input()
    cur.close()

def quote(s):
    if s:
        return '\'%s\'' % s
    else:
        return 'NULL'
