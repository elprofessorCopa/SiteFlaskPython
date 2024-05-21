from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField , SelectField 
from wtforms.validators import DataRequired, Email, EqualTo, Length,Regexp

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Entrez votre nom"})
    prenom = StringField('Prenom', validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Entrez votre prénom"})
    email = StringField('Email Address', validators=[DataRequired(), Email(message='Veuillez entrer une adress mail valide.')], render_kw={"placeholder": "Email Address"})
    password = PasswordField('Password', validators=[
    DataRequired(), 
    Length(min=5, max=10, message='Le mot de passe doit avoir entre 5 et 10 caractères.'), 
    Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="Le mot de passe doit contenir au moins une lettre majuscule, une lettre minuscule, un chiffre, et un caractère spécial."),  EqualTo('confirm_password', message='Les mots de passe ne correspondent pas.')], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Signup')

class Reservation(FlaskForm):
    billet_id = SelectField('ID Du Billet ', validators=[DataRequired()], render_kw={"placeholder": "Where to"})
    submit = SubmitField('Signup')

class AdminForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')