import os
import io
from collections import Counter

# --- 3rd Party Libraries ---
import fitz  # PyMuPDF
import camelot
import pandas as pd
import pytesseract
from PIL import Image

# --- Global Configuration ---
INPUT_FOLDER = "input_pdfs"
OUTPUT_FOLDER = "output"
FIGURES_FOLDER = "figures"

# Heuristic thresholds for content structuring
OCR_THRESHOLD = 100       # Min text length on a page to trigger OCR
OCR_DPI = 300             # DPI for scanning pages for OCR
HEADING_L1_THRESHOLD = 3.5  # Font size difference for H2
HEADING_L2_THRESHOLD = 1.5  # Font size difference for H3

def get_font_stats(page):
    """
    Finds the most common font size on a page to identify 'paragraph' text.
    """
    spans = []
    for block in page.get_text("dict", flags=fitz.TEXTFLAGS_SEARCH).get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                spans.append((span["size"], span["flags"]))
    
    if not spans:
        return 0  # Empty page

    # Find the most common font size
    size_counter = Counter(s[0] for s in spans)
    most_common_size = size_counter.most_common(1)[0][0]
    return most_common_size


def extract_text_and_headings(page, most_common_size):
    """
    Extracts text from a digital page, applying heading styles based on font.
    """
    page_dict = page.get_text("dict", flags=fitz.TEXTFLAGS_SEARCH)
    blocks = page_dict.get("blocks", [])
    md_text = []
    
    for block in blocks:
        block_text = []
        is_heading_2 = False
        is_heading_3 = False
        
        for line in block.get("lines", []):
            if not line.get("spans", []):
                continue
                
            first_span = line["spans"][0]
            font_size = first_span["size"]
            is_bold = (first_span["flags"] & 16) > 0  # Flag 16 = Bold

            # Heuristic: Identify headings based on font size and bold style
            if is_bold and font_size > (most_common_size + HEADING_L1_THRESHOLD):
                is_heading_2 = True
            elif is_bold and font_size > (most_common_size + HEADING_L2_THRESHOLD):
                is_heading_3 = True

            for span in line.get("spans", []):
                block_text.append(span["text"])
        
        if block_text:
            full_line_text = " ".join(block_text).strip()
            # Append text with appropriate Markdown
            if is_heading_2:
                md_text.append(f"\n## {full_line_text}\n")
            elif is_heading_3:
                md_text.append(f"\n### {full_line_text}\n")
            else:
                md_text.append(f"{full_line_text} ") # Join paragraphs
    
    return "\n".join(md_text)


def process_scanned_page(page):
    """
    Uses Tesseract OCR to extract text from a scanned page image.
    """
    try:
        pix = page.get_pixmap(dpi=OCR_DPI)
        img_bytes = pix.tobytes("png")
        pil_image = Image.open(io.BytesIO(img_bytes))
        page_text = pytesseract.image_to_string(pil_image, lang='eng')
        
        if page_text:
            return f"*(This page was processed with OCR)*\n{page_text}"
        else:
            return "*(This page appears to be scanned, but no text was found by OCR)*"
    except Exception as e:
        return f"*(Error during OCR processing: {e})*"


def extract_tables(pdf_path, page_num):
    """
    Extracts tables from a single page using Camelot (lattice method).
    """
    table_md_content = []
    try:
        # Camelot needs page numbers to be 1-indexed
        tables = camelot.read_pdf(pdf_path, pages=str(page_num), flavor='lattice')
        
        if tables.n > 0:
            table_md_content.append("\n\n--- *Tables Found* ---\n")
            for i, table in enumerate(tables):
                table_md_content.append(f"### Table {i+1}\n")
                table_md_content.append(table.df.to_markdown(index=False) + "\n")
    except Exception as e:
        pass
    return "\n".join(table_md_content)


def extract_images(page, doc, doc_figures_folder, page_num):
    """
    Extracts raster images from a single page and saves them.
    """
    image_md_content = []
    image_list = page.get_images(full=True)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        image_name = f"page{page_num}_img{img_index}.{image_ext}"
        image_save_path = os.path.join(doc_figures_folder, image_name)
        
        with open(image_save_path, "wb") as img_file:
            img_file.write(image_bytes)
        
        # Create the relative markdown link
        image_md_link = f"![{image_name}](./{FIGURES_FOLDER}/{image_name})\n"
        image_md_content.append(image_md_link)
    return "\n".join(image_md_content)


def process_pdf(pdf_path, doc_output_folder):
    """
    Manages the full extraction pipeline for a single PDF document.
    """
    # Ensure the output directory for this doc's figures exists
    doc_figures_folder = os.path.join(doc_output_folder, FIGURES_FOLDER)
    os.makedirs(doc_figures_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    markdown_content = []

    # 1. Extract Metadata
    title = doc.metadata.get('title', os.path.basename(pdf_path).replace('.pdf', ''))
    author = doc.metadata.get('author', 'Unknown Author')
    markdown_content.append(f"# {title}\n")
    markdown_content.append(f"**Author:** {author}\n---\n")

    # 2. Extract Table of Contents
    toc = doc.get_toc()
    if toc:
        markdown_content.append("## Table of Contents\n")
        for level, toc_title, page in toc:
            indent = "  " * (level - 1)
            markdown_content.append(f"{indent}- {toc_title} (Page {page})")
        markdown_content.append("\n---\n")

    # 3. Process each page for content
    for page_num, page in enumerate(doc):
        current_page_num = page_num + 1
        markdown_content.append(f"\n---\n*Page {current_page_num}*\n---\n")

        # A. Process Text (handles both digital and scanned)
        digital_text = page.get_text("text")
        if len(digital_text.strip()) < OCR_THRESHOLD:
            page_text = process_scanned_page(page)
        else:
            most_common_size = get_font_stats(page)
            page_text = extract_text_and_headings(page, most_common_size)
        markdown_content.append(page_text)

        # B. Extract Tables
        table_text = extract_tables(pdf_path, current_page_num)
        markdown_content.append(table_text)

        # C. Extract Images
        image_text = extract_images(page, doc, doc_figures_folder, current_page_num)
        markdown_content.append(image_text)
    
    doc.close()

    # 4. Save the final Markdown file
    md_filename = os.path.basename(pdf_path).replace('.pdf', '.md')
    md_output_path = os.path.join(doc_output_folder, md_filename)
    
    with open(md_output_path, 'w', encoding='utf-8') as md_file:
        md_file.write("\n".join(markdown_content))
    
    print(f"Processed: {md_filename}")


def main():
    """
    Main function to find and process all PDFs in the input folder.
    """
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Input folder '{INPUT_FOLDER}' not found. Please create it.")
        return

    print(f"Starting PDF processing in '{INPUT_FOLDER}'...")
    
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_FOLDER, filename)
            doc_name = os.path.splitext(filename)[0]
            doc_output_folder = os.path.join(OUTPUT_FOLDER, doc_name)
            
            # Create a specific output folder for each document
            os.makedirs(doc_output_folder, exist_ok=True)
                
            print(f"Processing '{filename}'...")
            try:
                # Process the file
                process_pdf(pdf_path, doc_output_folder)
            except Exception as e:
                # Don't let one bad file stop the whole batch
                print(f"!!! FAILED to process '{filename}': {e}")

    print("...Processing complete.")


if __name__ == "__main__":
    main()