from django.core.management.base import BaseCommand
from productions.services import analyze_script
import os

class Command(BaseCommand):
    help = 'Analyzes a script file and outputs the breakdown'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True,
                          help='Path to the script file (.txt or .pdf)')
        parser.add_argument('--use-ai', action='store_true',
                          help='Use AI-powered analysis (requires OpenAI API key)')

    def handle(self, *args, **options):
        file_path = options['file']
        use_ai = options['use_ai']
        
        if not os.path.exists(file_path):
            self.stderr.write(f"File not found: {file_path}")
            return
        
        # Read the file
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
        self.stdout.write(f"Analyzing script using {'AI' if use_ai else 'basic'} analysis...")
        breakdown = analyze_script(text, use_ai=use_ai)

        # Output the results
        for category, items in breakdown.items():
            self.stdout.write(self.style.SUCCESS(f"\n{category.upper()}:"))
            for item in items:
                self.stdout.write(f"- {item}")