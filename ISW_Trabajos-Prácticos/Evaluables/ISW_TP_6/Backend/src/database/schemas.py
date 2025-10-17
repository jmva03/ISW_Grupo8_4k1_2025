from typing import Optional

from sqlalchemy import ForeignKey, Integer, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Actividad(Base):
    __tablename__ = 'actividad'

    nombre: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    requiere_talla: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    cupos_maximos: Mapped[int] = mapped_column(Integer, nullable=False)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    edad_minima: Mapped[Optional[int]] = mapped_column(Integer)

    turno: Mapped[list['Turno']] = relationship('Turno', back_populates='actividad')


class Turno(Base):
    __tablename__ = 'turno'

    actividad_id: Mapped[int] = mapped_column(ForeignKey('actividad.id'), nullable=False)
    inicio: Mapped[str] = mapped_column(Text, nullable=False)
    fin: Mapped[str] = mapped_column(Text, nullable=False)
    estado: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'abierto'"))
    cupos_disponibles: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("''"))
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    actividad: Mapped['Actividad'] = relationship('Actividad', back_populates='turno')
    reserva: Mapped[list['Reserva']] = relationship('Reserva', back_populates='turno')


class Reserva(Base):
    __tablename__ = 'reserva'

    turno_id: Mapped[int] = mapped_column(ForeignKey('turno.id'), nullable=False)
    cantidad_personas: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'pendiente'"))
    tyc_aceptados: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    creada_en: Mapped[str] = mapped_column(Text, nullable=False)
    participantes: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    turno: Mapped['Turno'] = relationship('Turno', back_populates='reserva')
