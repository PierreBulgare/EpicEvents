import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Contrat(Base):
    __tablename__ = 'contrats'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    montant_total = Column(Float(precision=2), nullable=False)
    montant_restant = Column(Float(precision=2), nullable=False)
    date_creation = Column(DateTime)
    statut_signe = Column(Boolean, default=False)
    date_signature = Column(DateTime, nullable=True)
    derniere_maj = Column(DateTime, nullable=True)

    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.id'))
    client = relationship(
        'Client',
        back_populates='contrats',
        foreign_keys=[client_id]
        )

    gestionnaire_id = Column(
        UUID(as_uuid=True),
        ForeignKey('collaborateurs.id')
        )
    gestionnaire = relationship(
        'Collaborateur',
        back_populates='contrats',
        foreign_keys=[gestionnaire_id]
        )

    evenement = relationship(
        'Evenement',
        back_populates='contrat',
        uselist=False,
        foreign_keys='Evenement.contrat_id'
        )

    def __str__(self):
        return str(self.id)