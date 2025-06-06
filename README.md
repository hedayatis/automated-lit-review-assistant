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
- Saves hours of manual data entry and formatting, freeing you to focus on reading and synthesis

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hedayatis/automated-lit-review-assistant.git
   cd automated-lit-review-assistant
