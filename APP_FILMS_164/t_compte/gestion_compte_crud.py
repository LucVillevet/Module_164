"""Gestion des "routes" FLASK et des données pour les films.
Fichier : gestion_films_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.t_compte.gestion_compte_wtf_forms import *


# @app.route("/comptes_afficher/<int:id_compte_sel>", methods=['GET', 'POST'])
@app.route("/comptes_afficher", methods=['GET', 'POST'])
def comptes_afficher():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_comptes_afficher_data = """SELECT ID_compte, Pseudo, Password FROM t_compte"""
                mc_afficher.execute(strsql_comptes_afficher_data)

                # Récupère les données de la requête.
                data_comptes_afficher = mc_afficher.fetchall()
                print("data_comptes ", data_comptes_afficher, " Type : ", type(data_comptes_afficher))

                # Différencier les messages.
                if not data_comptes_afficher:
                    flash("""La table "t_compte" est vide. !""", "warning")
                else:
                    flash(f"Données de la base de données des comptes affichés !!", "success")

                print("donnees_afficher  ", data_comptes_afficher)
                # Envoie la page "HTML" au serveur.
                return render_template("t_compte/compte_afficher.html", data=data_comptes_afficher)

        except Exception as Exception_comptes_afficher:
            raise ExceptionComptesAfficher(f"fichier : {Path(__file__).name}  ;  {comptes_afficher.__name__} ;"
                                               f"{Exception_comptes_afficher}")


"""Ajouter un film grâce au formulaire "film_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""


@app.route("/compte_add", methods=['GET', 'POST'])
def compte_add():
    # Objet formulaire pour AJOUTER un film
    form_add_compte = FormWTFAddCompte()
    try:
        if request.method == "POST":
            if form_add_compte.validate_on_submit():
                pseudo_add = form_add_compte.pseudo_add_wtf.data
                password_add = form_add_compte.password_add_wtf.data
                valeurs_insertion_dictionnaire = {"value_pseudo": pseudo_add,
                                                  "value_password": password_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_compte = """INSERT INTO t_compte (ID_compte, Pseudo, Password, Droits) 
                                            VALUES (NULL,%(value_pseudo)s,%(value_password)s,NULL) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_compte, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('comptes_afficher'))

        elif request.method == "GET":
            return render_template("t_compte/compte_add.html", form_add_compte=form_add_compte)

    except Exception as Exception_comptes_ajouter_wtf:
        raise ExceptionComptesAjouter(f"fichier : {Path(__file__).name}  ;  "
                                        f"{compte_add.__name__} ; "
                                        f"{Exception_comptes_ajouter_wtf}")


"""Editer(update) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/compte_update", methods=['GET', 'POST'])
def compte_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_compte_update = request.values['id_compte_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_compte = FormWTFUpdateCompte()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update_compte.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            pseudo_update = form_update_compte.pseudo_update_wtf.data
            password_update = form_update_compte.password_update_wtf.data

            valeur_update_dictionnaire = {"value_id_compte": id_compte_update,
                                          "value_pseudo": pseudo_update,
                                          "value_password": password_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_compte = """UPDATE t_compte SET Pseudo = %(value_pseudo)s,
                                                           Password = %(value_password)s
                                                           WHERE ID_compte = %(value_id_compte)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_compte, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('comptes_afficher'))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_genre" de la "t_genre"
            str_sql_id_compte = "SELECT * FROM t_compte WHERE ID_compte = %(value_id_compte)s"
            valeur_select_dictionnaire = {"value_id_compte": id_compte_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_compte, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_compte = mybd_conn.fetchone()
            print("data_compte ", data_compte, " type ", type(data_compte))

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_compte.pseudo_update_wtf.data = data_compte["Pseudo"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" pseudo  ", data_compte["Pseudo"], "  type ", type(data_compte["Pseudo"]))
            form_update_compte.password_update_wtf.data = data_compte["Password"]

            return render_template("t_compte/compte_update.html", form_update_compte=form_update_compte)

    except Exception as Exception_compte_update_wtf:
        raise ExceptionComptesUpdate(f"fichier : {Path(__file__).name}  ;  "
                                     f"{compte_update.__name__} ; "
                                     f"{Exception_compte_update_wtf}")


"""Effacer(delete) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/compte_delete", methods=['GET', 'POST'])
def compte_delete():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_compte_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_compte_delete = request.values['id_compte_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_compte = FormWTFDeleteCompte()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_compte.submit_btn_annuler.data:
            return redirect(url_for("comptes_afficher"))

        if form_delete_compte.submit_btn_conf_del_compte.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_compte_delete = session['data_compte_delete']
            print("data_compte_delete ", data_compte_delete)

            flash(f"Effacer le compte de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True
            return render_template("t_compte/compte_delete.html",
                                   form_delete_compte=form_delete_compte,
                                   btn_submit_del=btn_submit_del,
                                   data_compte_del=data_compte_delete
                                   )
        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_compte.submit_btn_del_compte.data:
            valeur_delete_dictionnaire = {"value_id_compte": id_compte_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_compte = """UPDATE t_donnees SET FK_compte = 0 WHERE FK_compte = %(value_id_compte)s"""
            str_sql_delete_compte = """DELETE FROM t_compte WHERE ID_compte = %(value_id_compte)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_genre_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_compte, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_compte, valeur_delete_dictionnaire)

            flash(f"Compte définitivement effacé !!", "success")
            print(f"Compte définitivement effacé !!")

            # afficher les données
            return redirect(url_for('comptes_afficher'))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_compte": id_compte_delete}
            print(id_compte_delete, type(id_compte_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_compte_delete = """SELECT * FROM t_compte WHERE ID_compte = %(value_id_compte)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_compte_delete, valeur_select_dictionnaire)
                data_compte_delete = mydb_conn.fetchall()
                print("data_compte_delete...", data_compte_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_compte_delete'] = data_compte_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

            return render_template("t_compte/compte_delete.html",
                                   form_delete_compte=form_delete_compte,
                                   btn_submit_del=btn_submit_del,
                                   data_compte_del=data_compte_delete
                                   )

    except Exception as Exception_compte_delete_wtf:
        raise ExceptionComptesDelete(f"fichier : {Path(__file__).name}  ;  "
                                     f"{compte_delete.__name__} ; "
                                     f"{Exception_compte_delete_wtf}")
