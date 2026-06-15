"""
generate_samples.py
Creates sample PDF documents: project contracts, invoices, expense reports, employee directory.
Run once:  python generate_samples.py
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER
from pathlib import Path

OUTPUT_DIR = Path("pdfs")
OUTPUT_DIR.mkdir(exist_ok=True)

TITLE_STYLE  = ParagraphStyle('T',  fontSize=16, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4,  textColor=colors.HexColor('#1a365d'))
SUB_STYLE    = ParagraphStyle('S',  fontSize=11, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=10, textColor=colors.HexColor('#2d3748'))
HEADER_STYLE = ParagraphStyle('H',  fontSize=9,  fontName='Helvetica-Bold', spaceAfter=4,        textColor=colors.HexColor('#2d3748'))


def _doc(filename):
    return SimpleDocTemplate(str(OUTPUT_DIR / filename), pagesize=A4,
                             rightMargin=20*mm, leftMargin=20*mm,
                             topMargin=18*mm,  bottomMargin=18*mm)


def _kv(data):
    t = Table(data, colWidths=(80*mm, 90*mm))
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), colors.HexColor('#edf2f7')),
        ('FONTNAME',      (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',      (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS',(0,0), (-1,-1), [colors.HexColor('#f7fafc'), colors.white]),
        ('PADDING',       (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


# ── PROJECTS ─────────────────────────────────────────────────────────────────

PROJECTS = [
    dict(id='PRJ-001', name='E-Commerce Platform',     client='ABC Corporation',  value=500000,  start='01-Jan-2025', end='30-Jun-2025', status='Active',    mgr='Sathish Srinivasan'),
    dict(id='PRJ-002', name='Mobile Banking App',      client='XYZ Bank',         value=750000,  start='15-Jan-2025', end='31-Dec-2025', status='Active',    mgr='Sathish Srinivasan'),
    dict(id='PRJ-003', name='HR Management System',    client='DEF Limited',      value=300000,  start='01-Nov-2024', end='31-Dec-2024', status='Completed', mgr='Sathish Srinivasan'),
    dict(id='PRJ-004', name='Supply Chain Solution',   client='GHI Industries',   value=450000,  start='01-Mar-2025', end='31-Aug-2025', status='On Hold',   mgr='Sathish Srinivasan'),
    dict(id='PRJ-005', name='CRM Implementation',      client='JKL Corporation',  value=250000,  start='01-Jan-2025', end='28-Feb-2025', status='Completed', mgr='Sathish Srinivasan'),
]

def create_project(p):
    doc = _doc(f"Project_Contract_{p['id']}.pdf")
    story = [
        Paragraph('TECHSOLUTIONS PVT LTD', TITLE_STYLE),
        Paragraph('PROJECT CONTRACT DOCUMENT', SUB_STYLE),
        HRFlowable(width='100%', thickness=2, color=colors.HexColor('#3182ce')),
        Spacer(1, 6*mm),
        _kv([
            ['Document Type',        'Project Contract'],
            ['Project ID',           p['id']],
            ['Project Name',         p['name']],
            ['Client Name',          p['client']],
            ['Contract Value (INR)', f"Rs. {p['value']:,}"],
            ['Start Date',           p['start']],
            ['End Date',             p['end']],
            ['Project Status',       p['status']],
            ['Project Manager',      p['mgr']],
        ]),
    ]
    doc.build(story)
    print(f'  Project_Contract_{p["id"]}.pdf')


# ── INVOICES ─────────────────────────────────────────────────────────────────

INVOICES = [
    dict(id='INV-001', pid='PRJ-001', proj='E-Commerce Platform',   client='ABC Corporation', date='15-Jan-2025', amount=100000, status='Paid',        pdate='20-Jan-2025', desc='Milestone 1 – Requirements & Design'),
    dict(id='INV-002', pid='PRJ-001', proj='E-Commerce Platform',   client='ABC Corporation', date='15-Feb-2025', amount=150000, status='Paid',        pdate='22-Feb-2025', desc='Milestone 2 – Backend Development'),
    dict(id='INV-003', pid='PRJ-002', proj='Mobile Banking App',    client='XYZ Bank',        date='20-Jan-2025', amount=200000, status='Paid',        pdate='28-Jan-2025', desc='Milestone 1 – Architecture & UI Design'),
    dict(id='INV-004', pid='PRJ-002', proj='Mobile Banking App',    client='XYZ Bank',        date='20-Mar-2025', amount=250000, status='Outstanding', pdate='',            desc='Milestone 2 – Core Banking Integration'),
    dict(id='INV-005', pid='PRJ-003', proj='HR Management System',  client='DEF Limited',     date='30-Nov-2024', amount=150000, status='Paid',        pdate='05-Dec-2024', desc='Phase 1 – Payroll & Attendance'),
    dict(id='INV-006', pid='PRJ-003', proj='HR Management System',  client='DEF Limited',     date='31-Dec-2024', amount=150000, status='Paid',        pdate='05-Jan-2025', desc='Phase 2 – Leave & Performance'),
    dict(id='INV-007', pid='PRJ-004', proj='Supply Chain Solution', client='GHI Industries',  date='15-Mar-2025', amount=100000, status='Paid',        pdate='20-Mar-2025', desc='Initial Advance – Project Kickoff'),
    dict(id='INV-008', pid='PRJ-005', proj='CRM Implementation',    client='JKL Corporation', date='20-Jan-2025', amount=150000, status='Paid',        pdate='25-Jan-2025', desc='Phase 1 – Setup & Configuration'),
    dict(id='INV-009', pid='PRJ-005', proj='CRM Implementation',    client='JKL Corporation', date='28-Feb-2025', amount=100000, status='Paid',        pdate='05-Mar-2025', desc='Phase 2 – Training & Go-Live'),
]

def create_invoice(inv):
    doc = _doc(f"Invoice_{inv['id']}.pdf")
    story = [
        Paragraph('TECHSOLUTIONS PVT LTD', TITLE_STYLE),
        Paragraph('TAX INVOICE', SUB_STYLE),
        HRFlowable(width='100%', thickness=2, color=colors.HexColor('#38a169')),
        Spacer(1, 6*mm),
        _kv([
            ['Document Type',        'Invoice'],
            ['Invoice Number',       inv['id']],
            ['Project ID',           inv['pid']],
            ['Project Name',         inv['proj']],
            ['Client Name',          inv['client']],
            ['Invoice Date',         inv['date']],
            ['Invoice Amount (INR)', f"Rs. {inv['amount']:,}"],
            ['Payment Status',       inv['status']],
            ['Payment Date',         inv['pdate'] or 'Pending'],
            ['Description',          inv['desc']],
        ]),
        Spacer(1, 5*mm),
        Paragraph('Invoice Breakdown:', HEADER_STYLE),
    ]
    gst = int(inv['amount'] * 0.18)
    breakdown = [
        ['Description',     'Amount (INR)'],
        [inv['desc'],       f"Rs. {inv['amount']:,}"],
        ['GST @ 18%',       f"Rs. {gst:,}"],
        ['Total Payable',   f"Rs. {inv['amount'] + gst:,}"],
    ]
    t = Table(breakdown, colWidths=(110*mm, 60*mm))
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,0),  colors.HexColor('#38a169')),
        ('TEXTCOLOR',   (0,0), (-1,0),  colors.white),
        ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTNAME',    (0,1), (-1,-2), 'Helvetica'),
        ('FONTNAME',    (0,-1),(-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('BACKGROUND',  (0,-1),(-1,-1), colors.HexColor('#f0fff4')),
        ('PADDING',     (0,0), (-1,-1), 6),
        ('ALIGN',       (1,0), (1,-1),  'RIGHT'),
    ]))
    story.append(t)
    doc.build(story)
    print(f'  Invoice_{inv["id"]}.pdf')


# ── EXPENSES ─────────────────────────────────────────────────────────────────

EXPENSES = [
    dict(id='EXP-001', pid='PRJ-001', proj='E-Commerce Platform',   month='January 2025',  total=60000,  items=[('Developer Salaries',40000),('Cloud Infrastructure',12000),('Software Licences',5000),('Miscellaneous',3000)]),
    dict(id='EXP-002', pid='PRJ-001', proj='E-Commerce Platform',   month='February 2025', total=70000,  items=[('Developer Salaries',45000),('Cloud Infrastructure',15000),('Testing Tools',7000),('Miscellaneous',3000)]),
    dict(id='EXP-003', pid='PRJ-002', proj='Mobile Banking App',    month='January 2025',  total=80000,  items=[('Developer Salaries',55000),('API Integration',15000),('Security Audit',7000),('Miscellaneous',3000)]),
    dict(id='EXP-004', pid='PRJ-002', proj='Mobile Banking App',    month='February 2025', total=90000,  items=[('Developer Salaries',60000),('Cloud Services',18000),('QA Testing',9000),('Miscellaneous',3000)]),
    dict(id='EXP-005', pid='PRJ-002', proj='Mobile Banking App',    month='March 2025',    total=85000,  items=[('Developer Salaries',58000),('Cloud Services',16000),('UAT Support',8000),('Miscellaneous',3000)]),
    dict(id='EXP-006', pid='PRJ-003', proj='HR Management System',  month='November 2024', total=70000,  items=[('Developer Salaries',48000),('Server Costs',12000),('Training Material',7000),('Miscellaneous',3000)]),
    dict(id='EXP-007', pid='PRJ-003', proj='HR Management System',  month='December 2024', total=65000,  items=[('Developer Salaries',45000),('Server Costs',10000),('Documentation',7000),('Miscellaneous',3000)]),
    dict(id='EXP-008', pid='PRJ-004', proj='Supply Chain Solution', month='March 2025',    total=30000,  items=[('Initial Planning',20000),('Requirement Analysis',7000),('Miscellaneous',3000)]),
    dict(id='EXP-009', pid='PRJ-005', proj='CRM Implementation',    month='January 2025',  total=55000,  items=[('Developer Salaries',38000),('CRM Licence',10000),('Training',5000),('Miscellaneous',2000)]),
    dict(id='EXP-010', pid='PRJ-005', proj='CRM Implementation',    month='February 2025', total=60000,  items=[('Developer Salaries',40000),('CRM Licence',10000),('Go-Live Support',8000),('Miscellaneous',2000)]),
]

def create_expense(exp):
    doc = _doc(f"Expense_Report_{exp['id']}.pdf")
    story = [
        Paragraph('TECHSOLUTIONS PVT LTD', TITLE_STYLE),
        Paragraph('EXPENSE REPORT', SUB_STYLE),
        HRFlowable(width='100%', thickness=2, color=colors.HexColor('#d69e2e')),
        Spacer(1, 6*mm),
        _kv([
            ['Document Type',       'Expense Report'],
            ['Report ID',           exp['id']],
            ['Project ID',          exp['pid']],
            ['Project Name',        exp['proj']],
            ['Reporting Month',     exp['month']],
            ['Total Expenses (INR)',f"Rs. {exp['total']:,}"],
        ]),
        Spacer(1, 5*mm),
        Paragraph('Expense Breakdown:', HEADER_STYLE),
    ]
    rows = [['Expense Category', 'Amount (INR)']] + \
           [[item, f"Rs. {amt:,}"] for item, amt in exp['items']] + \
           [['TOTAL', f"Rs. {exp['total']:,}"]]
    t = Table(rows, colWidths=(110*mm, 60*mm))
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),  (-1,0),  colors.HexColor('#d69e2e')),
        ('TEXTCOLOR',     (0,0),  (-1,0),  colors.white),
        ('FONTNAME',      (0,0),  (-1,0),  'Helvetica-Bold'),
        ('FONTNAME',      (0,1),  (-1,-2), 'Helvetica'),
        ('FONTNAME',      (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),  (-1,-1), 9),
        ('GRID',          (0,0),  (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('BACKGROUND',    (0,-1), (-1,-1), colors.HexColor('#fffbeb')),
        ('ROWBACKGROUNDS',(0,1),  (-1,-2), [colors.white, colors.HexColor('#fffff0')]),
        ('PADDING',       (0,0),  (-1,-1), 6),
        ('ALIGN',         (1,0),  (1,-1),  'RIGHT'),
    ]))
    story.append(t)
    doc.build(story)
    print(f'  Expense_Report_{exp["id"]}.pdf')


# ── EMPLOYEE DIRECTORY ───────────────────────────────────────────────────────

def create_employees():
    doc = _doc('Employee_Directory.pdf')
    story = [
        Paragraph('TECHSOLUTIONS PVT LTD', TITLE_STYLE),
        Paragraph('EMPLOYEE DIRECTORY', SUB_STYLE),
        HRFlowable(width='100%', thickness=2, color=colors.HexColor('#805ad5')),
        Spacer(1, 6*mm),
        _kv([
            ['Document Type',   'Employee Directory'],
            ['Total Employees', '18'],
            ['Report Date',     '15-Jun-2025'],
        ]),
        Spacer(1, 5*mm),
        Paragraph('Department Breakdown:', HEADER_STYLE),
    ]
    rows = [
        ['Department',          'Head Count'],
        ['Software Development','8'],
        ['Quality Assurance',   '3'],
        ['Business Analysis',   '2'],
        ['UI/UX Design',        '2'],
        ['Project Management',  '2'],
        ['Administration',      '1'],
        ['TOTAL',               '18'],
    ]
    t = Table(rows, colWidths=(110*mm, 60*mm))
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),  (-1,0),  colors.HexColor('#805ad5')),
        ('TEXTCOLOR',     (0,0),  (-1,0),  colors.white),
        ('FONTNAME',      (0,0),  (-1,0),  'Helvetica-Bold'),
        ('FONTNAME',      (0,1),  (-1,-2), 'Helvetica'),
        ('FONTNAME',      (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),  (-1,-1), 9),
        ('GRID',          (0,0),  (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('BACKGROUND',    (0,-1), (-1,-1), colors.HexColor('#faf5ff')),
        ('ROWBACKGROUNDS',(0,1),  (-1,-2), [colors.white, colors.HexColor('#f5f0ff')]),
        ('PADDING',       (0,0),  (-1,-1), 6),
        ('ALIGN',         (1,0),  (1,-1),  'CENTER'),
    ]))
    story.append(t)
    doc.build(story)
    print('  Employee_Directory.pdf')


if __name__ == '__main__':
    print('Generating sample PDFs into pdfs/ ...\n')
    print('Project Contracts:')
    for p in PROJECTS:    create_project(p)
    print('\nInvoices:')
    for i in INVOICES:    create_invoice(i)
    print('\nExpense Reports:')
    for e in EXPENSES:    create_expense(e)
    print('\nEmployee Directory:')
    create_employees()
    total = len(PROJECTS) + len(INVOICES) + len(EXPENSES) + 1
    print(f'\nDone — {total} PDFs created in pdfs/')
