import json
from typing import Dict, Any, List
from app.llms.base import LearningPattern
import logging

logger = logging.getLogger(__name__)

class ResponseAnalyzer:
    def __init__(self):
        self.quality_metrics = {}

    def analyze_response_quality(self, requirements: str, generated_response: Dict, language: str) -> Dict[str, Any]:
        """Analyze response quality generated"""
        quality_score = 0
        feedback = []
                
        structure_score = self._analyze_structure(generated_response)
        quality_score += structure_score * 0.3
        
        if structure_score > 0.7:
            feedback.append("✅ Well-organized structure.")
        else:
            feedback.append("⚠️ The structure needs improvement.")
        
        completeness_score = self._analyze_completeness(generated_response, requirements)
        quality_score += completeness_score * 0.4
        
        if completeness_score > 0.7:
            feedback.append("✅ Fully functional and complete code.")
        else:
            feedback.append("⚠️ Incomplete code.")
        
        relevance_score = self._analyze_relevance(requirements, generated_response)
        quality_score += relevance_score * 0.3
        
        if relevance_score > 0.7:
            feedback.append("✅ Meets the requirements.")
        else:
            feedback.append("⚠️ Not very relevant to the requirements")

        return {
            'quality_score': min(quality_score, 1.0),
            'feedback': feedback,
            'structure_score': structure_score,
            'completeness_score': completeness_score,
            'relevance_score': relevance_score
        }

    def _analyze_structure(self, response: Dict) -> float:
        """Analyzes the structure of the response."""
        score = 0.0
        
        if 'files' in response:
            files = response['files']
            if len(files) > 0:
                score += 0.3
              
            
            config_files = [f for f in files if any(ext in f['path'] for ext in ['.json', '.yml', '.yaml', '.toml', '.ini'])]
            if config_files:
                score += 0.2
            
            
            main_files = [f for f in files if any(term in f['path'].lower() for term in ['main', 'app', 'index', 'server'])]
            if main_files:
                score += 0.2
                
            
            has_folders = any('/' in f['path'] for f in files)
            if has_folders:
                score += 0.3
        
        return min(score, 1.0)

    def _analyze_completeness(self, response: Dict, requirements: str) -> float:
        """Analyzes the completeness of the generated code."""
        score = 0.0
        requirements_lower = requirements.lower()
        
        if 'files' not in response:
            return 0.0
            
        files = response['files']
        total_content_length = sum(len(f.get('content', '')) for f in files)
        
        
        if total_content_length > 1000:
            score += 0.3
        elif total_content_length > 500:
            score += 0.2
        else:
            score += 0.1

        
        if 'authentication' in requirements_lower:
            auth_files = [f for f in files if any(term in f['path'].lower() for term in ['auth', 'login', 'user'])]
            if auth_files:
                score += 0.2
        
        if 'database' in requirements_lower:
            db_files = [f for f in files if any(term in f['path'].lower() for term in ['model', 'schema', 'database', 'db'])]
            if db_files:
                score += 0.2
        
        if 'api' in requirements_lower:
            api_files = [f for f in files if any(term in f['path'].lower() for term in ['route', 'api', 'endpoint', 'controller'])]
            if api_files:
                score += 0.2

        return min(score, 1.0)

    def _analyze_relevance(self, requirements: str, response: Dict) -> float:
        """Analyzes the relevance in relation to the requirements."""
        requirements_words = set(requirements.lower().split())
        response_text = json.dumps(response).lower()
        response_words = set(response_text.split())
        
        common_words = requirements_words.intersection(response_words)
        
        if not requirements_words:
            return 0.0
            
        return len(common_words) / len(requirements_words)

    def extract_learning_pattern(self, requirements: str, response: Dict, quality_analysis: Dict) -> LearningPattern:
        """Extracts a learning pattern from the response."""
        return LearningPattern(
            input_pattern=requirements[:500],  
            output_pattern=json.dumps(response)[:1000],  
            language=self._detect_language(response),
            context={
                'quality_score': quality_analysis['quality_score'],
                'structure_score': quality_analysis['structure_score'],
                'requirements_complexity': self._assess_requirements_complexity(requirements)
            },
            confidence_score=quality_analysis['quality_score'] * 100,
            usage_count=1
        )

    def _detect_language(self, response: Dict) -> str:
        """Detects the primary language based on the generated files."""
        if 'files' not in response:
            return 'unknown'
            
        extensions = {}
        for file in response['files']:
            path = file['path']
            if '.' in path:
                ext = path.split('.')[-1].lower()
                extensions[ext] = extensions.get(ext, 0) + 1
        
        if not extensions:
            return 'unknown'
            
        
        lang_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'java': 'java',
            'cpp': 'c++',
            'c': 'c',
            'go': 'go',
            'rs': 'rust',
            'php': 'php',
            'rb': 'ruby'
        }
        
        main_ext = max(extensions.items(), key=lambda x: x[1])[0]
        return lang_map.get(main_ext, main_ext)

    def _assess_requirements_complexity(self, requirements: str) -> str:
        """Evaluates the complexity of the requirements."""
        word_count = len(requirements.split())
        if word_count < 50:
            return 'low'
        elif word_count < 150:
            return 'medium'
        else:
            return 'high'