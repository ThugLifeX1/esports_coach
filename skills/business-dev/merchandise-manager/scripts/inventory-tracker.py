import json
from datetime import datetime

INV_FILE = "inventory.json"

def load_inv():
    try:
        with open(INV_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"منتجات": {}}

def save_inv(data):
    with open(INV_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_product():
    data = load_inv()
    name = input("اسم المنتج: ").strip()
    
    product = {
        "النوع": input("النوع (تيشيرت/هودي/كاب/إكسسوار): ").strip(),
        "سعر_التكلفة": float(input("سعر التكلفة: ").strip() or "0"),
        "سعر_البيع": float(input("سعر البيع: ").strip() or "0"),
        "المخزون": int(input("الكمية الحالية: ").strip() or "0"),
        "الحد_الأدنى": int(input("الحد الأدنى للمخزون: ").strip() or "20"),
        "المبيعات_الشهرية": 0,
        "الحالة": "متوفر",
        "آخر_تحديث": datetime.now().strftime("%Y-%m-%d")
    }
    
    if product["المخزون"] <= 0:
        product["الحالة"] = "نفد"
    elif product["المخزون"] <= product["الحد_الأدنى"]:
        product["الحالة"] = "منخفض"
    
    data["منتجات"][name] = product
    save_inv(data)
    print(f"تم إضافة: {name} | حالة: {product['الحالة']}")

def check_alerts():
    data = load_inv()
    print("\n=== تنبيهات المخزون ===")
    
    alerts = []
    for name, p in data["منتجات"].items():
        if p["المخزون"] <= 0:
            alerts.append(f"  🔴 {name}: نفد!")
        elif p["المخزون"] <= p["الحد_الأدنى"]:
            alerts.append(f"  🟡 {name}: منخفض ({p['المخزون']} قطعة - الحد: {p['الحد_الأدنى']})")
    
    if not alerts:
        print("  لا توجد تنبيهات - المخزون كافٍ")
    else:
        for a in alerts:
            print(a)

def record_sale():
    data = load_inv()
    name = input("اسم المنتج: ").strip()
    qty = int(input("الكمية المباعة: ").strip() or "1")
    
    if name in data["منتجات"]:
        data["منتجات"][name]["المخزون"] -= qty
        data["منتجات"][name]["المبيعات_الشهرية"] += qty
        
        stock = data["منتجات"][name]["المخزون"]
        min_stock = data["منتجات"][name]["الحد_الأدنى"]
        
        if stock <= 0:
            data["منتجات"][name]["الحالة"] = "نفد"
        elif stock <= min_stock:
            data["منتجات"][name]["الحالة"] = "منخفض"
        
        data["منتجات"][name]["آخر_تحديث"] = datetime.now().strftime("%Y-%m-%d")
        save_inv(data)
        print(f"تم تسجيل البيع: {name} x{qty} | المتبقي: {stock}")

if __name__ == "__main__":
    print("1. إضافة منتج\n2. تنبيهات المخزون\n3. تسجيل بيع")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_product()
    elif choice == "2":
        check_alerts()
    elif choice == "3":
        record_sale()
