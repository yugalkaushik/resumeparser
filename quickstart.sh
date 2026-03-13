#!/bin/bash

# PyResParser Quick Start Script
# This script sets up and runs PyResParser locally

set -e

echo "🚀 PyResParser Quick Start Setup"
echo "=================================="

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}1. Checking Python installation...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $python_version found${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}2. Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}2. Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}3. Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${BLUE}4. Upgrading pip...${NC}"
pip install --quiet --upgrade pip
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install dependencies
echo -e "${BLUE}5. Installing dependencies...${NC}"
pip install --quiet -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Download spaCy model
echo -e "${BLUE}6. Downloading spaCy NLP model...${NC}"
python -m spacy download en_core_web_sm --quiet
echo -e "${GREEN}✓ spaCy model downloaded${NC}"

# Download NLTK data
echo -e "${BLUE}7. Downloading NLTK data...${NC}"
python -m nltk.downloader words stopwords --quiet
echo -e "${GREEN}✓ NLTK data downloaded${NC}"

# Verify installation
echo -e "${BLUE}8. Verifying installation...${NC}"
python -c "from pyresparser import ResumeParser; print('✓ Package verification passed')"
echo -e "${GREEN}✓ Installation verified${NC}"

echo ""
echo -e "${GREEN}=================================="
echo "✓ Setup complete!"
echo "==================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run CLI: python3 -m pyresparser.command_line -f resume.pdf"
echo "3. Use in Python:"
echo "   from pyresparser import ResumeParser"
echo "   data = ResumeParser('resume.pdf').get_extracted_data()"
echo ""
echo -e "${BLUE}Documentation: See SETUP_GUIDE.md for detailed usage${NC}"
