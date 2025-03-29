from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False, unique=True)   # commercial, gestion, support

    collaborateurs = relationship('Collaborateur', back_populates='role')

class Collaborateur(Base):
    __tablename__ = 'collaborateurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    role = relationship('Role', back_populates='collaborateurs')
    password_hash = Column(String(255), nullable=False)

    clients = relationship('Client', back_populates='contact_commercial')
    contrats_gestion = relationship('Contrat', back_populates='contact_gestion', foreign_keys='Contrat.contact_gestion_id')

    evenements_support = relationship('Evenement', back_populates='contact_support', foreign_keys='Evenement.contact_support_id')
    evenements_commercial = relationship('Evenement', back_populates='contact_commercial', foreign_keys='Evenement.contact_commercial_id')

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    nom_complet = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telephone = Column(String(50))
    nom_entreprise = Column(String(100))
    date_creation = Column(DateTime)
    derniere_maj = Column(DateTime)

    contact_commercial_id = Column(Integer, ForeignKey('collaborateurs.id'))
    contact_commercial = relationship('Collaborateur', back_populates='clients')

    contrats = relationship('Contrat', back_populates='client')

class Contrat(Base):
    __tablename__ = 'contrats'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    montant_total = Column(Float, nullable=False)
    montant_restant = Column(Float, nullable=False)
    date_creation = Column(DateTime)
    statut_signe = Column(Boolean, default=False)

    client = relationship('Client', back_populates='contrats')

    contact_gestion_id = Column(Integer, ForeignKey('collaborateurs.id'))
    contact_gestion = relationship('Collaborateur', back_populates='contrats_gestion')

    evenement = relationship('Evenement', back_populates='contrat', uselist=False)

class Evenement(Base):
    __tablename__ = 'evenements'
    id = Column(Integer, primary_key=True)
    contrat_id = Column(Integer, ForeignKey('contrats.id'))
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    lieu = Column(String(255))
    nombre_participants = Column(Integer)
    notes = Column(String(500))

    contrat = relationship('Contrat', back_populates='evenement')

    contact_commercial_id = Column(Integer, ForeignKey('collaborateurs.id'))
    contact_commercial = relationship('Collaborateur', back_populates='evenements_commercial', foreign_keys=[contact_commercial_id])

    contact_support_id = Column(Integer, ForeignKey('collaborateurs.id'))
    contact_support = relationship('Collaborateur', back_populates='evenements_support', foreign_keys=[contact_support_id])
