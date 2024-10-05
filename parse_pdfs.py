import fitz  # PyMuPDF
import re
from pymongo import MongoClient
from config.config import PDF_DIRECTORY

# Initialize MongoDB connection
client = MongoClient('localhost', 27017)
db = client['dnd_database']  # Create or connect to a database
collection_names = ['races', 'classes', 'feats', 'skills', 'spells', 'stat_blocks']
collections = {name: db[name] for name in collection_names}

# Parsing logic to identify table headers
def is_table_or_diagram(text):
    """Check if the text looks like a table or diagram header (e.g., 'Table 1-2: Example Text')."""
    table_pattern = r"Table \d+-\d+:"
    return re.search(table_pattern, text) is not None

# Logic to remove non-text graphics
def extract_text_without_graphics(pdf_path):
    """Extract text from a PDF while removing non-text graphics but preserving tables and diagrams."""
    doc = fitz.open(pdf_path)
    full_text = []
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]  # Extract text blocks
        
        page_text = []
        for block in blocks:
            if block['type'] == 0:  # Text block
                block_text = block['lines']
                for line in block_text:
                    for span in line['spans']:
                        text = span['text']
                        if is_table_or_diagram(text):
                            page_text.append(text)
                        else:
                            page_text.append(text)
            # Skip non-text blocks (like images)
        
        full_text.append("\n".join(page_text))
    
    return "\n".join(full_text)

# Prompt for missing data based on type
def prompt_for_input(field, data_type):
    """Prompt the user for input when necessary, enforcing specific input formats (regex, numerical, etc.)."""
    while True:
        user_input = input(f"Please input the {field} ({data_type}): ")
        if data_type == 'regex':
            try:
                re.compile(user_input)
                return user_input
            except re.error:
                print("Invalid regex pattern. Try again.")
        elif data_type == 'numerical':
            if user_input.isdigit():
                return int(user_input)
            else:
                print("Please enter a valid number.")
        elif data_type == 'text':
            if user_input.strip():
                return user_input
            else:
                print("Text input cannot be empty.")
        else:
            print(f"Unknown data type {data_type}. Please try again.")

# Core parsing logic for identifying DnD content
def identify_and_parse_dnd_data(text):
    """Identify patterns for races, classes, feats, skills, spells, and stat blocks in the extracted text."""
    parsed_data = {
        'races': [],
        'classes': [],
        'feats': [],
        'skills': [],
        'spells': [],
        'stat_blocks': []
    }
    
    # Add your own parsing logic below, this is an example structure
    race_pattern = r"Race: (.+)"
    class_pattern = r"Class: (.+)"
    feat_pattern = r"Feat: (.+)"
    skill_pattern = r"Skill: (.+)"
    spell_pattern = r"Spell: (.+)"
    stat_block_pattern = r"Stat Block: (.+)"
    
    parsed_data['races'] = re.findall(race_pattern, text)
    parsed_data['classes'] = re.findall(class_pattern, text)
    parsed_data['feats'] = re.findall(feat_pattern, text)
    parsed_data['skills'] = re.findall(skill_pattern, text)
    parsed_data['spells'] = re.findall(spell_pattern, text)
    parsed_data['stat_blocks'] = re.findall(stat_block_pattern, text)
    
    return parsed_data

# Store parsed data into MongoDB
def store_in_mongodb(data):
    """Store parsed data into the appropriate MongoDB collections."""
    for category, entries in data.items():
        if category in collections:
            for entry in entries:
                if collections[category].find_one({"name": entry}) is None:
                    collections[category].insert_one({"name": entry})

# Process PDFs in the specified directory
def process_pdfs_in_directory(directory):
    """Process each PDF in the specified directory, extracting and storing relevant DnD data."""
    import os
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            print(f"Processing {filename}...")
            text = extract_text_without_graphics(pdf_path)
            
            parsed_data = identify_and_parse_dnd_data(text)
            store_in_mongodb(parsed_data)
            print(f"Finished processing {filename}. Data stored in MongoDB.")

# Main execution
if __name__ == "__main__":
    print(f"Starting PDF parsing in directory: {PDF_DIRECTORY}")
    process_pdfs_in_directory(PDF_DIRECTORY)
    print("All PDFs processed.")