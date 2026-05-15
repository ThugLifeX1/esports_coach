import json
from datetime import datetime

FINANCE_FILE = "finance_data.json"

def load_data():
    try:
        with open(FINANCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"ميزانية": {}, "مصروفات": [], "إيرادات": []}

def save_data(data):
    with open(FINANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def set_budget():
    data = load_data()
    category = input("القسم (رواتب/سفر/دار_ألعاب/تسويق/أجهزة/أخرى): ").strip()
    year = input("السنة (YYYY): ").strip()
    amount = float(input("الميزانية السنوية: ").strip() or "0")
    if year not in data["ميزانية"]:
        data["ميزانية"][year] = {}
    data["ميزانية"][year][category] = {
        "المبلغ": amount,
        "المصروف": 0
    }
    save_data(data)
    print(f"تم تحديد ميزانية {category} لسنة {year}: {amount:,.0f}")

def add_expense():
    data = load_data()
    year = datetime.now().strftime("%Y")
    category = input("القسم: ").strip()
    amount = float(input("المبلغ: ").strip() or "0")
    expense = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "القسم": category,
        "الوصف": input("الوصف: ").strip(),
        "المبلغ": amount,
        "الفاتورة": input("رقم الفاتورة: ").strip(),
        "الطالب": input("اسم الطالب: ").strip(),
        "الحالة": "معلق"
    }
    data["مصروفات"].append(expense)
    if year in data["ميزانية"] and category in data["ميزانية"][year]:
        data["ميزانية"][year][category]["المصروف"] += amount
    save_data(data)
    print("تم تسجيل المصروف")

def add_revenue():
    data = load_data()
    revenue = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "المصدر": input("المصدر (رعاية/جوائز/بضائع/بث/شراكة/أخرى): ").strip(),
        "الوصف": input("الوصف: ").strip(),
        "المبلغ": float(input("المبلغ: ").strip() or "0"),
        "مستحق_التاريخ": input("تاريخ الاستحقاق (YYYY-MM-DD): ").strip(),
        "الحالة": "مستحق"
    }
    data["إيرادات"].append(revenue)
    save_data(data)
    print("تم تسجيل الإيراد")

def budget_summary():
    data = load_data()
    year = input("السنة (YYYY) أو اتركه فارغاً للسنة الحالية: ").strip() or datetime.now().strftime("%Y")
    if year not in data["ميزانية"]:
        print(f"لا ميزانية لسنة {year}")
        return
    print(f"\n=== ملخص الميزانية {year} ===\n")
    total_budget = 0
    total_spent = 0
    for cat, info in data["ميزانية"][year].items():
        budget = info["المبلغ"]
        spent = info["المصروف"]
        pct = (spent / budget * 100) if budget > 0 else 0
        total_budget += budget
        total_spent += spent
        status = "⚠️" if pct > 90 else "✓"
        print(f" {status} {cat}: {spent:,.0f} / {budget:,.0f} ({pct:.0f}%)")
    overall_pct = (total_spent / total_budget * 100) if total_budget > 0 else 0
    print(f"\nالإجمالي: {total_spent:,.0f} / {total_budget:,.0f} ({overall_pct:.0f}%)")

def pending_expenses():
    data = load_data()
    pending = [e for e in data["مصروفات"] if e["الحالة"] == "معلق"]
    if not pending:
        print("لا مصروفات معلقة")
        return
    print(f"\n=== مصروفات معلقة ({len(pending)}) ===\n")
    for e in pending:
        print(f" {e['التاريخ']} | {e['القسم']} | {e['المبلغ']:,.0f} | {e['الوصف']}")

if __name__ == "__main__":
    print("1. تحديد ميزانية\n2. تسجيل مصروف\n3. تسجيل إيراد\n4. ملخص الميزانية\n5. مصروفات معلقة")
    choice = input("اختر: ").strip()
    if choice == "1": set_budget()
    elif choice == "2": add_expense()
    elif choice == "3": add_revenue()
    elif choice == "4": budget_summary()
    elif choice == "5": pending_expenses()
