from sqlalchemy.orm import Mapped, mapped_column, relationship
#from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_as_dict = {"id": self.id, 
                "title": self.title, 
                "description": self.description, 
                "is_complete": True if self.completed_at != None else False}
        
        if self.goal:
            task_as_dict["goal"] = self.goal.title

        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id")
        new_task = cls(title = task_data["title"],
                        description = task_data["description"],
                        completed_at = None if ("is_complete" not in task_data 
                                                or task_data["is_complete"] is False) 
                                                else cls.completed_at,
                        goal_id = goal_id)
        
        return new_task

