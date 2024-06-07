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


class FormWTFAddLieu(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    Regexp("", message="")
    emplacement_add_wtf = StringField("Emplacement", validators=[Length(min=1, max=2000,
                                                        message="Le nom de l'endroit dans la réalité")])
    submit = SubmitField("Enregistrer Lieu")


class FormWTFUpdateLieu(FlaskForm):
    """
        Dans le formulaire "film_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    emplacement_update_wtf = StringField("Emplacement", widget=TextArea())
    submit = SubmitField("Enregistrer Lieu")


class FormWTFDeleteLieu(FlaskForm):
    """
        Dans le formulaire "film_delete_wtf.html"

        nom_film_delete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    lieu_delete_wtf = StringField("Effacer ce lieu")
    submit_btn_del_lieu = SubmitField("Effacer lieu")
    submit_btn_conf_del_lieu = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
