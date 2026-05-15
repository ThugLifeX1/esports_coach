import json
from datetime import datetime

TRACKER_FILE = "sponsor_tracker.json"

def load_data():
    try:
        with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"رعاة": {}}

def save_data(data):
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_sponsor():
    data = load_data()
    name = input("اسم الراعي: ").strip()
    
    sponsor = {
        "القطاع": input("القطاع: ").strip(),
        "الحزمة": input("الحزمة (بلاتيني/ذهبي/فضي/برونزي): ").strip(),
        "القيمة_السنوية": float(input("القيمة السنوية: ").strip() or "0"),
        "تاريخ_البداية": input("تاريخ البداية (YYYY-MM-DD): ").strip(),
        "تاريخ_الانتهاء": input("تاريخ الانتهاء (YYYY-MM-DD): ").strip(),
        "الجهة_المتواصلة": input("جهة التواصل: ").strip(),
        "البريد": input("البريد الإلكتروني: ").strip(),
        "الحالة": "نشط",
        "التزامات": [],
        "ملاحظات": input("ملاحظات: ").strip()
    }
    
    data["رعاة"][name] = sponsor
    save_data(data)
    print(f"تم إضافة الراعي: {name}")

def show_sponsors():
    data = load_data()
    sponsors = data["رعاة"]
    
    if not sponsors:
        print("لا يوجد رعاة")
        return
    
    total_revenue = 0
    print(f"\n=== الرعاة النشطون ({len(sponsors)}) ===\n")
    for name, info in sponsors.items():
        status = info["الحالة"]
        value = info["القيمة_السنوية"]
        total_revenue += value
        expiry = info["تاريخ_الانتهاء"]
        print(f"  {name} | {info['الحزمة']} | {value:,.0f} سنوياً | ينتهي: {expiry} | {status}")
    
    print(f"\nإجمالي الإيرادات السنوية: {total_revenue:,.0f}")

def check_renewals():
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    days_30 = (datetime.now() + __import__('datetime').timedelta(days=90)).strftime("%Y-%m-%d")
    
    print("\n=== عقود قريبة الانتهاء (90 يوم) ===")
    found = False
    for name, info in data["رعاة"].items():
        if info["تاريخ_الانتهاء"] <= days_30 and info["الحالة"] == "نشط":
            print(f"  ⚠️ {name} | ينتهي: {info['تاريخ_الانتهاء']} | {info['الحزمة']}")
            found = True
    
    if not found:
        print("لا توجد عقود قريبة الانتهاء")

if __name__ == "__main__":
    print("1. إضافة راعي\n2. عرض الرعاة\n3. فحص التجديدات")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_sponsor()
    elif choice == "2":
        show_sponsors()
    elif choice == "3":
        check_renewals()
