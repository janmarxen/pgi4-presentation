#!/usr/bin/env python3
"""
Script to generate PDF from HTML slides using Chrome headless mode
"""
import subprocess
import time
import os
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8080/presentation"
OUTPUT_DIR = Path("pdf_output")
SLIDES = [
    "slide1.html",
    "slide3.html", 
    "slide5.html",
    "slide2.html",
    "slide6.html", 
    "slide7.html"
]

def create_pdf(slide_file, output_file):
    """Generate PDF from HTML slide using Chrome headless"""
    url = f"{BASE_URL}/{slide_file}"
    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--print-to-pdf=" + str(output_file),
        "--print-to-pdf-no-header",
        "--virtual-time-budget=2000",
        "--run-all-compositor-stages-before-draw",
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Generated: {output_file}")
            return True
        else:
            print(f"❌ Failed to generate {output_file}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout generating {output_file}")
        return False
    except Exception as e:
        print(f"❌ Error generating {output_file}: {e}")
        return False

def merge_pdfs(pdf_files, output_file):
    """Merge multiple PDFs into one using ghostscript"""
    cmd = ["gs", "-dBATCH", "-dNOPAUSE", "-q", "-sDEVICE=pdfwrite", f"-sOutputFile={output_file}"] + pdf_files
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Merged PDF created: {output_file}")
            return True
        else:
            print(f"❌ Failed to merge PDFs: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error merging PDFs: {e}")
        return False

def main():
    print("🎯 Generating PDF presentation...")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Generate individual PDFs
    pdf_files = []
    for i, slide in enumerate(SLIDES, 1):
        output_file = OUTPUT_DIR / f"slide_{i:02d}.pdf"
        if create_pdf(slide, output_file):
            pdf_files.append(str(output_file))
        time.sleep(1)  # Small delay between generations
    
    if pdf_files:
        # Merge all PDFs
        final_pdf = "Jan_Marxen_PGI4_Presentation.pdf"
        if merge_pdfs(pdf_files, final_pdf):
            print(f"\n🎉 Complete presentation PDF created: {final_pdf}")
            print(f"📧 Ready to send to interviewers!")
        
        # Clean up individual files
        for pdf_file in pdf_files:
            try:
                os.remove(pdf_file)
            except:
                pass
        try:
            OUTPUT_DIR.rmdir()
        except:
            pass
    else:
        print("❌ No PDFs were generated successfully")

if __name__ == "__main__":
    main()
