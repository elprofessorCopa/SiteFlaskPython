from app import db,admin
import datetime
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView



class Utilisateur(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nom = db.Column(db.String(50),unique=False,nullable=False)
    prenom = db.Column(db.String(50),unique=False,nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(50),unique=False,nullable=False)
    def __repr__(self):
        return f'User{self.nom}'
    
class Billets(db.Model):
    numero = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destination = db.Column(db.String(50), unique=False, nullable=False)
    destination_image = db.Column(db.String(50), unique=False, nullable=False)
    prix = db.Column(db.Integer, nullable=False)
    date_depart = db.Column(db.DateTime, nullable=False)
    date_retour = db.Column(db.DateTime, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.datetime.today())
    description = db.Column(db.String(), unique=False, nullable=False)

    
    def __repr__(self):
        return f'Billet {self.numero} - {self.destination}'
    
class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_de_billets =  db.Column(db.Integer, nullable=False)
    billet_id = db.Column(db.Integer, db.ForeignKey('billets.numero'), nullable=False)
    methode_paiement = db.Column(db.String(50), unique=False, nullable=False)
    commentaire = db.Column(db.String(), unique=False, nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date_reservation = db.Column(db.DateTime, default = datetime.datetime.today(), nullable=False)
    
    utilisateur = db.relationship('Utilisateur', backref=db.backref('reservations', lazy=True))
    billet = db.relationship('Billets', backref=db.backref('reservations', lazy=True))

    def __repr__(self):
        return f'Reservation {self.id} - Utilisateur {self.utilisateur_id} - Billet {self.billet_id}'


class Galery(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(50), unique=False, nullable=False)
    

class Administrateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def verifier_mot_de_passe(self, mot_de_passe):
        return self.password == mot_de_passe


class PostView(ModelView):
    can_delete = True
    form_columns = ["utilisateur_id", "billet_id", "date_reservation","utilisateur"]
    column_list = ["utilisateur_id", "billet_id", "date_reservation","utilisateur"]

admin.add_view(ModelView(Utilisateur, db.session))
admin.add_view(ModelView(Billets, db.session))
admin.add_view(ModelView(Administrateur, db.session))
admin.add_view(PostView(Reservations, db.session))
admin.add_view(ModelView(Galery, db.session))
    
    
    
    
