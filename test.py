from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashBoard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Utilisateurs(db.Model):
    

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    mdp = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        """Representation of table Utilisateur."""
        return '<Utilisateurs %r>' % self.login


@app.route('/', methods=['get','post'])
def index():
    
    if request.method == 'POST':
        if 'connexion' in request.form:

            login = request.form['login']
            mdp = request.form['mdp']
            loginBd = Utilisateurs.query.get(login)
            mdpBd = Utilisateurs.query.get(mdp)
            Connex = Utilisateurs.query.filter_by(login=login).all()
            if Connex.login == login and Connex.mdp == mdp:

                return render_template ("index.html")

        
            else:
            
                return render_template('Connexion.html')
                #return render_template('Inscription.html')
            

        if  'inscription' in request.form:
            return render_template('Inscription.html')
    
    return render_template("Connexion.html")  


@app.route('/inscrip')
def redInscrip():
    return render_template ('Inscription.html')

@app.route('/',methods=['get','post'])
def inscription():
    
    if request.method == 'POST':
       if 'valider' in request.form:

            new_login = request.form['login']
            new_mdp = request.form['mdp']
            new_utilisateur = Utilisateurs(login=new_login, mdp=new_mdp)
            db.session.add(new_utilisateur)
            db.session.commit()
            return 'hello'
        
            

        #if  'retour' in request.form:

        #    return render_template('Connexion.html')


@app.route('/dash')
def redIndex():
    return render_template ('index.html')
    