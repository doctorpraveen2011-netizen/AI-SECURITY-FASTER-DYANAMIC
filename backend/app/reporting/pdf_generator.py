import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFReportGenerator:
    @staticmethod
    def generate_security_report(
        metrics: dict,
        mitigations: list,
        vulnerabilities: list,
        test_summary: list
    ) -> io.BytesIO:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#FF8A00'),
            spaceAfter=14
        )
        subtitle_style = ParagraphStyle(
            'SubTitleStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#555555'),
            spaceAfter=18
        )
        section_style = ParagraphStyle(
            'SectionStyle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#14161D'),
            spaceBefore=14,
            spaceAfter=8
        )

        elements = []
        elements.append(Paragraph("AI SECURITY FASTER – SOC AUDIT REPORT", title_style))
        elements.append(Paragraph("Automated Red-Teaming & Blue-Teaming Security Assessment Report", subtitle_style))
        elements.append(Spacer(1, 10))

        # Metrics Table
        elements.append(Paragraph("1. Executive Summary & KPIs", section_style))
        kpi_data = [
            ["Metric", "Value", "Trend / Benchmark"],
            ["Total Security Tests Executed", str(metrics.get("total_tests", 48)), metrics.get("total_tests_trend", "+12%")],
            ["Vulnerabilities Detected", str(metrics.get("vulnerabilities", 27)), metrics.get("vulnerabilities_trend", "+8%")],
            ["Verified Mitigated Risks", str(metrics.get("mitigated_risks", 24)), metrics.get("mitigated_trend", "+15%")],
            ["Average Automated Scan Latency", str(metrics.get("avg_scan_time", "2m 14s")), "SOC Baseline"]
        ]
        t_kpi = Table(kpi_data, colWidths=[200, 100, 200])
        t_kpi.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#14161D')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FF8A00')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ]))
        elements.append(t_kpi)
        elements.append(Spacer(1, 14))

        # Mitigations Table
        elements.append(Paragraph("2. Blue Team Defense Verification", section_style))
        mit_data = [["Vulnerability Category", "Before Risk", "After Defense", "Status"]]
        for m in mitigations[:6]:
            mit_data.append([
                m.get("name", "Defense"),
                m.get("before_label", f"{int(m.get('before_risk_pct', 80))}%"),
                m.get("after_label", f"{int(m.get('after_risk_pct', 12))}%"),
                m.get("status", "VERIFIED")
            ])
        t_mit = Table(mit_data, colWidths=[200, 100, 100, 100])
        t_mit.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#14161D')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#10B981')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ]))
        elements.append(t_mit)

        doc.build(elements)
        buffer.seek(0)
        return buffer
