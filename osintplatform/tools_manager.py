from abc import ABC, abstractmethod
nbre_outils = 5

class Commande(ABC):
    @abstractmethod
    def executer(self):
        pass

class requestCommande(Commande):
    

class ActionneurDoutils:
    request = []
    extractData = []
    storeData = []
    renderData = []
    def __init__(self):
        for i in range(nbre_outils):
            self.request[i] = Commande()
            self.extractData[i] = Commande()
            self.storeData[i] = Commande()
            self.renderData[i] = Commande()

