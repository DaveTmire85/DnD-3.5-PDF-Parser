# DnD 3.5 PDF Parser and Compendium Builder

This project is designed to parse Dungeons and Dragons 3.5 sourcebook PDFs, extract relevant game data (races, classes, feats, skills, spells, and stat blocks), and store it in a MongoDB database. It also provides prompts for missing or incomplete data, and ensures all parsed data is formatted correctly.

## Features
- Extracts data from PDFs while preserving important tables and diagrams.
- Prompts for missing data and ensures proper formatting using regular expressions.
- Stores parsed data in a MongoDB NoSQL database for easy querying.
- Supports batch processing of multiple PDFs.

## Requirements
- Python 3.x
- PyMuPDF (`fitz`)
- PyMongo
- MongoDB

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/DaveTmire85/DnD-3.5-PDF-Parser.git
    cd DnD-3.5-PDF-Parser
    ```

2. Run the installation script:

    ```bash
    ./install.sh
    ```

3. Follow the prompts to input your PDF directory, and the script will process all the PDFs and store the data in MongoDB.

## Usage
- The script `parse_pdfs.py` handles PDF processing and parsing.
- MongoDB will store parsed data in collections such as `races`, `classes`, `feats`, `skills`, `spells`, and `stat_blocks`.

## License
This project is licensed under the MIT License, and is pending approval from Wizards of the Coast® as of 05OCT2024.