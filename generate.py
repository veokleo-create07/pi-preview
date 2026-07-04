#!/usr/bin/env python3
import csv
import re
from pathlib import Path
from datetime import datetime
import secrets

TEMPLATE_PATH = Path("template.html")
OUTPUT_DIR = Path("dist")
CSV_PATH = Path("leads.csv")
BASE_URL = "https://pi-preview-coral.vercel.app"

def slugify(s):
    s = str(s).lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'\s+', '-', s).strip('-')
    return s[:40]

def main():
    if not TEMPLATE_PATH.exists():
        print(f"ERROR: {TEMPLATE_PATH} not found")
        return

    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found")
        return

    template = TEMPLATE_PATH.read_text()
    preview_dir = OUTPUT_DIR / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    year = str(datetime.now().year)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            firm = row.get("Full name", "").strip()
            city = row.get("First Name", "").strip()
            state = row.get("Last Name", "").strip()
            phone = row.get("Title", "").strip()
            company = row.get("Company", "").strip()

            if not firm or not city:
                print(f"SKIP: missing firm or city in row {row}")
                continue

            unique_id = secrets.token_hex(4)
            slug = f"{slugify(firm)}-{slugify(city)}-{unique_id}"
            target_dir = preview_dir / slug

            if target_dir.exists():
                print(f"SKIP: already exists {slug}")
                continue

            target_dir.mkdir(parents=True, exist_ok=True)

            html = (template
                    .replace("{{FIRM_NAME}}", firm)
                    .replace("{{CITY}}", city)
                    .replace("{{STATE}}", state)
                    .replace("{{PHONE}}", phone)
                    .replace("{{YEAR}}", company or year))

            (target_dir / "index.html").write_text(html, encoding="utf-8")

            url = f"{BASE_URL}/preview/{slug}/"
            generated.append({"firm": firm, "city": city, "url": url})
            print(f"  ✓ {firm} ({city}) -> {url}")

    print(f"\nDone. Generated {len(generated)} new sites. Old sites unchanged.")

if __name__ == "__main__":
    main()
