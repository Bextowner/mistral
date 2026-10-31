#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt Home-Lab_Roadmap_Gesamt.pdf aus Home-Lab_Roadmap_Befehle.md (Markdown -> PDF)."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, Preformatted, KeepTogether, HRFlowable)
import html as html_mod

ACCENT = colors.HexColor("#1a5270")
ACCENT2 = colors.HexColor("#2980b9")
LIGHT = colors.HexColor("#eaf2f8")
GREEN = colors.HexColor("#1e8449")
CODE_BG = colors.HexColor("#f4f6f7")
GREY = colors.HexColor("#5d6d7e")

styles = getSampleStyleSheet()
h1s = ParagraphStyle('H1s', parent=styles['Heading1'], fontSize=18, textColor=ACCENT, spaceAfter=10, spaceBefore=0)
h2s = ParagraphStyle('H2s', parent=styles['Heading2'], fontSize=14, textColor=ACCENT, spaceBefore=14, spaceAfter=6)
h3s = ParagraphStyle('H3s', parent=styles['Heading3'], fontSize=11.5, textColor=ACCENT2, spaceBefore=10, spaceAfter=4)
bodys = ParagraphStyle('Bodys', parent=styles['BodyText'], fontSize=9.5, leading=13.5, alignment=TA_LEFT)
notes = ParagraphStyle('Notes', parent=bodys, textColor=GREY, fontSize=9, leading=12)
quote = ParagraphStyle('Quote', parent=bodys, leftIndent=8, textColor=colors.HexColor("#1a5270"), fontSize=9.5)
code = ParagraphStyle('Code', fontName='Courier', fontSize=7.6, leading=9.6, textColor=colors.HexColor("#1b2631"))
bold = ParagraphStyle('Boldx', parent=bodys)

def md_inline(s):
    s = html_mod.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<font face="Courier" size="8.5">\1</font>', s)
    return s

def render_table(rows, col_hint=0):
    n = len(rows[0])
    if n == 2:
        widths = [55*mm, 115*mm]
    elif n == 3:
        widths = [40*mm, 60*mm, 70*mm]
    elif n == 4:
        widths = [30*mm, 45*mm, 50*mm, 47*mm]
    else:
        widths = [170/n]*n
        widths = [w*mm for w in widths]
    data = []
    for i, r in enumerate(rows):
        row = []
        for c in r:
            c = c.replace('|', '/')
            if i == 0:
                row.append(Paragraph(f"<b>{md_inline(c)}</b>", bodys))
            else:
                row.append(Paragraph(md_inline(c), bodys))
        data.append(row)
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#b0c4d4")),
          ('VALIGN', (0,0), (-1,-1), 'TOP'),
          ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
          ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4)]
    if rows and rows[0] and not rows[0][0].startswith('---'):
        st.append(('BACKGROUND', (0,0), (-1,0), LIGHT))
    t.setStyle(TableStyle(st))
    return t

def render_code(lines):
    text = '\n'.join(l for l in lines)
    pre = Preformatted(text, code)
    t = Table([[pre]], colWidths=[170*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BORDER', (0,0), (-1,-1), 0.5, colors.HexColor("#cfd8dc")),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

def build(md_path, pdf_path):
    with open(md_path, encoding='utf-8') as f:
        lines = f.read().split('\n')

    story = []
    i = 0
    n = len(lines)
    first_h1 = True
    while i < n:
        line = lines[i]

        if line.startswith('```'):
            block = []
            i += 1
            while i < n and not lines[i].startswith('```'):
                block.append(lines[i])
                i += 1
            i += 1
            story.append(render_code(block))
            story.append(Spacer(1, 4))
            continue

        if line.startswith('|') and i+1 < n and set(lines[i+1].replace(' ', '')) <= set('-:|'):
            rows = [[c.strip() for c in line.strip('|').split('|')]]
            i += 2
            while i < n and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip('|').split('|')])
                i += 1
            story.append(render_table(rows))
            story.append(Spacer(1, 6))
            continue

        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m:
            level, text = len(m.group(1)), m.group(2)
            if level == 1:
                if first_h1:
                    story.append(Paragraph(md_inline(text), h1s))
                    story.append(HRFlowable(width='100%', thickness=1, color=ACCENT, spaceAfter=6))
                    first_h1 = False
                else:
                    story.append(Paragraph(md_inline(text), h1s))
            elif level == 2:
                txt = md_inline(text)
                if 'Abschlusstest' in text or 'Abschluss-Prüfung' in text:
                    t = Table([[Paragraph(f"<b>{'✔ ' if '✔' not in text else ''}{md_inline(text)}</b>",
                                ParagraphStyle('tt', parent=bodys, textColor=colors.white))]], colWidths=[170*mm])
                    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), GREEN),
                                           ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                                           ('LEFTPADDING', (0,0), (-1,-1), 8)]))
                    story.append(Spacer(1, 6)); story.append(t)
                else:
                    story.append(Paragraph(txt, h2s))
                    story.append(HRFlowable(width='100%', thickness=0.6, color=ACCENT2, spaceAfter=4))
            else:
                story.append(Paragraph(md_inline(text), h3s))
            i += 1
            continue

        if line.startswith('>'):
            quote_lines = []
            while i < n and lines[i].startswith('>'):
                quote_lines.append(lines[i].lstrip('> ').rstrip())
                i += 1
            block = [Paragraph(md_inline(l) if l else '<br/>', quote) for l in quote_lines]
            t = Table([[block]], colWidths=[170*mm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), LIGHT),
                ('LINEBEFORE', (0,0), (0,-1), 2.5, ACCENT),
                ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(t); story.append(Spacer(1, 5))
            continue

        if re.match(r'^\s*[-*]\s+\[[ x]\]\s+', line):
            items = []
            while i < n and re.match(r'^\s*[-*]\s+\[[ x]\]\s+', lines[i]):
                c = re.sub(r'^\s*[-*]\s+\[[ x]\]\s+', '', lines[i])
                items.append('☐ ' + md_inline(c))
                i += 1
            block = [Paragraph(it, bodys) for it in items]
            t = Table([[block]], colWidths=[170*mm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eafaf1")),
                ('BORDER', (0,0), (-1,-1), 0.7, GREEN),
                ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(Spacer(1, 4)); story.append(t); story.append(Spacer(1, 6))
            continue

        if re.match(r'^\s*[-*]\s+', line):
            items = []
            while i < n and re.match(r'^\s*[-*]\s+\S', lines[i]):
                items.append('• ' + md_inline(re.sub(r'^\s*[-*]\s+', '', lines[i])))
                i += 1
            for it in items:
                story.append(Paragraph(it, bodys))
            story.append(Spacer(1, 3))
            continue

        if line.strip() == '---':
            story.append(Spacer(1, 6))
            i += 1
            continue

        if line.strip():
            story.append(Paragraph(md_inline(line.strip()), bodys))
            story.append(Spacer(1, 3))
        i += 1

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=15*mm, bottomMargin=15*mm,
                            title="Home-Lab Umstellung: Gesamtanleitung",
                            author="Vibe Code (Mistral)")
    doc.build(story)
    print("PDF erstellt:", pdf_path)

build('/workspace/github__Bextowner__mistral/Home-Lab_Roadmap_Befehle.md',
      '/workspace/github__Bextowner__mistral/Home-Lab_Roadmap_Gesamt.pdf')
