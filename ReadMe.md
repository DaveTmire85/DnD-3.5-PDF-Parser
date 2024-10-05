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

2. Set up MongoDB on Ubuntu 22.04:

    To set up MongoDB on Ubuntu 22.04 for your project, follow these steps:

    1. Import the MongoDB Public GPG Key

    First, import the MongoDB GPG key to verify the packages:

    ```bash
    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo tee /etc/apt/trusted.gpg.d/mongodb-server-6.0.asc
    ```

    2. Create a List File for MongoDB

    Create a MongoDB repository list file for apt:

    ```bash
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    ```

    3. Update the Package Database

    Update the local package database:

    ```bash
    sudo apt-get update
    ```

    4. Install MongoDB

    Now install MongoDB:

    ```bash
    sudo apt-get install -y mongodb-org
    ```

    5. Start and Enable MongoDB Service

    After installation, start the MongoDB service:

    ```bash
    sudo systemctl start mongod
    ```

    Check if MongoDB is running:

    ```bash
    sudo systemctl status mongod
    ```

    To ensure MongoDB starts on boot, enable it:

    ```bash
    sudo systemctl enable mongod
    ```

    6. Access the MongoDB Shell

    Once MongoDB is running, you can access the MongoDB shell to test your setup:

    ```bash
    mongosh
    ```

    This will connect you to the MongoDB instance where you can run database commands, such as checking if the dnd_database has been created after running your script:

    ```
    show dbs
    ```

    7. Configuring MongoDB (Optional)

    MongoDB listens on localhost by default. If you want to access it remotely, you'll need to modify the MongoDB config file:

    ```bash
    sudo nano /etc/mongod.conf
    ```

    Find the following line:

    ```
    # network interfaces
    net:
      port: 27017
      bindIp: 127.0.0.1
    ```

    Change bindIp to:

    ```
    bindIp: 0.0.0.0
    ```

    Then restart MongoDB:

    ```bash
    sudo systemctl restart mongod
    ```

    Note: Allow MongoDB through the firewall if you are configuring remote access:

    ```bash
    sudo ufw allow 27017
    ```

    8. Setting Up Your Python Script to Use MongoDB

    Ensure that pymongo is installed (this would already be handled by your install.sh):

    ```bash
    pip3 install pymongo
    ```

    The script will now connect to MongoDB on the default localhost:27017, storing and managing your DnD data.

3. Run the installation script:

    ```bash
    ./install.sh
    ```

4. Follow the prompts to input your PDF directory, and the script will process all the PDFs and store the data in MongoDB.

## Usage
- The script `parse_pdfs.py` handles PDF processing and parsing.
- MongoDB will store parsed data in collections such as `races`, `classes`, `feats`, `skills`, `spells`, and `stat_blocks`.

## License
This project is licensed under the MIT License, and is pending approval from Wizards of the Coast® as of 05OCT2024.
