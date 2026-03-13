# PyResParser

A simple resume parser used for extracting information from resumes.

**Auto-saves extracted data to `output/` folder as JSON!**

## Quick Start

### 1. Setup (One-time)

```bash
cd /home/yugalkaushik/projects/pyresparser

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -m nltk.downloader words stopwords
```

### 2. Run - Parse a Resume

```bash
python3 -m pyresparser.command_line resume.pdf
```

That's it! Data is automatically saved to `output/Resume_Name_TIMESTAMP.json`

### 3. (Optional) Selective Field Extraction

Create a config file to extract only specific fields:

```bash
python3 -m pyresparser.command_line resume.pdf --config-file extraction_config.json
```

See [CLI Documentation](cli.md) for configuration details.

## Extracted Data

Example output:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "mobile_number": "9876543210",
  "skills": ["Python", "JavaScript", "React", "Django"],
  "total_experience": 5.5,
  "college_name": "MIT",
  "company_names": ["Google"],
  "experience": [...],
  "no_of_pages": 2
}
```

## Features

- ✓ Parse resume (PDF/DOCX)
- ✓ Extract: name, email, phone, skills
- ✓ Extract: experience, company, education
- ✓ Auto-save to JSON in `output/` folder
- ✓ Fast and accurate

## Output Location

All parsed resumes are saved in:
```
output/
└── Resume_Name_YYYYMMDD_HHMMSS.json
```

```
[
  {
    'college_name': ['Marathwada Mitra Mandal’s College of Engineering'],
    'company_names': None,
    'degree': ['B.E. IN COMPUTER ENGINEERING'],
    'designation': ['Manager',
                    'TECHNICAL CONTENT WRITER',
                    'DATA ENGINEER'],
    'email': 'omkarpathak27@gmail.com',
    'mobile_number': '8087996634',
    'name': 'Omkar Pathak',
    'no_of_pages': 3,
    'skills': ['Operating systems',
              'Linux',
              'Github',
              'Testing',
              'Content',
              'Automation',
              'Python',
              'Css',
              'Website',
              'Django',
              'Opencv',
              'Programming',
              'C',
              ...],
    'total_experience': 1.83
  }
]
```

## Supported Resume File Formats

- Parsing of PDF and DOCx files are supported on all Operating Systems
- If you want to parse DOC files you can install [textract](https://textract.readthedocs.io/en/stable/installation.html) for your OS (Linux, MacOS)
- Note: You just have to install textract (and nothing else) and doc files will get parsed easily

# Advanced Options

## Explicitly specifying skills file

Pyresparser comes with built-in skills file that defaults to many technical skills. You can find the default skills file [here](https://github.com/OmkarPathak/pyresparser/blob/master/pyresparser/skills.csv).

For extracting data against your specified skills, create a CSV file with no headers.

```python
from pyresparser import ResumeParser
data = ResumeParser('/path/to/resume/file', skills_file='/path/to/skills.csv').get_extracted_data()
```

## Explicitly providing regex to parse phone numbers

While pyresparser parses most of the phone numbers correctly, there is a possibility of new patterns being added in near future. Hence, we can explicitly provide the regex required to parse the desired phone numbers. This can be done using

```python
from pyresparser import ResumeParser
data = ResumeParser('/path/to/resume/file', custom_regex='pattern').get_extracted_data()
```