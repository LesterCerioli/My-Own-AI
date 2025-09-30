import json
import requests
from typing import Dict, Any
from app.llms.base import LLMBase
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class DeepSeekLLM(LLMBase):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        max_tokens = kwargs.get('max_tokens', 4000)
        temperature = kwargs.get('temperature', 0.7)
        
        payload = {
            "model": "deepseek-coder",
            "messages": [
                {
                    "role": "system",
                    "content": self._build_system_prompt(kwargs.get('learning_context'))
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            try:
                structured_response = json.loads(content)
                structured_response['tokens_used'] = result.get('usage', {}).get('total_tokens', 0)
                return structured_response
            except json.JSONDecodeError:
                return self._parse_code_blocks(content)
                
        except Exception as e:
            logger.error(f"DeepSeek LLM error: {str(e)}")
            raise

    def _build_system_prompt(self, learning_context: Dict = None) -> str:
        base_prompt = """You are an expert software architect. Generate complete file structures with actual code implementation. Return JSON format with files array containing path and content."""
        
        if learning_context and learning_context.get('patterns'):
            base_prompt += "\n\nLearning Context from previous successful projects:\n"
            for pattern in learning_context['patterns'][:3]:  # Top 3 patterns
                base_prompt += f"- Input: {pattern['input_pattern'][:100]}...\n"
                base_prompt += f"  Output Pattern: {pattern['output_pattern'][:200]}...\n"
        
        return base_prompt

    def _parse_code_blocks(self, content: str) -> Dict[str, Any]:
        files = []
        lines = content.split('\n')
        current_file = None
        current_content = []
        
        for line in lines:
            if line.startswith('```') and ':' in line:
                if current_file and current_content:
                    files.append({
                        "path": current_file,
                        "content": '\n'.join(current_content[:-1] if current_content else '')
                    })
                current_file = line.replace('```', '').strip().split(':')[-1].strip()
                current_content = []
            elif current_file and not line.startswith('```'):
                current_content.append(line)
        
        if current_file and current_content:
            files.append({
                "path": current_file,
                "content": '\n'.join(current_content)
            })
        
        return {
            "files": files, 
            "structure_explanation": "Generated from code blocks",
            "tokens_used": 0
        }

    def get_model_name(self) -> str:
        return "deepseek-coder"