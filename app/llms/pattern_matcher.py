import re
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher
from app.llms.base import LearningPattern
import logging

logger = logging.getLogger(__name__)

class PatternMatcher:
    def __init__(self):
        self.patterns_cache = {}

    def find_similar_patterns(self, requirements: str, language: str, all_patterns: List[LearningPattern]) -> List[Dict]:
        """Encontra padrões similares baseados nos requisitos e linguagem"""
        similar_patterns = []
        
        for pattern in all_patterns:
            if pattern.language.lower() != language.lower():
                continue
                
            similarity_score = self._calculate_similarity(requirements, pattern.input_pattern)
            combined_score = self._calculate_combined_score(similarity_score, pattern)
            
            if combined_score > 0.3:  
                similar_patterns.append({
                    'pattern': pattern,
                    'similarity_score': similarity_score,
                    'combined_score': combined_score
                })
                
        similar_patterns.sort(key=lambda x: x['combined_score'], reverse=True)
        return similar_patterns[:5]  # Retorna top 5

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade entre dois textos"""
        
        seq_similarity = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return seq_similarity
            
        jaccard_similarity = len(words1.intersection(words2)) / len(words1.union(words2))
        
        
        return (seq_similarity + jaccard_similarity) / 2

    def _calculate_combined_score(self, similarity: float, pattern: LearningPattern) -> float:
        """Calculate combined score considering similarity, confidence, and usage"""
        confidence_weight = pattern.confidence_score / 100.0
        usage_weight = min(pattern.usage_count / 100.0, 1.0)  
        
        return (similarity * 0.5) + (confidence_weight * 0.3) + (usage_weight * 0.2)

    def extract_requirements_pattern(self, requirements: str) -> Dict[str, Any]:
        """Extracts patterns from requirements for future learning."""
        patterns = {
            'frameworks': self._extract_frameworks(requirements),
            'libraries': self._extract_libraries(requirements),
            'architectures': self._extract_architecture(requirements),
            'complexity': self._assess_complexity(requirements)
        }
        return patterns

    def _extract_frameworks(self, text: str) -> List[str]:
        frameworks = ['fastapi', 'django', 'flask', 'fiber', 'gin', 'react', 'vue', 'angular', 'spring', 'express', 'nextjs']
        found = []
        for framework in frameworks:
            if framework in text.lower(): 
                found.append(framework)
        return found

    def _extract_libraries(self, text: str) -> List[str]:
        libraries = ['sqlalchemy', 'pydantic', 'jwt', 'oauth', 'redis', 'celery']
        found = []
        for lib in libraries:
            if lib in text.lower():
                found.append(lib)
        return found

    def _extract_architecture(self, text: str) -> List[str]:
        architectures = ['microservices', 'monolith', 'mvc', 'mvvm', 'rest', 'graphql']
        found = []
        for arch in architectures:
            if arch in text.lower():
                found.append(arch)
        return found

    def _assess_complexity(self, text: str) -> str:
        complexity_indicators = {
            'low': ['simple', 'basic', 'crud', 'single'],
            'medium': ['authentication', 'api', 'database', 'multiple'],
            'high': ['microservices', 'distributed', 'real-time', 'scalable', 'complex']
        }
        
        text_lower = text.lower()
        score = 0
        for level, indicators in complexity_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    if level == 'low':
                        score += 1
                    elif level == 'medium':
                        score += 2
                    else:
                        score += 3
        
        if score >= 6:
            return 'high'
        elif score >= 3:
            return 'medium'
        else:
            return 'low'