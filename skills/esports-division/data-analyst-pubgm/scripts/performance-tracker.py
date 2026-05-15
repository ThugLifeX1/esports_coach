import json
import csv
from datetime import datetime

DATA_FILE = "performance_data.json"

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"مباريات": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_match():
    data = load_data()
    print("=== إضافة بيانات مباراة ===")
    
    match = {
        "match_id": f"M{datetime.now().strftime('%Y%m%d%H%M')}",
        "date": input("التاريخ (YYYY-MM-DD): ").strip(),
        "map": input("الخريطة (Erangel/Miramar/Sanhok/Vikendi): ").strip(),
        "type": input("النوع (سكريم/بطولة/تدريب): ").strip(),
        "players": []
    }
    
    while True:
        name = input("\nاسم اللاعب (أو 'تم' للإنهاء): ").strip()
        if name == "تم" or not name:
            break
        
        player = {
            "الاسم": name,
            "kills": int(input("  Kills: ").strip() or "0"),
            "deaths": int(input("  Deaths: ").strip() or "1"),
            "damage": int(input("  Damage: ").strip() or "0"),
            "headshots": int(input("  Headshots: ").strip() or "0"),
            "survival_time": int(input("  وقت البقاء (ثانية): ").strip() or "0"),
            "placement": int(input("  الترتيب: ").strip() or "50"),
            "revives": int(input("  Revives: ").strip() or "0"),
            "knocks": int(input("  Knocks: ").strip() or "0")
        }
        
        kd = player["kills"] / max(player["deaths"], 1)
        hs_rate = (player["headshots"] / max(player["kills"], 1)) * 100
        player["kd_ratio"] = round(kd, 2)
        player["headshot_rate"] = round(hs_rate, 1)
        
        match["players"].append(player)
    
    data["مباريات"].append(match)
    save_data(data)
    print(f"\nتم حفظ المباراة: {match['match_id']}")

def generate_summary():
    data = load_data()
    matches = data["مباريات"]
    
    if not matches:
        print("لا توجد بيانات")
        return
    
    player_stats = {}
    for match in matches:
        for p in match["players"]:
            name = p["الاسم"]
            if name not in player_stats:
                player_stats[name] = {"kills": [], "damage": [], "kd": [], "hs_rate": [], "placements": []}
            player_stats[name]["kills"].append(p["kills"])
            player_stats[name]["damage"].append(p["damage"])
            player_stats[name]["kd"].append(p["kd_ratio"])
            player_stats[name]["hs_rate"].append(p["headshot_rate"])
            player_stats[name]["placements"].append(p["placement"])
    
    print("\n=== ملخص الأداء ===")
    print(f"{'اللاعب':<15} {'K/D':<8} {'Damage':<10} {'HS%':<8} {'Avg Rank':<10} {'مباريات':<8}")
    print("-" * 60)
    
    for name, stats in player_stats.items():
        avg_kd = sum(stats["kd"]) / len(stats["kd"])
        avg_dmg = sum(stats["damage"]) / len(stats["damage"])
        avg_hs = sum(stats["hs_rate"]) / len(stats["hs_rate"])
        avg_place = sum(stats["placements"]) / len(stats["placements"])
        count = len(stats["kd"])
        
        print(f"{name:<15} {avg_kd:<8.2f} {avg_dmg:<10.0f} {avg_hs:<8.1f} {avg_place:<10.1f} {count:<8}")

def export_csv():
    data = load_data()
    filename = f"performance_export_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["التاريخ", "الخريطة", "النوع", "اللاعب", "Kills", "Deaths", "Damage", "Headshots", "K/D", "HS%", "الترتيب"])
        
        for match in data["مباريات"]:
            for p in match["players"]:
                writer.writerow([
                    match["date"], match["map"], match["type"],
                    p["الاسم"], p["kills"], p["deaths"], p["damage"],
                    p["headshots"], p["kd_ratio"], p["headshot_rate"], p["placement"]
                ])
    
    print(f"تم التصدير: {filename}")

if __name__ == "__main__":
    print("1. إضافة مباراة\n2. ملخص الأداء\n3. تصدير CSV")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_match()
    elif choice == "2":
        generate_summary()
    elif choice == "3":
        export_csv()
