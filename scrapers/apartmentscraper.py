from abc import ABCMeta, abstractmethod

class ApartmentScraper:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def getAllApartments(self): pass
    