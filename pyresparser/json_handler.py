# JSON Handler - Automatic resume data storage

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union


class JSONHandler:
    """Manages automatic JSON storage of extracted resume data"""
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize JSONHandler
        
        :param output_dir: Directory where JSON files will be stored
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save_single_resume(self, data: Dict, filename: str = None) -> Path:
        """
        Save a single resume's extracted data to JSON file
        
        :param data: Extracted resume data dictionary
        :param filename: Output filename (auto-generated if not provided)
        :return: Path to saved JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = data.get('name', 'Resume').replace(' ', '_')
            filename = f"{name}_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def save_batch_resumes(self, data_list: List[Dict], batch_name: str = None) -> Path:
        """
        Save multiple resumes' extracted data to a single JSON file
        
        :param data_list: List of extracted resume data dictionaries
        :param batch_name: Name for the batch file (auto-generated if not provided)
        :return: Path to saved JSON file
        """
        if batch_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            batch_name = f"batch_resumes_{timestamp}.json"
        
        filepath = self.output_dir / batch_name
        
        batch_data = {
            'timestamp': datetime.now().isoformat(),
            'total_resumes': len(data_list),
            'resumes': [
                {
                    'data': resume_data,
                    'processed_at': datetime.now().isoformat()
                }
                for resume_data in data_list
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_resume_data(self, filepath: str) -> Dict:
        """
        Load previously saved resume data from JSON file
        
        :param filepath: Path to JSON file
        :return: Resume data dictionary
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_saved_files(self) -> List[Path]:
        """
        List all saved JSON files in the output directory
        
        :return: List of JSON file paths
        """
        return sorted(self.output_dir.glob('*.json'))
    
    def get_latest_file(self) -> Path:
        """
        Get the most recently created JSON file
        
        :return: Path to latest file or None if no files exist
        """
        files = self.list_saved_files()
        return files[-1] if files else None
    
    def get_stats(self) -> Dict:
        """
        Get statistics about saved files
        
        :return: Dictionary with file statistics
        """
        files = self.list_saved_files()
        total_size = sum(f.stat().st_size for f in files)
        
        return {
            'total_files': len(files),
            'output_directory': str(self.output_dir.absolute()),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'files': [
                {
                    'name': f.name,
                    'size_bytes': f.stat().st_size,
                    'created': datetime.fromtimestamp(f.stat().st_ctime).isoformat()
                }
                for f in files
            ]
        }
