from sqlalchemy.orm import Mapped, mapped_column, relationship
#from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    #task_ids: Mapped[Optional[int]] = mapped_column(ForeignKey("task.id"))
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self, include_task_ids = False, include_goal_id_in_tasks = False):
        goal_as_dict = {"id": self.id, 
                "title": self.title,
                "tasks": [task.to_dict(include_goal_id = include_goal_id_in_tasks) for task in self.tasks]
                }
    
        if not self.tasks:
            goal_as_dict["tasks"] = []
        if include_task_ids and self.tasks:
            goal_as_dict["task_ids"] = [task.id for task in self.tasks]

        return goal_as_dict
    
    #def to_dict_add_keys():

    
    @classmethod
    def from_dict(cls, goal_data):
        # task_ids = goal_data.get("task_ids")
        # task_id_list = [task.id for task in task_ids]
        
        new_goal = cls(title = goal_data["title"])
                    #tasks = Task()
            
        return new_goal
