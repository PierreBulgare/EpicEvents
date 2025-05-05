from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.orm import relationship
from .base import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False, unique=True)

    collaborateurs = relationship(
        'Collaborateur',
        back_populates='role',
        foreign_keys='Collaborateur.role_id'
        )
    
    def __str__(self):
        return self.nom
