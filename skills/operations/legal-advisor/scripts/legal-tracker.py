import json
from datetime import datetime

LEGAL_FILE = "legal_data.json"

def load_data():
    try:
        with open(LEGAL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"عقود": {}, "قضايا": [], "استشارات": [], "علامات_تجارية": {}}

def save_data(data):
    with open(LEGAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_contract():
    data = load_data()
    contract_id = input("معرف العقد: ").strip()
    data["عقود"][contract_id] = {
        "النوع": input("النوع (لاعب/رعاية/شراكة/موظف/مستقل): ").strip(),
        "الأطراف": input("الأطراف: ").strip(),
        "تاريخ_التوقيع": input("تاريخ التوقيع (YYYY-MM-DD): ").strip(),
        "تاريخ_الانتهاء": input("تاريخ الانتهاء (YYYY-MM-DD): ").strip(),
        "القيمة": float(input("القيمة: ").strip() or "0"),
        "الحالة": input("الحالة (مسودة/قيد_المراجعة/موقع/منتهي/ملغى): ").strip(),
        "ملاحظات": input("ملاحظات: ").strip()
    }
    save_data(data)
    print(f"تم إضافة العقد: {contract_id}")

def add_case():
    data = load_data()
    case = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "النوع": input("النوع (نزاع/مخالفة/ملكية_فكرية/عقدي/أخرى): ").strip(),
        "الوصف": input("الوصف: ").strip(),
        "الأطراف": input("الأطراف المتنازعة: ").strip(),
        "الأولوية": input("الأولوية (عاجل/عادي/منخفض): ").strip(),
        "الحالة": "مفتوح",
        "الإجراءات": []
    }
    data["قضايا"].append(case)
    save_data(data)
    print("تم تسجيل القضية")

def add_consultation():
    data = load_data()
    consult = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "الطالب": input("الطالب (القسم/الشخص): ").strip(),
        "الموضوع": input("الموضوع: ").strip(),
        "التفاصيل": input("التفاصيل: ").strip(),
        "الحالة": "قيد المراجعة",
        "الرأي_القانوني": ""
    }
    data["استشارات"].append(consult)
    save_data(data)
    print("تم تسجيل الاستشارة")

def show_expiring_contracts():
    data = load_data()
    from datetime import timedelta
    threshold = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    print("\n=== عقود قريبة الانتهاء (90 يوم) ===")
    found = False
    for cid, info in data["عقود"].items():
        if info["تاريخ_الانتهاء"] <= threshold and info["الحالة"] in ["موقع", "قيد_المراجعة"]:
            print(f" ⚠️ {cid} | {info['النوع']} | ينتهي: {info['تاريخ_الانتهاء']} | {info['الأطراف']}")
            found = True
    if not found:
        print("لا توجد عقود قريبة الانتهاء")

def show_open_cases():
    data = load_data()
    open_cases = [c for c in data["قضايا"] if c["الحالة"] == "مفتوح"]
    if not open_cases:
        print("لا قضايا مفتوحة")
        return
    print(f"\n=== القضايا المفتوحة ({len(open_cases)}) ===\n")
    for i, c in enumerate(open_cases, 1):
        print(f" {i}. [{c['الأولوية']}] {c['النوع']}: {c['الوصف']} ({c['التاريخ']})")

def contract_summary():
    data = load_data()
    if not data["عقود"]:
        print("لا توجد عقود")
        return
    print(f"\n=== ملخص العقود ({len(data['عقود'])}) ===\n")
    for cid, info in data["عقود"].items():
        print(f" {cid} | {info['النوع']} | {info['الحالة']} | {info['تاريخ_الانتهاء']}")

if __name__ == "__main__":
    print("1. إضافة عقد\n2. تسجيل قضية\n3. تسجيل استشارة\n4. عقود قريبة الانتهاء\n5. قضايا مفتوحة\n6. ملخص العقود")
    choice = input("اختر: ").strip()
    if choice == "1": add_contract()
    elif choice == "2": add_case()
    elif choice == "3": add_consultation()
    elif choice == "4": show_expiring_contracts()
    elif choice == "5": show_open_cases()
    elif choice == "6": contract_summary()
