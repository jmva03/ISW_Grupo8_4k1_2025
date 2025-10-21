from typing import Optional

from datetime import datetime
from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint, text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import datetime

class Base(DeclarativeBase):
    pass


class Actividad(Base):
    __tablename__ = 'actividad'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    requiere_talla: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    cupos_maximos: Mapped[int] = mapped_column(Integer, nullable=False)
    edad_minima: Mapped[Optional[int]] = mapped_column(Integer)

    turno: Mapped[list['Turno']] = relationship('Turno', back_populates='actividad')


class Turno(Base):
    __tablename__ = 'turno'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    actividad_id: Mapped[int] = mapped_column(ForeignKey('actividad.id'), nullable=False)
    inicio: Mapped[str] = mapped_column(Text, nullable=False)   # HH:MM
    fin: Mapped[str] = mapped_column(Text, nullable=False)      # HH:MM
    estado: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'abierto'"))
    cupos_disponibles: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("''"))  # YYYY-MM-DD

    actividad: Mapped['Actividad'] = relationship('Actividad', back_populates='turno')
    reserva: Mapped[list['Reserva']] = relationship('Reserva', back_populates='turno')


class Reserva(Base):
    __tablename__ = 'reserva'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    turno_id: Mapped[int] = mapped_column(ForeignKey('turno.id'), nullable=False)
    cantidad_personas: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'pendiente'"))
    tyc_aceptados: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))  # 0/1
    creada_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # <- cambiado a DateTime

    turno: Mapped['Turno'] = relationship('Turno', back_populates='reserva')
    reserva_participante: Mapped[list['ReservaParticipante']] = relationship('ReservaParticipante', back_populates='reserva')


class ReservaParticipante(Base):
    __tablename__ = 'reserva_participante'
    __table_args__ = (
        UniqueConstraint('reserva_id', 'dni'),
    )

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    reserva_id: Mapped[int] = mapped_column(ForeignKey('reserva.id'), nullable=False)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    dni: Mapped[str] = mapped_column(Text, nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    talla: Mapped[Optional[str]] = mapped_column(Text)

    reserva: Mapped['Reserva'] = relationship('Reserva', back_populates='reserva_participante')