from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.llms.base import LLMBase, LearningPattern
from app.llms.deepseek_llm import DeepSeekLLM
from app.llms.pattern_matcher import PatternMatcher
from app.llms.response_analyzer import ResponseAnalyzer
from app.models import LearningData
import uuid
import logging

logger = logging.getLogger(__name__)

class LearningOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.llm: LLMBase = DeepSeekLLM()
        self.pattern_matcher = PatternMatcher()
        self.response_analyzer = ResponseAnalyzer()
        self.learning_threshold = 0.7  

    def generate_with_learning(self, requirements: str, language: str) -> Dict[str, Any]:
        """Generate code using previous learning"""
        
        learning_patterns = self._get_relevant_learning_patterns(requirements, language)
                
        learning_context = self._build_learning_context(learning_patterns)
                
        response = self.llm.generate(requirements, learning_context=learning_context)
                
        quality_analysis = self.response_analyzer.analyze_response_quality(
            requirements, response, language
        )
                
        if quality_analysis['quality_score'] >= self.learning_threshold:
            self._learn_from_response(requirements, response, quality_analysis, language)
        
        return {
            'response': response,
            'quality_analysis': quality_analysis,
            'learning_used': len(learning_patterns) > 0
        }

    def _get_relevant_learning_patterns(self, requirements: str, language: str) -> List[LearningPattern]:
        """Gets relevant learning patterns from the database"""
        db_patterns = self.db.query(LearningData).filter(
            LearningData.language == language
        ).order_by(LearningData.success_rate.desc(), LearningData.usage_count.desc()).limit(50).all()
                
        patterns = []
        for db_pattern in db_patterns:
            patterns.append(LearningPattern(
                input_pattern=db_pattern.input_pattern,
                output_pattern=db_pattern.output_pattern,
                language=db_pattern.language,
                context={},  # Can be expanded
                confidence_score=db_pattern.success_rate,
                usage_count=db_pattern.usage_count
            ))
        
        return self.pattern_matcher.find_similar_patterns(requirements, language, patterns)

    def _build_learning_context(self, patterns: List[LearningPattern]) -> Dict[str, Any]:
        """Builds learning context for the LLM"""
        if not patterns:
            return {}
            
        return {
            'patterns': [
                {
                    'input_pattern': p.input_pattern,
                    'output_pattern': p.output_pattern,
                    'confidence': p.confidence_score
                }
                for p in patterns[:3]  # Limit to 3 patterns to avoid overloading
            ],
            'total_patterns_available': len(patterns),
            'average_confidence': sum(p.confidence_score for p in patterns) / len(patterns)
        }

    def _learn_from_response(self, requirements: str, response: Dict, 
                           quality_analysis: Dict, language: str):
        """Learns from high-quality responses"""
        try:
            # Extract learning pattern
            pattern = self.response_analyzer.extract_learning_pattern(
                requirements, response, quality_analysis
            )
                        
            existing_pattern = self.db.query(LearningData).filter(
                LearningData.language == language,
                LearningData.input_pattern.ilike(f"%{requirements[:100]}%")
            ).first()
            
            if existing_pattern:
                
                existing_pattern.usage_count += 1
                existing_pattern.success_rate = min(100, existing_pattern.success_rate + 5)
                existing_pattern.output_pattern = pattern.output_pattern
            else:
                
                new_pattern = LearningData(
                    id=uuid.uuid4(),
                    input_pattern=pattern.input_pattern,
                    output_pattern=pattern.output_pattern,
                    language=pattern.language,
                    success_rate=pattern.confidence_score,
                    usage_count=pattern.usage_count
                )
                self.db.add(new_pattern)
            
            self.db.commit()
            logger.info(f"New pattern learned for {language} with score {quality_analysis['quality_score']}")
            
        except Exception as e:
            logger.error(f"Error learning from response: {str(e)}")
            self.db.rollback()

    def get_learning_metrics(self) -> Dict[str, Any]:
        """Gets learning metrics"""
        total_patterns = self.db.query(LearningData).count()
        patterns_by_language = self.db.query(
            LearningData.language, 
            db.func.count(LearningData.id)
        ).group_by(LearningData.language).all()
        
        avg_success_rate = self.db.query(db.func.avg(LearningData.success_rate)).scalar() or 0
        
        return {
            'total_patterns': total_patterns,
            'patterns_by_language': dict(patterns_by_language),
            'average_success_rate': round(avg_success_rate, 2),
            'learning_threshold': self.learning_threshold
        }