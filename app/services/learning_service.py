from sqlalchemy.orm import Session
from app.models import LearningData
from app.schemas import LearningDataBase
import uuid
import logging

logger = logging.getLogger(__name__)

class LearningService:
    def __init__(self, db: Session):
        self.db = db

    def add_learning_pattern(self, input_pattern: str, output_pattern: str, language: str):
        
        existing = self.db.query(LearningData).filter(
            LearningData.language == language,
            LearningData.input_pattern.ilike(f"%{input_pattern}%")
        ).first()
        
        if existing:
            existing.usage_count += 1
            self.db.commit()
            return existing
        else:
            new_pattern = LearningData(
                id=uuid.uuid4(),
                input_pattern=input_pattern,
                output_pattern=output_pattern,
                language=language,
                usage_count=1
            )
            self.db.add(new_pattern)
            self.db.commit()
            self.db.refresh(new_pattern)
            return new_pattern

    def get_relevant_patterns(self, requirements: str, language: str, limit: int = 5):
        return self.db.query(LearningData).filter(
            LearningData.language == language,
            LearningData.input_pattern.ilike(f"%{requirements}%")
        ).order_by(LearningData.usage_count.desc()).limit(limit).all()

    def update_success_rate(self, pattern_id: uuid.UUID, success: bool):
        pattern = self.db.query(LearningData).filter(LearningData.id == pattern_id).first()
        if pattern:
            if success:
                pattern.success_rate = min(100, pattern.success_rate + 10)
            else:
                pattern.success_rate = max(0, pattern.success_rate - 5)
            self.db.commit()