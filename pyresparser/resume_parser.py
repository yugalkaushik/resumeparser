# Author: Omkar Pathak

import os
import multiprocessing as mp
import io
import json
import spacy
import pprint
from spacy.matcher import Matcher
from . import utils


class ResumeParser(object):

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None,
        config_file=None
    ):
        nlp = spacy.load('en_core_web_sm')
        # Try to load custom NER model, fallback to standard model if not available
        try:
            custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))
        except OSError:
            # Custom model not available, use standard model as fallback
            custom_nlp = nlp
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__config = self.__load_config(config_file)
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'college_name': None,
            'degree': None,
            'designation': None,
            'experience': None,
            'company_names': None,
            'no_of_pages': None,
            'total_experience': None,
        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = utils.extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()
    
    def __load_config(self, config_file):
        """Load extraction configuration from JSON file"""
        if config_file is None:
            # Default: extract all fields
            return {
                'name': True,
                'email': True,
                'mobile_number': True,
                'skills': True,
                'college_name': True,
                'degree': True,
                'designation': True,
                'experience': True,
                'company_names': True,
                'no_of_pages': True,
                'total_experience': True,
            }
        
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                return config_data.get('fields', {})
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"⚠️  Config file '{config_file}' not found or invalid. Using defaults.")
            return self.__load_config(None)

    def get_extracted_data(self):
        """Get extracted data filtered by configuration"""
        return self.__apply_config_filter()
    
    def __apply_config_filter(self):
        """Filter extracted data based on config file"""
        filtered_data = {}
        
        for field, should_extract in self.__config.items():
            if should_extract:
                # Include field from details (will be None if not found)
                filtered_data[field] = self.__details.get(field, None)
            else:
                # Field not requested, set to None
                filtered_data[field] = None
        
        return filtered_data

    def __get_basic_details(self):
        cust_ent = utils.extract_entities_wih_custom_model(
                            self.__custom_nlp
                        )
        name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        skills = utils.extract_skills(
                    self.__nlp,
                    self.__noun_chunks,
                    self.__skills_file
                )
        entities = utils.extract_entity_sections_grad(self.__text_raw)

        # extract name
        try:
            self.__details['name'] = cust_ent['Name'][0]
        except (IndexError, KeyError):
            self.__details['name'] = name

        # extract email
        self.__details['email'] = email

        # extract mobile number
        self.__details['mobile_number'] = mobile

        # extract skills
        self.__details['skills'] = skills

        # extract education section
        if 'education' in entities and len(entities['education']) > 0:
            edu_section = entities['education']
            # First line usually contains degree
            if len(edu_section) > 0:
                self.__details['degree'] = edu_section[0].strip()
            # Second line usually contains college name
            if len(edu_section) > 1:
                self.__details['college_name'] = edu_section[1].strip()

        # extract designation (from experience section if available)
        if 'experience' in entities and len(entities['experience']) > 0:
            exp_section = entities['experience']
            # Look for designation/title patterns in first few lines
            for line in exp_section[:3]:
                line_lower = line.lower()
                if any(title in line_lower for title in ['engineer', 'developer', 'analyst', 'manager', 'lead', 'designer', 'architect']):
                    self.__details['designation'] = line.strip()
                    break

        # extract company names from ORG entities
        if 'ORG' in cust_ent:
            # Filter out tech terms and common words that aren't companies
            non_company_words = {
                'javascript', 'typescript', 'python', 'java', 'c', 'sql', 'c++', 'c#',
                'html', 'html5', 'css', 'node', 'node.js', 'react', 'angular', 'vue', 'vue.js',
                'git', 'github', 'linux', 'unix', 'windows',
                'education', 'experience', 'projects', 'skills', 'certifications',
                'data structures', 'algorithms', 'programming', 'coding', 'framework',
                'database', 'sql', 'mysql', 'postgresql', 'mongodb',
                'api', 'rest', 'graphql', 'microservices', 'architecture',
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ci/cd',
                'agile', 'scrum', 'kanban', 'testing', 'automation',
                'object-oriented', 'design patterns', 'solid', 'dry',
                'semantic', 'processing', 'foundation'  # Known false positives
            }
            companies = [
                org for org in cust_ent['ORG'] 
                if org.lower() not in non_company_words and len(org) > 2 and ' ' in org or len(org) > 5
            ]
            if companies:
                self.__details['company_names'] = list(set(companies))

        # extract experience
        try:
            self.__details['experience'] = entities['experience']
            try:
                exp = round(
                    utils.get_total_experience(entities['experience']) / 12,
                    2
                )
                self.__details['total_experience'] = exp
            except KeyError:
                self.__details['total_experience'] = 0
        except KeyError:
            self.__details['total_experience'] = 0
        
        self.__details['no_of_pages'] = utils.get_number_of_pages(
                                            self.__resume
                                        )
        return


def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes/'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [
        pool.apply_async(
            resume_result_wrapper,
            args=(x,)
        ) for x in resumes
    ]

    results = [p.get() for p in results]

    pprint.pprint(results)
