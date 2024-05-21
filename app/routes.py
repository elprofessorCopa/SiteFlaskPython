from app import app ,db,bcrypt,login_manager,admin
from flask import render_template,flash,redirect,url_for,request
from app.models import Utilisateur, Billets, Galery, Reservations, Administrateur
from flask_login import login_user,logout_user, current_user, login_required
from app.forms import LoginForm, SignupForm, Reservation, AdminForm
import datetime
from flask_admin.contrib.sqla import ModelView



@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(user_id)


@app.route('/connect', methods=['POST', 'GET'])
def connect():
    login_form = LoginForm()
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        existing_user = Utilisateur.query.filter_by(email=signup_form.email.data).first()
        if existing_user:
            flash('Email address already exists. Please use a different email address.', 'danger')
        else:
            password = signup_form.password.data
            psw_hash = bcrypt.generate_password_hash(password).decode("utf8")
            new_user = Utilisateur(nom=signup_form.nom.data,
                                   prenom=signup_form.prenom.data,
                                   email=signup_form.email.data,
                                   password=psw_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created successfully! Please log in.', 'success')
            return redirect(url_for('connect'))
    
    if login_form.validate_on_submit():
        user = Utilisateur.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('travel'))
        else:
            flash('Échec de la connexion. Veuillez vérifier votre e-mail et votre mot de passe.', 'danger')

    return render_template("connexion.html", login_form=login_form, signup_form=signup_form)
    
@app.route('/', methods=['GET', 'POST'])
@app.route('/travel', methods=['GET', 'POST'])
def travel():
    form = Reservation()

    # Récupérer les données depuis la base de données
    billets = Billets.query.all()  # Supposons que Billets soit le modèle de votre table
    images = Galery.query.all()

    # Récupérez les numéros de billets depuis la base de données
    numeros_billets = Billets.query.with_entities(Billets.numero).all()

    # Peuplez les options du champ billet_id avec les numéros des billets
    form.billet_id.choices = [(billet.numero, billet.numero) for billet in numeros_billets]

    if form.validate_on_submit():
        # Traitement de la soumission du formulaire (si nécessaire)
        pass

    return render_template("index1.html", billets=billets, images=images, form=form)






@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('travel'))


@app.route('/make_reservation',methods=['GET', 'POST'])
@login_required
def make_reservation():
    # Récupérer les données du formulaire
    nombre_billets = request.form.get('nombre_billets')
    billet_id = request.form.get('billets')
    methode_paiement = request.form.get('paiement')
    commentaire = request.form.get('text')

    # Récupérer l'ID de l'utilisateur à partir de la session
    utilisateur_id = current_user.id

    # Créer une nouvelle instance de Reservation
    nouvelle_reservation = Reservations(
        nombre_de_billets=nombre_billets,
        billet_id=billet_id,
        methode_paiement=methode_paiement,
        commentaire=commentaire,
        utilisateur_id=utilisateur_id,
        date_reservation=datetime.datetime.today()
    )

    # Ajouter et committez la nouvelle réservation à la base de données
    db.session.add(nouvelle_reservation)
    db.session.commit()

    flash('Réservation effectuée avec succès!', 'success')
    return redirect(url_for('travel'))


@app.route('/reservations')
@login_required
def reservations():
    # Récupérer les réservations de l'utilisateur actuellement connecté
    user_reservations = Reservations.query.filter_by(utilisateur_id=current_user.id).all()

    total_price = 0

    for reservation in user_reservations:
        # Calculer le prix total de chaque réservation
        total_price += reservation.nombre_de_billets * reservation.billet.prix

    return render_template('reservation.html', reservations=user_reservations, total_price=total_price)

@app.route('/reservation/delete/<int:reservation_id>', methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    # Récupérer la réservation à supprimer
    reservation = Reservations.query.get_or_404(reservation_id)

    if reservation.utilisateur_id != current_user.id:
        flash("Vous n'êtes pas autorisé à supprimer cette réservation.", 'danger')
        return redirect(url_for('reservations'))

    # Supprimer la réservation de la base de données
    db.session.delete(reservation)
    db.session.commit()

    flash('La réservation a été supprimée avec succès.', 'success')
    return redirect(url_for('reservations'))



@app.route('/connectAdmin', methods=['GET', 'POST'])
def connectAdmin():
     admin_form = AdminForm()
    
     if admin_form.validate_on_submit():
        email = admin_form.email.data
        mot_de_passe = admin_form.password.data

        administrateur = Administrateur.query.filter_by(email=email).first()

        if administrateur and administrateur.verifier_mot_de_passe(mot_de_passe):
            login_user(administrateur)
            flash('Vous êtes connecté en tant qu\'administrateur.', 'success')
            return redirect('/admin')  # Redirection vers l'interface administrateur par défaut
        else:
            utilisateur = Utilisateur.query.filter_by(email=email).first()

            if utilisateur and bcrypt.check_password_hash(utilisateur.password, mot_de_passe):
                login_user(utilisateur)
                flash('Vous êtes connecté.', 'success')
                return redirect(url_for('travel'))
            else:
                flash('Échec de la connexion. Veuillez vérifier vos identifiants.', 'danger')

     return render_template('conAdmin.html',admin_form=admin_form)