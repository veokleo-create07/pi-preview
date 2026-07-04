#!/usr/bin/env python3
import csv
import re
import secrets
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "template" / "index.html"
OUTPUT_DIR = ROOT / "previews"
CSV_PATH = ROOT / "leads.csv"
BASE_URL = "https://pi-preview-coral.vercel.app"

STATE_ABBREV = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
}


def slugify(value: str) -> str:
    value = str(value).lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"\s+", "-", value).strip("-")
    return value[:40]


def state_short(state: str) -> str:
    state = state.strip()
    if len(state) == 2 and state.isalpha():
        return state.upper()
    return STATE_ABBREV.get(state.lower(), state[:2].upper())


def attorney_name(firm: str) -> str:
    firm = firm.strip()
    if "&" in firm:
        return firm.split("&", 1)[0].strip()
    return firm


def replace_tokens(template: str, tokens: dict[str, str]) -> str:
    html = template
    for key, value in tokens.items():
        html = html.replace(f"{{{{{key}}}}}", value)
    return html


def main() -> None:
    if not TEMPLATE_PATH.exists():
        print(f"ERROR: {TEMPLATE_PATH} not found")
        return

    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found")
        return

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    year = str(datetime.now().year)

    with CSV_PATH.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
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
            target_dir = OUTPUT_DIR / slug

            if target_dir.exists():
                print(f"SKIP: already exists {slug}")
                continue

            target_dir.mkdir(parents=True, exist_ok=True)

            tokens = {
                "FIRM_NAME": firm,
                "ATTORNEY_NAME": attorney_name(firm),
                "CITY": city,
                "STATE": state,
                "STATE_SHORT": state_short(state),
                "PHONE": phone,
                "YEAR": company or year,
                "SLUG": slug,
            }

            html = replace_tokens(template, tokens)
            (target_dir / "index.html").write_text(html, encoding="utf-8")

            url = f"{BASE_URL}/previews/{slug}/"
            generated.append({"firm": firm, "city": city, "state": state, "slug": slug, "url": url})
            print(f"  ✓ {firm} ({city}) -> {url}")

    print(f"\nDone. Generated {len(generated)} new sites.")
    print(f"Existing previews in {OUTPUT_DIR} are unchanged.")


if __name__ == "__main__":
    main()
