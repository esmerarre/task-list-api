from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self, include_tasks=False, include_task_ids = False, include_goal_id_in_tasks = False):
        goal_as_dict = {"id": self.id, 
                "title": self.title,
                }
    
        if include_tasks:
            goal_as_dict["tasks"] = []
        if self.tasks and include_tasks:
            goal_as_dict["tasks"] = [task.to_dict(include_goal_id = include_goal_id_in_tasks) for task in self.tasks]
        elif include_task_ids and self.tasks:
            goal_as_dict["task_ids"] = [task.id for task in self.tasks]

        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):        
        new_goal = cls(title = goal_data["title"]) 
        return new_goal
