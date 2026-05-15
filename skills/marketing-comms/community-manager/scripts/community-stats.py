import json
from datetime import datetime

STATS_FILE = "community_stats.json"

def load_stats():
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"سجلات": []}

def save_stats(data):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_weekly_stats():
    data = load_stats()
    print("=== إحصائيات المجتمع الأسبوعية ===\n")
    
    record = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "Discord": {
            "الأعضاء": int(input("إجمالي أعضاء Discord: ").strip() or "0"),
            "النشطون": int(input("الأعضاء النشطون أسبوعياً: ").strip() or "0"),
            "الرسائل": int(input("عدد الرسائل الأسبوعية: ").strip() or "0"),
            "العضو_الجديد": int(input("الأعضاء الجدد هذا الأسبوع: ").strip() or "0")
        },
        "Facebook": {
            "الأعضاء": int(input("أعضاء مجموعة Facebook: ").strip() or "0"),
            "المشاركات": int(input("المشاركات الأسبوعية: ").strip() or "0"),
            "التعليقات": int(input("التعليقات الأسبوعية: ").strip() or "0")
        },
        "Telegram": {
            "الأعضاء": int(input("أعضاء مجموعة Telegram: ").strip() or "0"),
            "الرسائل": int(input("الرسائل الأسبوعية: ").strip() or "0")
        },
        "الفعاليات": {
            "العدد": int(input("عدد الفعاليات هذا الأسبوع: ").strip() or "0"),
            "المشاركون": int(input("إجمالي المشاركين: ").strip() or "0")
        },
        "الملاحظات": {
            "المستلمة": int(input("ملاحظات مستلمة: ").strip() or "0"),
            "تم_الحل": int(input("تم حلها: ").strip() or "0")
        }
    }
    
    discord_active_pct = (record["Discord"]["النشطون"] / max(record["Discord"]["الأعضاء"], 1)) * 100
    record["معدل_التفاعل"] = round(discord_active_pct, 1)
    
    data["سجلات"].append(record)
    save_stats(data)
    
    print(f"\nمعدل التفاعل Discord: {record['معدل_التفاعل']}%")
    print(f"نسبة حل الملاحظات: {(record['الملاحظات']['تم_الحل']/max(record['الملاحظات']['المستلمة'],1))*100:.0f}%")

def show_trends():
    data = load_stats()
    records = data["سجلات"]
    if len(records) < 2:
        print("تحتاج سجلين على الأقل لعرض الاتجاهات")
        return
    
    print("\n=== اتجاهات المجتمع ===")
    for i in range(1, len(records)):
        prev = records[i-1]["Discord"]["الأعضاء"]
        curr = records[i]["Discord"]["الأعضاء"]
        growth = ((curr - prev) / max(prev, 1)) * 100
        print(f"  {records[i]['التاريخ']}: {curr} عضو ({growth:+.1f}%) | تفاعل: {records[i]['معدل_التفاعل']}%")

if __name__ == "__main__":
    print("1. تسجيل إحصائيات\n2. عرض الاتجاهات")
    choice = input("اختر: ").strip()
    if choice == "1":
        log_weekly_stats()
    elif choice == "2":
        show_trends()
