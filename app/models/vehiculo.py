from abc import ABC

class Vehiculo:
    def __init__(self, patente, contacto):
        self.patente = patente
        self.contacto = contacto

    @property
    def contacto(self):
        return self.__contacto

    @contacto.setter
    def contacto(self, contacto):
        if not isinstance(contacto, int) or not len(contacto) == 9:
            raise ValueError("Número de contacto inválido")
        self.__contacto = contacto

    @property
    def patente(self):
        return self.__patente

    @patente.setter
    def patente(self, patente):
        if not len(patente) == 6:
            raise ValueError("La patente debe tener 6 caracteres")
        self.__patente = patente
    

    