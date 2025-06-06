# Automated Literature Review Assistant

**Python script to parse BibTeX/text references, fetch missing DOIs, and generate a CSV/Excel for streamlined literature reviews.**

---

## 📋 Description

Over ten years of reviewing academic papers, I noticed how time-consuming it is to collect and organize bibliographic references. This “Automated Literature Review Assistant”:

- Parses all `.bib` or `.txt` files in a given folder for BibTeX entries  
- Looks up missing DOIs via CrossRef (and falls back to Google Scholar if needed)  
- Generates a CSV and Excel file with:
  - Clickable DOI links  
  - A “PDF Location” column (pointing to your folder)  
  - Full raw BibTeX entries  
  - A blank “Notes” column for manual annotations
-  Creates plots showing paper counts by **year** and **journal**, so you can visualize your literature distribution at a glance  
- Saves hours of manual data entry and formatting, freeing you to focus on reading and synthesis

---

## 🚀 Installation

1. **Clone the repository**
   git clone https://github.com/hedayatis/automated-lit-review-assistant.git
   cd automated-lit-review-assistant


⚙️ Usage
Place all your .bib and/or .txt files containing BibTeX entries into the same folder as literature_review.py.

(Optional) Add any plain‐text abstracts in files named <CitationKey>.txt if you want local abstracts to be used.

Run the main script:
python literature_review.py
After it finishes, you’ll find:

literature_review_final.csv

literature_review_final.xlsx (if you have openpyxl installed)

Both files will include:

Citation Key

Entry Type

Authors

Year

Title

Journal/Book Title

Volume / Issue / Pages / Publisher

DOI / URL (clickable in Excel)

Date Added

PDF Location (automatically set to your folder)

Notes (empty, for your manual comments)

Full Reference (raw BibTeX entry)

🎯 Citation
If you use this tool in your own work, please cite it in APA format:
Hedayati, S. (2025). Automated Literature Review Assistant [Computer software]. GitHub. https://github.com/hedayatis/automated-lit-review-assistant 

📝 License
This project is licensed under the MIT License. See LICENSE for details.
