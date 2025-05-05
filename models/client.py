import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom_complet = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telephone = Column(String(50))
    nom_entreprise = Column(String(100))
    date_creation = Column(DateTime)
    derniere_maj = Column(DateTime)

    commercial_id = Column(
        UUID(as_uuid=True),
        ForeignKey('collaborateurs.id')
        )
    commercial = relationship(
        'Collaborateur',
        back_populates='clients',
        foreign_keys=[commercial_id]
        )

    contrats = relationship(
        'Contrat',
        back_populates='client',
        foreign_keys='Contrat.client_id'
        )
    
    def __str__(self):
        return self.nom_complet
