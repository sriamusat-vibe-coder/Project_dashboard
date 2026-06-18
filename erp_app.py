"""
BIM Bytes Solutions - Integrated ERP System
Run:  python erp_app.py    (auto-creates DB on first run)
Seed: python erp_seed.py   (add demo data)

Demo Credentials
  admin@bimbytes.com    / Admin@123    → Admin
  director@bimbytes.com / Director@123 → Director
  finance@bimbytes.com  / Finance@123  → Finance Manager
  hr@bimbytes.com       / Hr@123       → HR Manager
  bim@bimbytes.com      / Bim@123      → BIM Manager
  pm@bimbytes.com       / Pm@123       → Project Manager
  emp@bimbytes.com      / Emp@123      → Employee
"""
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, jsonify, abort)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
                         login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from functools import wraps
from sqlalchemy import func
import os

app = Flask(__name__, static_folder='static')
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'bim-erp-2024-xK9#mP2'),
    SQLALCHEMY_DATABASE_URI='sqlite:///bim_erp.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the ERP system.'
login_manager.login_message_category = 'warning'

# ── Constants ────────────────────────────────────────────────────────────────
ROLES = {'admin':'Admin','director':'Director','finance':'Finance Manager',
         'hr':'HR Manager','bim_manager':'BIM Manager',
         'project_manager':'Project Manager','employee':'Employee'}
PROJECT_STATUSES = ['Lead','Awarded','Ongoing','On Hold','Completed','Cancelled']
PROJECT_TYPES    = ['BIM Modeling','BIM Coordination','LOD Development','Clash Detection',
                    'As-Built Documentation','BIM Consulting','BIM Management',
                    'Infrastructure BIM','MEP BIM','Structural BIM']
DEPARTMENTS      = ['BIM Production','BIM Coordination','Project Management',
                    'Finance','HR & Administration','Business Development','IT & Technology']
CURRENCIES       = ['INR','AED','USD','EUR','SGD','GBP']
LEAD_STAGES      = ['New Lead','Qualified','Proposal Submitted','Negotiation','Won','Lost']
LEAVE_TYPES      = ['Annual Leave','Sick Leave','Casual Leave','Maternity Leave',
                    'Paternity Leave','Unpaid Leave','Compensatory Leave']
EXPENSE_CATS     = ['BIM Software','Office','Project','Travel','Training','Miscellaneous']
EXP_SUBCATS = {
    'BIM Software':['Revit License','AutoCAD License','Navisworks','Autodesk Construction Cloud',
                    'Enscape','Lumion','SketchUp Pro','BIM 360','Civil 3D','Other Software'],
    'Office':['Rent','Electricity','Internet','Water','Office Supplies','Maintenance'],
    'Project':['Site Visit','Printing & Plotting','Outsourcing','Consultant Fees','Survey'],
    'Travel':['Flight','Hotel','Local Transport','Cab'],
    'Training':['Online Course','Seminar','Workshop','Certification'],
    'Miscellaneous':['Marketing','Legal','Bank Charges','Other'],
}

# ── Models ───────────────────────────────────────────────────────────────────
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(30), nullable=False, default='employee')
    employee_id   = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    last_login    = db.Column(db.DateTime)
    employee      = db.relationship('Employee', backref='user', foreign_keys=[employee_id])
    def set_password(self, pw):   self.password_hash = generate_password_hash(pw)
    def check_password(self, pw): return check_password_hash(self.password_hash, pw)
    @property
    def role_label(self): return ROLES.get(self.role, self.role)
    def can(self, *roles): return self.role == 'admin' or self.role in roles
    def get_id(self): return str(self.id)

class Employee(db.Model):
    __tablename__    = 'employees'
    id               = db.Column(db.Integer, primary_key=True)
    employee_id      = db.Column(db.String(20), unique=True, nullable=False)
    name             = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(120))
    phone            = db.Column(db.String(20))
    department       = db.Column(db.String(60))
    job_title        = db.Column(db.String(100))
    manager_id       = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    date_of_joining  = db.Column(db.Date)
    date_of_birth    = db.Column(db.Date)
    gender           = db.Column(db.String(10))
    country          = db.Column(db.String(50), default='India')
    status           = db.Column(db.String(20), default='Active')
    employment_type  = db.Column(db.String(20), default='Full-time')
    salary           = db.Column(db.Float, default=0)
    hourly_rate      = db.Column(db.Float, default=0)
    leave_balance    = db.Column(db.Float, default=18)
    skills           = db.Column(db.Text)
    address          = db.Column(db.Text)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    manager          = db.relationship('Employee', remote_side=[id], backref='subordinates')
    timesheets       = db.relationship('Timesheet', backref='employee', lazy=True, foreign_keys='Timesheet.employee_id')
    expenses         = db.relationship('Expense', backref='employee', lazy=True)
    leaves           = db.relationship('Leave', backref='employee', lazy=True)

class Client(db.Model):
    __tablename__  = 'clients'
    id             = db.Column(db.Integer, primary_key=True)
    client_code    = db.Column(db.String(20), unique=True)
    name           = db.Column(db.String(100), nullable=False)
    country        = db.Column(db.String(50))
    city           = db.Column(db.String(50))
    email          = db.Column(db.String(120))
    phone          = db.Column(db.String(30))
    industry       = db.Column(db.String(80))
    contact_person = db.Column(db.String(100))
    website        = db.Column(db.String(200))
    notes          = db.Column(db.Text)
    status         = db.Column(db.String(20), default='Active')
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    projects       = db.relationship('Project', backref='client', lazy=True)
    leads          = db.relationship('Lead', backref='client', lazy=True)
    invoices       = db.relationship('Invoice', backref='client', lazy=True)

class Lead(db.Model):
    __tablename__       = 'leads'
    id                  = db.Column(db.Integer, primary_key=True)
    lead_id             = db.Column(db.String(20), unique=True)
    client_id           = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    client_name         = db.Column(db.String(150))
    title               = db.Column(db.String(200), nullable=False)
    estimated_value     = db.Column(db.Float, default=0)
    probability         = db.Column(db.Float, default=0)
    currency            = db.Column(db.String(10), default='INR')
    stage               = db.Column(db.String(30), default='New Lead')
    assigned_to_id      = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    source              = db.Column(db.String(50))
    expected_close_date = db.Column(db.Date)
    description         = db.Column(db.Text)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to_employee = db.relationship('Employee', backref='assigned_leads', foreign_keys=[assigned_to_id])

class Project(db.Model):
    __tablename__      = 'projects'
    id                 = db.Column(db.Integer, primary_key=True)
    project_id         = db.Column(db.String(20), unique=True, nullable=False)
    name               = db.Column(db.String(200), nullable=False)
    client_id          = db.Column(db.Integer, db.ForeignKey('clients.id'))
    project_type       = db.Column(db.String(60))
    software           = db.Column(db.String(100))
    lod_level          = db.Column(db.String(20))
    bim_standard       = db.Column(db.String(50))
    num_buildings      = db.Column(db.Integer)
    country            = db.Column(db.String(50))
    city               = db.Column(db.String(50))
    currency           = db.Column(db.String(10), default='INR')
    contract_value     = db.Column(db.Float, default=0)
    start_date         = db.Column(db.Date)
    end_date           = db.Column(db.Date)
    status             = db.Column(db.String(30), default='Ongoing')
    project_manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    bim_manager_id     = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    description        = db.Column(db.Text)
    created_at         = db.Column(db.DateTime, default=datetime.utcnow)
    project_manager    = db.relationship('Employee', foreign_keys=[project_manager_id], backref='managed_projects')
    bim_manager        = db.relationship('Employee', foreign_keys=[bim_manager_id], backref='bim_projects')
    milestones         = db.relationship('Milestone', backref='project', lazy=True, cascade='all, delete-orphan')
    team_members       = db.relationship('ProjectTeam', backref='project', lazy=True, cascade='all, delete-orphan')
    invoices           = db.relationship('Invoice', backref='project', lazy=True)
    project_expenses   = db.relationship('Expense', backref='project', lazy=True)
    project_timesheets = db.relationship('Timesheet', backref='project', lazy=True)
    bim_records        = db.relationship('BIMRecord', backref='project', lazy=True, cascade='all, delete-orphan')
    @property
    def total_invoiced(self):  return sum(i.total_amount for i in self.invoices)
    @property
    def total_received(self):  return sum(p.amount for i in self.invoices for p in i.payments)
    @property
    def total_expenses(self):  return sum(e.amount for e in self.project_expenses if e.status == 'Finance Approved')
    @property
    def profit(self):          return self.total_received - self.total_expenses

class ProjectTeam(db.Model):
    __tablename__  = 'project_team'
    id             = db.Column(db.Integer, primary_key=True)
    project_id     = db.Column(db.Integer, db.ForeignKey('projects.id'))
    employee_id    = db.Column(db.Integer, db.ForeignKey('employees.id'))
    role_in_project= db.Column(db.String(60))
    assigned_date  = db.Column(db.Date, default=date.today)
    employee       = db.relationship('Employee', backref='project_assignments')

class Milestone(db.Model):
    __tablename__  = 'milestones'
    id             = db.Column(db.Integer, primary_key=True)
    project_id     = db.Column(db.Integer, db.ForeignKey('projects.id'))
    name           = db.Column(db.String(200), nullable=False)
    description    = db.Column(db.Text)
    due_date       = db.Column(db.Date)
    completed_date = db.Column(db.Date)
    amount         = db.Column(db.Float)
    status         = db.Column(db.String(30), default='Pending')
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    __tablename__  = 'invoices'
    id             = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(30), unique=True, nullable=False)
    project_id     = db.Column(db.Integer, db.ForeignKey('projects.id'))
    client_id      = db.Column(db.Integer, db.ForeignKey('clients.id'))
    invoice_date   = db.Column(db.Date, nullable=False)
    due_date       = db.Column(db.Date)
    subtotal       = db.Column(db.Float, default=0)
    tax_amount     = db.Column(db.Float, default=0)
    discount       = db.Column(db.Float, default=0)
    total_amount   = db.Column(db.Float, default=0)
    currency       = db.Column(db.String(10), default='INR')
    status         = db.Column(db.String(20), default='Pending')
    payment_terms  = db.Column(db.String(30))
    notes          = db.Column(db.Text)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    payments       = db.relationship('Payment', backref='invoice', lazy=True, cascade='all, delete-orphan')
    @property
    def amount_paid(self):  return sum(p.amount for p in self.payments)
    @property
    def outstanding(self):  return max(0, self.total_amount - self.amount_paid)
    @property
    def is_overdue(self):
        return self.due_date and self.due_date < date.today() and self.status != 'Paid'

class Payment(db.Model):
    __tablename__  = 'payments'
    id             = db.Column(db.Integer, primary_key=True)
    invoice_id     = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    payment_date   = db.Column(db.Date, nullable=False)
    amount         = db.Column(db.Float, nullable=False)
    currency       = db.Column(db.String(10), default='INR')
    payment_method = db.Column(db.String(30))
    reference      = db.Column(db.String(100))
    notes          = db.Column(db.Text)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    __tablename__       = 'expenses'
    id                  = db.Column(db.Integer, primary_key=True)
    expense_id          = db.Column(db.String(20), unique=True)
    project_id          = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    employee_id         = db.Column(db.Integer, db.ForeignKey('employees.id'))
    expense_date        = db.Column(db.Date, nullable=False)
    category            = db.Column(db.String(50))
    sub_category        = db.Column(db.String(100))
    amount              = db.Column(db.Float, nullable=False)
    currency            = db.Column(db.String(10), default='INR')
    description         = db.Column(db.Text)
    vendor              = db.Column(db.String(100))
    receipt_url         = db.Column(db.String(200))
    status              = db.Column(db.String(30), default='Pending')
    manager_approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    manager_approved_at = db.Column(db.DateTime)
    finance_approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    finance_approved_at = db.Column(db.DateTime)
    rejection_reason    = db.Column(db.Text)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    manager_approver    = db.relationship('User', foreign_keys=[manager_approved_by])
    finance_approver    = db.relationship('User', foreign_keys=[finance_approved_by])

class Timesheet(db.Model):
    __tablename__  = 'timesheets'
    id             = db.Column(db.Integer, primary_key=True)
    employee_id    = db.Column(db.Integer, db.ForeignKey('employees.id'))
    project_id     = db.Column(db.Integer, db.ForeignKey('projects.id'))
    work_date      = db.Column(db.Date, nullable=False)
    hours          = db.Column(db.Float, default=0)
    overtime_hours = db.Column(db.Float, default=0)
    task_description = db.Column(db.Text)
    status         = db.Column(db.String(20), default='Draft')
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at    = db.Column(db.DateTime)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by    = db.relationship('User', foreign_keys=[approved_by_id])

class Leave(db.Model):
    __tablename__ = 'leaves'
    id            = db.Column(db.Integer, primary_key=True)
    employee_id   = db.Column(db.Integer, db.ForeignKey('employees.id'))
    leave_type    = db.Column(db.String(30))
    start_date    = db.Column(db.Date, nullable=False)
    end_date      = db.Column(db.Date, nullable=False)
    days_requested= db.Column(db.Float)
    reason        = db.Column(db.Text)
    status        = db.Column(db.String(20), default='Pending')
    approved_by_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at   = db.Column(db.DateTime)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by   = db.relationship('User', foreign_keys=[approved_by_id])

class BIMRecord(db.Model):
    __tablename__  = 'bim_records'
    id             = db.Column(db.Integer, primary_key=True)
    project_id     = db.Column(db.Integer, db.ForeignKey('projects.id'))
    record_type    = db.Column(db.String(50))
    record_date    = db.Column(db.Date)
    model_version  = db.Column(db.String(20))
    lod_level      = db.Column(db.String(20))
    status         = db.Column(db.String(30), default='Open')
    clash_count    = db.Column(db.Integer)
    description    = db.Column(db.Text)
    file_path      = db.Column(db.String(300))
    submitted_by   = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_by_employee = db.relationship('Employee', foreign_keys=[submitted_by])

class Notification(db.Model):
    __tablename__ = 'notifications'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'))
    title         = db.Column(db.String(200))
    message       = db.Column(db.Text)
    ntype         = db.Column(db.String(20), default='info')
    is_read       = db.Column(db.Boolean, default=False)
    link          = db.Column(db.String(200))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    user          = db.relationship('User', backref='notifications')

# ── Login Manager ────────────────────────────────────────────────────────────
@login_manager.user_loader
def load_user(uid): return User.query.get(int(uid))

# ── Helpers ──────────────────────────────────────────────────────────────────
def role_required(*roles):
    def deco(f):
        @wraps(f)
        def wrapped(*a, **kw):
            if not current_user.is_authenticated: return redirect(url_for('login'))
            if not current_user.can(*roles): abort(403)
            return f(*a, **kw)
        return wrapped
    return deco

def inr(val):
    if val is None: return '₹0'
    try:
        v = float(val)
        if v >= 1e7:   return f'₹{v/1e7:.2f} Cr'
        elif v >= 1e5: return f'₹{v/1e5:.2f} L'
        else:          return f'₹{v:,.0f}'
    except: return '₹0'

def _parse_date(s):
    if not s: return None
    try: return datetime.strptime(s, '%Y-%m-%d').date()
    except: return None

def _today_str(): return date.today().strftime('%Y-%m-%d')

@app.template_filter('inr')
def inr_filter(val): return inr(val)

@app.template_filter('fmt_date')
def fmt_date(d):
    if not d: return '—'
    return d.strftime('%d %b %Y') if isinstance(d, (date, datetime)) else '—'

@app.template_filter('days_ago')
def days_ago(dt):
    if not dt: return ''
    delta = datetime.utcnow() - (dt if isinstance(dt, datetime) else datetime.combine(dt, datetime.min.time()))
    if delta.days == 0:   return 'Today'
    elif delta.days == 1: return 'Yesterday'
    elif delta.days < 7:  return f'{delta.days}d ago'
    return dt.strftime('%d %b %Y') if hasattr(dt, 'strftime') else ''

@app.context_processor
def inject_globals():
    ctx = dict(inr=inr, today=_today_str(), today_dt=date.today(), now=datetime.utcnow())
    if current_user.is_authenticated:
        unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        notifs = Notification.query.filter_by(user_id=current_user.id).order_by(
            Notification.created_at.desc()).limit(5).all()
        ctx.update(unread_count=unread, recent_notifs=notifs)
    else:
        ctx.update(unread_count=0, recent_notifs=[])
    return ctx

# ── Auth ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        pw    = request.form.get('password', '')
        user  = User.query.filter_by(email=email).first()
        if user and user.is_active and user.check_password(pw):
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=bool(request.form.get('remember')))
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('erp/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# ── Dashboard ────────────────────────────────────────────────────────────────
@app.route('/')
@login_required
def dashboard():
    all_projects = Project.query.all()
    all_invoices = Invoice.query.all()
    total_contract    = sum(p.contract_value or 0 for p in all_projects)
    total_invoiced    = sum(i.total_amount or 0 for i in all_invoices)
    total_received    = sum(i.amount_paid for i in all_invoices)
    total_outstanding = total_invoiced - total_received
    total_expenses    = sum(e.amount for e in Expense.query.filter_by(status='Finance Approved').all())
    total_profit      = total_received - total_expenses
    return render_template('erp/dashboard.html',
        total_projects=len(all_projects),
        active_projects=sum(1 for p in all_projects if p.status in ('Ongoing','Awarded')),
        completed_projects=sum(1 for p in all_projects if p.status=='Completed'),
        on_hold_projects=sum(1 for p in all_projects if p.status=='On Hold'),
        total_contract=total_contract, total_invoiced=total_invoiced,
        total_received=total_received, total_outstanding=total_outstanding,
        total_expenses=total_expenses, total_profit=total_profit,
        employee_count=Employee.query.filter_by(status='Active').count(),
        overdue_count=sum(1 for i in all_invoices if i.is_overdue),
        pending_leaves=Leave.query.filter_by(status='Pending').count(),
        pending_expenses=Expense.query.filter_by(status='Pending').count(),
        leads_by_stage={s: Lead.query.filter_by(stage=s).count() for s in LEAD_STAGES},
        recent_projects=Project.query.order_by(Project.created_at.desc()).limit(6).all(),
        recent_invoices=Invoice.query.order_by(Invoice.created_at.desc()).limit(5).all())

@app.route('/api/dashboard-data')
@login_required
def dashboard_api():
    months, rev_data, exp_data, net_data = [], [], [], []
    for i in range(5, -1, -1):
        d = date.today().replace(day=1) - timedelta(days=i*30)
        ym = d.strftime('%Y-%m')
        m_rev = db.session.query(func.sum(Payment.amount)).filter(
            func.strftime('%Y-%m', Payment.payment_date) == ym).scalar() or 0
        m_exp = db.session.query(func.sum(Expense.amount)).filter(
            Expense.status=='Finance Approved',
            func.strftime('%Y-%m', Expense.expense_date)==ym).scalar() or 0
        months.append(d.strftime('%b %Y')); rev_data.append(m_rev)
        exp_data.append(m_exp); net_data.append(m_rev - m_exp)
    all_inv = Invoice.query.all()
    country_rev = {}
    for inv in all_inv:
        if inv.project and inv.project.country:
            country_rev[inv.project.country] = country_rev.get(inv.project.country, 0) + inv.amount_paid
    proj_profit = [{'name':p.name[:20],'revenue':p.total_received,
                    'expense':p.total_expenses,'profit':p.profit}
                   for p in Project.query.all()]
    return jsonify(dict(
        months=months, revenue=rev_data, expenses=exp_data, net=net_data,
        invoice_status=dict(
            paid=Invoice.query.filter_by(status='Paid').count(),
            pending=Invoice.query.filter(Invoice.status.in_(['Pending','Overdue'])).count(),
            partial=Invoice.query.filter_by(status='Partially Paid').count()),
        country_revenue=[{'country':k,'revenue':v}
                         for k,v in sorted(country_rev.items(),key=lambda x:-x[1])],
        project_profitability=proj_profit))

# ── Projects ─────────────────────────────────────────────────────────────────
@app.route('/projects')
@login_required
def projects_list():
    sf = request.args.get('status','')
    qry = Project.query
    if sf: qry = qry.filter_by(status=sf)
    if current_user.role == 'employee' and current_user.employee_id:
        my_ids = [pt.project_id for pt in ProjectTeam.query.filter_by(employee_id=current_user.employee_id).all()]
        qry = qry.filter(Project.id.in_(my_ids))
    return render_template('erp/projects/list.html',
        projects=qry.order_by(Project.created_at.desc()).all())

@app.route('/projects/new', methods=['GET','POST'])
@login_required
@role_required('admin','director','project_manager','bim_manager')
def projects_new():
    clients   = Client.query.order_by(Client.name).all()
    employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    if request.method == 'POST':
        f = request.form
        p = Project(project_id=f.get('project_id','').strip(), name=f['name'],
            client_id=f.get('client_id') or None, project_type=f.get('project_type'),
            software=f.get('software'), lod_level=f.get('lod_level'),
            bim_standard=f.get('bim_standard'),
            num_buildings=int(f.get('num_buildings') or 0) or None,
            country=f.get('country'), currency=f.get('currency','INR'),
            contract_value=float(f.get('contract_value') or 0),
            start_date=_parse_date(f.get('start_date')),
            end_date=_parse_date(f.get('end_date')),
            status=f.get('status','Ongoing'),
            project_manager_id=f.get('project_manager_id') or None,
            description=f.get('description'))
        db.session.add(p); db.session.commit()
        flash(f'Project {p.project_id} created!', 'success')
        return redirect(url_for('projects_detail', pid=p.id))
    return render_template('erp/projects/form.html',
        project=None, clients=clients, employees=employees)

@app.route('/projects/<int:pid>')
@login_required
def projects_detail(pid):
    project = Project.query.get_or_404(pid)
    all_employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    timesheets = Timesheet.query.filter_by(project_id=pid).order_by(Timesheet.work_date.desc()).limit(15).all()
    bim_records = BIMRecord.query.filter_by(project_id=pid).order_by(BIMRecord.created_at.desc()).all()
    return render_template('erp/projects/detail.html',
        project=project, all_employees=all_employees,
        timesheets=timesheets, bim_records=bim_records)

@app.route('/projects/<int:pid>/edit', methods=['GET','POST'])
@login_required
@role_required('admin','director','project_manager','bim_manager','finance')
def projects_edit(pid):
    project   = Project.query.get_or_404(pid)
    clients   = Client.query.order_by(Client.name).all()
    employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    if request.method == 'POST':
        f = request.form
        project.name=f['name']; project.client_id=f.get('client_id') or None
        project.project_type=f.get('project_type'); project.software=f.get('software')
        project.lod_level=f.get('lod_level'); project.bim_standard=f.get('bim_standard')
        project.num_buildings=int(f.get('num_buildings') or 0) or None
        project.country=f.get('country'); project.currency=f.get('currency','INR')
        project.contract_value=float(f.get('contract_value') or 0)
        project.start_date=_parse_date(f.get('start_date'))
        project.end_date=_parse_date(f.get('end_date'))
        project.status=f.get('status',project.status)
        project.project_manager_id=f.get('project_manager_id') or None
        project.description=f.get('description')
        db.session.commit(); flash('Project updated!', 'success')
        return redirect(url_for('projects_detail', pid=project.id))
    return render_template('erp/projects/form.html',
        project=project, clients=clients, employees=employees)

@app.route('/projects/<int:pid>/milestones/add', methods=['POST'])
@login_required
def milestones_add(pid):
    f = request.form
    db.session.add(Milestone(project_id=pid, name=f['name'],
        due_date=_parse_date(f.get('due_date')),
        amount=float(f.get('amount') or 0) or None))
    db.session.commit(); flash('Milestone added!', 'success')
    return redirect(url_for('projects_detail', pid=pid))

@app.route('/milestones/<int:mid>/update', methods=['POST'])
@login_required
def milestone_update(mid):
    m = Milestone.query.get_or_404(mid)
    m.status = request.form.get('status', m.status)
    if m.status == 'Completed': m.completed_date = date.today()
    db.session.commit()
    return redirect(url_for('projects_detail', pid=m.project_id))

@app.route('/projects/<int:pid>/team/add', methods=['POST'])
@login_required
def team_add(pid):
    db.session.add(ProjectTeam(project_id=pid,
        employee_id=request.form['employee_id'],
        role_in_project=request.form.get('role_in_project','Team Member')))
    db.session.commit(); flash('Team member added!', 'success')
    return redirect(url_for('projects_detail', pid=pid))

@app.route('/team/<int:tid>/remove', methods=['POST'])
@login_required
def team_remove(tid):
    pt = ProjectTeam.query.get_or_404(tid); pid = pt.project_id
    db.session.delete(pt); db.session.commit()
    return redirect(url_for('projects_detail', pid=pid))

# ── CRM ──────────────────────────────────────────────────────────────────────
@app.route('/crm/clients')
@login_required
def clients_list():
    return render_template('erp/crm/clients.html',
        clients=Client.query.order_by(Client.name).all())

@app.route('/crm/clients/new', methods=['GET','POST'])
@login_required
@role_required('admin','director','project_manager','bim_manager','finance')
def clients_new():
    if request.method == 'POST':
        f = request.form; count = Client.query.count() + 1
        db.session.add(Client(client_code=f'CLI-{count:03d}',
            name=f['name'], country=f.get('country'), city=f.get('city'),
            email=f.get('email'), phone=f.get('phone'), industry=f.get('industry'),
            contact_person=f.get('contact_person'), website=f.get('website'), notes=f.get('notes')))
        db.session.commit(); flash('Client added!', 'success')
        return redirect(url_for('clients_list'))
    return render_template('erp/crm/client_form.html')

@app.route('/crm/leads')
@login_required
def leads_list():
    sf = request.args.get('stage','')
    qry = Lead.query
    if sf: qry = qry.filter_by(stage=sf)
    return render_template('erp/crm/leads.html',
        leads=qry.order_by(Lead.created_at.desc()).all())

@app.route('/crm/leads/new', methods=['GET','POST'])
@login_required
@role_required('admin','director','project_manager','bim_manager')
def leads_new():
    if request.method == 'POST':
        f = request.form; count = Lead.query.count() + 1
        db.session.add(Lead(lead_id=f'LEAD-{count:03d}',
            client_id=f.get('client_id') or None,
            client_name=f.get('client_name'),
            title=f['title'],
            estimated_value=float(f.get('estimated_value') or 0),
            probability=float(f.get('probability') or 0),
            currency=f.get('currency','INR'),
            stage=f.get('stage','New Lead'),
            assigned_to_id=f.get('assigned_to') or None,
            expected_close_date=_parse_date(f.get('expected_close_date')),
            description=f.get('description')))
        db.session.commit(); flash('Lead created!', 'success')
        return redirect(url_for('leads_list'))
    return render_template('erp/crm/lead_form.html',
        clients=Client.query.order_by(Client.name).all(),
        employees=Employee.query.filter_by(status='Active').order_by(Employee.name).all())

@app.route('/crm/leads/<int:lid>/stage', methods=['POST'])
@login_required
def leads_stage(lid):
    l = Lead.query.get_or_404(lid)
    l.stage = request.form['stage']; l.updated_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('leads_list'))

# ── Finance ───────────────────────────────────────────────────────────────────
@app.route('/finance/invoices')
@login_required
def invoices_list():
    sf = request.args.get('status','')
    qry = Invoice.query
    if sf: qry = qry.filter_by(status=sf)
    return render_template('erp/finance/invoices.html',
        invoices=qry.order_by(Invoice.invoice_date.desc()).all())

@app.route('/finance/invoices/new', methods=['GET','POST'])
@login_required
@role_required('admin','director','finance')
def invoices_new():
    projects = Project.query.order_by(Project.name).all()
    clients  = Client.query.order_by(Client.name).all()
    if request.method == 'POST':
        f = request.form
        sub  = float(f.get('subtotal') or 0)
        tax  = float(f.get('tax_amount') or 0)
        disc = float(f.get('discount') or 0)
        total = float(f.get('total_amount') or (sub + tax - disc))
        inv = Invoice(invoice_number=f['invoice_number'],
            project_id=f.get('project_id') or None,
            client_id=f.get('client_id') or None,
            invoice_date=_parse_date(f['invoice_date']),
            due_date=_parse_date(f.get('due_date')),
            subtotal=sub, tax_amount=tax, discount=disc, total_amount=total,
            currency=f.get('currency','INR'),
            status=f.get('status','Pending'),
            payment_terms=f.get('payment_terms'),
            notes=f.get('notes'))
        db.session.add(inv); db.session.commit()
        flash(f'Invoice {inv.invoice_number} created!', 'success')
        return redirect(url_for('invoice_detail', iid=inv.id))
    last = Invoice.query.order_by(Invoice.id.desc()).first()
    next_inv_num = f'INV-{(last.id+1 if last else 1):04d}'
    return render_template('erp/finance/invoice_form.html',
        projects=projects, clients=clients, next_inv_num=next_inv_num)

@app.route('/finance/invoices/<int:iid>', methods=['GET','POST'])
@login_required
def invoice_detail(iid):
    invoice = Invoice.query.get_or_404(iid)
    if request.method == 'POST':
        if not current_user.can('admin','director','finance'): abort(403)
        f = request.form
        pmt = Payment(invoice_id=iid,
            payment_date=_parse_date(f['payment_date']),
            amount=float(f['amount']),
            payment_method=f.get('payment_method'),
            reference=f.get('reference'))
        db.session.add(pmt)
        paid = invoice.amount_paid + pmt.amount
        if paid >= invoice.total_amount: invoice.status = 'Paid'
        elif paid > 0:                  invoice.status = 'Partially Paid'
        db.session.commit(); flash('Payment recorded!', 'success')
        return redirect(url_for('invoice_detail', iid=iid))
    return render_template('erp/finance/invoice_detail.html', invoice=invoice)

@app.route('/finance/outstanding')
@login_required
@role_required('admin','director','finance')
def outstanding():
    invoices = Invoice.query.filter(Invoice.status != 'Paid').order_by(Invoice.due_date).all()
    return render_template('erp/finance/outstanding.html',
        invoices=invoices, today_dt=date.today())

# ── HR ────────────────────────────────────────────────────────────────────────
@app.route('/hr/employees')
@login_required
def employees_list():
    dept = request.args.get('dept','')
    qry = Employee.query
    if dept: qry = qry.filter_by(department=dept)
    return render_template('erp/hr/employees.html',
        employees=qry.order_by(Employee.name).all())

@app.route('/hr/employees/new', methods=['GET','POST'])
@login_required
@role_required('admin','hr')
def employees_new():
    all_employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    users = User.query.order_by(User.name).all()
    if request.method == 'POST':
        f = request.form
        emp = Employee(employee_id=f.get('employee_id','').strip(),
            name=f['name'], email=f.get('email'), phone=f.get('phone'),
            department=f.get('department'), job_title=f.get('job_title'),
            manager_id=f.get('manager_id') or None,
            date_of_joining=_parse_date(f.get('date_of_joining')),
            date_of_birth=_parse_date(f.get('date_of_birth')),
            gender=f.get('gender'), country=f.get('country','India'),
            status=f.get('status','Active'),
            employment_type=f.get('employment_type','Full-time'),
            salary=float(f.get('salary') or 0),
            hourly_rate=float(f.get('hourly_rate') or 0),
            leave_balance=float(f.get('leave_balance') or 18),
            skills=f.get('skills'), address=f.get('address'),
            user_id=f.get('user_id') or None)
        db.session.add(emp); db.session.commit()
        flash(f'Employee {emp.name} added!', 'success')
        return redirect(url_for('employees_list'))
    return render_template('erp/hr/employee_form.html',
        employee=None, all_employees=all_employees, users=users)

@app.route('/hr/employees/<int:eid>')
@login_required
def employees_detail(eid):
    employee = Employee.query.get_or_404(eid)
    if current_user.role == 'employee' and current_user.employee_id != eid: abort(403)
    return render_template('erp/hr/employee_detail.html', employee=employee)

@app.route('/hr/employees/<int:eid>/edit', methods=['GET','POST'])
@login_required
@role_required('admin','hr')
def employees_edit(eid):
    employee = Employee.query.get_or_404(eid)
    all_employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    users = User.query.order_by(User.name).all()
    if request.method == 'POST':
        f = request.form
        employee.name=f['name']; employee.email=f.get('email')
        employee.phone=f.get('phone'); employee.department=f.get('department')
        employee.job_title=f.get('job_title'); employee.manager_id=f.get('manager_id') or None
        employee.date_of_joining=_parse_date(f.get('date_of_joining'))
        employee.status=f.get('status'); employee.employment_type=f.get('employment_type')
        employee.salary=float(f.get('salary') or 0)
        employee.hourly_rate=float(f.get('hourly_rate') or 0)
        employee.leave_balance=float(f.get('leave_balance') or 18)
        employee.skills=f.get('skills'); employee.address=f.get('address')
        employee.user_id=f.get('user_id') or None
        db.session.commit(); flash('Employee updated!', 'success')
        return redirect(url_for('employees_detail', eid=eid))
    return render_template('erp/hr/employee_form.html',
        employee=employee, all_employees=all_employees, users=users)

@app.route('/hr/leaves')
@login_required
def leaves_list():
    if current_user.can('hr','director','admin','project_manager'):
        sf = request.args.get('status','')
        qry = Leave.query
        if sf: qry = qry.filter_by(status=sf)
        leaves = qry.order_by(Leave.created_at.desc()).all()
    else:
        leaves = Leave.query.filter_by(employee_id=current_user.employee_id).order_by(Leave.created_at.desc()).all()
    return render_template('erp/hr/leaves.html', leaves=leaves,
        employees=Employee.query.filter_by(status='Active').order_by(Employee.name).all())

@app.route('/hr/leaves/apply', methods=['GET','POST'])
@login_required
def leaves_apply():
    if request.method == 'POST':
        f = request.form
        sd = _parse_date(f['start_date']); ed = _parse_date(f['end_date'])
        days = (ed - sd).days + 1 if sd and ed else 1
        db.session.add(Leave(
            employee_id=f.get('employee_id') or current_user.employee_id,
            leave_type=f['leave_type'], start_date=sd, end_date=ed,
            days_requested=days, reason=f.get('reason')))
        db.session.commit(); flash('Leave request submitted!', 'success')
        return redirect(url_for('leaves_list'))
    return render_template('erp/hr/leave_form.html',
        employees=Employee.query.filter_by(status='Active').order_by(Employee.name).all())

@app.route('/hr/leaves/<int:lid>/action', methods=['POST'])
@login_required
@role_required('admin','hr','director','project_manager')
def leaves_action(lid):
    l = Leave.query.get_or_404(lid)
    l.status = 'Approved' if request.form['action']=='approve' else 'Rejected'
    l.approved_by_id = current_user.id; l.approved_at = datetime.utcnow()
    db.session.commit(); flash(f'Leave {l.status.lower()}.', 'success')
    return redirect(url_for('leaves_list'))

# ── Expenses ──────────────────────────────────────────────────────────────────
@app.route('/expenses')
@login_required
def expenses_list():
    sf = request.args.get('status','')
    if current_user.can('admin','director','finance','hr','project_manager','bim_manager'):
        qry = Expense.query
    else:
        qry = Expense.query.filter_by(employee_id=current_user.employee_id)
    if sf: qry = qry.filter_by(status=sf)
    return render_template('erp/expenses/list.html',
        expenses=qry.order_by(Expense.created_at.desc()).all(),
        categories=EXPENSE_CATS)

@app.route('/expenses/new', methods=['GET','POST'])
@login_required
def expenses_new():
    projects  = Project.query.order_by(Project.name).all()
    employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    if request.method == 'POST':
        f = request.form; count = Expense.query.count() + 1
        db.session.add(Expense(expense_id=f'EXP-{count:03d}',
            project_id=f.get('project_id') or None,
            employee_id=f.get('employee_id') or current_user.employee_id,
            expense_date=_parse_date(f['expense_date']),
            category=f.get('category'), sub_category=f.get('sub_category'),
            amount=float(f.get('amount') or 0),
            description=f.get('description'),
            vendor=f.get('vendor'), receipt_url=f.get('receipt_url')))
        db.session.commit(); flash('Expense submitted!', 'success')
        return redirect(url_for('expenses_list'))
    return render_template('erp/expenses/form.html',
        projects=projects, employees=employees,
        categories=EXPENSE_CATS, subcats=EXP_SUBCATS)

@app.route('/expenses/<int:eid>/approve', methods=['POST'])
@login_required
def expenses_approve(eid):
    e = Expense.query.get_or_404(eid)
    action = request.form.get('action','')
    if not action: return redirect(url_for('expenses_list'))
    if action == 'reject':
        e.status = 'Rejected'; e.rejection_reason = request.form.get('reason')
    elif action == 'manager_approve' and e.status == 'Pending' and current_user.can('project_manager','bim_manager','hr','director'):
        e.status = 'Manager Approved'
        e.manager_approved_by = current_user.id; e.manager_approved_at = datetime.utcnow()
    elif action == 'finance_approve' and e.status == 'Manager Approved' and current_user.can('finance','director'):
        e.status = 'Finance Approved'
        e.finance_approved_by = current_user.id; e.finance_approved_at = datetime.utcnow()
    else:
        abort(403)
    db.session.commit(); flash(f'Expense {e.status}.', 'success' if 'Approved' in e.status else 'warning')
    return redirect(url_for('expenses_list'))

# ── Timesheets ────────────────────────────────────────────────────────────────
@app.route('/timesheets')
@login_required
def timesheets_list():
    sf = request.args.get('status','')
    if current_user.can('admin','director','hr','project_manager','bim_manager'):
        qry = Timesheet.query
    else:
        qry = Timesheet.query.filter_by(employee_id=current_user.employee_id)
    if sf: qry = qry.filter_by(status=sf)
    return render_template('erp/timesheets/list.html',
        timesheets=qry.order_by(Timesheet.work_date.desc()).limit(200).all())

@app.route('/timesheets/new', methods=['GET','POST'])
@login_required
def timesheets_new():
    projects  = Project.query.order_by(Project.name).all()
    employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    if request.method == 'POST':
        f = request.form
        db.session.add(Timesheet(
            employee_id=f.get('employee_id') or current_user.employee_id,
            project_id=f.get('project_id') or None,
            work_date=_parse_date(f['work_date']),
            hours=float(f.get('hours') or 0),
            overtime_hours=float(f.get('overtime_hours') or 0),
            task_description=f.get('task_description'),
            status=f.get('status','Submitted')))
        db.session.commit(); flash('Timesheet saved!', 'success')
        return redirect(url_for('timesheets_list'))
    return render_template('erp/timesheets/form.html',
        projects=projects, employees=employees)

@app.route('/timesheets/<int:tid>/approve', methods=['POST'])
@login_required
@role_required('admin','director','project_manager','bim_manager','hr')
def timesheets_approve(tid):
    ts = Timesheet.query.get_or_404(tid)
    ts.status = 'Approved'
    ts.approved_by_id = current_user.id; ts.approved_at = datetime.utcnow()
    db.session.commit(); flash('Timesheet approved.', 'success')
    return redirect(url_for('timesheets_list'))

# ── BIM Operations ────────────────────────────────────────────────────────────
@app.route('/bim/records')
@login_required
def bim_records():
    rt = request.args.get('type','')
    qry = BIMRecord.query
    if rt: qry = qry.filter_by(record_type=rt)
    return render_template('erp/bim/records.html',
        records=qry.order_by(BIMRecord.created_at.desc()).all())

@app.route('/bim/records/new', methods=['GET','POST'])
@login_required
@role_required('admin','bim_manager','project_manager')
def bim_records_new():
    projects  = Project.query.order_by(Project.name).all()
    employees = Employee.query.filter_by(status='Active').order_by(Employee.name).all()
    if request.method == 'POST':
        f = request.form
        db.session.add(BIMRecord(
            project_id=f.get('project_id'),
            record_type=f.get('record_type'),
            record_date=_parse_date(f.get('record_date')),
            model_version=f.get('model_version'),
            lod_level=f.get('lod_level'),
            status=f.get('status','Open'),
            clash_count=int(f.get('clash_count') or 0) or None,
            description=f.get('description'),
            file_path=f.get('file_path'),
            submitted_by=f.get('submitted_by') or None))
        db.session.commit(); flash('BIM record added!', 'success')
        return redirect(url_for('bim_records'))
    return render_template('erp/bim/record_form.html',
        projects=projects, employees=employees)

# ── Reports ───────────────────────────────────────────────────────────────────
@app.route('/reports')
@login_required
@role_required('admin','director','finance','hr')
def reports_index():
    projects = Project.query.all()
    all_inv  = Invoice.query.all()
    total_contract  = sum(p.contract_value or 0 for p in projects)
    total_received  = sum(i.amount_paid for i in all_inv)
    total_expenses  = sum(e.amount for e in Expense.query.filter_by(status='Finance Approved').all())
    total_profit    = total_received - total_expenses
    profit_margin   = (total_profit / total_received * 100) if total_received else 0

    exp_by_cat_raw = db.session.query(Expense.category, func.sum(Expense.amount))\
        .filter_by(status='Finance Approved').group_by(Expense.category).all()
    expense_by_cat = [(r[0], r[1]) for r in exp_by_cat_raw]

    country_raw = db.session.query(Project.country, func.count(Project.id),
        func.sum(Project.contract_value)).group_by(Project.country).all()
    from collections import namedtuple
    CRow = namedtuple('CRow', ['country','count','total'])
    revenue_by_country = [CRow(r[0] or 'Unknown', r[1], r[2] or 0) for r in country_raw]

    emp_util = []
    ERow = namedtuple('ERow', ['emp','total_hours','approved_hours'])
    for e in Employee.query.filter_by(status='Active').all():
        total_h = db.session.query(func.sum(Timesheet.hours))\
            .filter_by(employee_id=e.id).scalar() or 0
        appr_h  = db.session.query(func.sum(Timesheet.hours))\
            .filter_by(employee_id=e.id, status='Approved').scalar() or 0
        emp_util.append(ERow(e, total_h, appr_h))
    emp_util.sort(key=lambda x: -x.total_hours)

    leave_raw = db.session.query(Leave.leave_type,
        func.sum(db.case((Leave.status=='Approved',1),else_=0)),
        func.sum(db.case((Leave.status=='Pending',1),else_=0)),
        func.sum(Leave.days_requested)).group_by(Leave.leave_type).all()
    LRow = namedtuple('LRow',['type','approved','pending','total_days'])
    leave_summary = [LRow(r[0],r[1],r[2],r[3] or 0) for r in leave_raw]

    dept_raw = db.session.query(Employee.department,
        func.sum(db.case((Employee.status=='Active',1),else_=0)),
        func.count(Employee.id)).group_by(Employee.department).all()
    DRow = namedtuple('DRow',['dept','active','total'])
    dept_headcount = [DRow(r[0] or 'Other',r[1],r[2]) for r in dept_raw]

    return render_template('erp/reports/index.html',
        projects=projects, total_contract=total_contract,
        total_received=total_received, total_expenses=total_expenses,
        total_profit=total_profit, profit_margin=profit_margin,
        expense_by_cat=expense_by_cat, revenue_by_country=revenue_by_country,
        emp_utilization=emp_util, leave_summary=leave_summary,
        dept_headcount=dept_headcount)

# ── Admin ─────────────────────────────────────────────────────────────────────
@app.route('/admin/users')
@login_required
@role_required('admin')
def admin_users():
    return render_template('erp/admin/users.html',
        users=User.query.order_by(User.name).all())

@app.route('/admin/users/new', methods=['GET','POST'])
@login_required
@role_required('admin')
def admin_users_new():
    if request.method == 'POST':
        f = request.form
        if User.query.filter_by(email=f['email'].strip().lower()).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('admin_users'))
        u = User(name=f['name'], email=f['email'].strip().lower(),
                 role=f['role'], employee_id=f.get('employee_id') or None)
        u.set_password(f['password']); db.session.add(u); db.session.commit()
        flash(f'User {u.name} created!', 'success')
        return redirect(url_for('admin_users'))
    return render_template('erp/admin/user_form.html',
        employees=Employee.query.filter_by(status='Active').order_by(Employee.name).all())

@app.route('/admin/users/<int:uid>/toggle', methods=['POST'])
@login_required
@role_required('admin')
def admin_users_toggle(uid):
    u = User.query.get_or_404(uid)
    if u.id == current_user.id: flash("Cannot deactivate yourself!", 'danger')
    else:
        u.is_active = not u.is_active; db.session.commit()
        flash(f'User {"activated" if u.is_active else "deactivated"}.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:uid>/reset', methods=['POST'])
@login_required
@role_required('admin')
def admin_users_reset(uid):
    u = User.query.get_or_404(uid)
    new_pw = f'{u.name.split()[0].title()}@123'
    u.set_password(new_pw); db.session.commit()
    flash(f'Password reset for {u.name}. New password: {new_pw}', 'info')
    return redirect(url_for('admin_users'))

@app.route('/notifications/read', methods=['POST'])
@login_required
def mark_notifications_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'ok': True})

# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(403)
def forbidden(e): return render_template('erp/errors/403.html'), 403
@app.errorhandler(404)
def not_found(e):  return render_template('erp/errors/404.html'), 404

# ── Startup: create tables + auto-seed if empty ───────────────────────────────
with app.app_context():
    db.create_all()
    try:
        from erp_seed import seed as _auto_seed
        _auto_seed()
    except Exception as _e:
        print(f'Seed skipped: {_e}')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f'BIM Bytes Solutions ERP  ->  http://localhost:{port}')
    app.run(debug=debug, port=port, host='0.0.0.0')
