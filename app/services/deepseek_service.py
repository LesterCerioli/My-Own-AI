import json
import requests
from app.config import settings
from app.schemas import DeepSeekRequest
import logging

logger = logging.getLogger(__name__)

class DeepSeekService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate_project_structure(self, requirements: str, language: str) -> dict:
        prompt = self._build_prompt(requirements, language)
        
        payload = {
            "model": "deepseek-coder",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert software architect. Generate complete file structures with actual code implementation. Return JSON format with files array containing path and content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, try to extract code blocks
                return self._parse_code_blocks(content)
                
        except Exception as e:
            logger.error(f"DeepSeek API error: {str(e)}")
            raise

    def _build_prompt(self, requirements: str, language: str) -> str:
        return f"""
        Create a complete project structure for a {language} application with the following requirements:
        
        {requirements}
        
        Return your response as a JSON object with this structure:
        {{
            "files": [
                {{
                    "path": "path/to/file.ext",
                    "content": "complete file content here"
                }}
            ],
            "structure_explanation": "Brief explanation of the project structure"
        }}
        
        Include all necessary files: configuration files, source code, documentation, etc.
        Make sure the code is complete and functional.
        """

    def _parse_code_blocks(self, content: str) -> dict:
        
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
        
        return {"files": files, "structure_explanation": "Generated from code blocks"}