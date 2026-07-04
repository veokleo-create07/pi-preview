# PI Preview

Template and generated preview sites for personal injury law firm outreach.

## Correct raw template URL

The repo name is **`pi-preview`** (not `pi-previews`):

- https://raw.githubusercontent.com/veokleo-create07/pi-preview/main/template/index.html
- https://raw.githubusercontent.com/veokleo-create07/pi-preview/main/template.html

## Generate previews

### Node (single test prospect)

```bash
node scripts/generate.js
```

### Python (batch from CSV)

Place a `leads.csv` in the repo root, then:

```bash
python3 scripts/generate.py
```

CSV columns expected (Google Sheets / n8n export):

| Column | Maps to |
|--------|---------|
| Full name | Firm name |
| First Name | City |
| Last Name | State |
| Title | Phone |
| Company | Year (optional) |

Output is written to `previews/<slug>/index.html` and served at:

`https://pi-preview-coral.vercel.app/previews/<slug>/`
