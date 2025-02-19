import json
from pathlib import Path
from pydantic import BaseModel, ValidationError
from typing import Dict

class PromptTemplate(BaseModel):
    name: str
    template: str
    context_fields: list[str]

class PromptManager:
    def __init__(self, prompt_templates : Dict):
        self.templates = self._load_prompts(prompt_templates)
        
    def _load_prompts(self, prompt_templates) -> Dict[str, PromptTemplate]:
        print('########prompt_templates ',prompt_templates)
        templates = {}
        for data in prompt_templates:
            try:
                print('data',data)
                print('template',prompt_templates[data])
                template = PromptTemplate(**prompt_templates[data])
                templates[template.name] = template
            except ValidationError as e:
                print(f"Invalid prompt template: {e}")
        print('#######templates',templates)
        return templates

    def get_template(self, name: str) -> PromptTemplate:
        return self.templates.get(name)