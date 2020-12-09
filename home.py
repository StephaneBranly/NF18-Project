#!/usr/bin/python3
import psycopg2
import os


def menu(conn):
    os.system("clear")
    print('Vous etes bien connectes !')


def main():
    try:
        server = quote(
            input("Nom du serveur : "))
        dbname = quote(input("Nom de la BDD : "))
        username = quote(input("Nom utilisateur : "))
        password = quote(input("Mot de passe : "))

        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (
            server, dbname, username, password))

        print("Vous êtes connecté à la base de données. Bienvenue %s ! \n" % (username))
        menu(conn)
        conn.close()

    except psycopg2.Error as e:
        print("\nLa connexion a échoué...")
        print(e)


def quote(s):
    if s:
        return '\'%s\'' % s
    else:
        return 'NULL'


# Exécution du programme
main()
