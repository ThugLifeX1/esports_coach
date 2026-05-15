import json
from datetime import datetime

AUDIT_FILE = "brand_audits.json"

def load_audits():
    try:
        with open(AUDIT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"تدقيقات": []}

def save_audits(data):
    with open(AUDIT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def run_audit():
    data = load_audits()
    print("=== تدقيق العلامة التجارية ===\n")
    
    channels = ["الموقع", "Twitter/X", "Instagram", "Discord", "YouTube", "TikTok", "Twitch", "مطبوعات", "ميرتش"]
    audit = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "القنوات": {},
        "المعدل_الكلي": 0,
        "ملاحظات": ""
    }
    
    for channel in channels:
        print(f"\n--- {channel} ---")
        items = ["الشعار صحيح", "الألوان مطابقة", "الخطوط صحيحة", "النبرة متسقة", "التحديث حديث"]
        score = 0
        for item in items:
            answer = input(f"  {item}؟ (نعم/لا): ").strip()
            if answer == "نعم":
                score += 1
        
        pct = (score / len(items)) * 100
        audit["القنوات"][channel] = {"النتيجة": f"{pct:.0f}%", "التفاصيل": score}
        print(f"  نتيجة {channel}: {pct:.0f}%")
    
    total = sum(v["التفاصيل"] for v in audit["القنوات"].values())
    max_total = len(channels) * 5
    audit["المعدل_الكلي"] = round((total / max_total) * 100, 1)
    audit["ملاحظات"] = input("\nملاحظات عامة: ").strip()
    
    data["تدقيقات"].append(audit)
    save_audits(data)
    
    print(f"\nالمعدل الكلي: {audit['المعدل_الكلي']}%")
    if audit["المعدل_الكلي"] >= 90:
        print("الحالة: ممتاز - العلامة متسقة")
    elif audit["المعدل_الكلي"] >= 75:
        print("الحالة: جيد - يحتاج تحسينات طفيفة")
    else:
        print("الحالة: يحتاج تدخل - عدم اتساق واضح")

def show_history():
    data = load_audits()
    if not data["تدقيقات"]:
        print("لا توجد تدقيقات سابقة")
        return
    print("\n=== سجل التدقيقات ===")
    for a in data["تدقيقات"]:
        print(f"  {a['التاريخ']} | المعدل: {a['المعدل_الكلي']}%")

if __name__ == "__main__":
    print("1. إجراء تدقيق\n2. عرض السجل")
    choice = input("اختر: ").strip()
    if choice == "1":
        run_audit()
    elif choice == "2":
        show_history()
