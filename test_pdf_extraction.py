#!/usr/bin/env python3
"""
Test PDF extraction to diagnose issues
"""
import sys
from pathlib import Path

print("=" * 70)
print("PDF EXTRACTION DIAGNOSTIC TOOL")
print("=" * 70)

# Check installed libraries
print("\n1. Checking installed PDF libraries...")
libraries = {
    'fitz (PyMuPDF)': 'fitz',
    'pymupdf': 'pymupdf',
    'pypdf': 'pypdf',
    'pdfplumber': 'pdfplumber',
    'PIL (Pillow)': 'PIL'
}

installed = {}
for name, module in libraries.items():
    try:
        __import__(module)
        print(f"   ✓ {name} - INSTALLED")
        installed[name] = True
    except ImportError:
        print(f"   ✗ {name} - NOT INSTALLED")
        installed[name] = False

# Find PDF file
print("\n2. Looking for PDF files in data/uploads/...")
uploads_dir = Path("data/uploads")
pdf_files = list(uploads_dir.glob("*.pdf"))

if pdf_files:
    print(f"   Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"   - {pdf.name} ({pdf.stat().st_size} bytes)")
else:
    print("   ✗ No PDF files found!")
    sys.exit(1)

# Test extraction on each PDF
for pdf_file in pdf_files:
    print(f"\n3. Testing extraction on: {pdf_file.name}")
    print("-" * 70)
    
    # Method 1: PyMuPDF
    if installed.get('fitz (PyMuPDF)'):
        print("   Method 1: PyMuPDF (fitz)")
        try:
            import fitz
            doc = fitz.open(str(pdf_file))
            print(f"      - Pages: {len(doc)}")
            
            total_text = ""
            for i, page in enumerate(doc):
                text = page.get_text("text")
                print(f"      - Page {i+1}: {len(text)} characters")
                total_text += text
            
            if total_text.strip():
                print(f"      ✓ Successfully extracted {len(total_text)} characters")
                print(f"      Preview: {total_text[:200]}...")
            else:
                print(f"      ✗ Extracted 0 characters (likely image-based PDF)")
                
        except Exception as e:
            print(f"      ✗ Error: {e}")
    
    # Method 2: pdfplumber
    if installed.get('pdfplumber'):
        print("\n   Method 2: pdfplumber")
        try:
            import pdfplumber
            with pdfplumber.open(str(pdf_file)) as pdf:
                print(f"      - Pages: {len(pdf.pages)}")
                
                total_text = ""
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    print(f"      - Page {i+1}: {len(text)} characters")
                    total_text += text
                
                if total_text.strip():
                    print(f"      ✓ Successfully extracted {len(total_text)} characters")
                    print(f"      Preview: {total_text[:200]}...")
                else:
                    print(f"      ✗ Extracted 0 characters")
                    
        except Exception as e:
            print(f"      ✗ Error: {e}")
    
    # Method 3: pypdf
    if installed.get('pypdf'):
        print("\n   Method 3: pypdf")
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_file))
            print(f"      - Pages: {len(reader.pages)}")
            
            total_text = ""
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                print(f"      - Page {i+1}: {len(text)} characters")
                total_text += text
            
            if total_text.strip():
                print(f"      ✓ Successfully extracted {len(total_text)} characters")
                print(f"      Preview: {total_text[:200]}...")
            else:
                print(f"      ✗ Extracted 0 characters")
                
        except Exception as e:
            print(f"      ✗ Error: {e}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("\nIf all methods show 0 characters, the PDF is likely:")
print("  1. Image-based (scanned) - needs OCR")
print("  2. Corrupted or encrypted")
print("  3. Unreadable format")
print("\nNEXT STEPS:")
print("  1. Try enabling OCR in the Upload page")
print("  2. Convert the PDF to a standard format")
print("  3. Check if the PDF opens in Adobe Reader")
