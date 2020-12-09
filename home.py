#!/usr/bin/python3
import psycopg2
import os


def menu(conn):
    os.system("clear")
    print('\tVous etes bien connectes !')

    choice = 0
    continu = True
    while(continu):
        print("\n\t### Que voulez-vous faire ? ###")
        print("\n\t0\tQuitter")
        print("\n\t1\tGestion des clients et de leurs animaux")
        print("\n\t2\tGestion interne (personnel, medicaments, rapports, especes)")
        choice = int(input("\n> "))
        os.system("clear")

        if(choice == 0):
            continu = False
            print("\n\tAu revoir.")


def main():
    try:
        # server = quote(
        #     input("Nom du serveur : "))
        # dbname = quote(input("Nom de la BDD : "))
        # username = quote(input("Nom utilisateur : "))
        # password = quote(input("Mot de passe : "))
        server = 'localhost'
        dbname = 'nf18'
        username = 'postgres'
        password = 'admin'
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (
            server, dbname, username, password))

        menu(conn)
        conn.close()
        print("\n\tVous êtes déconnecté.")

    except psycopg2.Error as e:
        print("\n\tLa connexion a échoué...")
        print(e)


def quote(s):
    if s:
        return '\'%s\'' % s
    else:
        return 'NULL'


# Exécution du programme
main()
