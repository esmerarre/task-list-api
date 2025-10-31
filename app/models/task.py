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



