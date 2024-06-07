"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.t_lieu.gestion_lieu_wtf_forms import *

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/lieux_afficher", methods=['GET', 'POST'])
def lieux_afficher():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_lieux_afficher_data = """SELECT ID_lieu, Emplacement FROM t_lieu"""
                mc_afficher.execute(strsql_lieux_afficher_data)

                # Récupère les données de la requête.
                data_lieux_afficher = mc_afficher.fetchall()
                print("data_lieux ", data_lieux_afficher, " Type : ", type(data_lieux_afficher))

                # Différencier les messages.
                if not data_lieux_afficher:
                    flash("""La table "t_lieu" est vide. !""", "warning")
                else:
                    flash(f"Données de la base de données des emplacements affichés !!", "success")

                print("donnees_afficher  ", data_lieux_afficher)
                # Envoie la page "HTML" au serveur.
                return render_template("t_lieu/lieu_afficher.html", data=data_lieux_afficher)

        except Exception as Exception_lieu_afficher:
            raise ExceptionLieuAfficher(f"fichier : {Path(__file__).name}  ;  {lieux_afficher.__name__} ;"
                                           f"{Exception_lieu_afficher}")


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/lieu_ajouter", methods=['GET', 'POST'])
def lieu_ajouter():
    # Objet formulaire pour AJOUTER un film
    form_add_lieu = FormWTFAddLieu()
    try:
        if request.method == "POST":
            if form_add_lieu.validate_on_submit():
                emplacement_add = form_add_lieu.emplacement_add_wtf.data
                valeurs_insertion_dictionnaire = {"value_emplacement": emplacement_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_lieu = """INSERT INTO t_lieu (ID_lieu, Emplacement) 
                                                VALUES (NULL,%(value_emplacement)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_lieu, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('lieux_afficher'))

        elif request.method == "GET":
            return render_template("t_lieu/lieu_add.html", form_add_lieu=form_add_lieu)

    except Exception as Exception_lieu_ajouter_wtf:
        raise ExceptionLieuAjouter(f"fichier : {Path(__file__).name}  ;  "
                                        f"{lieu_ajouter.__name__} ; "
                                        f"{Exception_lieu_ajouter_wtf}")


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/lieu_update", methods=['GET', 'POST'])
def lieu_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_lieu_update = request.values['id_lieu_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_lieu = FormWTFUpdateLieu()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update_lieu.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            emplacement_update = form_update_lieu.emplacement_update_wtf.data

            valeur_update_dictionnaire = {"value_id_lieu": id_lieu_update,
                                          "value_emplacement": emplacement_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_lieu = """UPDATE t_lieu SET Emplacement = %(value_emplacement)s 
                                       WHERE ID_lieu = %(value_id_lieu)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_lieu, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('lieux_afficher'))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_genre" de la "t_genre"
            str_sql_id_lieu = "SELECT * FROM t_lieu WHERE ID_lieu = %(value_id_lieu)s"
            valeur_select_dictionnaire = {"value_id_lieu": id_lieu_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_lieu, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_lieu = mybd_conn.fetchone()
            print("data_lieu ", data_lieu, " type ", type(data_lieu))

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_lieu.emplacement_update_wtf.data = data_lieu["Emplacement"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" Emplacement ", data_lieu["Emplacement"], " type ", type(data_lieu["Emplacement"]))

            return render_template("t_lieu/lieu_update.html", form_update_lieu=form_update_lieu)

    except Exception as Exception_lieu_update_wtf:
        raise ExceptionLieuUpdate(f"fichier : {Path(__file__).name}  ;  "
                                      f"{lieu_update.__name__} ; "
                                      f"{Exception_lieu_update_wtf}")


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/lieu_delete", methods=['GET', 'POST'])
def lieu_delete():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_lieu_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_lieu_delete = request.values['id_lieu_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_lieu = FormWTFDeleteLieu()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_lieu.submit_btn_annuler.data:
            return redirect(url_for("lieux_afficher"))

        if form_delete_lieu.submit_btn_conf_del_lieu.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_lieu_delete = session['data_lieu_delete']
            print("data_lieu_delete ", data_lieu_delete)

            flash(f"Effacer l'emplacement de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True
            return render_template("t_lieu/lieu_delete.html",
                                   form_delete_lieu=form_delete_lieu,
                                   btn_submit_del=btn_submit_del,
                                   data_lieu_del=data_lieu_delete
                                   )
        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_lieu.submit_btn_del_lieu.data:
            valeur_delete_dictionnaire = {"value_id_lieu": id_lieu_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_lieu = """UPDATE t_donnees SET FK_emplacement = 0 
                                          WHERE FK_emplacement = %(value_id_lieu)s"""
            str_sql_delete_lieu = """DELETE FROM t_lieu WHERE ID_lieu = %(value_id_lieu)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_genre_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_lieu, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_lieu, valeur_delete_dictionnaire)

            flash(f"Lieu définitivement effacé !!", "success")
            print(f"Lieu définitivement effacé !!")

            # afficher les données
            return redirect(url_for('lieux_afficher'))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_lieu": id_lieu_delete}
            print(id_lieu_delete, type(id_lieu_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_lieu_delete = """SELECT * FROM t_lieu WHERE ID_lieu = %(value_id_lieu)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_lieu_delete, valeur_select_dictionnaire)
                data_lieu_delete = mydb_conn.fetchall()
                print("data_lieu_delete...", data_lieu_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_lieu_delete'] = data_lieu_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

            return render_template("t_lieu/lieu_delete.html",
                                   form_delete_lieu=form_delete_lieu,
                                   btn_submit_del=btn_submit_del,
                                   data_lieu_del=data_lieu_delete
                                   )

    except Exception as Exception_lieu_delete_wtf:
        raise ExceptionLieuDelete(f"fichier : {Path(__file__).name}  ;  "
                                      f"{lieu_delete.__name__} ; "
                                      f"{Exception_lieu_delete_wtf}")
