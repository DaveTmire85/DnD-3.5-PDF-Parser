#!/bin/bash

# Check if Python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install Python3 before continuing."
    exit
fi

# Install pip if not installed
if ! command -v pip3 &> /dev/null
then
    echo "Pip is not installed. Installing pip..."
    sudo apt-get install python3-pip -y
fi

# Install MongoDB if not installed
if ! command -v mongod &> /dev/null
then
    echo "MongoDB is not installed. Installing MongoDB..."
    sudo apt-get install -y mongodb
fi

# Start MongoDB service
sudo service mongodb start

# Install Python dependencies
pip3 install -r requirements.txt

# Prompt the user for the path to the PDF directory
echo "Please enter the path to the directory containing your DnD PDFs:"
read pdf_dir

# Store the PDF directory in config.py
echo "PDF_DIRECTORY = '$pdf_dir'" > config/config.py

# Run the Python script
echo "Running the PDF parser..."
python3 parse_pdfs.py