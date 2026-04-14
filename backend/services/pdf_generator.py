from pathlib import Path


def generate_pdf_from_html(html_content: str, output_path: str):
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise RuntimeError(
            "PDF generation requires WeasyPrint. Install backend dependencies before using /resume/pdf."
        ) from exc

    HTML(string=html_content, base_url=str(Path(output_path).resolve().parent)).write_pdf(output_path)
