from enum import Enum


class AutoNumber(Enum):
	def __new__(cls, name):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value, name
		return obj

	def __int__(self):
		return self._value_[0]

	def __str__(self):
		return self._value_[1]


class ArticleStates(AutoNumber):
	AVAILABLE = 'Disponible'
	BORROWED = 'Prestado'
	REPAIRING = 'En reparación'
	LOST = 'Perdido'


class PlaceStates(AutoNumber):
	AVAILABLE = 'Disponible'
	BORROWED = 'Prestado'
	REPAIRING = 'En reparación'


class LoanStates(AutoNumber):
	PROCESSING = 'En proceso'
	APPROVED = 'Aprobado'
	REJECTED = 'Rechazado'
	EXPIRED = 'Caducado'
	FINISHED = 'Finalizado'


class ReservationStates(AutoNumber):
	PROCESSING = 'En proceso'
	APPROVED = 'Aprobada'
	REJECTED = 'Rechazada'
	FINISHED = 'Finalizada'

