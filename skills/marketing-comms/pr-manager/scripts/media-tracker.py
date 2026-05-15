import json
from datetime import datetime

TRACKER_FILE = "media_coverage.json"

def load_data():
    try:
        with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"تغطيات": []}

def save_data(data):
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_coverage():
    data = load_data()
    print("=== إضافة تغطية إعلامية ===")
    
    coverage = {
        "id": f"MC{datetime.now().strftime('%Y%m%d%H%M')}",
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "المنصة": input("المنصة/الجهة الإعلامية: ").strip(),
        "الصحفي": input("اسم الصحفي: ").strip(),
        "النوع": input("النوع (مقابلة/مقال/بيان_صحفي/بث/تغريدة): ").strip(),
        "الاتجاه": input("الاتجاه (إيجابي/محايد/سلبي): ").strip(),
        "الرابط": input("الرابط: ").strip(),
        "الملخص": input("ملخص: ").strip(),
        "الإجراء": input("الإجراء المتخذ: ").strip()
    }
    
    data["تغطيات"].append(coverage)
    save_data(data)
    print(f"تم التسجيل: {coverage['id']} | {coverage['الاتجاه']}")

def monthly_summary():
    data = load_data()
    coverages = data["تغطيات"]
    
    if not coverages:
        print("لا توجد تغطيات")
        return
    
    current_month = datetime.now().strftime("%Y-%m")
    monthly = [c for c in coverages if c["التاريخ"].startswith(current_month)]
    
    positive = sum(1 for c in monthly if c["الاتجاه"] == "إيجابي")
    neutral = sum(1 for c in monthly if c["الاتجاه"] == "محايد")
    negative = sum(1 for c in monthly if c["الاتجاه"] == "سلبي")
    
    print(f"\n=== ملخص الشهر ({current_month}) ===")
    print(f"إجمالي التغطيات: {len(monthly)}")
    print(f"إيجابي: {positive} | محايد: {neutral} | سلبي: {negative}")
    if monthly:
        print(f"نسبة الإيجابي: {(positive/len(monthly))*100:.0f}%")

if __name__ == "__main__":
    print("1. إضافة تغطية\n2. ملخص شهري")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_coverage()
    elif choice == "2":
        monthly_summary()
