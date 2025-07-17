#!/usr/bin/env python3
"""
Generate HTML documentation from Markdown source.
"""

import markdown
import os

def generate_html():
    """Generate HTML documentation."""
    print("🌐 Generating HTML documentation...")
    
    # Read Markdown content
    with open('DOCUMENTATION.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert Markdown to HTML with extensions
    html_content = markdown.markdown(
        md_content, 
        extensions=[
            'tables', 
            'fenced_code', 
            'toc',
            'codehilite',
            'attr_list'
        ]
    )
    
    # CSS styling
    css_style = """
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #fafafa;
    }
    
    .container {
        background-color: white;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        margin-top: 30px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    
    h1 {
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        color: #2980b9;
        font-size: 2.5em;
    }
    
    h2 {
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 8px;
        color: #34495e;
        font-size: 2em;
    }
    
    h3 {
        color: #2c3e50;
        font-size: 1.5em;
    }
    
    code {
        background-color: #f8f9fa;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
        font-size: 0.9em;
        color: #e74c3c;
    }
    
    pre {
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 20px;
        border-radius: 8px;
        overflow-x: auto;
        border-left: 4px solid #3498db;
        margin: 20px 0;
    }
    
    pre code {
        background-color: transparent;
        color: #ecf0f1;
        padding: 0;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    
    th {
        background-color: #3498db;
        color: white;
        font-weight: 600;
    }
    
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    tr:hover {
        background-color: #e8f4fd;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        margin: 20px 0;
        padding: 10px 20px;
        background-color: #f8f9fa;
        font-style: italic;
        border-radius: 0 4px 4px 0;
    }
    
    ul, ol {
        padding-left: 30px;
    }
    
    li {
        margin-bottom: 8px;
    }
    
    a {
        color: #3498db;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    .toc {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        border: 1px solid #e9ecef;
    }
    
    .toc ul {
        list-style-type: none;
        padding-left: 20px;
    }
    
    .toc > ul {
        padding-left: 0;
    }
    
    .toc a {
        color: #2c3e50;
        font-weight: 500;
    }
    
    .highlight {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 4px;
        border-left: 4px solid #ffc107;
        margin: 20px 0;
    }
    
    .success {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 4px;
        border-left: 4px solid #28a745;
        margin: 20px 0;
    }
    
    .info {
        background-color: #d1ecf1;
        padding: 15px;
        border-radius: 4px;
        border-left: 4px solid #17a2b8;
        margin: 20px 0;
    }
    
    @media (max-width: 768px) {
        body {
            padding: 10px;
        }
        
        .container {
            padding: 20px;
        }
        
        h1 {
            font-size: 2em;
        }
        
        h2 {
            font-size: 1.5em;
        }
        
        table {
            font-size: 0.9em;
        }
        
        th, td {
            padding: 8px;
        }
    }
    
    .footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e9ecef;
        text-align: center;
        color: #6c757d;
        font-size: 0.9em;
    }
    </style>
    """
    
    # JavaScript for enhanced functionality
    js_script = """
    <script>
    // Add smooth scrolling for anchor links
    document.addEventListener('DOMContentLoaded', function() {
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // Add copy buttons to code blocks
        const codeBlocks = document.querySelectorAll('pre code');
        codeBlocks.forEach(block => {
            const button = document.createElement('button');
            button.textContent = 'Copy';
            button.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
            `;
            
            const pre = block.parentElement;
            pre.style.position = 'relative';
            pre.appendChild(button);
            
            button.addEventListener('click', () => {
                navigator.clipboard.writeText(block.textContent).then(() => {
                    button.textContent = 'Copied!';
                    setTimeout(() => {
                        button.textContent = 'Copy';
                    }, 2000);
                });
            });
        });
    });
    </script>
    """
    
    # Create complete HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Commits AI - Complete Documentation</title>
        <meta name="description" content="Comprehensive documentation for Smart Commits AI - Universal Git commit message generator">
        <meta name="keywords" content="git, commit, AI, automation, development, tools">
        <meta name="author" content="Joshi">
        {css_style}
    </head>
    <body>
        <div class="container">
            {html_content}
            <div class="footer">
                <p>Generated on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Smart Commits AI</strong> - Transform your Git workflow with AI-powered commit messages</p>
            </div>
        </div>
        {js_script}
    </body>
    </html>
    """
    
    # Write HTML file
    with open('Smart_Commits_AI_Documentation.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print("✅ HTML generated: Smart_Commits_AI_Documentation.html")
    
    # Get file size
    size = os.path.getsize('Smart_Commits_AI_Documentation.html') / 1024
    print(f"📄 File size: {size:.1f} KB")

if __name__ == "__main__":
    generate_html()
