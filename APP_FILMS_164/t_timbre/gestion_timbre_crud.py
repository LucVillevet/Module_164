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
from APP_FILMS_164.t_timbre.gestion_timbre_wtf_forms import *

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/types_afficher", methods=['GET', 'POST'])
def types_afficher():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_types_afficher_data = """SELECT ID_timbre, Type FROM t_timbre"""
                mc_afficher.execute(strsql_types_afficher_data)

                # Récupère les données de la requête.
                data_types_afficher = mc_afficher.fetchall()
                print("data_types ", data_types_afficher, " Type : ", type(data_types_afficher))

                # Différencier les messages.
                if not data_types_afficher:
                    flash("""La table "t_timbre" est vide. !""", "warning")
                else:
                    flash(f"Types de timbre de la base de données affichés !!", "success")

                print("donnees_afficher  ", data_types_afficher)
                # Envoie la page "HTML" au serveur.
                return render_template("t_type/type_afficher.html", data=data_types_afficher)

        except Exception as Exception_type_afficher:
            raise ExceptionTypeAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{types_afficher.__name__} ; "
                                          f"{Exception_type_afficher}")


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


@app.route("/type_ajouter", methods=['GET', 'POST'])
def type_ajouter():
    # Objet formulaire pour AJOUTER un film
    form_add_type = FormWTFAddType()
    try:
        if request.method == "POST":
            if form_add_type.validate_on_submit():
                type_add = form_add_type.type_add_wtf.data
                valeurs_insertion_dictionnaire = {"value_type": type_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_type = """INSERT INTO t_timbre (ID_timbre, Type) 
                                                    VALUES (NULL,%(value_type)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_type, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('types_afficher'))

        elif request.method == "GET":
            return render_template("t_type/type_add.html", form_add_type=form_add_type)

    except Exception as Exception_type_ajouter_wtf:
        raise ExceptionTypeAjouter(f"fichier : {Path(__file__).name}  ;  "
                                        f"{type_ajouter.__name__} ; "
                                        f"{Exception_type_ajouter_wtf}")


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


@app.route("/type_update", methods=['GET', 'POST'])
def type_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_type_update = request.values['id_type_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_type = FormWTFUpdateType()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update_type.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            type_update = form_update_type.type_update_wtf.data

            valeur_update_dictionnaire = {"value_id_type": id_type_update,
                                          "value_type": type_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_type = """UPDATE t_timbre SET Type = %(value_type)s 
                                           WHERE ID_timbre = %(value_id_type)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_type, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('types_afficher'))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_genre" de la "t_genre"
            str_sql_id_type = "SELECT * FROM t_timbre WHERE ID_timbre = %(value_id_type)s"
            valeur_select_dictionnaire = {"value_id_type": id_type_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_type, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_type = mybd_conn.fetchone()
            print("data_type ", data_type, " type ", type(data_type))

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_type.type_update_wtf.data = data_type["Type"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" Type ", data_type["Type"], " type ", type(data_type["Type"]))

            return render_template("t_type/type_update.html", form_update_type=form_update_type)

    except Exception as Exception_type_update_wtf:
        raise ExceptionTypeUpdate(f"fichier : {Path(__file__).name}  ;  "
                                      f"{type_update.__name__} ; "
                                      f"{Exception_type_update_wtf}")


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/type_delete", methods=['GET', 'POST'])
def type_delete():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_type_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_type_delete = request.values['id_type_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_type = FormWTFDeleteType()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_type.submit_btn_annuler.data:
            return redirect(url_for("types_afficher"))

        if form_delete_type.submit_btn_conf_del_type.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_type_delete = session['data_type_delete']
            print("data_type_delete ", data_type_delete)

            flash(f"Effacer le type de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True
            return render_template("t_type/type_delete.html",
                                   form_delete_type=form_delete_type,
                                   btn_submit_del=btn_submit_del,
                                   data_type_del=data_type_delete
                                   )
        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_type.submit_btn_del_type.data:
            valeur_delete_dictionnaire = {"value_id_type": id_type_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_type = """UPDATE t_donnees SET FK_timbre = 0 
                                              WHERE FK_timbre = %(value_id_type)s"""
            str_sql_delete_type = """DELETE FROM t_timbre WHERE ID_timbre = %(value_id_type)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_genre_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_type, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_type, valeur_delete_dictionnaire)

            flash(f"Type définitivement effacé !!", "success")
            print(f"Type définitivement effacé !!")

            # afficher les données
            return redirect(url_for('types_afficher'))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_type": id_type_delete}
            print(id_type_delete, type(id_type_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_type_delete = """SELECT * FROM t_timbre WHERE ID_timbre = %(value_id_type)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_type_delete, valeur_select_dictionnaire)
                data_type_delete = mydb_conn.fetchall()
                print("data_type_delete...", data_type_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_type_delete'] = data_type_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

            return render_template("t_type/type_delete.html",
                                   form_delete_type=form_delete_type,
                                   btn_submit_del=btn_submit_del,
                                   data_lieu_del=data_type_delete
                                   )

    except Exception as Exception_type_delete_wtf:
        raise ExceptionTypeDelete(f"fichier : {Path(__file__).name}  ;  "
                                      f"{type_delete.__name__} ; "
                                      f"{Exception_type_delete_wtf}")

