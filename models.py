from pydantic import BaseModel, Field


class Todo(BaseModel):
    task: str = Field(..., description="Task name", max_length=100)
    task_desc: str = Field(..., description="Task description", max_length=500)
    done: bool = False
