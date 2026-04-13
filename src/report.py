from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

# severity colour map
SEV_COLORS = {
    "critical": colors.HexColor("#E24B4A"),
    "major":    colors.HexColor("#EF9F27"),
    "minor":    colors.HexColor("#1D9E75"),
    "info":     colors.HexColor("#378ADD"),
}

SEV_BG = {
    "critical": colors.HexColor("#FCEBEB"),
    "major":    colors.HexColor("#FAEEDA"),
    "minor":    colors.HexColor("#E1F5EE"),
    "info":     colors.HexColor("#E6F1FB"),
}


def generate_pdf(filename: str, summary: str, issues: list[dict], file_id: str) -> str:
    """Generate a PDF validation report and return its file path."""

    os.makedirs("reports", exist_ok=True)
    output_path = f"reports/validation_{file_id}.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ── Header ──────────────────────────────────────────────
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#0C447C"),
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    sub_style = ParagraphStyle(
        "Sub",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#5F5E5A"),
        alignment=TA_CENTER,
        spaceAfter=2,
    )

    elements.append(Paragraph("DesignSense AI — Validation Report", title_style))
    elements.append(Paragraph(f"Part: {filename}", sub_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}", sub_style))
    elements.append(Spacer(1, 8*mm))

    # ── Summary counts ───────────────────────────────────────
    critical = sum(1 for i in issues if i["severity"] == "critical")
    major    = sum(1 for i in issues if i["severity"] == "major")
    minor    = sum(1 for i in issues if i["severity"] == "minor")

    count_data = [
        ["Total Issues", "Critical", "Major", "Minor"],
        [str(len(issues)), str(critical), str(major), str(minor)],
    ]
    count_table = Table(count_data, colWidths=[40*mm]*4)
    count_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#0C447C")),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 11),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("BACKGROUND",  (1,1), (1,1),  colors.HexColor("#FCEBEB")),
        ("BACKGROUND",  (2,1), (2,1),  colors.HexColor("#FAEEDA")),
        ("BACKGROUND",  (3,1), (3,1),  colors.HexColor("#E1F5EE")),
        ("TEXTCOLOR",   (1,1), (1,1),  colors.HexColor("#A32D2D")),
        ("TEXTCOLOR",   (2,1), (2,1),  colors.HexColor("#633806")),
        ("TEXTCOLOR",   (3,1), (3,1),  colors.HexColor("#085041")),
        ("FONTNAME",    (0,1), (-1,1), "Helvetica-Bold"),
        ("FONTSIZE",    (0,1), (-1,1), 16),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [None, None]),
        ("BOX",         (0,0), (-1,-1), 0.5, colors.HexColor("#D3D1C7")),
        ("INNERGRID",   (0,0), (-1,-1), 0.5, colors.HexColor("#D3D1C7")),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    elements.append(count_table)
    elements.append(Spacer(1, 6*mm))

    # ── Executive summary ────────────────────────────────────
    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#2C2C2A"),
    )
    elements.append(Paragraph(summary, body_style))
    elements.append(Spacer(1, 6*mm))

    # ── Issues table ─────────────────────────────────────────
    elements.append(Paragraph("Detailed Issue Log", styles["Heading2"]))
    elements.append(Spacer(1, 2*mm))

    table_header = ["#", "Severity", "Rule", "Description", "AI Suggestion"]
    table_data   = [table_header]

    for i, issue in enumerate(issues, 1):
        sev  = issue.get("severity", "info")
        desc = issue.get("description", "")
        ai   = issue.get("ai_suggestion", issue.get("fix", ""))

        # wrap long text in Paragraph for auto line-break
        desc_para = Paragraph(desc, ParagraphStyle("td", fontSize=8, leading=11))
        ai_para   = Paragraph(ai,   ParagraphStyle("td", fontSize=8, leading=11))
        sev_para  = Paragraph(
            f"<font color='{SEV_COLORS.get(sev, colors.black).hexval()}'><b>{sev.upper()}</b></font>",
            ParagraphStyle("sev", fontSize=8, alignment=TA_CENTER)
        )

        table_data.append([
            str(i),
            sev_para,
            issue.get("rule_id", ""),
            desc_para,
            ai_para,
        ])

    col_widths = [8*mm, 22*mm, 22*mm, 60*mm, 60*mm]
    issue_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    row_styles = [
        ("BACKGROUND",   (0,0), (-1,0),  colors.HexColor("#185FA5")),
        ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0),  9),
        ("ALIGN",        (0,0), (-1,0),  "CENTER"),
        ("BOX",          (0,0), (-1,-1), 0.5, colors.HexColor("#D3D1C7")),
        ("INNERGRID",    (0,0), (-1,-1), 0.5, colors.HexColor("#D3D1C7")),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("FONTSIZE",     (0,1), (-1,-1), 8),
    ]

    # alternating row background + severity tint on col 1
    for row_idx, issue in enumerate(issues, 1):
        sev = issue.get("severity", "info")
        bg  = colors.HexColor("#F1EFE8") if row_idx % 2 == 0 else colors.white
        row_styles.append(("BACKGROUND", (0, row_idx), (-1, row_idx), bg))
        row_styles.append(("BACKGROUND", (1, row_idx), (1,  row_idx), SEV_BG.get(sev, colors.white)))

    issue_table.setStyle(TableStyle(row_styles))
    elements.append(issue_table)

    # ── Footer note ──────────────────────────────────────────
    elements.append(Spacer(1, 8*mm))
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#888780"),
        alignment=TA_CENTER,
    )
    elements.append(Paragraph(
        "Generated by DesignSense AI — Varroc Eureka Challenge 2025 | For internal design review use only",
        footer_style
    ))

    doc.build(elements)
    return output_path