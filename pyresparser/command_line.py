# Author: Omkar Pathak

import os
import argparse
from pprint import pprint
import sys
from pyresparser import ResumeParser, JSONHandler


class ResumeParserCli(object):

    def __init__(self):
        self.__parser = argparse.ArgumentParser(description='Resume Parser - Extract information from resumes')
        self.__parser.add_argument(
            'file',
            help="path to resume file to be parsed")
        self.__parser.add_argument(
            '--config-file',
            type=str,
            default=None,
            help="optional path to extraction_config.json to specify which fields to extract")

    
    def parse(self):
        """Parse resume and save to output folder"""
        args = self.__parser.parse_args()
        
        # Check if file exists
        if not os.path.exists(args.file):
            print(f"❌ Error: File '{args.file}' not found")
            sys.exit(1)
        
        # Check if config file exists (if provided)
        if args.config_file and not os.path.exists(args.config_file):
            print(f"❌ Error: Config file '{args.config_file}' not found")
            sys.exit(1)
        
        # Parse resume
        print(f"📄 Parsing: {args.file}")
        if args.config_file:
            print(f"📋 Using config: {args.config_file}")
        try:
            resume_parser = ResumeParser(args.file, config_file=args.config_file)
            extracted_data = resume_parser.get_extracted_data()
        except Exception as e:
            print(f"❌ Error parsing resume: {e}")
            sys.exit(1)
        
        # Save to JSON
        handler = JSONHandler()
        filepath = handler.save_single_resume(extracted_data)
        
        # Print results
        print(f"\n✅ Success! Data saved to: {filepath}\n")
        print("=" * 70)
        print("EXTRACTED DATA:")
        print("=" * 70)
        pprint(extracted_data)
        
        return extracted_data


def main():
    cli_obj = ResumeParserCli()
    cli_obj.parse()


if __name__ == '__main__':
    main()
