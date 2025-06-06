import os
import re
import time
import requests
import pandas as pd
from datetime import datetime

# scholarly is used to scrape Google Scholar for a DOI if CrossRef fails
from scholarly import scholarly

def simple_bibtex_parser_with_raw(bib_content):
    """
    Basic BibTeX parser extracting fields and raw entry.
    """
    entries = []
    for chunk in bib_content.split('@')[1:]:
        raw_entry = '@' + chunk.strip()
        header, body = chunk.split('{', 1)
        entry_type = header.strip().split()[0]
        citation_key, rest = body.split(',', 1)
        fields = {}
        for match in re.finditer(r'(\w+)\s*=\s*\{([^}]*)\}', rest, flags=re.DOTALL):
            key = match.group(1).lower()
            value = match.group(2).strip().replace('\n', ' ')
            fields[key] = value
        entry = {
            'ID': citation_key.strip(),
            'ENTRYTYPE': entry_type.lower(),
            'raw': raw_entry,
            **fields
        }
        entries.append(entry)
    return entries

def query_crossref_for_doi(title, author=None, max_retries=3, pause=1.0):
    """
    Query CrossRef REST API for a given title (and optional author string).
    Returns the DOI if found, or None otherwise.
    """
    base_url = "https://api.crossref.org/works"
    params = {
        'query.title': title,
        'rows': 1
    }
    if author:
        params['query.author'] = author

    for attempt in range(max_retries):
        try:
            resp = requests.get(base_url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get('message', {}).get('items', [])
                if items:
                    return items[0].get('DOI')
                else:
                    return None
            else:
                time.sleep(pause)
        except Exception:
            time.sleep(pause)
    return None

def query_scholar_for_doi(title):
    """
    Use the scholarly library to search Google Scholar by title and extract DOI from returned 'bib' metadata.
    Returns the DOI if found, else None.
    """
    try:
        search_gen = scholarly.search_pubs(title)
        first_result = next(search_gen, None)
        if first_result and 'bib' in first_result:
            bib = first_result['bib']
            return bib.get('doi', None)
    except Exception:
        pass
    return None

# === CONFIGURATION: folder containing your .bib/.txt files ===
bib_folder = '.'
current_dir = os.path.abspath(bib_folder)

all_entries = []
for filename in os.listdir(bib_folder):
    if filename.lower().endswith(('.bib', '.txt')):
        with open(os.path.join(bib_folder, filename), encoding='utf-8') as f:
            content = f.read()
            entries = simple_bibtex_parser_with_raw(content)
            all_entries.extend(entries)

rows = []
for entry in all_entries:
    title = entry.get('title', '')
    authors = entry.get('author', '')

    # 1. If a DOI already exists in the BibTeX entry, use it.
    existing_doi = entry.get('doi', '').strip()
    if existing_doi:
        doi_to_use = existing_doi
    else:
        # 2. Try CrossRef
        doi_to_use = query_crossref_for_doi(title, authors)
        time.sleep(0.2)
        # 3. If CrossRef fails, try Google Scholar
        if not doi_to_use:
            doi_to_use = query_scholar_for_doi(title)
            time.sleep(0.2)

    # Build the clickable DOI link if a DOI was found
    if doi_to_use:
        doi_url = f"https://doi.org/{doi_to_use}"
        hyperlink = f'=HYPERLINK("{doi_url}", "{doi_url}")'
    else:
        hyperlink = ''

    row = {
        'Citation Key': entry.get('ID', ''),
        'Entry Type': entry.get('ENTRYTYPE', ''),
        'Authors': authors,
        'Year': entry.get('year', ''),
        'Title': title,
        'Journal/Book Title': entry.get('journal', entry.get('booktitle', '')),
        'Volume': entry.get('volume', ''),
        'Issue': entry.get('number', ''),
        'Pages': entry.get('pages', ''),
        'Publisher': entry.get('publisher', ''),
        'DOI / URL': hyperlink,
        'Date Added': datetime.today().strftime('%Y-%m-%d'),
        'PDF Location': current_dir,
        'Notes': '',
        'Full Reference': entry.get('raw', '')
    }
    rows.append(row)

columns = [
    'Citation Key', 'Entry Type', 'Authors', 'Year', 'Title',
    'Journal/Book Title', 'Volume', 'Issue', 'Pages', 'Publisher',
    'DOI / URL', 'Date Added', 'PDF Location', 'Notes', 'Full Reference'
]

df = pd.DataFrame(rows, columns=columns)

# Save to CSV
df.to_csv('literature_review_final.csv', index=False)

# Save to Excel (requires openpyxl)
try:
    df.to_excel('literature_review_final.xlsx', index=False)
except ModuleNotFoundError:
    print("openpyxl not installed; only CSV was created.")

# Print first few rows to confirm
print(df.head())
