import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Collaborateur(Base):
    __tablename__ = 'collaborateurs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    role = relationship(
        'Role', back_populates='collaborateurs', foreign_keys=[role_id])

    clients = relationship(
        'Client',
        back_populates='commercial',
        foreign_keys='Client.commercial_id'
    )
    contrats = relationship(
        'Contrat',
        back_populates='gestionnaire',
        foreign_keys='Contrat.gestionnaire_id'
    )
    evenements_support = relationship(
        'Evenement',
        back_populates='support',
        foreign_keys='Evenement.support_id'
    )
    evenements_commercial = relationship(
        'Evenement',
        back_populates='commercial',
        foreign_keys='Evenement.commercial_id'
    )

    def __str__(self):
        return self.nom
