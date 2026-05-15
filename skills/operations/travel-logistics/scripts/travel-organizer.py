import json
from datetime import datetime

TRIPS_FILE = "travel_trips.json"

def load_data():
    try:
        with open(TRIPS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"رحلات": {}}

def save_data(data):
    with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_trip():
    data = load_data()
    trip_id = input("معرف الرحلة (مثال: PMWC-2026): ").strip()
    data["رحلات"][trip_id] = {
        "البطولة": input("اسم البطولة: ").strip(),
        "الوجهة": input("الوجهة (المدينة، الدولة): ").strip(),
        "تاريخ_السفر": input("تاريخ السفر (YYYY-MM-DD): ").strip(),
        "تاريخ_العودة": input("تاريخ العودة (YYYY-MM-DD): ").strip(),
        "المسافرون": [x.strip() for x in input("أسماء المسافرين (مفصولة بفاصلة): ").split(",")],
        "الميزانية": float(input("الميزانية التقديرية: ").strip() or "0"),
        "المصروفات": [],
        "الحجوزات": {
            "طيران": "لم يُحجز",
            "فندق": "لم يُحجز",
            "نقل_محلي": "لم يُرتب",
            "تأشيرات": "لا تحتاج"
        },
        "الحالة": "تخطيط"
    }
    save_data(data)
    print(f"تم إنشاء الرحلة: {trip_id}")

def update_booking():
    data = load_data()
    trip_id = input("معرف الرحلة: ").strip()
    if trip_id not in data["رحلات"]:
        print("الرحلة غير موجودة")
        return
    print("1. طيران\n2. فندق\n3. نقل محلي\n4. تأشيرات")
    choice = input("اختر الحجز: ").strip()
    key = {"1": "طيران", "2": "فندق", "3": "نقل_محلي", "4": "تأشيرات"}.get(choice)
    if key:
        data["رحلات"][trip_id]["الحجوزات"][key] = input("الحالة: ").strip()
        save_data(data)
        print("تم تحديث الحجز")

def add_expense():
    data = load_data()
    trip_id = input("معرف الرحلة: ").strip()
    if trip_id not in data["رحلات"]:
        print("الرحلة غير موجودة")
        return
    data["رحلات"][trip_id]["المصروفات"].append({
        "البند": input("البند: ").strip(),
        "المبلغ": float(input("المبلغ: ").strip() or "0"),
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "الفاتورة": input("رقم الفاتورة: ").strip()
    })
    save_data(data)
    print("تم إضافة المصروف")

def trip_summary():
    data = load_data()
    trip_id = input("معرف الرحلة: ").strip()
    if trip_id not in data["رحلات"]:
        print("الرحلة غير موجودة")
        return
    t = data["رحلات"][trip_id]
    total_spent = sum(e["المبلغ"] for e in t["المصروفات"])
    remaining = t["الميزانية"] - total_spent
    print(f"\n=== {trip_id}: {t['البطولة']} ===")
    print(f"الوجهة: {t['الوجهة']} | {t['تاريخ_السفر']} → {t['تاريخ_العودة']}")
    print(f"المسافرون: {', '.join(t['المسافرون'])}")
    print(f"الميزانية: {t['الميزانية']:,.0f} | المصروف: {total_spent:,.0f} | المتبقي: {remaining:,.0f}")
    print("الحجوزات:")
    for k, v in t["الحجوزات"].items():
        print(f"  {k}: {v}")
    print(f"الحالة: {t['الحالة']}")

if __name__ == "__main__":
    print("1. إنشاء رحلة\n2. تحديث حجز\n3. إضافة مصروف\n4. ملخص الرحلة")
    choice = input("اختر: ").strip()
    if choice == "1": create_trip()
    elif choice == "2": update_booking()
    elif choice == "3": add_expense()
    elif choice == "4": trip_summary()
