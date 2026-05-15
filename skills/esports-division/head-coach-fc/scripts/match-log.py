import json
from datetime import datetime

LOG_FILE = "fc_match_log.json"

def load_log():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"مباريات": []}

def save_log(data):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_match():
    data = load_log()
    print("=== تسجيل مباراة FC ===")
    
    match = {
        "match_id": f"FC{datetime.now().strftime('%Y%m%d%H%M')}",
        "date": input("التاريخ (YYYY-MM-DD): ").strip(),
        "opponent": input("المنافس: ").strip(),
        "tournament": input("البطولة/النوع: ").strip(),
        "formation": input("التشكيلة: ").strip(),
        "goals_scored": int(input("أهداف مسجلة: ").strip() or "0"),
        "goals_conceded": int(input("أهداف مستقبلة: ").strip() or "0"),
        "possession": int(input("نسبة استحواذ %: ").strip() or "50"),
        "passes_accuracy": int(input("دقة التمرير %: ").strip() or "80"),
        "shots_on_target": int(input("تسديدات على المرمى: ").strip() or "0"),
        "result": "",
        "notes": input("ملاحظات: ").strip(),
        "player_performance": input("أداء اللاعب (1-10): ").strip()
    }
    
    if match["goals_scored"] > match["goals_conceded"]:
        match["result"] = "فوز"
    elif match["goals_scored"] == match["goals_conceded"]:
        match["result"] = "تعادل"
    else:
        match["result"] = "خسارة"
    
    data["مباريات"].append(match)
    save_log(data)
    print(f"\nتم تسجيل المباراة: {match['result']} ({match['goals_scored']}-{match['goals_conceded']})")

def show_stats():
    data = load_log()
    matches = data["مباريات"]
    
    if not matches:
        print("لا توجد مباريات مسجلة")
        return
    
    wins = sum(1 for m in matches if m["result"] == "فوز")
    draws = sum(1 for m in matches if m["result"] == "تعادل")
    losses = sum(1 for m in matches if m["result"] == "خسارة")
    total = len(matches)
    
    avg_scored = sum(m["goals_scored"] for m in matches) / total
    avg_conceded = sum(m["goals_conceded"] for m in matches) / total
    avg_possession = sum(m["possession"] for m in matches) / total
    
    print(f"\n=== إحصائيات الفريق ===")
    print(f"مباريات: {total} | فوز: {wins} | تعادل: {draws} | خسارة: {losses}")
    print(f"نسبة الفوز: {(wins/total)*100:.1f}%")
    print(f"متوسط أهداف مسجلة: {avg_scored:.1f}")
    print(f"متوسط أهداف مستقبلة: {avg_conceded:.1f}")
    print(f"متوسط استحواذ: {avg_possession:.0f}%")

if __name__ == "__main__":
    print("1. تسجيل مباراة\n2. عرض الإحصائيات")
    choice = input("اختر: ").strip()
    if choice == "1":
        log_match()
    elif choice == "2":
        show_stats()
