#!/usr/bin/env python3
"""
Generate PDF and DOCX documentation from Markdown source.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = {
        'pandoc': 'pandoc --version',
        'weasyprint': 'python -c "import weasyprint"',
        'python-docx': 'python -c "import docx"'
    }
    
    missing = []
    for name, check_cmd in dependencies.items():
        try:
            subprocess.run(check_cmd.split(), capture_output=True, check=True)
            print(f"✅ {name} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(name)
            print(f"❌ {name} is missing")
    
    return missing

def install_dependencies():
    """Install missing Python dependencies."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            'weasyprint', 'python-docx', 'markdown', 'beautifulsoup4'
        ], check=True)
        print("✅ Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def generate_pdf_with_weasyprint():
    """Generate PDF using WeasyPrint (Python-based)."""
    try:
        import markdown
        import weasyprint
        from bs4 import BeautifulSoup
        
        print("📄 Generating PDF with WeasyPrint...")
        
        # Read Markdown content
        with open('DOCUMENTATION.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert Markdown to HTML
        html = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
        
        # Add CSS styling
        css_style = """
        <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        h1 {
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 0;
            padding-left: 20px;
            font-style: italic;
        }
        .page-break {
            page-break-before: always;
        }
        </style>
        """
        
        # Create complete HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Smart Commits AI - Complete Documentation</title>
            {css_style}
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Generate PDF
        weasyprint.HTML(string=full_html).write_pdf('Smart_Commits_AI_Documentation.pdf')
        print("✅ PDF generated: Smart_Commits_AI_Documentation.pdf")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return False

def generate_docx():
    """Generate DOCX using python-docx."""
    try:
        import markdown
        from docx import Document
        from docx.shared import Inches, Pt
        from docx.enum.style import WD_STYLE_TYPE
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        import re
        
        print("📄 Generating DOCX...")
        
        # Read Markdown content
        with open('DOCUMENTATION.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Create new document
        doc = Document()
        
        # Set document margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        # Add title
        title = doc.add_heading('Smart Commits AI', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        subtitle = doc.add_heading('Complete Project Documentation', level=1)
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add page break
        doc.add_page_break()
        
        # Process Markdown content
        lines = md_content.split('\n')
        in_code_block = False
        code_content = []
        
        for line in lines:
            line = line.strip()
            
            # Skip title lines (already added)
            if line.startswith('# Smart Commits AI') or line.startswith('## Table of Contents'):
                continue
            
            # Handle code blocks
            if line.startswith('```'):
                if in_code_block:
                    # End of code block
                    if code_content:
                        code_para = doc.add_paragraph()
                        code_run = code_para.add_run('\n'.join(code_content))
                        code_run.font.name = 'Consolas'
                        code_run.font.size = Pt(9)
                    code_content = []
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
                continue
            
            if in_code_block:
                code_content.append(line)
                continue
            
            # Handle headings
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                heading_text = line.lstrip('#').strip()
                if heading_text:
                    doc.add_heading(heading_text, level=min(level, 9))
                continue
            
            # Handle empty lines
            if not line:
                doc.add_paragraph()
                continue
            
            # Handle lists
            if line.startswith('- ') or line.startswith('* '):
                list_text = line[2:].strip()
                # Remove markdown formatting
                list_text = re.sub(r'\*\*(.*?)\*\*', r'\1', list_text)  # Bold
                list_text = re.sub(r'\*(.*?)\*', r'\1', list_text)      # Italic
                list_text = re.sub(r'`(.*?)`', r'\1', list_text)        # Code
                doc.add_paragraph(list_text, style='List Bullet')
                continue
            
            # Handle numbered lists
            if re.match(r'^\d+\.', line):
                list_text = re.sub(r'^\d+\.\s*', '', line)
                # Remove markdown formatting
                list_text = re.sub(r'\*\*(.*?)\*\*', r'\1', list_text)
                list_text = re.sub(r'\*(.*?)\*', r'\1', list_text)
                list_text = re.sub(r'`(.*?)`', r'\1', list_text)
                doc.add_paragraph(list_text, style='List Number')
                continue
            
            # Handle regular paragraphs
            if line:
                # Remove markdown formatting
                clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # Bold
                clean_line = re.sub(r'\*(.*?)\*', r'\1', clean_line)  # Italic
                clean_line = re.sub(r'`(.*?)`', r'\1', clean_line)    # Code
                clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)  # Links
                doc.add_paragraph(clean_line)
        
        # Save document
        doc.save('Smart_Commits_AI_Documentation.docx')
        print("✅ DOCX generated: Smart_Commits_AI_Documentation.docx")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ DOCX generation failed: {e}")
        return False

def generate_pdf_with_pandoc():
    """Generate PDF using Pandoc (if available)."""
    try:
        print("📄 Generating PDF with Pandoc...")
        
        cmd = [
            'pandoc',
            'DOCUMENTATION.md',
            '-o', 'Smart_Commits_AI_Documentation_Pandoc.pdf',
            '--pdf-engine=weasyprint',
            '--css=docs_style.css',
            '--standalone',
            '--toc',
            '--toc-depth=3'
        ]
        
        # Create CSS file for Pandoc
        css_content = """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        """
        
        with open('docs_style.css', 'w') as f:
            f.write(css_content)
        
        subprocess.run(cmd, check=True)
        print("✅ PDF generated with Pandoc: Smart_Commits_AI_Documentation_Pandoc.pdf")
        
        # Clean up CSS file
        os.remove('docs_style.css')
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc PDF generation failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Pandoc not found")
        return False

def main():
    """Main function to generate documentation."""
    print("🚀 Smart Commits AI Documentation Generator")
    print("=" * 50)
    
    # Check if source file exists
    if not Path('DOCUMENTATION.md').exists():
        print("❌ DOCUMENTATION.md not found!")
        return 1
    
    # Check dependencies
    missing = check_dependencies()
    
    # Install Python dependencies if needed
    if 'weasyprint' in missing or 'python-docx' in missing:
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return 1
    
    success_count = 0
    
    # Generate PDF with WeasyPrint
    if generate_pdf_with_weasyprint():
        success_count += 1
    
    # Generate DOCX
    if generate_docx():
        success_count += 1
    
    # Try Pandoc PDF if available
    if 'pandoc' not in missing:
        if generate_pdf_with_pandoc():
            success_count += 1
    
    print("\n" + "=" * 50)
    if success_count > 0:
        print(f"✅ Successfully generated {success_count} document(s)")
        print("\nGenerated files:")
        for file in ['Smart_Commits_AI_Documentation.pdf', 
                     'Smart_Commits_AI_Documentation.docx',
                     'Smart_Commits_AI_Documentation_Pandoc.pdf']:
            if Path(file).exists():
                size = Path(file).stat().st_size / 1024  # KB
                print(f"  📄 {file} ({size:.1f} KB)")
    else:
        print("❌ No documents were generated successfully")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
