"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddCompte(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    Regexp("", message="")
    pseudo_add_wtf = StringField("Pseudo", validators=[Length(min=1, max=2000,
                                                        message="Mauvaise nouvelle, l'ID du compte sera plus utile")])
    password_add_wtf = StringField("Mot de passe", validators=[Length(min=1, max=2000,
                                                        message="Attention, il ne sera pas caché")])

    submit = SubmitField("Enregistrer Compte")


class FormWTFUpdateCompte(FlaskForm):
    """
        Dans le formulaire "film_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    pseudo_update_wtf = StringField("Pseudo", widget=TextArea())
    password_update_wtf = StringField("Mot de passe", widget=TextArea())
    submit = SubmitField("Enregistrer Compte")


class FormWTFDeleteCompte(FlaskForm):
    """
        Dans le formulaire "film_delete_wtf.html"

        nom_film_delete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    compte_delete_wtf = StringField("Effacer ce compte")
    submit_btn_del_compte = SubmitField("Effacer compte")
    submit_btn_conf_del_compte = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
