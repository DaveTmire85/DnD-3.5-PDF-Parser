import fitz  # PyMuPDF
import re
import sqlite3
import os
from android.content import Context
from android.net import Uri
from java import jclass

def create_database(context):
    db_path = os.path.join(context.getFilesDir().getAbsolutePath(), "dnd_database.sqlite")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for table in ['races', 'classes', 'feats', 'skills', 'spells', 'stat_blocks']:
        c.execute(f'''CREATE TABLE IF NOT EXISTS {table}
                     (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
    conn.commit()
    return conn

def extract_text_without_graphics(context, uri):
    try:
        input_stream = context.getContentResolver().openInputStream(Uri.parse(uri))
        doc = fitz.open(stream=input_stream, filetype="pdf")
        full_text = []
        
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text.append(page.get_text())
        
        return "\n".join(full_text)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def identify_and_parse_dnd_data(text):
    parsed_data = {
        'races': [],
        'classes': [],
        'feats': [],
        'skills': [],
        'spells': [],
        'stat_blocks': []
    }
    
    patterns = {
        'races': r"Race: (.+)",
        'classes': r"Class: (.+)",
        'feats': r"Feat: (.+)",
        'skills': r"Skill: (.+)",
        'spells': r"Spell: (.+)",
        'stat_blocks': r"Stat Block: (.+)"
    }
    
    for category, pattern in patterns.items():
        parsed_data[category] = re.findall(pattern, text)
    
    return parsed_data

def store_in_sqlite(conn, data):
    c = conn.cursor()
    for category, entries in data.items():
        for entry in entries:
            c.execute(f"INSERT OR IGNORE INTO {category} (name) VALUES (?)", (entry,))
    conn.commit()

def process_pdfs_in_directory(context, directory_uri):
    conn = create_database(context)
    
    results = []
    directory = context.getContentResolver().getTreeDocumentUri(Uri.parse(directory_uri))
    child_documents = context.getContentResolver().queryChildDocuments(directory, None, None)

    total_pdfs = sum(1 for _ in child_documents if _.getString(1) == "application/pdf")
    child_documents.moveToPosition(-1)  # Reset cursor

    processed_pdfs = 0

    while child_documents.moveToNext():
        document_uri = jclass("android.provider.DocumentsContract").buildChildDocumentsUriUsingTree(
            directory_uri, child_documents.getString(0))
        mime_type = child_documents.getString(1)
        display_name = child_documents.getString(2)

        if mime_type == "application/pdf":
            try:
                results.append({"title": f"Processing {display_name}", "content": "Started"})
                text = extract_text_without_graphics(context, str(document_uri))
                
                parsed_data = identify_and_parse_dnd_data(text)
                store_in_sqlite(conn, parsed_data)
                
                processed_pdfs += 1
                progress = (processed_pdfs / total_pdfs) * 100
                
                results.append({
                    "title": f"Finished processing {display_name}",
                    "content": f"Progress: {progress:.2f}%\nData stored in SQLite."
                })
                
                # Add detailed results
                for category, entries in parsed_data.items():
                    if entries:
                        results.append({
                            "title": f"{category.capitalize()} found in {display_name}",
                            "content": ", ".join(entries[:5]) + ("..." if len(entries) > 5 else "")
                        })
            except Exception as e:
                results.append({
                    "title": f"Error processing {display_name}",
                    "content": str(e)
                })

    child_documents.close()
    conn.close()
    return results

# This function will be called from the Android app
def main(context, directory_uri):
    return process_pdfs_in_directory(context, directory_uri)