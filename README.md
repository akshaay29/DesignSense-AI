<div align="center">

<!-- Banner -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:00C853,100:1B5E20&height=200&section=header&text=DesignSense%20AI&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=AI-Powered%20CAD%20Validation%20Platform&descAlignY=58&descSize=20&descColor=A5D6A7"/>

<br/>

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![Gemini](https://img.shields.io/badge/Gemini_2.0_Flash-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

**Catch design flaws before they cost you.**

*Built for Varroc Eureka Challenge 3.0 — Problem Statement 9*

<br/>

[🚀 Live Demo](#demo) · [📖 Documentation](#how-it-works) · [⚡ Quick Start](#quick-start) · [🤝 Contributing](#contributing)

<br/>

</div>

---

## 🎯 What is DesignSense AI?

DesignSense AI is a web-based platform that **automatically validates CAD designs** against DFM (Design for Manufacturability) rules the moment you upload a STEP file. Instead of just flagging error codes like traditional tools, it uses **Google Gemini AI** to generate plain-English fix suggestions — making expert-level design review accessible to every engineer on your team.

```
Upload STEP file  →  Geometry analysis  →  Rule checking  →  AI suggestions  →  PDF report
      (2s)               (3s)                  (1s)              (4s)              (2s)
```

> **Before DesignSense AI:** Junior engineer spends 2 days manually checking a bracket against 40-page DFM guidelines, misses 3 critical issues that cause ₹2,00,000 in rework at tooling stage.
>
> **After DesignSense AI:** Upload STEP → 12 seconds → 9 issues found, each with an AI-written fix → PDF report attached to BOM.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Geometry parsing** | Extracts face-level data — wall thickness, draft angles, hole diameters, face areas |
| 📏 **DFM rule engine** | 4 configurable rule categories with editable thresholds |
| 🤖 **AI fix suggestions** | Gemini 2.0 Flash generates expert-level, 2-sentence fix recommendations per issue |
| 📊 **Severity classification** | Critical / Major / Minor / Info with colour-coded badges |
| 📄 **PDF report generation** | Professional validation report with issue table, AI summary, and severity counts |
| ⚡ **Real-time dashboard** | Live issue count, executive summary, expandable issue cards |
| 🔧 **REST API** | FastAPI backend with `/validate` and `/report` endpoints |

---

## 🖥️ Demo

<div align="center">

### Upload → Validate → Report

```
┌─────────────────────────────────────────────────────────┐
│  CAD Validator          AI-Powered STEP File Analysis   │
├─────────────────┬───────────────────────────────────────┤
│                 │  Design Issues                        │
│  ┌───────────┐  │  ┌─ 8 Critical ──┐ ┌─ 3 Major ──┐   │
│  │  Drop     │  │  │               │ │            │   │
│  │  STEP     │  │  │ Wall thickness│ │Draft angle │   │
│  │  file     │  │  │ too thin      │ │insufficient│   │
│  │  here     │  │  └───────────────┘ └────────────┘   │
│  └───────────┘  │                                       │
│                 │  AI Executive Summary                  │
│  [Download PDF] │  "Validation complete. Found 8        │
│                 │   critical issues requiring immediate  │
│                 │   attention before manufacturing..."   │
└─────────────────┴───────────────────────────────────────┘
```

</div>

---

## 🏗️ Architecture

```
DesignSense AI
│
├── 🌐 Frontend (Next.js 16 + Tailwind CSS)
│   ├── app/page.tsx          — Main dashboard
│   ├── components/
│   │   ├── file-uploader.tsx — Drag-and-drop STEP upload
│   │   ├── issues-sidebar.tsx — Issue cards with severity badges
│   │   └── header.tsx        — Navigation
│   └── .env.local            — NEXT_PUBLIC_API_URL
│
├── ⚙️ Backend (Python + FastAPI)
│   ├── main.py               — FastAPI server + CORS
│   └── src/
│       ├── parser.py         — STEP geometry extraction (pythonocc)
│       ├── rules.py          — DFM rule engine
│       ├── ai_engine.py      — Gemini API integration
│       └── report.py         — PDF generation (ReportLab)
│
└── 📁 Config
    ├── .env                  — GEMINI_API_KEY
    └── uploads/              — Temporary file storage
```

---

## 🔬 DFM Rules

| Rule ID | Name | Default Threshold | Severity |
|---|---|---|---|
| `DFM-001` | Wall thickness too thin | < 2.0 mm | 🔴 Critical |
| `DFM-002` | Insufficient draft angle | < 1.5° | 🟡 Major |
| `DFM-003` | Hole diameter too small | < 2.5 mm | 🟡 Major |
| `DFM-004` | Face area too small | < 40 mm² | 🟢 Minor |

All thresholds are editable in `src/rules.py`. New rules can be added by extending the `RULES` dict.

---

## ⚡ Quick Start

### Prerequisites

- Python 3.11+ (via conda recommended)
- Node.js 18+
- Google Gemini API key — [get one free here](https://aistudio.google.com/app/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/designsense-ai.git
cd designsense-ai
```

### 2. Set up the backend

```bash
# Create conda environment (recommended for pythonocc)
conda create -n designsense python=3.11 -y
conda activate designsense

# Install dependencies
pip install fastapi uvicorn reportlab google-genai python-multipart python-dotenv

# Add your Gemini API key
echo "GEMINI_API_KEY=your-key-here" > .env
```

### 3. Set up the frontend

```bash
cd frontend
npm install --legacy-peer-deps

# Set backend URL
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local
```

### 4. Run both servers

**Terminal 1 — Backend:**
```bash
# From project root
conda activate designsense
uvicorn main:app --reload
# → Running at http://127.0.0.1:8000
# → Docs at http://127.0.0.1:8000/docs
```

**Terminal 2 — Frontend:**
```bash
# From /frontend
npm run dev
# → Running at http://localhost:3000
```

### 5. Test it

Open `http://localhost:3000`, drag in any `.step` or `.stp` file, and watch the validation run.

---

## 📡 API Reference

### `POST /validate`

Upload a STEP file and receive structured validation results.

**Request:**
```bash
curl -X POST http://localhost:8000/validate \
  -F "file=@your_part.step"
```

**Response:**
```json
{
  "filename": "bracket.step",
  "face_count": 15,
  "issue_count": 9,
  "summary": "Validation complete for 'bracket.step'. Found 3 critical, 6 major issues...",
  "issues": [
    {
      "issue_id": "DFM-001-F2",
      "rule_id": "DFM-001",
      "title": "Wall thickness too thin",
      "face_index": 2,
      "severity": "critical",
      "description": "Wall thickness 1.2mm is below minimum 2.0mm for injection moulding.",
      "fix": "Increase wall thickness to at least 2.0mm or add structural ribs.",
      "ai_suggestion": "Increase wall thickness at Face #2 to a minimum of 2.5mm to ensure structural integrity during injection moulding. Consider adding ribbing perpendicular to the load direction to distribute stress without adding excessive material weight."
    }
  ]
}
```

### `POST /report`

Upload a STEP file and receive a downloadable PDF validation report.

```bash
curl -X POST http://localhost:8000/report \
  -F "file=@your_part.step" \
  --output validation_report.pdf
```

### `GET /health`

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

---

## 🧠 How It Works

### 1. Geometry extraction
The uploaded STEP file is parsed using **pythonocc-core** (Python bindings for OpenCASCADE). Each face is extracted with its bounding box dimensions, surface area, and geometric type (planar/curved).

### 2. Rule checking
The rule engine iterates over all faces and checks each against configurable thresholds. Each violation becomes an `Issue` object with a severity level, affected face index, and rule reference.

### 3. AI enrichment
The `IssueSet` is sent to **Gemini 2.0 Flash** with a system prompt instructing it to respond as a senior Varroc DFM engineer. Gemini returns structured JSON with a 2-sentence `ai_suggestion` for each issue.

### 4. Report generation
**ReportLab** renders a professional PDF with a colour-coded summary table, AI executive summary, and per-issue details. The report is streamed back as a file download.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, Tailwind CSS, TypeScript, Lucide icons |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Geometry | pythonocc-core (OpenCASCADE kernel) |
| AI | Google Gemini 2.0 Flash API |
| PDF | ReportLab |
| Deployment | Railway.app (backend), Vercel (frontend) |

---

## 📁 Project Structure

```
designsense-ai/
├── main.py                 # FastAPI application entry point
├── .env                    # Backend environment variables
├── src/
│   ├── __init__.py
│   ├── parser.py           # STEP file geometry extraction
│   ├── rules.py            # DFM rule definitions and checker
│   ├── ai_engine.py        # Gemini API integration
│   └── report.py           # PDF report generator
├── uploads/                # Temporary uploaded files
├── reports/                # Generated PDF reports
└── frontend/
    ├── app/
    │   ├── page.tsx         # Main dashboard page
    │   ├── layout.tsx       # Root layout
    │   └── globals.css      # Global styles
    ├── components/
    │   ├── header.tsx
    │   ├── file-uploader.tsx
    │   └── issues-sidebar.tsx
    ├── .env.local           # Frontend environment variables
    └── package.json
```

---

## 🔧 Configuration

### Adding a new DFM rule

Open `src/rules.py` and add to the `RULES` dict:

```python
"min_fillet_radius": {
    "id":       "DFM-005",
    "title":    "Fillet radius too small",
    "min_mm":   0.5,
    "severity": "major",
    "message":  "Fillet radius {val}mm is below recommended {min}mm.",
    "fix":      "Increase fillet radius to at least 0.5mm to reduce stress concentration.",
},
```

Then add the check in `check_rules()`. The AI engine and report generator pick it up automatically.

### Changing AI behaviour

Edit the `SYSTEM_PROMPT` in `src/ai_engine.py` to change the engineering persona, response style, or output format.

---

## 🗺️ Roadmap

- [x] STEP file upload and geometry extraction
- [x] 4-rule DFM engine
- [x] Gemini AI fix suggestions
- [x] PDF report generation
- [x] React dashboard with severity badges
- [ ] Real pythonocc ray-cast wall thickness (replace bounding box approximation)
- [ ] CATIA V5 plugin via CAA API
- [ ] PLM integration (Teamcenter REST API)
- [ ] ML geometry classifier trained on historical NCR data
- [ ] Support for IGES, JT, and Parasolid formats
- [ ] Multi-user teams with shared rule libraries

---

## 🤝 Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
# Open a Pull Request
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [pythonocc-core](https://github.com/tpaviot/pythonocc-core) — Python bindings for OpenCASCADE
- [Google Gemini API](https://ai.google.dev) — AI-powered fix suggestions
- [FastAPI](https://fastapi.tiangolo.com) — Async Python web framework
- [ReportLab](https://www.reportlab.com) — PDF generation
- **Varroc Engineering** — for Problem Statement 9, Eureka Challenge 3.0

---

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:1B5E20,100:00C853&height=100&section=footer"/>


*If this helped you, please ⭐ the repo*

</div>
