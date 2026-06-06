"""
Export Handler - Generate exports in multiple formats (PDF, MD, TXT, APKG)
"""
from pathlib import Path
from typing import Optional, Dict, Any
import io
from utils.retry import retry_call
from utils.error_handler import report_error


class ExportHandler:
    """Handle exporting notes, summaries, and flashcards in various formats"""

    def export_to_markdown(self, content: str, title: str = "Export") -> str:
        """Export content to Markdown format (already structured)"""
        return content

    def export_to_txt(self, content: str) -> str:
        """Export content to plain text format"""
        # Remove markdown formatting
        import re
        text = content
        # Remove markdown headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        # Remove bold/italic
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        # Remove markdown links
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        return text

    def export_to_pdf(self, content: str, title: str = "Export", output_path: Optional[str] = None) -> Optional[bytes]:
        """
        Export content to PDF format using WeasyPrint
        
        Args:
            content: Markdown content to export
            title: Document title
            output_path: Path to save PDF (optional)
            
        Returns:
            bytes: PDF content or None if failed
        """
        try:
            from weasyprint import HTML, CSS
            import tempfile
            import os

            # Convert markdown to HTML
            html_content = self._markdown_to_html(content, title)

            # Create PDF with retries because rendering can fail transiently on first load
            pdf_bytes = retry_call(lambda: HTML(string=html_content).write_pdf(), tries=3, delay=0.5, backoff=2.0)

            # Save to file if path provided
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)

            return pdf_bytes

        except ImportError:
            print("WeasyPrint not installed. Install with: pip install weasyprint")
            return None
        except Exception as e:
            report_error(e, "Error exporting to PDF", user_facing=False)
            return None

    def export_to_html(self, content: str, title: str = "Export") -> str:
        """Export content to HTML format"""
        html_content = self._markdown_to_html(content, title)
        return html_content

    def export_notes_package(self, notes: Dict[str, Any], output_path: str) -> bool:
        """
        Export a complete notes package with multiple formats
        
        Args:
            notes: Dict with 'content', 'flashcards', 'quiz', etc.
            output_path: Base directory for exports
            
        Returns:
            bool: Success status
        """
        try:
            base_path = Path(output_path)
            base_path.mkdir(parents=True, exist_ok=True)

            # Save markdown
            if 'content' in notes:
                with open(base_path / 'notes.md', 'w', encoding='utf-8') as f:
                    f.write(notes['content'])

            # Save text
            if 'content' in notes:
                txt_content = self.export_to_txt(notes['content'])
                with open(base_path / 'notes.txt', 'w', encoding='utf-8') as f:
                    f.write(txt_content)

            # Save PDF
            if 'content' in notes:
                pdf_path = base_path / 'notes.pdf'
                self.export_to_pdf(notes['content'], output_path=str(pdf_path))

            # Save flashcards CSV
            if 'flashcards' in notes:
                import csv
                with open(base_path / 'flashcards.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Front', 'Back', 'Topic'])
                    for card in notes['flashcards']:
                        writer.writerow([
                            card.get('front', ''),
                            card.get('back', ''),
                            card.get('topic', '')
                        ])

            return True

        except Exception as e:
            print(f"Error exporting notes package: {e}")
            return False

    @staticmethod
    def _markdown_to_html(markdown_content: str, title: str = "Document") -> str:
        """Convert markdown content to HTML"""
        try:
            import markdown
            html_body = markdown.markdown(markdown_content, extensions=['tables', 'codehilite'])
        except ImportError:
            # Fallback: simple conversion
            html_body = markdown_content.replace('\n', '<br>')

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                    color: #333;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                    margin-top: 1.5em;
                    margin-bottom: 0.5em;
                }}
                h1 {{
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                ul, ol {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                li {{
                    margin: 5px 0;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 10px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    padding-left: 10px;
                    margin-left: 0;
                    color: #666;
                }}
                .stats {{
                    background-color: #ecf0f1;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        return html
