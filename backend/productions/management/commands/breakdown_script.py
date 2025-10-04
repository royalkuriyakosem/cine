from django.core.management.base import BaseCommand
from productions.services import analyze_script
import os

class Command(BaseCommand):
    help = 'Analyzes a script file and outputs the breakdown'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True,
                          help='Path to the script file (.txt or .pdf)')

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stderr.write(f"File not found: {file_path}")
            return
        
        # Basic file type handling
        if file_path.endswith('.pdf'):
            try:
                import PyPDF2
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text()
            except ImportError:
                self.stderr.write("PyPDF2 is required for PDF files. Install with: pip install PyPDF2")
                return
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

        # Analyze the script
        breakdown = analyze_script(text)

        # Output the results
        for category, items in breakdown.items():
            self.stdout.write(self.style.SUCCESS(f"\n{category.upper()}:"))
            for item in items:
                self.stdout.write(f"- {item}")