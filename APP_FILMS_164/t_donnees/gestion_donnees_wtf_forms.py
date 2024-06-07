"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField, DateTimeField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea
import datetime


class FormWTFAddTimbre(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    Regexp("", message="Erreur")
    fk_compte_add_wtf = IntegerField("ID du compte concerné", validators=[NumberRange(min=1, max=None,
                                                                             message=u"Entrez l'indentifiant du "
                                                                                     u"compte, ne pas confondre "
                                                                                     u"avec le pseudo.")])
    fk_emplacement_add_wtf = IntegerField("ID du lieu", validators=[NumberRange(min=1, max=None,
                                                                       message=u"Entrez l'ID dans la "
                                                                               u"base de données.")])
    fk_type_add_wtf = IntegerField("ID du type", validators=[NumberRange(min=1, max=None,
                                                                       message=u"Entrez l'ID dans la "
                                                                               u"base de données.")])
    date_add_wtf = DateField("Date du timbrage", validators=[InputRequired("Date obligatoire"),
                                                                DataRequired("Date non valide")])
    heure_add_wtf = TimeField("Heure du timbrage", validators=[InputRequired("Heure obligatoire"),
                                                        DataRequired("Heure non valide")])
    commentaire_add_wtf = StringField("Description ", widget=TextArea())

    submit = SubmitField("Enregistrer timbre")


class FormWTFUpdateTimbre(FlaskForm):
    """
        Dans le formulaire "film_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    fk_compte_update_wtf = IntegerField("ID du compte concerné", validators=[NumberRange(min=1, max=None,
                                                                                         message=u"Entrez l'indentifiant du "
                                                                                                 u"compte, ne pas confondre "
                                                                                                 u"avec le pseudo.")])
    fk_emplacement_update_wtf = IntegerField("ID du lieu", validators=[NumberRange(min=1, max=None,
                                                                                message=u"Entrez l'ID dans la "
                                                                                        u"base de données.")])
    fk_type_update_wtf = IntegerField("ID du type", validators=[NumberRange(min=1, max=None,
                                                                         message=u"Entrez l'ID dans la "
                                                                                 u"base de données.")])
    date_update_wtf = DateField("Date du timbrage", validators=[InputRequired("Date obligatoire"),
                                                                    DataRequired("Date non valide")])
    heure_update_wtf = TimeField("Heure du timbrage", validators=[InputRequired("Heure obligatoire"),
                                                            DataRequired("Heure non valide")])
    commentaire_update_wtf = StringField("Description ", widget=TextArea())

    submit = SubmitField("Enregistrer timbre")


class FormWTFDeleteTimbre(FlaskForm):
    """
        Dans le formulaire "film_delete_wtf.html"

        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    submit_btn_del_timbre = SubmitField("Effacer timbre")
    submit_btn_conf_del_timbre = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
