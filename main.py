import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

# ============================================================
# 1. РОБОТА З ФАЙЛОМ ДАНИХ
# ============================================================

DATA_FILE = "sleep_data.json"

def load_data() -> List[Dict]:
    """Завантажує дані з JSON-файлу. Якщо файлу немає - створює порожній список."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(data: List[Dict]) -> None:
    """Зберігає дані у JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# 2. ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ ПЕРЕВІРКИ ВВОДУ
# ============================================================

def validate_time(time_str: str) -> bool:
    """Перевіряє, чи є рядок коректним часом у форматі HH:MM."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def validate_date(date_str: str) -> bool:
    """Перевіряє, чи є рядок коректною датою у форматі YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def calculate_duration(sleep_time: str, wake_time: str) -> float:
    """Розраховує тривалість сну в годинах, враховуючи перехід через опівніч."""
    sleep_dt = datetime.strptime(sleep_time, "%H:%M")
    wake_dt = datetime.strptime(wake_time, "%H:%M")
    
    # Якщо час пробудження раніше або дорівнює часу засинання - додаємо 24 години
    if wake_dt <= sleep_dt:
        wake_dt += timedelta(hours=24)
    
    delta = wake_dt - sleep_dt
    return round(delta.total_seconds() / 3600, 2)

def get_date_from_user(prompt: str) -> str:
    """Запитує дату у користувача, поки не буде введено коректну."""
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
            print(f"Використано сьогоднішню дату: {date_str}")
            return date_str
        if validate_date(date_str):
            # Перевірка, що дата не в майбутньому
            if datetime.strptime(date_str, "%Y-%m-%d") > datetime.now():
                print("❌ Не можна додавати записи з майбутньої дати!")
                continue
            return date_str
        print("❌ Некоректний формат дати! Використовуйте YYYY-MM-DD")

def get_time_from_user(prompt: str) -> str:
    """Запитує час у користувача, поки не буде введено коректний."""
    while True:
        time_str = input(prompt).strip()
        if validate_time(time_str):
            return time_str
        print("❌ Некоректний формат часу! Використовуйте HH:MM (наприклад, 23:30)")

def get_yes_no(prompt: str) -> bool:
    """Запитує так/ні, повертає True/False."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("так", "т", "+", "yes", "y", "1"):
            return True
        if answer in ("ні", "н", "-", "no", "n", "0"):
            return False
        print("❌ Введіть 'так' або 'ні'")

# ============================================================
# 3. ОСНОВНІ ФУНКЦІЇ ПРОГРАМИ (ОБОВ'ЯЗКОВІ)
# ============================================================

def add_sleep_record(data: List[Dict]) -> List[Dict]:
    """Функція 1: Додавання запису сну."""
    print("\n" + "=" * 50)
    print("🛌 ДОДАВАННЯ ЗАПИСУ СНУ")
    print("=" * 50)
    
    date = get_date_from_user("📅 Введіть дату (YYYY-MM-DD) або Enter для сьогодні: ")
    
    # Перевірка, чи вже є запис на цю дату
    for record in data:
        if record["date"] == date:
            print(f"⚠️ Запис на {date} вже існує!")
            if not get_yes_no("Бажаєте перезаписати його? (так/ні): "):
                return data
            data = [r for r in data if r["date"] != date]
            break
 print("\n⏰ Введіть час засинання та пробудження:")
    sleep_time = get_time_from_user("   Час засинання (HH:MM): ")
    wake_time = get_time_from_user("   Час пробудження (HH:MM): ")
    
    duration = calculate_duration(sleep_time, wake_time)
    
    record = {
        "date": date,
        "sleep_time": sleep_time,
        "wake_time": wake_time,
        "duration_hours": duration
    }
    
    data.append(record)
    save_data(data)
    
    print(f"\n✅ Запис додано! Тривалість сну: {duration:.2f} годин")
    return data

def view_all_records(data: List[Dict]) -> None:
    """Функція 2: Перегляд усіх записів."""
    print("\n" + "=" * 50)
    print("📊 УСІ ЗАПИСИ СНУ")
    print("=" * 50)
    
    if not data:
        print("ℹ️ Немає жодного запису.")
        return
    
    sorted_data = sorted(data, key=lambda x: x["date"])
    
    total_sleep = 0
    for i, record in enumerate(sorted_data, 1):
        print(f"{i}. 📅 {record['date']}")
        print(f"   🛌 Заснув: {record['sleep_time']} → Прокинувся: {record['wake_time']}")
        print(f"   ⏱️ Тривалість: {record['duration_hours']:.2f} год")
        print()
        total_sleep += record['duration_hours']
    
    print(f"📈 Загалом: {len(data)} записів")
    print(f"⏱️ Загальна тривалість сну: {total_sleep:.2f} год")
    if data:
        print(f"📊 Середня тривалість: {total_sleep / len(data):.2f} год")

def average_sleep_last_week(data: List[Dict]) -> None:
    """Функція 3: Середня тривалість сну за останні 7 днів."""
    print("\n" + "=" * 50)
    print("📈 СЕРЕДНЯ ТРИВАЛІСТЬ СНУ ЗА ТИЖДЕНЬ")
    print("=" * 50)
    
    if not data:
        print("ℹ️ Немає даних для аналізу.")
        return
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    week_records = []
    for record in data:
        record_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
        if week_ago <= record_date <= today:
            week_records.append(record)
    
    if not week_records:
        print(f"ℹ️ Немає записів за останні 7 днів (з {week_ago} по {today})")
        return
    
    total = sum(r["duration_hours"] for r in week_records)
    avg = total / len(week_records)
    
    print(f"📊 За останні 7 днів: {len(week_records)} записів")
    print(f"⏱️ Загальна тривалість: {total:.2f} год")
    print(f"📈 Середня тривалість: {avg:.2f} год")
    
    print("\nДеталі за днями:")
    for r in sorted(week_records, key=lambda x: x["date"]):
        print(f"   {r['date']}: {r['duration_hours']:.2f} год")

def shortest_night(data: List[Dict]) -> None:
    """Функція 4: Найкоротша ніч за тиждень."""
    print("\n" + "=" * 50)
    print("🌙 НАЙКОРОТША НІЧ ЗА ТИЖДЕНЬ")
    print("=" * 50)
    
    if not data:
        print("ℹ️ Немає даних для аналізу.")
        return
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    week_records = []
    for record in data:
        record_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
        if week_ago <= record_date <= today:
            week_records.append(record)
    
    if not week_records:
        print(f"ℹ️ Немає записів за останні 7 днів (з {week_ago} по {today})")
        return
    
    shortest = min(week_records, key=lambda x: x["duration_hours"])
    
    print(f"🌙 Найкоротша ніч: {shortest['date']}")
    print(f"   🛌 Заснув: {shortest['sleep_time']} → Прокинувся: {shortest['wake_time']}")
    print(f"   ⏱️ Тривалість: {shortest['duration_hours']:.2f} год")
    
    same_duration = [r for r in week_records if r["duration_hours"] == shortest["duration_hours"]]
    if len(same_duration) > 1:
        print(f"\nℹ️ Ще {len(same_duration)-1} запис(ів) з такою ж тривалістю:")
        for r in same_duration:
            if r["date"] != shortest["date"]:
                print(f"   - {r['date']}: {r['duration_hours']:.2f} год")

# ============================================================
# 4. ДОДАТКОВІ ФУНКЦІЇ (ДЛЯ ЗРУЧНОСТІ, НЕ ОБОВ'ЯЗКОВІ)
# ============================================================
[16.06.2026 19:57] Сашуня): def edit_record(data: List[Dict]) -> List[Dict]:
    """Додаткова функція: редагування запису за датою."""
    print("\n" + "=" * 50)
    print("✏️ РЕДАГУВАННЯ ЗАПИСУ")
    print("=" * 50)
    
    if not data:
        print("ℹ️ Немає записів для редагування.")
        return data
    
    view_all_records(data)
    
    date = input("\n📅 Введіть дату запису для редагування (YYYY-MM-DD): ").strip()
    
    if not validate_date(date):
        print("❌ Некоректний формат дати!")
        return data
    
    found_index = -1
    for i, record in enumerate(data):
        if record["date"] == date:
            found_index = i
            break
    
    if found_index == -1:
        print(f"❌ Запис на {date} не знайдено.")
        return data
    
    print(f"\nПоточний запис: {data[found_index]['sleep_time']} → {data[found_index]['wake_time']} ({data[found_index]['duration_hours']:.2f} год)")
    
    if get_yes_no("Редагувати час засинання? (так/ні): "):
        data[found_index]["sleep_time"] = get_time_from_user("   Новий час засинання (HH:MM): ")
    
    if get_yes_no("Редагувати час пробудження? (так/ні): "):
        data[found_index]["wake_time"] = get_time_from_user("   Новий час пробудження (HH:MM): ")
    
    data[found_index]["duration_hours"] = calculate_duration(
        data[found_index]["sleep_time"],
        data[found_index]["wake_time"]
    )
    
    save_data(data)
    print(f"\n✅ Запис на {date} оновлено!")
    print(f"   Нова тривалість: {data[found_index]['duration_hours']:.2f} год")
    
    return data

def delete_record(data: List[Dict]) -> List[Dict]:
    """Додаткова функція: видалення запису за датою."""
    print("\n" + "=" * 50)
    print("🗑️ ВИДАЛЕННЯ ЗАПИСУ")
    print("=" * 50)
    
    if not data:
        print("ℹ️ Немає записів для видалення.")
        return data
    
    view_all_records(data)
    
    date = input("\n📅 Введіть дату запису для видалення (YYYY-MM-DD): ").strip()
    
    if not validate_date(date):
        print("❌ Некоректний формат дати!")
        return data
    
    found = None
    for record in data:
        if record["date"] == date:
            found = record
            break
    
    if not found:
        print(f"❌ Запис на {date} не знайдено.")
        return data
    
    print(f"\nЗапис на {date}: {found['duration_hours']:.2f} год")
    if get_yes_no("Ви впевнені, що хочете видалити? (так/ні): "):
        data = [r for r in data if r["date"] != date]
        save_data(data)
        print(f"✅ Запис на {date} видалено.")
    else:
        print("❌ Видалення скасовано.")
    
    return data

# ============================================================
# 5. ГОЛОВНЕ МЕНЮ
# ============================================================

def show_menu():
    """Показує головне меню програми."""
    print("\n" + "=" * 50)
    print("🌙 ЩОДЕННИК СНУ")
    print("=" * 50)
    print("1️⃣  Додати запис сну")
    print("2️⃣  Переглянути всі записи")
    print("3️⃣  Середня тривалість за тиждень")
    print("4️⃣  Найкоротша ніч за тиждень")
    print("5️⃣  ✏️  Редагувати запис (додатково)")
    print("6️⃣  🗑️  Видалити запис (додатково)")
    print("0️⃣  Вихід")
    print("=" * 50)

def main():
    """Головна функція програми."""
    print("🌙 ЩОДЕННИК СНУ v1.0")
    print("Варіант №24 — Навчальна практика")
    print("=" * 50)
    
    data = load_data()
    print(f"📊 Завантажено {len(data)} запис(ів)")
    
    while True:
        show_menu()
        choice = input("👉 Виберіть опцію: ").strip()
        
        if choice == "1":
            data = add_sleep_record(data)
        elif choice == "2":
            view_all_records(data)
        elif choice == "3":
            average_sleep_last_week(data)
        elif choice == "4":
            shortest_night(data)
        elif choice == "5":
            data = edit_record(data)
        elif choice == "6":
            data = delete_record(data)
        elif choice == "0":
            print("\n👋 До побачення! Гарного сну! 🌙")
            break
        else:
            print("❌ Некоректний вибір.
[16.06.2026 19:57] Сашуня): Введіть число від 0 до 6.")
        
        input("\nНатисніть Enter, щоб продовжити...")

if name == "__main__":
    main()
