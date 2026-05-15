import json
from datetime import datetime

HOUSE_FILE = "house_data.json"

def load_data():
    try:
        with open(HOUSE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"أجهزة": {}, "مشاكل": [], "مصاريف": [], "سكان": []}

def save_data(data):
    with open(HOUSE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def report_issue():
    data = load_data()
    issue = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "النوع": input("النوع (كهرباء/إنترنت/جهاز/تكييف/سباكة/أخرى): ").strip(),
        "الوصف": input("وصف المشكلة: ").strip(),
        "الأولوية": input("الأولوية (طوارئ/عاجل/عادي): ").strip(),
        "البلاغ": input("اسم المُبلِّغ: ").strip(),
        "الحالة": "مفتوح"
    }
    data["مشاكل"].append(issue)
    save_data(data)
    print("تم تسجيل المشكلة")

def add_equipment():
    data = load_data()
    eq_id = input("معرف الجهاز: ").strip()
    data["أجهزة"][eq_id] = {
        "الاسم": input("اسم الجهاز: ").strip(),
        "الموقع": input("الموقع (غرفة تدريب/صالة/...): ").strip(),
        "تاريخ_الشراء": input("تاريخ الشراء (YYYY-MM-DD): ").strip(),
        "العمر_الافتراضي": input("العمر الافتراضي (سنوات): ").strip(),
        "الحالة": "نشط",
        "آخر_صيانة": input("آخر صيانة (YYYY-MM-DD): ").strip()
    }
    save_data(data)
    print(f"تم إضافة الجهاز: {eq_id}")

def add_expense():
    data = load_data()
    expense = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "البند": input("البند (فواتير/صيانة/تموين/أجهزة/أخرى): ").strip(),
        "الوصف": input("الوصف: ").strip(),
        "المبلغ": float(input("المبلغ: ").strip() or "0"),
        "الفاتورة": input("رقم الفاتورة: ").strip()
    }
    data["مصاريف"].append(expense)
    save_data(data)
    print("تم إضافة المصروف")

def show_open_issues():
    data = load_data()
    open_issues = [i for i in data["مشاكل"] if i["الحالة"] == "مفتوح"]
    if not open_issues:
        print("لا توجد مشاكل مفتوحة")
        return
    print(f"\n=== المشاكل المفتوحة ({len(open_issues)}) ===\n")
    for i, issue in enumerate(open_issues, 1):
        print(f" {i}. [{issue['الأولوية']}] {issue['النوع']}: {issue['الوصف']} ({issue['التاريخ']})")

def close_issue():
    data = load_data()
    show_open_issues()
    open_idx = [i for i, x in enumerate(data["مشاكل"]) if x["الحالة"] == "مفتوح"]
    choice = int(input("رقم المشكلة: ").strip()) - 1
    if 0 <= choice < len(open_idx):
        data["مشاكل"][open_idx[choice]]["الحالة"] = "مغلق"
        save_data(data)
        print("تم إغلاق المشكلة")

def monthly_summary():
    data = load_data()
    current_month = datetime.now().strftime("%Y-%m")
    month_expenses = [e for e in data["مصاريف"] if e["التاريخ"].startswith(current_month)]
    total = sum(e["المبلغ"] for e in month_expenses)
    open_issues = len([i for i in data["مشاكل"] if i["الحالة"] == "مفتوح"])
    print(f"\n=== ملخص الشهر {current_month} ===")
    print(f"المصروفات: {total:,.0f} ({len(month_expenses)} بند)")
    print(f"المشاكل المفتوحة: {open_issues}")
    print(f"الأجهزة المسجلة: {len(data['أجهزة'])}")

if __name__ == "__main__":
    print("1. الإبلاغ عن مشكلة\n2. إضافة جهاز\n3. إضافة مصروف\n4. المشاكل المفتوحة\n5. إغلاق مشكلة\n6. ملخص شهري")
    choice = input("اختر: ").strip()
    if choice == "1": report_issue()
    elif choice == "2": add_equipment()
    elif choice == "3": add_expense()
    elif choice == "4": show_open_issues()
    elif choice == "5": close_issue()
    elif choice == "6": monthly_summary()
