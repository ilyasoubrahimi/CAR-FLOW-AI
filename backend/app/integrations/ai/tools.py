from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class ToolResult(BaseModel):
    tool_name: str
    output: Any

class AI_Tool_Registry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._definitions: Dict[str, ToolDefinition] = {}

    def register(self, name: str, func: Callable, description: str, parameters: Dict[str, Any]):
        self._tools[name] = func
        self._definitions[name] = ToolDefinition(name=name, description=description, parameters=parameters)

    async def execute(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"Tool {tool_name} not found")
        return await self._tools[tool_name](**kwargs)

    def get_definitions(self) -> List[ToolDefinition]:
        return list(self._definitions.values())

tool_registry = AI_Tool_Registry()
