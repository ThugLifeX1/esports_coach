import json
from datetime import datetime

LOG_FILE = "partnership_log.json"

def load_log():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"شراكات": {}}

def save_log(data):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_partnership():
    data = load_log()
    name = input("اسم الشريك: ").strip()
    
    partnership = {
        "النوع": input("النوع (منصة/تعليمية/حكومية/إعلامية/تقنية/مجتمعية): ").strip(),
        "تاريخ_البداية": input("تاريخ البداية (YYYY-MM-DD): ").strip(),
        "المدة": input("المدة (سنة/سنتان): ").strip(),
        "الأهداف": [],
        "الحالة": "نشط",
        "الجهة_المتواصلة": input("جهة التواصل: ").strip(),
        "البريد": input("البريد: ").strip(),
        "ملاحظات": input("ملاحظات: ").strip(),
        "آخر_مراجعة": datetime.now().strftime("%Y-%m-%d")
    }
    
    print("الأهداف المشتركة (اكتب 'تم' للإنهاء):")
    while True:
        g = input("- ").strip()
        if g == "تم" or not g:
            break
        partnership["الأهداف"].append(g)
    
    data["شراكات"][name] = partnership
    save_log(data)
    print(f"تم إضافة الشراكة: {name}")

def list_partnerships():
    data = load_log()
    if not data["شراكات"]:
        print("لا توجد شراكات")
        return
    
    print(f"\n=== الشراكات النشطة ({len(data['شراكات'])}) ===")
    for name, info in data["شراكات"].items():
        print(f"  {name} | {info['النوع']} | من: {info['تاريخ_البداية']} | {info['المدة']} | {info['الحالة']}")

def add_note():
    data = load_log()
    name = input("اسم الشريك: ").strip()
    if name not in data["شراكات"]:
        print("الشراكة غير موجودة")
        return
    
    note = input("ملاحظة جديدة: ").strip()
    data["شراكات"][name]["ملاحظات"] += f"\n[{datetime.now().strftime('%Y-%m-%d')}] {note}"
    data["شراكات"][name]["آخر_مراجعة"] = datetime.now().strftime("%Y-%m-%d")
    save_log(data)
    print(f"تم إضافة الملاحظة: {name}")

if __name__ == "__main__":
    print("1. إضافة شراكة\n2. عرض الشراكات\n3. إضافة ملاحظة")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_partnership()
    elif choice == "2":
        list_partnerships()
    elif choice == "3":
        add_note()
