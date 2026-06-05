import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_changez_moi'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/locative_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    rent_amount = db.Column(db.Float, nullable=False)
    deposit_amount = db.Column(db.Float)
    surface_area = db.Column(db.Float)
    rooms = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lease(db.Model):
    __tablename__ = 'leases'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    rent_amount = db.Column(db.Float, nullable=False)
    deposit_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RentalRequest(db.Model):
    __tablename__ = 'rental_requests'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash('Accès non autorisé', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Connexion réussie', 'success')
            return redirect(url_for('dashboard'))
        flash('Email ou mot de passe incorrect', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if User.query.filter_by(email=email).first():
            flash('Email déjà utilisé', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        user = User(email=email, password_hash=hashed_password, role=role, 
                   first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin_dashboard.html')
    elif current_user.role == 'owner':
        return render_template('owner_dashboard.html')
    else:
        return render_template('tenant_dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        db.session.commit()
        flash('Profil mis à jour', 'success')
    return render_template('profile.html', user=current_user)

@app.route('/api/properties', methods=['GET'])
@login_required
def api_properties():
    if current_user.role == 'admin':
        properties = Property.query.all()
    elif current_user.role == 'owner':
        properties = Property.query.filter_by(owner_id=current_user.id).all()
    else:
        properties = Property.query.filter_by(is_available=True).all()
    
    return jsonify([{
        'id': p.id, 'title': p.title, 'address': p.address, 'city': p.city,
        'rent_amount': p.rent_amount, 'is_available': p.is_available,
        'owner_id': p.owner_id
    } for p in properties])

@app.route('/api/users', methods=['GET'])
@login_required
@role_required('admin')
def api_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id, 'email': u.email, 'role': u.role,
        'first_name': u.first_name, 'last_name': u.last_name,
        'phone': u.phone, 'address': u.address
    } for u in users])

@app.route('/api/leases', methods=['GET'])
@login_required
def api_leases():
    if current_user.role == 'admin':
        leases = Lease.query.all()
    elif current_user.role == 'owner':
        leases = Lease.query.join(Property).filter(Property.owner_id == current_user.id).all()
    else:
        leases = Lease.query.filter_by(tenant_id=current_user.id).all()
    
    return jsonify([{
        'id': l.id, 'property_id': l.property_id, 'tenant_id': l.tenant_id,
        'start_date': l.start_date.isoformat(), 'end_date': l.end_date.isoformat(),
        'rent_amount': l.rent_amount, 'status': l.status
    } for l in leases])

@app.route('/api/payments', methods=['GET'])
@login_required
def api_payments():
    if current_user.role == 'admin':
        payments = Payment.query.all()
    elif current_user.role == 'owner':
        payments = Payment.query.join(Lease).join(Property).filter(Property.owner_id == current_user.id).all()
    else:
        payments = Payment.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': p.id, 'lease_id': p.lease_id, 'amount': p.amount,
        'due_date': p.due_date.isoformat(), 'payment_date': p.payment_date.isoformat() if p.payment_date else None,
        'status': p.status, 'payment_method': p.payment_method
    } for p in payments])

@app.route('/api/complaints', methods=['GET'])
@login_required
def api_complaints():
    if current_user.role == 'admin':
        complaints = Complaint.query.all()
    elif current_user.role == 'owner':
        complaints = Complaint.query.join(Property).filter(Property.owner_id == current_user.id).all()
    else:
        complaints = Complaint.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': c.id, 'title': c.title, 'description': c.description,
        'type': c.type, 'status': c.status, 'created_at': c.created_at.isoformat(),
        'property_id': c.property_id
    } for c in complaints])

@app.route('/api/rental-requests', methods=['GET'])
@login_required
def api_rental_requests():
    if current_user.role == 'admin':
        requests = RentalRequest.query.all()
    elif current_user.role == 'owner':
        requests = RentalRequest.query.join(Property).filter(Property.owner_id == current_user.id).all()
    else:
        requests = RentalRequest.query.filter_by(tenant_id=current_user.id).all()
    
    return jsonify([{
        'id': r.id, 'property_id': r.property_id, 'tenant_id': r.tenant_id,
        'message': r.message, 'status': r.status, 'created_at': r.created_at.isoformat()
    } for r in requests])

@app.route('/api/stats')
@login_required
@role_required('admin')
def api_stats():
    total_users = User.query.count()
    total_properties = Property.query.count()
    total_leases = Lease.query.count()
    total_payments = Payment.query.count()
    total_complaints = Complaint.query.count()
    
    return jsonify({
        'total_users': total_users,
        'total_properties': total_properties,
        'total_leases': total_leases,
        'total_payments': total_payments,
        'total_complaints': total_complaints,
        'monthly_revenue': 0
    })

# Créer les tables et l'admin au démarrage
def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                first_name='Admin',
                last_name='System'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin@example.com / admin123")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
