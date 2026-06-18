"""Seed demo data for BIM Bytes Solutions ERP. Run once: python erp_seed.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from erp_app import app, db
from erp_app import (User, Employee, Client, Lead, Project, ProjectTeam,
                     Milestone, Invoice, Payment, Expense, Timesheet, Leave,
                     BIMRecord, Notification)
from datetime import date, timedelta, datetime

def seed():
    """Seed demo data. Safe to call from within an existing app context or standalone."""
    if User.query.count() > 0:
        return  # already seeded

        # ── Employees ──────────────────────────────────────────────────────────
        emps = [
            Employee(employee_id='EMP-001', name='Sathish Srinivasan', email='sathish@bimbytes.com',
                     phone='+91 98765 00001', department='Project Management',
                     job_title='Managing Director', date_of_joining=date(2020,1,1),
                     date_of_birth=date(1985,4,15), gender='Male', country='India',
                     salary=250000, hourly_rate=1500, leave_balance=24,
                     skills='Revit,Navisworks,BIM 360,AutoCAD,Project Management'),
            Employee(employee_id='EMP-002', name='Rajesh Kumar', email='rajesh@bimbytes.com',
                     phone='+91 98765 00002', department='Project Management',
                     job_title='Director – Operations', date_of_joining=date(2020,3,1),
                     date_of_birth=date(1980,7,20), gender='Male', country='India',
                     salary=200000, hourly_rate=1200, leave_balance=21,
                     skills='Strategic Planning,Client Management,BIM Standards'),
            Employee(employee_id='EMP-003', name='Anita Roy', email='anita@bimbytes.com',
                     phone='+91 98765 00003', department='Finance',
                     job_title='Finance Manager', date_of_joining=date(2021,1,15),
                     date_of_birth=date(1988,3,10), gender='Female', country='India',
                     salary=120000, hourly_rate=750, leave_balance=18,
                     skills='Tally,Financial Analysis,GST,Project Costing'),
            Employee(employee_id='EMP-004', name='Vijay Patel', email='vijay@bimbytes.com',
                     phone='+91 98765 00004', department='HR & Administration',
                     job_title='HR Manager', date_of_joining=date(2021,4,1),
                     date_of_birth=date(1990,8,5), gender='Male', country='India',
                     salary=90000, hourly_rate=550, leave_balance=18,
                     skills='Recruitment,Payroll,Performance Management,HRIS'),
            Employee(employee_id='EMP-005', name='Rahul Gupta', email='rahul@bimbytes.com',
                     phone='+91 98765 00005', department='BIM Production',
                     job_title='BIM Manager', date_of_joining=date(2020,6,1),
                     date_of_birth=date(1987,12,22), gender='Male', country='India',
                     salary=150000, hourly_rate=900, leave_balance=18,
                     skills='Revit,Navisworks,BIM 360,Dynamo,ISO 19650,LOD Standards'),
            Employee(employee_id='EMP-006', name='Priya Mehta', email='priya@bimbytes.com',
                     phone='+91 98765 00006', department='Project Management',
                     job_title='Senior Project Manager', date_of_joining=date(2021,2,1),
                     date_of_birth=date(1989,5,18), gender='Female', country='India',
                     salary=130000, hourly_rate=800, leave_balance=18,
                     skills='MS Project,AutoCAD,Revit,Client Communication'),
            Employee(employee_id='EMP-007', name='Arjun Sharma', email='arjun@bimbytes.com',
                     phone='+91 98765 00007', department='BIM Coordination',
                     job_title='Senior BIM Coordinator', date_of_joining=date(2021,7,1),
                     date_of_birth=date(1993,2,14), gender='Male', country='India',
                     salary=85000, hourly_rate=500, leave_balance=18,
                     skills='Revit,Navisworks,AutoCAD,Clash Detection,BIM 360'),
            Employee(employee_id='EMP-008', name='Sneha Iyer', email='sneha@bimbytes.com',
                     phone='+91 98765 00008', department='BIM Coordination',
                     job_title='BIM Coordinator', date_of_joining=date(2022,1,15),
                     date_of_birth=date(1995,9,30), gender='Female', country='India',
                     salary=65000, hourly_rate=400, leave_balance=18,
                     skills='Revit,Navisworks,AutoCAD,Enscape'),
            Employee(employee_id='EMP-009', name='Kiran Reddy', email='kiran@bimbytes.com',
                     phone='+91 98765 00009', department='BIM Production',
                     job_title='Senior BIM Modeler', date_of_joining=date(2021,9,1),
                     date_of_birth=date(1994,6,11), gender='Male', country='India',
                     salary=70000, hourly_rate=430, leave_balance=18,
                     skills='Revit,AutoCAD,Lumion,SketchUp'),
            Employee(employee_id='EMP-010', name='Pooja Nair', email='pooja@bimbytes.com',
                     phone='+91 98765 00010', department='BIM Production',
                     job_title='BIM Modeler', date_of_joining=date(2022,5,1),
                     date_of_birth=date(1997,11,3), gender='Female', country='India',
                     salary=55000, hourly_rate=340, leave_balance=18,
                     skills='Revit,AutoCAD,3ds Max'),
            Employee(employee_id='EMP-011', name='Amit Singh', email='amit@bimbytes.com',
                     phone='+91 98765 00011', department='BIM Coordination',
                     job_title='QA Lead', date_of_joining=date(2021,11,1),
                     date_of_birth=date(1992,4,25), gender='Male', country='India',
                     salary=80000, hourly_rate=490, leave_balance=18,
                     skills='Quality Control,Navisworks,ISO 19650,BIM Audit'),
            Employee(employee_id='EMP-012', name='Divya Patel', email='divya@bimbytes.com',
                     phone='+91 98765 00012', department='Finance',
                     job_title='Finance Executive', date_of_joining=date(2022,3,1),
                     date_of_birth=date(1996,1,17), gender='Female', country='India',
                     salary=45000, hourly_rate=280, leave_balance=18,
                     skills='Tally,MS Excel,GST Filing,Invoicing'),
            Employee(employee_id='EMP-013', name='Suresh Rao', email='suresh@bimbytes.com',
                     phone='+91 98765 00013', department='BIM Production',
                     job_title='BIM Modeler', date_of_joining=date(2022,8,15),
                     date_of_birth=date(1998,7,8), gender='Male', country='India',
                     salary=50000, hourly_rate=310, leave_balance=18,
                     skills='Revit,AutoCAD,BIM 360'),
            Employee(employee_id='EMP-014', name='Meena Krishnan', email='meena@bimbytes.com',
                     phone='+91 98765 00014', department='Business Development',
                     job_title='Business Analyst', date_of_joining=date(2022,6,1),
                     date_of_birth=date(1993,10,20), gender='Female', country='India',
                     salary=75000, hourly_rate=460, leave_balance=18,
                     skills='Market Research,CRM,Proposal Writing,Client Relations'),
            Employee(employee_id='EMP-015', name='Ravi Shankar', email='ravi@bimbytes.com',
                     phone='+91 98765 00015', department='BIM Production',
                     job_title='MEP BIM Coordinator', date_of_joining=date(2023,1,2),
                     date_of_birth=date(1996,3,12), gender='Male', country='India',
                     salary=68000, hourly_rate=420, leave_balance=18,
                     skills='Revit MEP,AutoCAD MEP,Navisworks,HVAC BIM'),
        ]
        db.session.add_all(emps); db.session.flush()
        # reporting managers
        for i in range(2, len(emps)): emps[i].manager_id = emps[0].id
        for i in [6,7,8,9,12,14]: emps[i].manager_id = emps[4].id
        emps[10].manager_id = emps[5].id
        emps[11].manager_id = emps[2].id
        emps[13].manager_id = emps[1].id
        db.session.flush()

        # ── Users ──────────────────────────────────────────────────────────────
        users_data = [
            ('Sathish Srinivasan', 'admin@bimbytes.com',    'Admin@123',    'admin',           emps[0].id),
            ('Rajesh Kumar',       'director@bimbytes.com', 'Director@123', 'director',        emps[1].id),
            ('Anita Roy',          'finance@bimbytes.com',  'Finance@123',  'finance',         emps[2].id),
            ('Vijay Patel',        'hr@bimbytes.com',       'Hr@123',       'hr',              emps[3].id),
            ('Rahul Gupta',        'bim@bimbytes.com',      'Bim@123',      'bim_manager',     emps[4].id),
            ('Priya Mehta',        'pm@bimbytes.com',       'Pm@123',       'project_manager', emps[5].id),
            ('Arjun Sharma',       'emp@bimbytes.com',      'Emp@123',      'employee',        emps[6].id),
        ]
        users = []
        for name, email, pw, role, eid in users_data:
            u = User(name=name, email=email, role=role, employee_id=eid)
            u.set_password(pw); db.session.add(u); users.append(u)
        db.session.flush()

        # ── Clients ────────────────────────────────────────────────────────────
        clients_data = [
            ('CLI-001','ABC Construction LLC','India','Mumbai','construction@abc.com','+91 22 4567 8901','Construction','Ramesh Malhotra'),
            ('CLI-002','Urban Transit Authority','India','Delhi','projects@urbantransit.gov.in','+91 11 2345 6789','Infrastructure','Sunil Verma'),
            ('CLI-003','Prestige Retail Developers','India','Bengaluru','bim@prestige.in','+91 80 4567 8901','Real Estate','Kavita Sharma'),
            ('CLI-004','HealthTrust International','Singapore','Singapore','projects@healthtrust.sg','+65 6234 5678','Healthcare','David Tan'),
            ('CLI-005','Al-Futtaim Properties','UAE','Dubai','bim@alfuttaim.ae','+971 4 234 5678','Real Estate','Ahmed Al-Rashid'),
            ('CLI-006','Airport Authority of India','India','Delhi','bim@aai.aero','+91 11 2342 3456','Infrastructure','R.K. Sharma'),
            ('CLI-007','Lodha Developers','India','Mumbai','tech@lodha.com','+91 22 6789 0123','Real Estate','Nikhil Lodha'),
        ]
        clients = []
        for code,name,country,city,email,phone,industry,contact in clients_data:
            c = Client(client_code=code,name=name,country=country,city=city,
                       email=email,phone=phone,industry=industry,contact_person=contact)
            db.session.add(c); clients.append(c)
        db.session.flush()

        # ── Projects ──────────────────────────────────────────────────────────
        projects_data = [
            ('PRJ-001','High-Rise Office Tower BIM','BIM Coordination',clients[0].id,'India','Mumbai',
             5000000,date(2024,10,1),date(2025,9,30),'Ongoing',emps[5].id,emps[4].id,
             'Revit,Navisworks,BIM 360','LOD 300','ISO 19650',
             'Complete BIM coordination for 32-floor commercial tower including Arch, Structural and MEP.'),
            ('PRJ-002','Metro Station BIM Coordination','BIM Coordination',clients[1].id,'India','Delhi',
             8000000,date(2024,8,1),date(2025,12,31),'Ongoing',emps[5].id,emps[4].id,
             'Revit,Navisworks,4D Simulation','LOD 350','IS 15883',
             'BIM coordination across 5 metro stations. Clash detection and 4D simulation.'),
            ('PRJ-003','Phoenix Mall BIM','BIM Modeling',clients[2].id,'India','Bengaluru',
             3500000,date(2024,4,1),date(2024,12,31),'Completed',emps[5].id,emps[4].id,
             'Revit,AutoCAD','LOD 400','ISO 19650',
             'Architectural BIM for 4-level shopping mall. LOD 400 deliverable.'),
            ('PRJ-004','HealthTrust Hospital BIM','MEP BIM',clients[3].id,'Singapore','Singapore',
             6500000,date(2025,1,15),date(2025,10,31),'On Hold',emps[5].id,emps[4].id,
             'Revit MEP,AutoCAD MEP','LOD 300','Singapore BIM Guide',
             'MEP BIM for 250-bed hospital. Project on hold pending client approvals.'),
            ('PRJ-005','Residential Complex BIM','Structural BIM',clients[0].id,'India','Pune',
             2000000,date(2024,6,1),date(2024,11,30),'Completed',emps[1].id,emps[4].id,
             'Revit Structure,AutoCAD','LOD 350','IS 875',
             'Structural BIM for 3 residential towers, 18 floors each.'),
            ('PRJ-006','T3 Airport Terminal Expansion','BIM Coordination',clients[5].id,'India','Delhi',
             12000000,date(2025,2,1),date(2026,3,31),'Ongoing',emps[5].id,emps[4].id,
             'Revit,Navisworks,Civil 3D,BIM 360','LOD 400','ISO 19650',
             'BIM coordination for Terminal 3 expansion. Multi-discipline federated model.'),
            ('PRJ-007','Al-Futtaim Mixed-Use Tower','BIM Modeling',clients[4].id,'UAE','Dubai',
             9500000,date(2025,4,1),date(2026,6,30),'Awarded',emps[1].id,emps[4].id,
             'Revit,Navisworks,Enscape','LOD 400','UAE BIM Standard',
             '45-floor mixed-use tower. Architectural, Structural, MEP BIM and coordination.'),
        ]
        projects = []
        for pid,name,ptype,cid,country,city,cv,sd,ed,status,mgr,bim,sw,lod,std,desc in projects_data:
            p = Project(project_id=pid,name=name,project_type=ptype,client_id=cid,
                        country=country,city=city,contract_value=cv,start_date=sd,end_date=ed,
                        status=status,project_manager_id=mgr,bim_manager_id=bim,
                        software=sw,lod_level=lod,bim_standard=std,description=desc)
            db.session.add(p); projects.append(p)
        db.session.flush()

        # ── Milestones ────────────────────────────────────────────────────────
        ms_data = [
            (projects[0].id,'Concept Design BIM (LOD 100)',date(2024,12,15),1000000,'Completed'),
            (projects[0].id,'Design Development BIM (LOD 200)',date(2025,3,31),1200000,'Completed'),
            (projects[0].id,'Construction Documents BIM (LOD 300)',date(2025,6,30),1500000,'In Progress'),
            (projects[0].id,'Final As-Built BIM (LOD 400)',date(2025,9,30),1300000,'Pending'),
            (projects[1].id,'Station 1 & 2 BIM Models',date(2025,2,28),2000000,'Completed'),
            (projects[1].id,'Clash Detection Report – Batch 1',date(2025,4,30),1000000,'Completed'),
            (projects[1].id,'Station 3,4,5 BIM Models',date(2025,8,31),3000000,'In Progress'),
            (projects[1].id,'4D Simulation Delivery',date(2025,12,31),2000000,'Pending'),
            (projects[5].id,'Existing Terminal Survey Model',date(2025,4,30),2500000,'Completed'),
            (projects[5].id,'New Terminal BIM – Arch & Structural',date(2025,9,30),5000000,'In Progress'),
            (projects[5].id,'MEP BIM Integration',date(2025,12,31),4500000,'Pending'),
        ]
        for pid,name,dd,amt,status in ms_data:
            m = Milestone(project_id=pid,name=name,due_date=dd,amount=amt,status=status)
            if status=='Completed': m.completed_date = dd - timedelta(days=5)
            db.session.add(m)

        # ── Team Members ──────────────────────────────────────────────────────
        team_data = [
            (projects[0].id, emps[6].id,  'Senior BIM Coordinator'),
            (projects[0].id, emps[7].id,  'BIM Coordinator'),
            (projects[0].id, emps[8].id,  'BIM Modeler'),
            (projects[0].id, emps[10].id, 'QA Engineer'),
            (projects[1].id, emps[6].id,  'BIM Lead'),
            (projects[1].id, emps[8].id,  'BIM Modeler'),
            (projects[1].id, emps[9].id,  'BIM Modeler'),
            (projects[1].id, emps[14].id, 'MEP BIM Coordinator'),
            (projects[1].id, emps[10].id, 'QA Engineer'),
            (projects[2].id, emps[7].id,  'BIM Coordinator'),
            (projects[2].id, emps[12].id, 'BIM Modeler'),
            (projects[5].id, emps[6].id,  'Senior BIM Coordinator'),
            (projects[5].id, emps[8].id,  'BIM Modeler'),
            (projects[5].id, emps[14].id, 'MEP BIM Coordinator'),
            (projects[5].id, emps[9].id,  'BIM Modeler'),
            (projects[6].id, emps[7].id,  'BIM Coordinator'),
            (projects[6].id, emps[14].id, 'MEP BIM Coordinator'),
        ]
        for pid,eid,role in team_data:
            db.session.add(ProjectTeam(project_id=pid,employee_id=eid,role_in_project=role))

        # ── Invoices & Payments ───────────────────────────────────────────────
        invoices_data = [
            ('INV-0001',projects[0].id,clients[0].id,date(2024,11,1),date(2024,11,30),1000000,180000,0,'Paid','Net 30'),
            ('INV-0002',projects[0].id,clients[0].id,date(2025,2,1), date(2025,2,28), 1200000,216000,0,'Paid','Net 30'),
            ('INV-0003',projects[0].id,clients[0].id,date(2025,5,1), date(2025,5,31), 1000000,180000,0,'Pending','Net 30'),
            ('INV-0004',projects[1].id,clients[1].id,date(2024,10,1),date(2024,10,31),2000000,0,0,'Paid','Milestone-based'),
            ('INV-0005',projects[1].id,clients[1].id,date(2025,1,15),date(2025,2,14), 2000000,0,0,'Paid','Milestone-based'),
            ('INV-0006',projects[1].id,clients[1].id,date(2025,4,1), date(2025,4,30), 2000000,0,0,'Partially Paid','Milestone-based'),
            ('INV-0007',projects[2].id,clients[2].id,date(2024,6,1), date(2024,6,30), 1500000,270000,0,'Paid','Net 30'),
            ('INV-0008',projects[2].id,clients[2].id,date(2024,9,15),date(2024,10,15),1200000,216000,0,'Paid','Net 30'),
            ('INV-0009',projects[4].id,clients[0].id,date(2024,7,1), date(2024,7,31), 1000000,180000,0,'Paid','Net 30'),
            ('INV-0010',projects[4].id,clients[0].id,date(2024,10,1),date(2024,10,31),800000,144000,0,'Paid','Net 30'),
            ('INV-0011',projects[5].id,clients[5].id,date(2025,3,1), date(2025,3,31), 3000000,540000,0,'Paid','Milestone-based'),
            ('INV-0012',projects[5].id,clients[5].id,date(2025,6,1), date(2025,6,30), 3000000,540000,0,'Pending','Milestone-based'),
            ('INV-0013',projects[6].id,clients[4].id,date(2025,5,1), date(2025,5,31), 2500000,0,0,'Paid','Net 45'),
        ]
        invoices = []
        for num,pid,cid,inv_date,due_date,sub,tax,disc,status,terms in invoices_data:
            inv = Invoice(invoice_number=num,project_id=pid,client_id=cid,
                          invoice_date=inv_date,due_date=due_date,
                          subtotal=sub,tax_amount=tax,discount=disc,
                          total_amount=sub+tax-disc,status=status,payment_terms=terms)
            db.session.add(inv); invoices.append(inv)
        db.session.flush()

        payments_data = [
            (invoices[0].id,  date(2024,11,25), 1180000, 'Bank Transfer', 'NEFT/2024/001'),
            (invoices[1].id,  date(2025,2,20),  1416000, 'Bank Transfer', 'NEFT/2025/023'),
            (invoices[3].id,  date(2024,10,28), 2000000, 'Bank Transfer', 'RTGS/2024/045'),
            (invoices[4].id,  date(2025,2,10),  2000000, 'Bank Transfer', 'RTGS/2025/012'),
            (invoices[5].id,  date(2025,4,28),  1000000, 'Bank Transfer', 'RTGS/2025/056'),
            (invoices[6].id,  date(2024,6,28),  1770000, 'Bank Transfer', 'NEFT/2024/067'),
            (invoices[7].id,  date(2024,10,20), 1416000, 'Bank Transfer', 'NEFT/2024/089'),
            (invoices[8].id,  date(2024,7,28),  1180000, 'Bank Transfer', 'NEFT/2024/078'),
            (invoices[9].id,  date(2024,10,28),  944000, 'Bank Transfer', 'NEFT/2024/092'),
            (invoices[10].id, date(2025,3,28),  3540000, 'Bank Transfer', 'RTGS/2025/034'),
            (invoices[12].id, date(2025,5,28),  2500000, 'Wire Transfer', 'WIRE/2025/011'),
        ]
        for iid,pd,amt,method,ref in payments_data:
            db.session.add(Payment(invoice_id=iid,payment_date=pd,amount=amt,
                                   payment_method=method,reference=ref))

        # ── Expenses ──────────────────────────────────────────────────────────
        expenses_data = [
            ('EXP-001',projects[0].id,emps[4].id, date(2024,11,5), 'BIM Software','Revit License',     180000,'Revit 2025 annual license (5 seats)','Finance Approved'),
            ('EXP-002',projects[0].id,emps[4].id, date(2024,11,5), 'BIM Software','Autodesk Construction Cloud',95000,'ACC subscription annual','Finance Approved'),
            ('EXP-003',None,          emps[0].id, date(2024,11,1), 'Office',       'Rent',              80000,'Office rent – Nov 2024','Finance Approved'),
            ('EXP-004',None,          emps[0].id, date(2024,11,5), 'Office',       'Electricity',        8500,'Nov 2024 electricity bill','Finance Approved'),
            ('EXP-005',None,          emps[0].id, date(2024,11,5), 'Office',       'Internet',           3500,'Nov 2024 internet bill','Finance Approved'),
            ('EXP-006',projects[0].id,emps[6].id, date(2024,12,10),'Project',      'Site Visit',        15000,'Site visit – Office Tower Mumbai','Finance Approved'),
            ('EXP-007',None,          emps[0].id, date(2024,12,1), 'Office',       'Rent',              80000,'Office rent – Dec 2024','Finance Approved'),
            ('EXP-008',projects[1].id,emps[6].id, date(2025,1,8), 'Project',      'Site Visit',        22000,'Delhi metro site coordination visit','Finance Approved'),
            ('EXP-009',None,          emps[0].id, date(2025,1,1), 'Office',       'Rent',              80000,'Office rent – Jan 2025','Finance Approved'),
            ('EXP-010',projects[1].id,emps[4].id, date(2025,1,15),'BIM Software', 'Navisworks',        45000,'Navisworks Manage 2025 license','Finance Approved'),
            ('EXP-011',projects[0].id,emps[7].id, date(2025,2,14),'Training',     'Workshop',          12000,'Revit Advanced workshop','Finance Approved'),
            ('EXP-012',None,          emps[0].id, date(2025,2,1), 'Office',       'Rent',              80000,'Office rent – Feb 2025','Finance Approved'),
            ('EXP-013',projects[5].id,emps[4].id, date(2025,3,10),'BIM Software', 'Enscape',           55000,'Enscape license – airport project','Finance Approved'),
            ('EXP-014',projects[5].id,emps[6].id, date(2025,3,15),'Project',      'Site Visit',        35000,'Airport T3 expansion site visit','Finance Approved'),
            ('EXP-015',None,          emps[0].id, date(2025,3,1), 'Office',       'Rent',              80000,'Office rent – Mar 2025','Finance Approved'),
            ('EXP-016',projects[6].id,emps[4].id, date(2025,5,5), 'Travel',       'Flight',            42000,'Dubai trip – client meeting Al-Futtaim','Manager Approved'),
            ('EXP-017',projects[6].id,emps[4].id, date(2025,5,6), 'Travel',       'Hotel',             28000,'Hotel – Dubai 4 nights','Manager Approved'),
            ('EXP-018',projects[0].id,emps[8].id, date(2025,5,20),'Project',      'Printing & Plotting',8500,'Drawing prints for client review','Pending'),
            ('EXP-019',None,          emps[3].id, date(2025,6,5), 'Training',     'Certification',     18000,'HR certification course','Pending'),
            ('EXP-020',projects[5].id,emps[14].id,date(2025,6,10),'BIM Software', 'Civil 3D',          38000,'Civil 3D license for airport project','Pending'),
        ]
        for eid,pid,emp,exp_date,cat,subcat,amt,desc,status in expenses_data:
            db.session.add(Expense(expense_id=eid,project_id=pid,employee_id=emp,
                expense_date=exp_date,category=cat,sub_category=subcat,
                amount=amt,description=desc,status=status))

        # ── Timesheets ────────────────────────────────────────────────────────
        ts_data = [
            (emps[6].id, projects[0].id, date(2025,6,2),  8, 0, 'Revit modeling – Core & Shell','Approved'),
            (emps[6].id, projects[0].id, date(2025,6,3),  8, 0, 'Revit modeling – Floors 1-10','Approved'),
            (emps[6].id, projects[1].id, date(2025,6,4),  8, 0, 'Metro Station 3 coordination','Approved'),
            (emps[7].id, projects[0].id, date(2025,6,2),  8, 0, 'BIM coordination – MEP clash check','Approved'),
            (emps[7].id, projects[0].id, date(2025,6,3),  8, 2, 'Clash detection report preparation','Approved'),
            (emps[8].id, projects[0].id, date(2025,6,2),  8, 0, 'Structural BIM – Basement levels','Approved'),
            (emps[8].id, projects[1].id, date(2025,6,3),  8, 0, 'Metro station Arch modeling','Approved'),
            (emps[9].id, projects[1].id, date(2025,6,2),  8, 0, 'MEP BIM – HVAC routing','Submitted'),
            (emps[9].id, projects[1].id, date(2025,6,3),  8, 0, 'MEP BIM – Plumbing layout','Submitted'),
            (emps[14].id,projects[1].id, date(2025,6,2),  8, 0, 'MEP clash detection – Station 3','Approved'),
            (emps[14].id,projects[5].id, date(2025,6,3),  8, 0, 'Airport terminal MEP coordination','Approved'),
            (emps[10].id,projects[0].id, date(2025,6,2),  8, 0, 'QA review – LOD 300 check','Approved'),
            (emps[10].id,projects[1].id, date(2025,6,4),  8, 0, 'QA review – clash report audit','Submitted'),
            (emps[12].id,projects[2].id, date(2025,6,2),  8, 0, 'Mall BIM – as-built documentation','Approved'),
            (emps[4].id, projects[0].id, date(2025,6,2),  4, 0, 'BIM execution plan review','Approved'),
            (emps[4].id, projects[5].id, date(2025,6,3),  6, 0, 'Airport BIM – coordination meeting','Approved'),
            (emps[6].id, projects[5].id, date(2025,6,5),  8, 0, 'T3 terminal – concourse modeling','Draft'),
            (emps[7].id, projects[6].id, date(2025,6,4),  8, 0, 'Dubai tower – Arch BIM setup','Submitted'),
            (emps[14].id,projects[6].id, date(2025,6,4),  8, 0, 'Dubai tower – MEP scope review','Submitted'),
        ]
        for emp,pid,wd,hrs,ot,desc,status in ts_data:
            db.session.add(Timesheet(employee_id=emp,project_id=pid,work_date=wd,
                hours=hrs,overtime_hours=ot,task_description=desc,status=status))

        # ── Leaves ────────────────────────────────────────────────────────────
        leaves_data = [
            (emps[7].id,  'Sick Leave',    date(2025,4,10),date(2025,4,11),2,'Fever and cold','Approved'),
            (emps[8].id,  'Annual Leave',  date(2025,5,19),date(2025,5,23),5,'Family vacation','Approved'),
            (emps[9].id,  'Casual Leave',  date(2025,6,9), date(2025,6,9), 1,'Personal work','Pending'),
            (emps[10].id, 'Compensatory Leave',date(2025,6,13),date(2025,6,13),1,'Worked on Sunday','Pending'),
            (emps[12].id, 'Sick Leave',    date(2025,3,14),date(2025,3,15),2,'Flu','Approved'),
            (emps[14].id, 'Annual Leave',  date(2025,5,26),date(2025,5,30),5,'Personal trip','Approved'),
        ]
        for emp,ltype,sd,ed,days,reason,status in leaves_data:
            db.session.add(Leave(employee_id=emp,leave_type=ltype,start_date=sd,end_date=ed,
                days_requested=days,reason=reason,status=status))

        # ── Leads ─────────────────────────────────────────────────────────────
        leads_data = [
            ('LEAD-001',clients[6].id,None,'Palava City Phase 2 – BIM',25000000,70,'INR','Proposal Submitted',emps[13].id,date(2025,7,31),'Mega township BIM project. Awaiting proposal evaluation.'),
            ('LEAD-002',clients[4].id,None,'Mall of Emirates Expansion',18000000,60,'AED','Negotiation',       emps[13].id,date(2025,8,15),'BIM coordination for mall expansion. In final negotiation.'),
            ('LEAD-003',clients[1].id,None,'Rapid Metro Extension',     35000000,40,'INR','Qualified',         emps[5].id, date(2025,9,30),'Extension of metro network. Client qualified, scope being finalized.'),
            ('LEAD-004',None,'Hyderabad IT Park Developer','Hyderabad IT Park BIM',8000000,20,'INR','New Lead', emps[13].id,date(2025,10,31),'New inquiry from IT park developer.'),
            ('LEAD-005',clients[5].id,None,'New Greenfield Airport BIM',50000000,55,'INR','Proposal Submitted',emps[5].id, date(2025,12,31),'Full BIM services for new greenfield airport.'),
            ('LEAD-006',None,'Smart City Development Corp','Smart City Infrastructure',15000000,25,'INR','New Lead',emps[13].id,date(2026,1,31),'Smart city BIM and digital twin development.'),
        ]
        for lid,cid,cname,title,val,prob,curr,stage,assigned,ecd,desc in leads_data:
            db.session.add(Lead(lead_id=lid,client_id=cid,client_name=cname,title=title,
                estimated_value=val,probability=prob,currency=curr,stage=stage,
                assigned_to_id=assigned,expected_close_date=ecd,description=desc))

        # ── BIM Records ───────────────────────────────────────────────────────
        bim_data = [
            (projects[0].id,'Model Submission',date(2025,3,28),'V2.0','LOD 300','Approved',  None,'High-Rise Tower – LOD 300 Arch + Structural models submitted for client review.',emps[6].id),
            (projects[0].id,'Clash Detection Report',date(2025,4,15),'V2.1',None,'Approved',  47,'47 clashes detected, 45 resolved. 2 architectural vs structural pending client decision.',emps[6].id),
            (projects[1].id,'Model Submission',date(2025,2,25),'V1.5','LOD 350','Approved',  None,'Metro Station 1 & 2 federated BIM models approved by client engineer.',emps[7].id),
            (projects[1].id,'Clash Detection Report',date(2025,3,10),'V1.5',None,'Approved',  89,'89 clashes found across Arch/Structural/MEP. 82 resolved, 7 under review.',emps[7].id),
            (projects[5].id,'Model Submission',date(2025,4,28),'V1.0','LOD 200','Approved',  None,'T3 existing terminal survey model completed. As-built scan data integrated.',emps[6].id),
            (projects[5].id,'Model Submission',date(2025,6,10),'V1.2','LOD 300','In Review',  None,'New T3 terminal Architectural BIM submitted. Awaiting structural team review.',emps[8].id),
            (projects[6].id,'Model Submission',date(2025,5,15),'V1.0',None,'Approved',        None,'BIM Execution Plan for Dubai mixed-use tower. Approved by Al-Futtaim BIM lead.',emps[7].id),
        ]
        for pid,rtype,rdate,ver,lod,status,clash,desc,subby in bim_data:
            db.session.add(BIMRecord(project_id=pid,record_type=rtype,record_date=rdate,
                model_version=ver,lod_level=lod,status=status,clash_count=clash,
                description=desc,submitted_by=subby))

        # ── Notifications ──────────────────────────────────────────────────────
        for u in users:
            db.session.add(Notification(user_id=u.id,
                title='Welcome to BIM Bytes ERP!',
                message=f'Hello {u.name}, your account is ready. Explore the modules from the sidebar.',
                ntype='success', link='/'))
        db.session.add(Notification(user_id=users[0].id,
            title='3 Expenses Pending Approval',
            message='New expense requests are awaiting manager review.',
            ntype='warning', link='/expenses'))
        db.session.add(Notification(user_id=users[2].id,
            title='Invoice INV-0003 Due Soon',
            message='Invoice INV-0003 for ₹11.8L is due on 31 May 2025.',
            ntype='danger', link='/finance/invoices'))
        db.session.add(Notification(user_id=users[4].id,
            title='BIM Record Under Review',
            message='T3 Airport BIM submission is awaiting your technical review.',
            ntype='info', link='/bim/records'))

        db.session.commit()
        print("BIM Bytes ERP seeded successfully!")
        print("  15 employees, 7 users, 7 clients, 7 projects")
        print("  13 invoices, 20 expenses, 19 timesheets, 6 leaves")
        print("  6 leads, 7 BIM records, 11 milestones")
        print("\nDemo login credentials:")
        for name,email,pw,role,_ in users_data:
            print(f"  {email:<32} / {pw:<14} => {role}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed()
