import json
import csv
import os
from datetime import datetime

ROSTER_FILE = "../roster-manager/roster_data.json"
ANALYSIS_FILE = "team_analysis.json"
ARCHIVE_DIR = "analysis_archive"

MIN_PLAYERS = 4
MAX_PLAYERS = 6

def load_roster():
    try:
        with open(ROSTER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get("لاعبون", {})
    except FileNotFoundError:
        return {}

def load_analysis():
    try:
        with open(ANALYSIS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"مباريات": [], "تحاليل_أسبوعية": {}, "تحاليل_شهرية": {}, "تنبيهات": []}

def save_analysis(data):
    with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def verify_player(ign, roster):
    if ign in roster:
        return True, roster[ign]
    return False, None

def sync_roster():
    roster = load_roster()
    data = load_analysis()
    current = set(data.get("قائمة_الفريق", {}).keys())
    roster_igns = set(roster.keys())
    added = roster_igns - current
    removed = current - roster_igns
    if added or removed:
        data["قائمة_الفريق"] = {}
        for ign, info in roster.items():
            data["قائمة_الفريق"][ign] = {
                "UID": info.get("UID", ""),
                "الدور": info.get("الدور_في_الفريق", ""),
                "الجهاز": info.get("الجهاز", ""),
                "FPS": info.get("FPS", 0),
                "الحالة": info.get("الحالة", "نشط")
            }
        save_analysis(data)
        print(f"تمت المزامنة: +{len(added)} لاعب، -{len(removed)} لاعب")
    else:
        print("القائمة محدثة")
    return roster

def add_match_data():
    roster = load_roster()
    if not roster:
        print("قائمة الفريق فارغة. قم بإضافة لاعبين عبر مدير القائمة أولاً.")
        return
    data = load_analysis()
    print(f"لاعبو الفريق المتاحون: {', '.join(roster.keys())}")
    match = {
        "match_id": f"M{datetime.now().strftime('%Y%m%d%H%M')}",
        "date": input("التاريخ (YYYY-MM-DD): ").strip(),
        "map": input("الخريطة (Erangel/Miramar/Sanhok/Vikendi): ").strip(),
        "type": input("النوع (سكريم/بطولة/تدريب): ").strip(),
        "players": []
    }
    while True:
        ign = input("\nIGN اللاعب (أو 'تم'): ").strip()
        if ign == "تم" or not ign:
            break
        valid, info = verify_player(ign, roster)
        if not valid:
            print(f"⚠️ {ign} ليس ضمن قائمة الفريق. تم الرفض.")
            continue
        p = {
            "IGN": ign,
            "الدور": info.get("الدور_في_الفريق", ""),
            "kills": int(input("  Kills: ").strip() or "0"),
            "deaths": int(input("  Deaths: ").strip() or "1"),
            "damage": int(input("  Damage: ").strip() or "0"),
            "headshots": int(input("  Headshots: ").strip() or "0"),
            "survival_time": int(input("  وقت البقاء (ثانية): ").strip() or "0"),
            "placement": int(input("  الترتيب: ").strip() or "50"),
            "revives": int(input("  Revives: ").strip() or "0"),
            "knocks": int(input("  Knocks: ").strip() or "0")
        }
        p["kd_ratio"] = round(p["kills"] / max(p["deaths"], 1), 2)
        p["headshot_rate"] = round((p["headshots"] / max(p["kills"], 1)) * 100, 1)
        match["players"].append(p)
        print(f"  ✓ {ign} ({p['الدور']}) — K/D: {p['kd_ratio']}, DMG: {p['damage']}")
    data["مباريات"].append(match)
    save_analysis(data)
    print(f"\nتم حفظ المباراة: {match['match_id']} ({len(match['players'])} لاعب)")

def import_csv():
    roster = load_roster()
    if not roster:
        print("قائمة الفريق فارغة")
        return
    filepath = input("مسار ملف CSV: ").strip()
    if not os.path.exists(filepath):
        print("الملف غير موجود")
        return
    data = load_analysis()
    added = 0
    rejected = 0
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ign = row.get("IGN", row.get("اللاعب", "")).strip()
            if not verify_player(ign, roster)[0]:
                rejected += 1
                continue
            match = {
                "match_id": f"CSV-{datetime.now().strftime('%Y%m%d%H%M')}-{added}",
                "date": row.get("التاريخ", row.get("date", "")),
                "map": row.get("الخريطة", row.get("map", "")),
                "type": row.get("النوع", row.get("type", "استيراد")),
                "players": [{
                    "IGN": ign,
                    "kills": int(row.get("Kills", 0)),
                    "deaths": int(row.get("Deaths", 1)),
                    "damage": int(row.get("Damage", 0)),
                    "headshots": int(row.get("Headshots", 0)),
                    "survival_time": int(row.get("Survival_Time", 0)),
                    "placement": int(row.get("Placement", 50)),
                    "revives": int(row.get("Revives", 0)),
                    "knocks": int(row.get("Knocks", 0)),
                    "kd_ratio": round(int(row.get("Kills", 0)) / max(int(row.get("Deaths", 1)), 1), 2),
                    "headshot_rate": round((int(row.get("Headshots", 0)) / max(int(row.get("Kills", 0)), 1)) * 100, 1)
                }]
            }
            data["مباريات"].append(match)
            added += 1
    save_analysis(data)
    print(f"تم استيراد {added} سجل، رُفض {rejected} (خارج القائمة)")

def generate_weekly_report():
    roster = load_roster()
    data = load_analysis()
    matches = data["مباريات"]
    if not matches:
        print("لا توجد بيانات")
        return
    player_stats = {}
    for m in matches:
        for p in m["players"]:
            ign = p["IGN"]
            if ign not in player_stats:
                player_stats[ign] = {"kills": [], "damage": [], "kd": [], "hs": [], "placements": [], "revives": [], "matches": 0}
            player_stats[ign]["kills"].append(p["kills"])
            player_stats[ign]["damage"].append(p["damage"])
            player_stats[ign]["kd"].append(p["kd_ratio"])
            player_stats[ign]["hs"].append(p["headshot_rate"])
            player_stats[ign]["placements"].append(p["placement"])
            player_stats[ign]["revives"].append(p.get("revives", 0))
            player_stats[ign]["matches"] += 1
    week_key = datetime.now().strftime("2026-W%W")
    weekly = {}
    print(f"\n{'='*70}")
    print(f"  تقرير أداء الفريق — {week_key}")
    print(f"{'='*70}")
    print(f"{'IGN':<12} {'الدور':<10} {'K/D':<8} {'Damage':<10} {'HS%':<8} {'AvgRank':<10} {'مباريات':<8}")
    print("-" * 70)
    for ign in roster:
        if ign not in player_stats:
            print(f"{ign:<12} {roster[ign].get('الدور_في_الفريق',''):<10} — لا بيانات —")
            continue
        s = player_stats[ign]
        avg_kd = sum(s["kd"]) / len(s["kd"])
        avg_dmg = sum(s["damage"]) / len(s["damage"])
        avg_hs = sum(s["hs"]) / len(s["hs"])
        avg_place = sum(s["placements"]) / len(s["placements"])
        role = roster[ign].get("الدور_في_الفريق", "")
        trend = "→"
        if len(s["kd"]) >= 4:
            recent = sum(s["kd"][-2:]) / 2
            older = sum(s["kd"][:2]) / 2
            trend = "▲" if recent > older * 1.05 else ("▼" if recent < older * 0.95 else "→")
        weekly[ign] = {"kd": round(avg_kd, 2), "damage": round(avg_dmg), "hs_rate": round(avg_hs, 1), "survival": round(avg_place, 1), "trend": trend}
        print(f"{ign:<12} {role:<10} {avg_kd:<8.2f} {avg_dmg:<10.0f} {avg_hs:<8.1f} {avg_place:<10.1f} {s['matches']:<8} {trend}")
    data["تحاليل_أسبوعية"][week_key] = weekly
    save_analysis(data)

def compare_periods():
    data = load_analysis()
    weekly = data.get("تحاليل_أسبوعية", {})
    weeks = sorted(weekly.keys())
    if len(weeks) < 2:
        print("تحتاج أسبوعين على الأقل للمقارنة")
        return
    current = weekly[weeks[-1]]
    previous = weekly[weeks[-2]]
    print(f"\n{'='*60}")
    print(f"  مقارنة: {weeks[-2]} vs {weeks[-1]}")
    print(f"{'='*60}")
    print(f"{'IGN':<12} {'مؤشر':<8} {'السابق':<10} {'الحالي':<10} {'التغيير':<10}")
    print("-" * 55)
    for ign in current:
        if ign not in previous:
            continue
        for metric in ["kd", "damage", "hs_rate"]:
            prev_val = previous[ign].get(metric, 0)
            curr_val = current[ign].get(metric, 0)
            if prev_val > 0:
                change = ((curr_val - prev_val) / prev_val) * 100
                arrow = "▲" if change > 0 else ("▼" if change < 0 else "→")
                print(f"{ign:<12} {metric:<8} {prev_val:<10} {curr_val:<10} {arrow} {abs(change):.1f}%")

def check_alerts():
    data = load_analysis()
    weekly = data.get("تحاليل_أسبوعية", {})
    if len(weekly) < 2:
        print("لا بيانات كافية للتنبيهات")
        return
    weeks = sorted(weekly.keys())
    current = weekly[weeks[-1]]
    previous = weekly[weeks[-2]]
    alerts = []
    for ign, stats in current.items():
        if ign in previous:
            prev_kd = previous[ign].get("kd", 0)
            curr_kd = stats.get("kd", 0)
            if prev_kd > 0 and curr_kd < prev_kd * 0.8:
                alerts.append(f"⚠️ {ign}: K/D تراجع بنسبة {((prev_kd - curr_kd) / prev_kd * 100):.1f}% (من {prev_kd} إلى {curr_kd})")
    if alerts:
        print(f"\n=== تنبيهات مبكرة ({len(alerts)}) ===\n")
        for a in alerts:
            print(f"  {a}")
        data["تنبيهات"].extend(alerts)
        save_analysis(data)
    else:
        print("لا تنبيهات — أداء الفريق مستقر")

def show_player_history():
    roster = load_roster()
    data = load_analysis()
    ign = input("IGN اللاعب: ").strip()
    if not verify_player(ign, roster)[0]:
        print("اللاعب ليس ضمن قائمة الفريق")
        return
    weekly = data.get("تحاليل_أسبوعية", {})
    player_data = {w: s for w, s in weekly.items() if ign in s}
    if not player_data:
        print(f"لا تحاليل سابقة لـ {ign}")
        return
    print(f"\n=== سجل تطور {ign} ===\n")
    print(f"{'الأسبوع':<15} {'K/D':<8} {'Damage':<10} {'HS%':<8} {'AvgRank':<10}")
    print("-" * 50)
    for week in sorted(player_data.keys()):
        s = player_data[week][ign]
        print(f"{week:<15} {s.get('kd',0):<8.2f} {s.get('damage',0):<10} {s.get('hs_rate',0):<8.1f} {s.get('survival',0):<10}")

def export_csv():
    data = load_analysis()
    filename = f"team_export_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["التاريخ", "الخريطة", "النوع", "IGN", "Kills", "Deaths", "Damage", "Headshots", "K/D", "HS%", "الترتيب"])
        for m in data["مباريات"]:
            for p in m["players"]:
                writer.writerow([m["date"], m["map"], m["type"], p["IGN"], p["kills"], p.get("deaths",1), p["damage"], p["headshots"], p["kd_ratio"], p["headshot_rate"], p["placement"]])
    print(f"تم التصدير: {filename}")

if __name__ == "__main__":
    print("=== محلل بيانات الفريق ===")
    print("1. مزامنة القائمة من Roster Manager")
    print("2. إضافة بيانات مباراة")
    print("3. استيراد CSV")
    print("4. تقرير أداء أسبوعي")
    print("5. مقارنة بين فترتين")
    print("6. فحص التنبيهات المبكرة")
    print("7. سجل تطور لاعب")
    print("8. تصدير CSV")
    choice = input("اختر: ").strip()
    if choice == "1": sync_roster()
    elif choice == "2": add_match_data()
    elif choice == "3": import_csv()
    elif choice == "4": generate_weekly_report()
    elif choice == "5": compare_periods()
    elif choice == "6": check_alerts()
    elif choice == "7": show_player_history()
    elif choice == "8": export_csv()
