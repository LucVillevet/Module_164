"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
import datetime
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.t_donnees.gestion_donnees_wtf_forms import *

"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /films_genres_afficher
    
    But : Afficher les films avec les genres associés pour chaque film.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"
                 
"""


@app.route("/donnees_afficher/<int:id_compte_sel>", methods=['GET', 'POST'])
@app.route("/donnees_afficher", methods=['GET', 'POST'])
def donnees_afficher(id_compte_sel=0):
    print(" donnees_afficher id_compte_sel ", id_compte_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_donnees_afficher_data = """SELECT ID_donnee, Pseudo, Emplacement, Type,
                                                          Date, Heure, Commentaire FROM t_donnees
                                                          LEFT JOIN t_compte ON t_donnees.FK_compte = t_compte.ID_compte
                                                          LEFT JOIN t_lieu ON t_donnees.FK_emplacement = t_lieu.ID_lieu
                                                          LEFT JOIN t_timbre ON t_donnees.FK_timbre = t_timbre.ID_timbre
                                                          """
                if id_compte_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    strsql_donnees_afficher_data += """ ORDER BY Date, Heure"""
                    mc_afficher.execute(strsql_donnees_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_compte_selected_dictionnaire = {"value_id_compte_selected": id_compte_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_donnees_afficher_data += """ WHERE ID_compte = %(value_id_compte_selected)s
                                                        ORDER BY Date, Heure"""

                    mc_afficher.execute(strsql_donnees_afficher_data, valeur_id_compte_selected_dictionnaire)

                # Récupère les données de la requête.
                data_donnees_afficher = mc_afficher.fetchall()

                # Différencier les messages.
                if not data_donnees_afficher and id_compte_sel == 0:
                    flash("""La table "t_donnees" est vide. !""", "warning")
                elif not data_donnees_afficher and id_compte_sel > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"Le compte {id_compte_sel} demandé n'a aucun timbre (ou il n'existe pas !!)", "warning")
                else:
                    flash(f"Données de la base de données affichés !!", "success")

                print("donnees_afficher  ", data_donnees_afficher)
                # Envoie la page "HTML" au serveur.
                return render_template("t_donnees/donnees_afficher.html", data=data_donnees_afficher)

        except Exception as Exception_donnees_afficher:
            raise ExceptionDonneesAfficher(f"fichier : {Path(__file__).name}  ;  {donnees_afficher.__name__} ;"
                                               f"{Exception_donnees_afficher}")


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


# @app.route("/timbre_update/<int:id_timbre_edit_html>", methods=['GET', 'POST'])
@app.route("/timbre_update", methods=['GET', 'POST'])
def timbre_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_timbre_update = request.values['id_timbre_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_timbre = FormWTFUpdateTimbre()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update_timbre.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            fk_compte_update = form_update_timbre.fk_compte_update_wtf.data
            fk_emplacement_update = form_update_timbre.fk_emplacement_update_wtf.data
            fk_type_update = form_update_timbre.fk_type_update_wtf.data
            date_update = form_update_timbre.date_update_wtf.data
            heure_update = form_update_timbre.heure_update_wtf.data
            commentaire_update = form_update_timbre.commentaire_update_wtf.data

            valeur_update_dictionnaire = {"value_id_timbre": id_timbre_update,
                                          "value_fk_compte": fk_compte_update,
                                          "value_fk_emplacement": fk_emplacement_update,
                                          "value_fk_type": fk_type_update,
                                          "value_date": date_update,
                                          "value_heure": heure_update,
                                          "value_commentaire": commentaire_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_donnees = """UPDATE t_donnees SET FK_compte = %(value_fk_compte)s,
                                                        FK_emplacement = %(value_fk_emplacement)s,
                                                        FK_timbre = %(value_fk_type)s,
                                                        Date = %(value_date)s,
                                                        Heure = %(value_heure)s,
                                                        Commentaire = %(value_commentaire)s
                                                        WHERE ID_donnee = %(value_id_timbre)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_donnees, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('donnees_afficher', id_compte_sel=0))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_genre" de la "t_genre"
            str_sql_id_timbre = """SELECT ID_donnee, FK_compte, FK_emplacement, 
                                    FK_timbre, Date, Heure, Commentaire 
                                    FROM t_donnees WHERE ID_donnee = %(value_id_timbre)s"""
            valeur_select_dictionnaire = {"value_id_timbre": id_timbre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_timbre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_line = mybd_conn.fetchone()

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_timbre.fk_compte_update_wtf.data = data_line["FK_compte"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" compte  ", data_line["FK_compte"], "  type ", type(data_line["FK_compte"]))
            form_update_timbre.fk_emplacement_update_wtf.data = data_line["FK_emplacement"]
            form_update_timbre.fk_type_update_wtf.data = data_line["FK_timbre"]
            print(f" valeur  ", data_line["Date"], "  type ", type(data_line["Date"]))
            form_update_timbre.date_update_wtf.data = data_line["Date"]
            print(f" valeur  ", data_line["Heure"], "  type ", type(data_line["Heure"]))
            form_update_timbre.heure_update_wtf.data = datetime.time.fromisoformat(str(data_line["Heure"]))
            form_update_timbre.commentaire_update_wtf.data = data_line["Commentaire"]

            return render_template("t_donnees/donnees_update.html", form_update_timbre=form_update_timbre)

    except Exception as Exception_donnee_update:
        raise ExceptionDonneesUpdate(f"fichier : {Path(__file__).name}  ;  "
                                     f"{timbre_update.__name__} ; "
                                     f"{Exception_donnee_update}")


@app.route("/timbre_add", methods=['GET', 'POST'])
def timbre_add():
    try:
        # Objet formulaire pour AJOUTER un timbre
        form_add_timbre = FormWTFAddTimbre()
        if request.method == "POST":
            if form_add_timbre.validate_on_submit():
                fk_compte_add = form_add_timbre.fk_compte_add_wtf.data
                fk_emplacement_add = form_add_timbre.fk_emplacement_add_wtf.data
                fk_type_add = form_add_timbre.fk_type_add_wtf.data
                date_add = form_add_timbre.date_add_wtf.data
                heure_add = form_add_timbre.heure_add_wtf.data
                commentaire_add = form_add_timbre.commentaire_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_fk_compte": fk_compte_add,
                                                  "value_fk_emplacement": fk_emplacement_add,
                                                  "value_fk_type": fk_type_add,
                                                  "value_date": date_add,
                                                  "value_heure": heure_add,
                                                  "value_commentaire": commentaire_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_film = """INSERT INTO t_donnees (FK_compte, FK_emplacement, 
                                        Date, Heure, Commentaire, FK_timbre) 
                                        VALUES (%(value_fk_compte)s, %(value_fk_emplacement)s, 
                                        %(value_date)s, %(value_heure)s, %(value_commentaire)s,
                                        %(value_fk_type)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_film, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('donnees_afficher', id_compte_sel=0))
        elif request.method == "GET":
            return render_template("t_donnees/donnees_add.html", form_add_timbre=form_add_timbre)

    except Exception as Exception_timbre_ajouter:
        raise ExceptionDonneesAjouter(f"fichier : {Path(__file__).name}  ;  "
                                        f"{timbre_add.__name__} ; "
                                        f"{Exception_timbre_ajouter}")


# @app.route("/timbre_delete/<int:id_timbre_delete_html>", methods=['GET', 'POST'])
@app.route("/timbre_delete", methods=['GET', 'POST'])
def timbre_delete():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_timbre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_timbre_delete = request.values['id_timbre_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_timbre = FormWTFDeleteTimbre()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_timbre.submit_btn_annuler.data:
            return redirect(url_for("donnees_afficher", id_compte_sel=0))

        if form_delete_timbre.submit_btn_conf_del_timbre.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_timbre_delete = session['data_timbre_delete']
            print("data_timbre_delete ", data_timbre_delete)

            flash(f"Effacer le timbre de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

            return render_template("t_donnees/donnees_delete.html",
                                   form_delete_timbre=form_delete_timbre,
                                   btn_submit_del=btn_submit_del,
                                   data_timbre_del=data_timbre_delete
                                   )
        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_timbre.submit_btn_del_timbre.data:
            valeur_delete_dictionnaire = {"value_id_timbre": id_timbre_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_timbre = """DELETE FROM t_donnees WHERE ID_donnee = %(value_id_timbre)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_genre_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_timbre, valeur_delete_dictionnaire)

            flash(f"Timbre définitivement effacé !!", "success")
            print(f"Timbre définitivement effacé !!")

            # afficher les données
            return redirect(url_for('donnees_afficher', id_compte_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_timbre": id_timbre_delete}
            print(id_timbre_delete, type(id_timbre_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_donnees_delete = """SELECT * FROM t_donnees WHERE ID_donnee = %(value_id_timbre)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_donnees_delete, valeur_select_dictionnaire)
                data_timbre_delete = mydb_conn.fetchall()
                print("data_timbre_delete...", data_timbre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                for row in data_timbre_delete :
                    row["Heure"] = str(row["Heure"])
                session['data_timbre_delete'] = data_timbre_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

            return render_template("t_donnees/donnees_delete.html",
                                   form_delete_timbre=form_delete_timbre,
                                   btn_submit_del=btn_submit_del,
                                   data_timbre_del=data_timbre_delete
                                   )

    except Exception as Exception_donnees_delete:
        raise ExceptionDonneesDelete(f"fichier : {Path(__file__).name}  ;  "
                                     f"{timbre_delete.__name__} ; "
                                     f"{Exception_donnees_delete}")


"""
    nom: genres_films_afficher_data

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


def timbre_afficher_data(valeur_id_timbre_selected_dict):
    print("valeur_id_timbre_selected_dict...", valeur_id_timbre_selected_dict)
    try:

        strsql_film_selected = """SELECT id_film, nom_film, duree_film, description_film, cover_link_film, date_sortie_film, GROUP_CONCAT(id_genre) as GenresFilms FROM t_genre_film
                                        INNER JOIN t_film ON t_film.id_film = t_genre_film.fk_film
                                        INNER JOIN t_genre ON t_genre.id_genre = t_genre_film.fk_genre
                                        WHERE id_film = %(value_id_film_selected)s"""

        strsql_genres_films_non_attribues = """SELECT id_genre, intitule_genre FROM t_genre WHERE id_genre not in(SELECT id_genre as idGenresFilms FROM t_genre_film
                                                    INNER JOIN t_film ON t_film.id_film = t_genre_film.fk_film
                                                    INNER JOIN t_genre ON t_genre.id_genre = t_genre_film.fk_genre
                                                    WHERE id_film = %(value_id_film_selected)s)"""

        strsql_genres_films_attribues = """SELECT id_film, id_genre, intitule_genre FROM t_genre_film
                                            INNER JOIN t_film ON t_film.id_film = t_genre_film.fk_film
                                            INNER JOIN t_genre ON t_genre.id_genre = t_genre_film.fk_genre
                                            WHERE id_film = %(value_id_film_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_non_attribues, valeur_id_timbre_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("genres_films_afficher_data ----> data_genres_films_non_attribues ", data_genres_films_non_attribues,
                  " Type : ",
                  type(data_genres_films_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_film_selected, valeur_id_timbre_selected_dict)
            # Récupère les données de la requête.
            data_film_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_attribues, valeur_id_timbre_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_genres_films_attribues ", data_genres_films_attribues, " Type : ",
                  type(data_genres_films_attribues))

            # Retourne les données des "SELECT"
            return data_film_selected, data_genres_films_non_attribues, data_genres_films_attribues

    except Exception as Exception_timbre_afficher_data:
        raise ExceptionDonneesAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{timbre_afficher_data.__name__} ; "
                                               f"{Exception_timbre_afficher_data}")
