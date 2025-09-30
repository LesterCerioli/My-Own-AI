from typing import Dict, Any, List
from app.llms.base import LLMBase
from app.config import settings
import requests
import json
import logging

logger = logging.getLogger(__name__)

class GolangFiberHexagonalLLM(LLMBase):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        system_prompt = self._build_golang_hexagonal_system_prompt()
        user_prompt = self._build_golang_user_prompt(prompt, kwargs.get('learning_context'))
        
        payload = {
            "model": "deepseek-coder",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "max_tokens": 6000,
            "temperature": 0.5
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return self._parse_golang_response(content)
                
        except Exception as e:
            logger.error(f"Golang Fiber Hexagonal LLM error: {str(e)}")
            raise

    def _build_golang_hexagonal_system_prompt(self) -> str:
        return """You are an expert in Golang, Fiber framework, PostgreSQL, Hexagonal Architecture, and SOLID principles.

CRITICAL: You MUST return ONLY valid JSON with this exact structure:
{
    "files": [
        {
            "path": "full/file/path.go",
            "content": "complete Go code here"
        }
    ],
    "architecture": {
        "type": "hexagonal",
        "layers": ["domain", "application", "infrastructure", "interfaces"],
        "principles": ["SOLID", "Clean Architecture"]
    },
    "dependencies": ["list of main dependencies"],
    "explanation": "brief architectural explanation"
}

GOLANG HEXAGONAL ARCHITECTURE REQUIREMENTS:

1. DOMAIN LAYER:
   - Entities (business objects)
   - Value objects
   - Repository interfaces
   - Domain services interfaces

2. APPLICATION LAYER:
   - Use cases / application services
   - DTOs (Data Transfer Objects)
   - Ports (interfaces)

3. INFRASTRUCTURE LAYER:
   - Repository implementations (PostgreSQL)
   - External service implementations
   - Database migrations
   - Configuration

4. INTERFACES LAYER:
   - HTTP handlers (Fiber)
   - Middlewares
   - API routes
   - JSON serialization

SOLID PRINCIPLES IMPLEMENTATION:
- Single Responsibility: Each file has one clear purpose
- Open/Closed: Open for extension, closed for modification
- Liskov Substitution: Interfaces properly defined
- Interface Segregation: Specific interfaces
- Dependency Inversion: Depend on abstractions, not concretions

TECHNICAL STACK:
- Fiber web framework
- PostgreSQL with pgx driver
- Clean package organization
- Proper error handling
- Structured logging
- Configuration management
- Database migrations
"""

    def _build_golang_user_prompt(self, requirements: str, learning_context: Dict = None) -> str:
        prompt = f"""
Create a complete Golang project using Fiber framework with Hexagonal Architecture and SOLID principles.

PROJECT REQUIREMENTS:
{requirements}

TECHNICAL SPECIFICATIONS:
- Language: Golang 1.21+
- Web Framework: Fiber v2
- Database: PostgreSQL with pgx driver
- Architecture: Hexagonal (Ports and Adapters)
- Principles: SOLID, Clean Code
- API: RESTful JSON API

REQUIRED FILES STRUCTURE:
- cmd/api/main.go - Application entry point
- internal/domain/ - Domain entities and interfaces
- internal/application/ - Use cases and services
- internal/infrastructure/ - Database, external implementations
- internal/interfaces/ - HTTP handlers, routes
- pkg/ - Shared utilities
- configs/ - Configuration files
- migrations/ - Database migrations
- go.mod, go.sum - Dependencies
- Dockerfile, docker-compose.yml - Containerization
- README.md - Project documentation

SPECIFIC IMPLEMENTATION DETAILS:
- Use dependency injection
- Implement proper error handling
- Add structured logging
- Include database migrations
- Add health check endpoints
- Implement proper middleware chain
- Use environment variables for configuration
- Include unit test examples

Return ONLY the JSON object with files array. No other text.
"""

        if learning_context and learning_context.get('patterns'):
            prompt += "\n\nLEARNING CONTEXT FROM PREVIOUS SUCCESSFUL PROJECTS:\n"
            for pattern in learning_context['patterns'][:2]:
                prompt += f"Previous successful pattern: {pattern['input_pattern'][:200]}...\n"

        return prompt

    def _parse_golang_response(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, creating fallback structure")
            return self._create_fallback_golang_structure()

    def _create_fallback_golang_structure(self) -> Dict[str, Any]:
        return {
            "files": [
                {
                    "path": "go.mod",
                    "content": "module hexagonal-app\n\ngo 1.21\n\nrequire (\n\tgithub.com/gofiber/fiber/v2 v2.50.0\n\tgithub.com/jackc/pgx/v5 v5.4.3\n)"
                },
                {
                    "path": "cmd/api/main.go",
                    "content": "package main\n\nimport (\n\t\"log\"\n\t\"hexagonal-app/internal/infrastructure\"\n\t\"hexagonal-app/internal/interfaces\"\n)\n\nfunc main() {\n\t// Initialize configuration\n\tcfg := infrastructure.LoadConfig()\n\t\n\t// Initialize database\n\tdb, err := infrastructure.NewPostgreSQLDB(cfg)\n\tif err != nil {\n\t\tlog.Fatal(err)\n\t}\n\t\n\t// Initialize HTTP server\n\tserver := interfaces.NewServer(db, cfg)\n\t\n\t// Start server\n\tlog.Printf(\"Server starting on port %s\", cfg.Port)\n\tif err := server.Start(); err != nil {\n\t\tlog.Fatal(err)\n\t}\n}"
                }
            ],
            "architecture": {
                "type": "hexagonal",
                "layers": ["domain", "application", "infrastructure", "interfaces"],
                "principles": ["SOLID", "Clean Architecture"]
            },
            "dependencies": ["fiber", "pgx", "viper", "testify"],
            "explanation": "Fallback Golang Fiber Hexagonal structure"
        }

    def get_model_name(self) -> str:
        return "golang-fiber-hexagonal"

class PythonFastAPIHexagonalLLM(LLMBase):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        system_prompt = self._build_python_hexagonal_system_prompt()
        user_prompt = self._build_python_user_prompt(prompt, kwargs.get('learning_context'))
        
        payload = {
            "model": "deepseek-coder",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "max_tokens": 6000,
            "temperature": 0.5
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return self._parse_python_response(content)
                
        except Exception as e:
            logger.error(f"Python FastAPI Hexagonal LLM error: {str(e)}")
            raise

    def _build_python_hexagonal_system_prompt(self) -> str:
        return """You are an expert in Python 3.12, FastAPI, PostgreSQL, Hexagonal Architecture, and SOLID principles.

CRITICAL: You MUST return ONLY valid JSON with this exact structure:
{
    "files": [
        {
            "path": "full/file/path.py",
            "content": "complete Python code here"
        }
    ],
    "architecture": {
        "type": "hexagonal",
        "layers": ["domain", "application", "infrastructure", "api"],
        "principles": ["SOLID", "Clean Architecture", "Dependency Injection"]
    },
    "dependencies": ["list of main dependencies"],
    "explanation": "brief architectural explanation"
}

PYTHON FASTAPI HEXAGONAL ARCHITECTURE REQUIREMENTS:

1. DOMAIN LAYER:
   - Entities (Pydantic models or dataclasses)
   - Value objects
   - Repository interfaces (ABC)
   - Domain exceptions

2. APPLICATION LAYER:
   - Use cases / services
   - DTOs (Data Transfer Objects)
   - Ports (abstract classes)

3. INFRASTRUCTURE LAYER:
   - Database models (SQLAlchemy)
   - Repository implementations
   - External service adapters
   - Database configuration

4. API LAYER:
   - FastAPI routers
   - Dependency injection
   - Request/response models
   - API documentation

SOLID PRINCIPLES IMPLEMENTATION:
- Single Responsibility: Each class has one reason to change
- Open/Closed: Extensible through abstractions
- Liskov Substitution: Proper inheritance hierarchy
- Interface Segregation: Specific interfaces
- Dependency Inversion: Depend on abstractions

TECHNICAL STACK:
- Python 3.12
- FastAPI with async/await
- SQLAlchemy 2.0+ with async
- Pydantic v2 for validation
- PostgreSQL with asyncpg
- Dependency injection
- Environment configuration
- Automated testing
"""

    def _build_python_user_prompt(self, requirements: str, learning_context: Dict = None) -> str:
        prompt = f"""
Create a complete Python 3.12 project using FastAPI with Hexagonal Architecture and SOLID principles.

PROJECT REQUIREMENTS:
{requirements}

TECHNICAL SPECIFICATIONS:
- Python 3.12 with type hints
- FastAPI with async/await
- SQLAlchemy 2.0+ (async)
- PostgreSQL with asyncpg
- Pydantic v2 for validation
- Architecture: Hexagonal (Ports and Adapters)
- Principles: SOLID, Clean Architecture, Dependency Injection

REQUIRED FILES STRUCTURE:
- app/main.py - FastAPI application entry point
- app/domain/ - Domain models and interfaces
- app/application/ - Use cases and services
- app/infrastructure/ - Database, external implementations
- app/api/ - FastAPI routers and endpoints
- app/core/ - Configuration, dependencies, security
- migrations/ - Database migrations (Alembic)
- tests/ - Unit and integration tests
- requirements.txt - Python dependencies
- Dockerfile, docker-compose.yml - Containerization
- .env.example - Environment variables template

SPECIFIC IMPLEMENTATION DETAILS:
- Use dependency injection with FastAPI Depends
- Implement proper async/await patterns
- Use SQLAlchemy 2.0 async patterns
- Add comprehensive error handling
- Include structured logging
- Add API documentation with examples
- Implement proper middleware
- Include health check endpoints
- Add unit tests with pytest
- Use environment-based configuration

Return ONLY the JSON object with files array. No other text.
"""

        if learning_context and learning_context.get('patterns'):
            prompt += "\n\nLEARNING CONTEXT FROM PREVIOUS SUCCESSFUL PROJECTS:\n"
            for pattern in learning_context['patterns'][:2]:
                prompt += f"Previous successful pattern: {pattern['input_pattern'][:200]}...\n"

        return prompt

    def _parse_python_response(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, creating fallback structure")
            return self._create_fallback_python_structure()

    def _create_fallback_python_structure(self) -> Dict[str, Any]:
        return {
            "files": [
                {
                    "path": "requirements.txt",
                    "content": "fastapi==0.104.1\nuvicorn==0.24.0\nsqlalchemy==2.0.23\nasyncpg==0.29.0\npydantic==2.5.0\npython-dotenv==1.0.0\nalembic==1.12.1\npytest==7.4.3\npytest-asyncio==0.21.1"
                },
                {
                    "path": "app/main.py",
                    "content": "from fastapi import FastAPI\nfrom app.core.config import settings\nfrom app.api.routes import api_router\nfrom app.infrastructure.database import init_db\n\napp = FastAPI(\n    title=settings.PROJECT_NAME,\n    version=settings.VERSION,\n    openapi_url=f\"{settings.API_V1_STR}/openapi.json\"\n)\n\napp.include_router(api_router, prefix=settings.API_V1_STR)\n\n@app.on_event(\"startup\")\nasync def startup_event():\n    await init_db()\n\n@app.get(\"/health\")\nasync def health_check():\n    return {\"status\": \"healthy\"}\n\nif __name__ == \"__main__\":\n    import uvicorn\n    uvicorn.run(app, host=\"0.0.0.0\", port=8000)"
                }
            ],
            "architecture": {
                "type": "hexagonal",
                "layers": ["domain", "application", "infrastructure", "api"],
                "principles": ["SOLID", "Clean Architecture", "Dependency Injection"]
            },
            "dependencies": ["fastapi", "sqlalchemy", "asyncpg", "pydantic"],
            "explanation": "Fallback Python FastAPI Hexagonal structure"
        }

    def get_model_name(self) -> str:
        return "python-fastapi-hexagonal"