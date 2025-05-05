import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Evenement(Base):
    __tablename__ = 'evenements'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(255), nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    lieu = Column(String(255), nullable=False)
    nombre_participants = Column(Integer, nullable=False, default=1)
    notes = Column(String)
    date_creation = Column(DateTime, nullable=False)
    derniere_maj = Column(DateTime)

    contrat_id = Column(UUID(as_uuid=True), ForeignKey('contrats.id'), nullable=False)
    contrat = relationship(
        'Contrat',
        back_populates='evenement',
        foreign_keys=[contrat_id]
        )

    commercial_id = Column(
        UUID(as_uuid=True),
        ForeignKey('collaborateurs.id')
        )
    commercial = relationship(
        'Collaborateur',
        back_populates='evenements_commercial',
        foreign_keys=[commercial_id]
        )

    support_id = Column(
        UUID(as_uuid=True),
        ForeignKey('collaborateurs.id'),
        nullable=True
        )
    support = relationship(
        'Collaborateur',
        back_populates='evenements_support',
        foreign_keys=[support_id]
        )

    def __str__(self):
        return f"{self.nom} ({str(self.id)})"