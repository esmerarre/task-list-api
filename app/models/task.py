from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None]

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "is_complete": True if self.completed_at != None else False}
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title = task_data["title"],
                        description = task_data["description"],
                        completed_at = None if ("is_complete" not in task_data or task_data["is_complete"] is False) else cls.completed_at)
        
        return new_task

