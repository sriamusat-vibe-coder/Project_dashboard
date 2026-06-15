"""
pdf_parser.py — Parses project, invoice, expense, and employee PDFs.
Uses pdfplumber table extraction for accuracy.
"""
import re
import pdfplumber
from pathlib import Path
from typing import Optional


# ── Low-level helpers ─────────────────────────────────────────────────────────

def _read_pdf(path: str):
    """Return (full_text, flat_kv_dict) from a PDF."""
    text = ""
    kv = {}
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
                for table in (page.extract_tables() or []):
                    for row in table:
                        if row and len(row) >= 2:
                            key = str(row[0] or "").strip()
                            val = str(row[1] or "").strip()
                            if key:
                                kv[key] = val
                                kv[key.lower()] = val
    except Exception as e:
        print(f"  [parser] Could not read {path}: {e}")
    return text, kv


def _val(kv: dict, *keys) -> str:
    """Return first non-empty value matching any of the given keys (case-insensitive)."""
    for k in keys:
        v = kv.get(k) or kv.get(k.lower()) or ""
        if v and v.lower() not in ("none", "nan", "-"):
            return v.strip()
    return ""


def _amount(raw: str) -> float:
    """Extract the first number from a string like 'Rs. 5,00,000' → 500000.0"""
    match = re.search(r"(\d[\d,]*(?:\.\d+)?)", raw)
    if match:
        return float(match.group(1).replace(",", ""))
    return 0.0


# ── Document-type parsers ─────────────────────────────────────────────────────

def parse_project_pdf(path: str) -> Optional[dict]:
    text, kv = _read_pdf(path)
    if "Project Contract" not in text and "PROJECT CONTRACT" not in text:
        return None
    return {
        "type": "project",
        "source_file": Path(path).name,
        "project_id":     _val(kv, "Project ID"),
        "project_name":   _val(kv, "Project Name"),
        "client":         _val(kv, "Client Name"),
        "contract_value": _amount(_val(kv, "Contract Value (INR)", "Contract Value")),
        "start_date":     _val(kv, "Start Date"),
        "end_date":       _val(kv, "End Date"),
        "status":         _val(kv, "Project Status"),
        "manager":        _val(kv, "Project Manager"),
    }


def parse_invoice_pdf(path: str) -> Optional[dict]:
    text, kv = _read_pdf(path)
    if "Invoice" not in text and "INVOICE" not in text:
        return None
    if "Expense Report" in text or "EXPENSE REPORT" in text:
        return None
    pdate = _val(kv, "Payment Date")
    return {
        "type": "invoice",
        "source_file": Path(path).name,
        "invoice_id":   _val(kv, "Invoice Number"),
        "project_id":   _val(kv, "Project ID"),
        "project_name": _val(kv, "Project Name"),
        "client":       _val(kv, "Client Name"),
        "invoice_date": _val(kv, "Invoice Date"),
        "amount":       _amount(_val(kv, "Invoice Amount (INR)", "Invoice Amount")),
        "status":       _val(kv, "Payment Status"),
        "payment_date": "" if pdate.lower() in ("pending", "none", "") else pdate,
        "description":  _val(kv, "Description"),
    }


def parse_expense_pdf(path: str) -> Optional[dict]:
    text, kv = _read_pdf(path)
    if "Expense Report" not in text and "EXPENSE REPORT" not in text:
        return None
    return {
        "type": "expense",
        "source_file": Path(path).name,
        "report_id":    _val(kv, "Report ID"),
        "project_id":   _val(kv, "Project ID"),
        "project_name": _val(kv, "Project Name"),
        "month":        _val(kv, "Reporting Month"),
        "total":        _amount(_val(kv, "Total Expenses (INR)", "Total Expenses")),
    }


def parse_employee_pdf(path: str) -> Optional[dict]:
    text, kv = _read_pdf(path)
    if "Employee Directory" not in text and "EMPLOYEE DIRECTORY" not in text:
        return None
    return {
        "type": "employee",
        "source_file": Path(path).name,
        "total_employees": int(_amount(_val(kv, "Total Employees"))),
    }


_PARSERS = [parse_project_pdf, parse_invoice_pdf, parse_expense_pdf, parse_employee_pdf]


# ── Folder loader ─────────────────────────────────────────────────────────────

def load_all_pdfs(folder: str) -> dict:
    """Scan a folder for PDFs, auto-detect type, and return grouped data."""
    folder_path = Path(folder)
    if not folder_path.exists():
        return {"projects": [], "invoices": [], "expenses": [], "employees": [],
                "error": f"Folder not found: {folder}"}

    projects, invoices, expenses, employees = [], [], [], []
    targets = {"project": projects, "invoice": invoices, "expense": expenses, "employee": employees}

    pdf_files = sorted(folder_path.glob("*.pdf"))
    print(f"[parser] Found {len(pdf_files)} PDFs in {folder}")

    for pdf_file in pdf_files:
        for parser in _PARSERS:
            try:
                result = parser(str(pdf_file))
                if result:
                    targets[result["type"]].append(result)
                    break
            except Exception as e:
                print(f"  [parser] Error in {parser.__name__} on {pdf_file.name}: {e}")

    return {"projects": projects, "invoices": invoices,
            "expenses": expenses,  "employees": employees}


# ── Metrics computation ───────────────────────────────────────────────────────

def compute_metrics(data: dict) -> dict:
    projects  = data.get("projects",  [])
    invoices  = data.get("invoices",  [])
    expenses  = data.get("expenses",  [])
    employees = data.get("employees", [])

    # Project counts
    total_projects     = len(projects)
    active_projects    = sum(1 for p in projects if p["status"].lower() == "active")
    completed_projects = sum(1 for p in projects if p["status"].lower() == "completed")
    on_hold_projects   = sum(1 for p in projects if "hold" in p["status"].lower())

    # Financial KPIs
    total_contract_value = sum(p["contract_value"] for p in projects)
    total_invoiced       = sum(i["amount"] for i in invoices)
    total_received       = sum(i["amount"] for i in invoices if i["status"].lower() == "paid")
    total_outstanding    = sum(i["amount"] for i in invoices if i["status"].lower() != "paid")
    total_expenses       = sum(e["total"] for e in expenses)
    total_profit         = total_received - total_expenses
    net_cash_position    = total_profit

    employee_count = sum(e["total_employees"] for e in employees) if employees else 0

    # Monthly revenue (from paid invoice payment dates)
    monthly_revenue: dict[str, float] = {}
    for inv in invoices:
        if inv["status"].lower() == "paid" and inv.get("payment_date"):
            m = _to_month_key(inv["payment_date"])
            if m:
                monthly_revenue[m] = monthly_revenue.get(m, 0) + inv["amount"]

    # Monthly expense (from expense report months)
    monthly_expense: dict[str, float] = {}
    for exp in expenses:
        m = _month_str_to_key(exp["month"])
        if m:
            monthly_expense[m] = monthly_expense.get(m, 0) + exp["total"]

    all_months = sorted(set(list(monthly_revenue) + list(monthly_expense)))
    monthly_data = [
        {
            "month":   _key_to_label(m),
            "revenue": monthly_revenue.get(m, 0),
            "expense": monthly_expense.get(m, 0),
            "net":     monthly_revenue.get(m, 0) - monthly_expense.get(m, 0),
        }
        for m in all_months
    ]

    return {
        "total_projects":      total_projects,
        "active_projects":     active_projects,
        "completed_projects":  completed_projects,
        "on_hold_projects":    on_hold_projects,
        "total_contract_value":total_contract_value,
        "total_invoiced":      total_invoiced,
        "total_received":      total_received,
        "total_outstanding":   total_outstanding,
        "total_expenses":      total_expenses,
        "total_profit":        total_profit,
        "net_cash_position":   net_cash_position,
        "employee_count":      employee_count,
        "monthly_data":        monthly_data,
        "projects":  projects,
        "invoices":  invoices,
        "expenses":  expenses,
    }


# ── Date helpers ──────────────────────────────────────────────────────────────

_MONTH_NUM = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06",
              "jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}
_MONTH_LABEL = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun",
                "07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}


def _to_month_key(date_str: str) -> Optional[str]:
    """'20-Jan-2025' → '2025-01'"""
    m = re.search(r'(\w{3})[/-](\d{4})', date_str)
    if m:
        mn = _MONTH_NUM.get(m.group(1).lower()[:3])
        if mn:
            return f"{m.group(2)}-{mn}"
    m2 = re.search(r'(\d{1,2})[/-](\d{2})[/-](\d{4})', date_str)
    if m2:
        return f"{m2.group(3)}-{m2.group(2).zfill(2)}"
    return None


def _month_str_to_key(s: str) -> Optional[str]:
    """'January 2025' → '2025-01'"""
    parts = s.strip().split()
    if len(parts) == 2:
        mn = _MONTH_NUM.get(parts[0].lower()[:3])
        if mn:
            return f"{parts[1]}-{mn}"
    return None


def _key_to_label(key: str) -> str:
    """'2025-01' → 'Jan 2025'"""
    parts = key.split("-")
    if len(parts) == 2:
        return f"{_MONTH_LABEL.get(parts[1], parts[1])} {parts[0]}"
    return key
