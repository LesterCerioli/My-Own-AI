from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class LLMBase(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        pass
    
class LearningPattern(BaseModel):
    input_pattern: str
    output_pattern: str
    language: str
    content: Dict[str, Any]
    configdence_score: float
    usage_count: int
    
    