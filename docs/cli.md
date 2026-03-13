# CLI Usage

Simple resume parsing from command line.

## Commands

### Basic parsing (extract all fields)
```bash
python3 -m pyresparser.command_line <resume_file>
```

### Selective extraction (use config file)
```bash
python3 -m pyresparser.command_line <resume_file> --config-file <config.json>
```

## Examples

### Parse a resume with default settings

```bash
python3 -m pyresparser.command_line resume.pdf
```

Output:
```
📄 Parsing: resume.pdf

✅ Success! Data saved to: output/Resume_Name_20260314_010703.json

EXTRACTED DATA:
{...extracted data...}
```

### Parse with selective field extraction

```bash
python3 -m pyresparser.command_line resume.pdf --config-file extraction_config.json
```

Output:
```
📄 Parsing: resume.pdf
📋 Using config: extraction_config.json

✅ Success! Data saved to: output/Resume_Name_20260314_010704.json

EXTRACTED DATA:
{...only requested fields...}
```

### Parse from different locations

```bash
# From current directory
python3 -m pyresparser.command_line resume.pdf

# From subdirectory
python3 -m pyresparser.command_line ./resumes/resume.pdf

# With full path
python3 -m pyresparser.command_line /home/user/documents/resume.pdf
```

## Configuration (Optional)

Create a JSON config file to specify which fields to extract:

```json
{
  "fields": {
    "name": true,
    "email": true,
    "mobile_number": true,
    "skills": false,
    "college_name": false,
    "degree": false,
    "designation": false,
    "experience": false,
    "company_names": false,
    "total_experience": false,
    "no_of_pages": false
  }
}
```

- Set field to `true` to extract it
- Set field to `false` to skip it (result will be `null`)
- Template file `extraction_config.json` has all fields set to `true` by default

## Output

- ✓ Data automatically saved to `output/` folder
- ✓ Filename format: `Name_YYYYMMDD_HHMMSS.json`
- ✓ Easy to find and manage

## Supported Formats

- PDF files
- DOCX files