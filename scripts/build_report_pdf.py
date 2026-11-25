"""Render the study's Markdown report with ReportLab (optional dependency)."""
from __future__ import annotations

import argparse
import re
from html import escape
from pathlib import Path
from posixpath import normpath

ROOT = Path(__file__).resolve().parents[1]


def inline(text):
    text = escape(text)
    def link(match):
        label, target = match.groups()
        if not target.startswith("https://"):
            location, separator, anchor = target.partition("#")
            target = "https://github.com/sanketnichit/cti-evidence-lab/blob/main/" + normpath("research/" + location)
            target += separator + anchor
        return f'<link href="{target}" color="#156276">{label}</link>'
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    return text.replace("×", " x ").replace("—", " - ").replace("–", "-").replace("→", "-&gt;")


def build(destination):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, KeepTogether
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("ReportBody", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=8, allowWidows=0, allowOrphans=0))
    styles.add(ParagraphStyle("ReportTitle", fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=colors.HexColor("#153746"), spaceAfter=15))
    styles.add(ParagraphStyle("ReportHeading", fontName="Helvetica-Bold", fontSize=14, leading=19, spaceBefore=15, spaceAfter=9, keepWithNext=True))
    styles.add(ParagraphStyle("Cell", fontName="Helvetica", fontSize=8.4, leading=12, alignment=TA_LEFT))
    styles.add(ParagraphStyle("CodeBlock", fontName="Courier", fontSize=7, leading=10, spaceAfter=10))
    lines = (ROOT / "research/FEASIBILITY_REPORT_v0.1.md").read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("![") and "sequence_counterexample.svg" in line:
            if __package__:
                from .build_query_figure import drawing
            else:
                from build_query_figure import drawing
            figure = [drawing(), Spacer(1, 12)]
            if len(story) >= 2 and isinstance(story[-2], Paragraph) and story[-2].style.name == "ReportHeading":
                figure = story[-2:] + figure
                del story[-2:]
            story.append(KeepTogether(figure))
        elif line.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            story.append(Preformatted("\n".join(code), styles["CodeBlock"], maxLineLength=100))
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", c) for c in cells):
                    rows.append([Paragraph(inline(c), styles["Cell"]) for c in cells])
                i += 1
            widths = [100, 180, 215] if len(rows[0]) == 3 else [495 / len(rows[0])] * len(rows[0])
            if len(rows[0]) == 2 and rows[0][0].getPlainText() == "Source group":
                widths = [165, 330]
            if len(rows[0]) == 3 and rows[0][0].getPlainText() == "Representation":
                widths = [235, 130, 130]
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e4eef1")),
                                      ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                      ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.HexColor("#156276")),
                                      ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#d6dde0")),
                                      ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                      ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                      ("TOPPADDING", (0, 0), (-1, -1), 5),
                                      ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
            if len(rows) <= 8:
                group = [table]
                if story and isinstance(story[-1], Paragraph) and story[-1].style.name == "ReportHeading":
                    group.insert(0, story.pop())
                story.append(KeepTogether(group))
            else:
                story.append(table)
            story.append(Spacer(1, 12))
            continue
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["ReportTitle"]))
        elif line.startswith(("## ", "### ")):
            story.append(Paragraph(inline(line.lstrip("# ")), styles["ReportHeading"]))
        else:
            story.append(Paragraph(inline(line), styles["ReportBody"]))
        i += 1
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#d6dde0"))
        canvas.line(50, 43, A4[0] - 50, 43)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#50616b"))
        canvas.drawString(50, 30, "CTI Evidence Lab | Research manuscript draft | November 2026")
        canvas.drawRightString(A4[0] - 50, 30, str(doc.page))
        canvas.restoreState()
    doc = SimpleDocTemplate(str(destination), pagesize=A4, rightMargin=50, leftMargin=50,
                            topMargin=47, bottomMargin=58, title="When technique graphs lose incident sequence evidence",
                            author="Sanket Nichit")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/submission/CTI_Evidence_Lab_Report.pdf")
    print("Report written:", build(parser.parse_args().output).name)
