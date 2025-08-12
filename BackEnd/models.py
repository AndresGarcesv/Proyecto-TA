from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Profesora(Base):
    __tablename__ = "profesoras"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=True)
    especialidad = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activa = Column(Boolean, default=True)
    
    # Relaciones
    asistencias = relationship("Asistencia", back_populates="profesora")
    clases = relationship("Clase", back_populates="profesora")

class Asistencia(Base):
    __tablename__ = "asistencias"
    
    id = Column(Integer, primary_key=True, index=True)
    profesora_id = Column(Integer, ForeignKey("profesoras.id"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    presente = Column(Boolean, nullable=False)
    observaciones = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    profesora = relationship("Profesora", back_populates="asistencias")

class Clase(Base):
    __tablename__ = "clases"
    
    id = Column(Integer, primary_key=True, index=True)
    profesora_id = Column(Integer, ForeignKey("profesoras.id"), nullable=False)
    titulo = Column(String(200), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    ubicacion = Column(String(100), nullable=False)  # "Colegio" o "Centro TecnoAcademia"
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    activa = Column(Boolean, default=True)
    
    # Relaciones
    profesora = relationship("Profesora", back_populates="clases")