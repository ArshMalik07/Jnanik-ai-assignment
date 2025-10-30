# Document Ingestion Pipeline

A robust Python-based solution for extracting structured content from PDFs and converting them into well-formatted Markdown documents. This pipeline handles digital PDFs, scanned documents, multi-column layouts, tables, and embedded images.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Solution Approach](#solution-approach)
- [System Architecture](#system-architecture)
- [Key Design Decisions](#key-design-decisions)
- [Implementation Details](#implementation-details)
- [Installation](#installation)
- [Usage](#usage)
- [Output Structure](#output-structure)
- [Technical Specifications](#technical-specifications)
- [Limitations and Future Enhancements](#limitations-and-future-enhancements)

---

## 🎯 Overview

This document ingestion pipeline processes PDF documents and converts them into structured Markdown format while preserving:
- Document hierarchy (headings and sections)
- Tables with proper formatting
- Images and diagrams
- Metadata (title, author)
- Table of contents
- Page structure

### Problem Statement

Organizations often need to convert large volumes of PDF documents into machine-readable formats for:
- Knowledge base creation
- Content management systems
- Document search and retrieval
- AI/ML training data preparation
- Accessibility improvements

### Solution

An automated pipeline that intelligently processes various PDF types and generates clean, structured Markdown output suitable for downstream applications.

---

## ✨ Features

### Core Capabilities

✅ **Multi-Format PDF Support**
- Digital PDFs with embedded text
- Scanned/image-based PDFs (via OCR)
- Multi-column layouts
- Mixed content documents

✅ **Intelligent Content Extraction**
- Automatic heading detection (H2, H3 levels)
- Paragraph structure preservation
- Table extraction and conversion
- Image/diagram extraction
- Metadata extraction (title, author)
- Table of contents parsing

✅ **Smart Processing**
- Font analysis for heading detection
- OCR with quality optimization (300 DPI)
- Page-by-page processing
- Robust error handling

✅ **Structured Output**
- Clean Markdown format
- Organized folder structure
- Separate figure storage
- Clear page markers
- Markdown table formatting

---

## 🏗️ Solution Approach

### 1. Analysis Phase

**Challenge Identification:**
- PDFs come in various formats (digital vs. scanned)
- Complex layouts (multi-column, tables, images)
- Need to preserve document structure and hierarchy
- Must handle errors gracefully

**Requirements Analysis:**
- Extract text while maintaining structure
- Detect and format headings
- Extract tables in readable format
- Save images separately with references
- Support OCR for scanned documents

### 2. Design Philosophy

**Modular Architecture:**
- Separate concerns (text extraction, OCR, tables, images)
- Reusable functions for different PDF types
- Clear separation of processing stages

**Progressive Enhancement:**
- Start with basic text extraction
- Add intelligent heading detection
- Layer in table and image processing
- Apply OCR when needed

**Fail-Safe Operation:**
- Continue processing even if one component fails
- Provide clear error messages
- Mark problematic pages explicitly

### 3. Technology Selection

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **PDF Processing** | PyMuPDF (fitz) | Fast, reliable, comprehensive API |
| **OCR** | Tesseract | Industry standard, high accuracy |
| **Table Extraction** | Camelot | Specialized for PDF tables |
| **Image Processing** | Pillow (PIL) | Standard Python image library |
| **Data Handling** | Pandas | Efficient table-to-markdown conversion |

---

## 🔧 System Architecture

### High-Level Workflow

```
┌─────────────┐
│  Input PDFs │
│   (Folder)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Document Processing Loop      │
│  (Iterate through each PDF)     │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│     Metadata Extraction         │
│  - Title, Author                │
│  - Table of Contents            │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│     Page-by-Page Processing     │
│                                 │
│  ┌───────────────────────────┐ │
│  │  1. Text Extraction       │ │
│  │     - Font Analysis       │ │
│  │     - Heading Detection   │ │
│  │     - OR OCR if Scanned   │ │
│  └───────────────────────────┘ │
│                                 │
│  ┌───────────────────────────┐ │
│  │  2. Table Extraction      │ │
│  │     - Camelot Processing  │ │
│  │     - Markdown Conversion │ │
│  └───────────────────────────┘ │
│                                 │
│  ┌───────────────────────────┐ │
│  │  3. Image Extraction      │ │
│  │     - Save to figures/    │ │
│  │     - Generate References │ │
│  └───────────────────────────┘ │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Markdown File Generation      │
│  - Combine all content          │
│  - Format properly              │
│  - Save to output folder        │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────┐
│   Output    │
│ (Organized  │
│  Folders)   │
└─────────────┘
```

### Component Diagram

```
┌────────────────────────────────────────────────────┐
│                  process.py                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │         main()                           │    │
│  │  - Setup folders                         │    │
│  │  - Iterate PDFs                          │    │
│  │  - Call process_pdf()                    │    │
│  └──────────┬───────────────────────────────┘    │
│             │                                      │
│             ▼                                      │
│  ┌──────────────────────────────────────────┐    │
│  │      process_pdf()                       │    │
│  │  - Extract metadata                      │    │
│  │  - Extract TOC                           │    │
│  │  - Loop through pages                    │    │
│  │  - Aggregate content                     │    │
│  │  - Save markdown                         │    │
│  └──┬───────────┬────────────┬──────────────┘    │
│     │           │            │                    │
│     ▼           ▼            ▼                    │
│  ┌─────┐   ┌──────┐   ┌──────────────┐          │
│  │Font │   │Text/ │   │Image/Table   │          │
│  │Stats│   │OCR   │   │Extraction    │          │
│  └─────┘   └──────┘   └──────────────┘          │
│                                                    │
└────────────────────────────────────────────────────┘

External Libraries:
┌─────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐
│ PyMuPDF │ │Tesseract │ │ Camelot │ │ Pandas  │
└─────────┘ └──────────┘ └─────────┘ └─────────┘
```

---

## 💡 Key Design Decisions

### 1. **Adaptive Heading Detection**

**Decision:** Use font size analysis relative to the most common font size in each page.

**Rationale:**
- PDFs don't have semantic heading tags
- Font size varies across documents
- Relative comparison is more robust than absolute thresholds

**Implementation:**
```python
most_common_size = get_font_stats(page)
if is_bold and font_size > (most_common_size + 3.5):
    # Heading Level 2
elif is_bold and font_size > (most_common_size + 1.5):
    # Heading Level 3
```

**Trade-offs:**
- ✅ Adapts to different document styles
- ✅ Works across varied font sizes
- ⚠️ May miss headings that aren't bold
- ⚠️ Requires tuning of thresholds

### 2. **Scanned PDF Detection**

**Decision:** Use character count threshold (<100 chars) to detect scanned pages.

**Rationale:**
- Digital PDFs have abundant extractable text
- Scanned PDFs have minimal/no extractable text
- Simple heuristic that works reliably

**Implementation:**
```python
digital_text = page.get_text("text")
if len(digital_text.strip()) < 100:  # Scanned PDF
    # Apply OCR
else:
    # Extract digital text with heading detection
```

**Trade-offs:**
- ✅ Fast and efficient
- ✅ No false positives in practice
- ⚠️ Pages with <100 chars but digital text may trigger OCR unnecessarily
- ⚠️ Could be enhanced with image detection

### 3. **High-Resolution OCR (300 DPI)**

**Decision:** Use 300 DPI for OCR processing.

**Rationale:**
- Tesseract accuracy improves significantly with higher DPI
- 300 DPI is industry standard for document scanning
- Balance between quality and processing time

**Implementation:**
```python
pix = page.get_pixmap(dpi=300)
```

**Trade-offs:**
- ✅ Better OCR accuracy
- ✅ Handles small fonts well
- ⚠️ Slower processing
- ⚠️ Higher memory usage

**Alternatives Considered:**
- 150 DPI: Faster but lower accuracy
- 600 DPI: Minimal accuracy gain, much slower

### 4. **Page-by-Page Processing**

**Decision:** Process each page independently rather than document-level batch processing.

**Rationale:**
- Memory efficient for large documents
- Allows mixed processing (digital + scanned in same document)
- Better error isolation
- Enables incremental output

**Trade-offs:**
- ✅ Scalable to large documents
- ✅ Better error handling
- ✅ Progressive processing feedback
- ⚠️ Can't leverage document-wide patterns
- ⚠️ Slightly more overhead

### 5. **Camelot for Table Extraction**

**Decision:** Use Camelot with 'lattice' flavor for table detection.

**Rationale:**
- Specialized library for PDF tables
- 'lattice' flavor works well with bordered tables
- Converts directly to pandas DataFrame
- Easy markdown conversion

**Implementation:**
```python
tables = camelot.read_pdf(pdf_path, pages=str(page_num + 1), flavor='lattice')
md_table = table.df.to_markdown(index=False)
```

**Trade-offs:**
- ✅ High accuracy for bordered tables
- ✅ Clean markdown output
- ⚠️ May miss borderless tables
- ⚠️ Requires Ghostscript dependency

**Alternatives Considered:**
- 'stream' flavor: Better for borderless tables but less accurate overall
- Tabula: Java dependency, more complex setup
- Custom regex parsing: Too fragile

### 6. **Separate Figures Folder**

**Decision:** Store extracted images in a dedicated `figures/` subfolder.

**Rationale:**
- Clean separation of content types
- Easier to manage image assets
- Standard practice in documentation
- Relative paths work well with markdown

**Output Structure:**
```
output/
└── document_name/
    ├── document_name.md
    └── figures/
        ├── page1_img0.png
        ├── page2_img0.jpg
        └── page3_img0.png
```

**Trade-offs:**
- ✅ Clean organization
- ✅ Standard markdown conventions
- ✅ Easy to locate images
- ⚠️ Requires proper path management

### 7. **Error Handling Strategy**

**Decision:** Use try-except blocks with graceful degradation.

**Rationale:**
- Don't let one failure stop entire document processing
- Provide informative error messages
- Mark problematic sections in output

**Implementation:**
```python
try:
    # OCR processing
except Exception as e:
    page_text = f"*(Error during OCR processing: {e})*"

try:
    # Table extraction
except Exception as e:
    pass  # Continue without tables
```

**Trade-offs:**
- ✅ Robust processing
- ✅ Partial results better than nothing
- ⚠️ Silent failures for tables (by design)
- ⚠️ May produce incomplete output

### 8. **Font Flag Analysis for Bold Detection**

**Decision:** Use bitwise flag checking (flag & 16) to detect bold text.

**Rationale:**
- PyMuPDF stores font properties as bitwise flags
- Reliable method for bold detection
- Fast comparison operation

**Implementation:**
```python
is_bold = (first_span["flags"] & 16) > 0  # Flag 16 = Bold
```

**Technical Detail:**
- Font flags in PyMuPDF are bitmasks
- Bit 16 represents bold formatting
- Bitwise AND operation checks if bold bit is set

---

## 🔍 Implementation Details

### Core Functions

#### 1. `get_font_stats(page)`

**Purpose:** Analyzes font sizes on a page to determine the most common (body text) size.

**Algorithm:**
1. Extract all text spans from page
2. Collect font sizes
3. Use `Counter` to find most frequent size
4. Return as baseline for heading detection

**Code Flow:**
```python
spans = []
for block → line → span:
    spans.append((span["size"], span["flags"]))

size_counter = Counter(s[0] for s in spans)
most_common_size = size_counter.most_common(1)[0][0]
```

**Why This Matters:**
- Different documents use different base font sizes
- Relative sizing is more reliable than absolute thresholds
- Handles documents ranging from 8pt to 14pt body text

#### 2. `process_page_text_with_headings(page, most_common_size)`

**Purpose:** Extracts text from a page and applies markdown heading formatting based on font properties.

**Algorithm:**
1. Get page text in dictionary format (preserves structure)
2. Iterate through blocks and lines
3. For each line, check first span's properties:
   - Get font size
   - Check if bold (bitwise flag)
   - Compare size to baseline
4. Apply appropriate markdown formatting:
   - Large + bold → `## Heading`
   - Medium + bold → `### Subheading`
   - Normal → Regular text
5. Concatenate into markdown output

**Key Logic:**
```python
if is_bold and font_size > (most_common_size + 3.5):
    is_heading_2 = True  # Major section
elif is_bold and font_size > (most_common_size + 1.5):
    is_heading_3 = True  # Subsection
```

**Threshold Rationale:**
- +3.5 points: Typically distinguishes major headings (e.g., 18pt vs 12pt)
- +1.5 points: Captures subheadings (e.g., 14pt vs 12pt)
- Based on common typographic practices

#### 3. `process_pdf(pdf_path, doc_output_folder)`

**Purpose:** Main orchestration function that processes an entire PDF document.

**Processing Pipeline:**

**Stage 1: Setup**
```python
# Create figures folder
doc_figures_folder = os.path.join(doc_output_folder, FIGURES_FOLDER)
os.makedirs(doc_figures_folder)

# Open PDF
doc = fitz.open(pdf_path)
markdown_content = []
```

**Stage 2: Metadata Extraction**
```python
title = doc.metadata.get('title', fallback_to_filename)
author = doc.metadata.get('author', 'Unknown Author')
# Add to markdown with proper formatting
```

**Stage 3: Table of Contents**
```python
toc = doc.get_toc()  # Returns list of (level, title, page_num)
# Format with indentation based on level
```

**Stage 4: Page Loop**
```python
for page_num, page in enumerate(doc):
    # A. Text extraction (digital or OCR)
    # B. Table extraction
    # C. Image extraction
```

**Stage 5: Output**
```python
# Save markdown file
with open(md_output_path, 'w', encoding='utf-8') as md_file:
    md_file.write("\n".join(markdown_content))
```

### Processing Logic Decision Tree

```
For each page:
│
├─ Extract digital text
│
├─ Is text length < 100 chars?
│  │
│  ├─ YES → Scanned page
│  │   ├─ Convert page to image (300 DPI)
│  │   ├─ Run Tesseract OCR
│  │   ├─ Add OCR marker
│  │   └─ Use OCR text
│  │
│  └─ NO → Digital page
│      ├─ Analyze font statistics
│      ├─ Process with heading detection
│      └─ Use structured text
│
├─ Try extract tables (Camelot)
│  ├─ If tables found → Convert to markdown
│  └─ If error → Skip silently
│
└─ Extract images
   ├─ Get all images on page
   ├─ Save to figures/ folder
   └─ Add markdown references
```

---

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Tesseract OCR installed on system
- Ghostscript (for Camelot)

### System Dependencies

**Windows:**
```bash
# Install Tesseract
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH: C:\Program Files\Tesseract-OCR

# Install Ghostscript
# Download from: https://ghostscript.com/releases/gsdnld.html
```

**macOS:**
```bash
brew install tesseract
brew install ghostscript
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install ghostscript
```

### Python Dependencies

```bash
pip install pymupdf pillow pytesseract camelot-py[cv] pandas tabulate
```

**Dependency Breakdown:**
- `pymupdf` (fitz): PDF manipulation
- `pillow`: Image processing
- `pytesseract`: Tesseract wrapper
- `camelot-py[cv]`: Table extraction with CV support
- `pandas`: Data manipulation
- `tabulate`: Markdown table formatting

### Verification

Test your installation:
```python
import fitz
import pytesseract
import camelot
import pandas
print("All dependencies installed successfully!")
```

---

## 🚀 Usage

### Basic Usage

1. **Create input folder and add PDFs:**
```bash
mkdir input_pdfs
# Copy your PDF files to input_pdfs/
```

2. **Run the pipeline:**
```bash
python process.py
```

3. **Check output:**
```bash
ls output/
# Each PDF gets its own folder with .md and figures/
```

### Folder Structure

**Before Processing:**
```
project/
├── process.py
└── input_pdfs/
    ├── document1.pdf
    ├── document2.pdf
    └── scanned_report.pdf
```

**After Processing:**
```
project/
├── process.py
├── input_pdfs/
│   └── (your PDFs)
└── output/
    ├── document1/
    │   ├── document1.md
    │   └── figures/
    │       ├── page1_img0.png
    │       └── page3_img0.jpg
    ├── document2/
    │   ├── document2.md
    │   └── figures/
    └── scanned_report/
        ├── scanned_report.md
        └── figures/
```

## 📤 Output Structure

### Markdown File Format

```markdown
# Document Title
**Author:** Author Name
---

## Table of Contents
- Section 1 (Page 2)
  - Subsection 1.1 (Page 3)
- Section 2 (Page 5)

---

--- 

*Page 1*

--- 
## Introduction
This is the introduction text...

### Background
More detailed content...

--- *Tables Found on this Page* ---
### Table 1
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

![page1_img0.png](./figures/page1_img0.png)

--- 

*Page 2*

--- 
*(This page was processed with OCR)*
OCR extracted text content...
```

### Output Characteristics

✅ **Clean Formatting**
- Hierarchical headings (##, ###)
- Clear page separators
- OCR markers for transparency

✅ **Proper References**
- Images linked with relative paths
- Tables formatted as markdown
- Page numbers preserved

✅ **Organized Assets**
- All images in figures/ subfolder
- Descriptive filenames (page1_img0.png)
- One folder per document

---

## 🔧 Technical Specifications

### Performance Characteristics

| Metric | Specification |
|--------|---------------|
| **Processing Speed** | ~1-3 seconds per digital page |
| **OCR Speed** | ~5-10 seconds per scanned page |
| **Table Extraction** | ~2-5 seconds per table |
| **Memory Usage** | ~100-500 MB per document |
| **Supported PDF Versions** | 1.0 through 2.0 |

### Supported Content Types

| Content Type | Support Level | Notes |
|--------------|---------------|-------|
| **Text** | ✅ Full | Preserves formatting |
| **Headings** | ✅ Full | H2, H3 detection |
| **Bold/Italic** | ⚠️ Partial | Bold detected, italic not preserved |
| **Tables (Bordered)** | ✅ Full | Via Camelot lattice |
| **Tables (Borderless)** | ⚠️ Limited | May be missed |
| **Images** | ✅ Full | PNG, JPEG, etc. |
| **Diagrams** | ✅ Full | Extracted as images |
| **Hyperlinks** | ❌ No | Not preserved |
| **Annotations** | ❌ No | Not extracted |
| **Forms** | ❌ No | Not processed |

### File Format Support

**Input:**
- ✅ PDF 1.0 - 2.0
- ✅ Digital PDFs
- ✅ Scanned PDFs
- ✅ Mixed PDFs

**Output:**
- ✅ Markdown (.md)
- ✅ Images (PNG, JPEG, etc.)

---

## ⚠️ Limitations and Future Enhancements

### Current Limitations

1. **Borderless Tables**
   - May not detect tables without visible borders
   - Could miss tables formatted with whitespace only

2. **Complex Layouts**
   - Multi-column text may not maintain perfect column order
   - Sidebars and text boxes treated as regular content

3. **Heading Detection**
   - Relies on bold + font size
   - May miss headings formatted differently
   - No detection of H1 (assumes document title is H1)

4. **Hyperlinks**
   - Internal and external links not preserved
   - No anchor link generation

5. **Mathematical Equations**
   - Not specially handled
   - May appear as garbled text
   - LaTeX equations not detected

6. **Language Support**
   - OCR configured for English only
   - Could support other languages with configuration

### Future Enhancement Opportunities

#### Short Term (Easy)
- ✅ Add command-line arguments for folder paths
- ✅ Implement logging instead of print statements
- ✅ Add progress bars for large documents
- ✅ Configuration file for thresholds
- ✅ Support for additional OCR languages

#### Medium Term (Moderate Complexity)
- 📊 Improve multi-column detection and ordering
- 📊 Enhanced borderless table detection
- 📊 Preserve hyperlinks in markdown format
- 📊 Better handling of headers/footers
- 📊 Extract form fields and data

#### Long Term (Complex)
- 🚀 Machine learning for layout analysis
- 🚀 Mathematical equation detection and LaTeX conversion
- 🚀 Chart/graph data extraction
- 🚀 Semantic understanding of document structure
- 🚀 Support for batch processing with parallel execution
- 🚀 Web interface for document upload
- 🚀 API endpoint for integration

### Known Issues

**Issue 1: OCR Performance**
- **Problem:** OCR can be slow for documents with many scanned pages
- **Workaround:** Process in batches or use cloud OCR services
- **Future Fix:** Implement parallel page processing

**Issue 2: Table Detection**
- **Problem:** Camelot sometimes misses complex table layouts
- **Workaround:** Manual review of output
- **Future Fix:** Try 'stream' flavor or implement hybrid approach

**Issue 3: Memory Usage**
- **Problem:** Large documents (>500 pages) may consume significant memory
- **Workaround:** Process in smaller batches
- **Future Fix:** Implement streaming processing

---
