const fs = require('fs');
const path = require('path');

// ─── 1. PROSPECT DATA ───────────────────────────────────────────────
// Later this comes from n8n/Google Sheets — for now test with one firm

const prospect = {
  FIRM_NAME:      "Johnson & Associates",
  ATTORNEY_NAME:  "Michael Johnson",
  CITY:           "Miami",
  STATE:          "Florida",
  STATE_SHORT:    "FL",
  PHONE:          "(305) 555-0198",
  YEAR:           "2025",
};

// ─── 2. AUTO-GENERATE SLUG ──────────────────────────────────────────
function makeSlug(firmName, city) {
  return `${firmName}-${city}`
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')   // replace spaces/symbols with -
    .replace(/^-|-$/g, '');         // strip leading/trailing -
}

prospect.SLUG = makeSlug(prospect.FIRM_NAME, prospect.CITY);

// ─── 3. READ TEMPLATE ───────────────────────────────────────────────
const templatePath = path.join(__dirname, '..', 'template', 'index.html');
let html = fs.readFileSync(templatePath, 'utf8');

// ─── 4. REPLACE ALL TOKENS ──────────────────────────────────────────
Object.entries(prospect).forEach(([key, value]) => {
  const token = new RegExp(`{{${key}}}`, 'g');
  html = html.replace(token, value);
});

// ─── 5. CHECK FOR MISSED TOKENS ─────────────────────────────────────
const missed = html.match(/{{[A-Z_]+}}/g);
if (missed) {
  console.warn('⚠️  Unreplaced tokens found:', [...new Set(missed)].join(', '));
}

// ─── 6. WRITE OUTPUT ────────────────────────────────────────────────
const outputDir = path.join(__dirname, '..', 'previews', prospect.SLUG);
fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(path.join(outputDir, 'index.html'), html, 'utf8');

console.log(`✅ Generated: previews/${prospect.SLUG}/index.html`);
console.log(`🔗 URL will be: /previews/${prospect.SLUG}/`);
