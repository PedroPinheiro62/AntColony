#Pedro Pinheiro TD4
#Groupe A1a

from tkinter import * #importation de tkinter
from Colonie import * #importation des classes définies en forme.py

#définition de la classe ZoneAffichage
class ZoneAffichage(Canvas):
    def __init__(self,parent, w, h, c): #Constructeur de la classe ZoneAffichage
        Canvas.__init__(self, width = w, height = h, bg = c) #Heritage de la classe Canvas
        
#définition de la classe Civilisation
class Civilisation(Tk):
    def __init__(self): #Constructeur de la classe FenPrincipale
        Tk.__init__(self) #Heritage de la classe Tk
        self.title('Colonie de Fourmis') #ajoute le title à la Fenetre Principale
        
        #définition et positionnement du Frame pour les Boutons
        self.__frBut = Frame(self)
        self.__frBut.pack(side = TOP,padx = 5,pady = 5)
        
        #définition et positionnement des Boutons pour commencer la simulation et fermer la fennetre.
        self.__boutonBegin = Button(self.__frBut,text = 'Begin Simulation', width = 15, command = self.simulation).pack(side = LEFT,padx = 5,pady = 5)
        self.__boutonQuit = Button(self.__frBut,text = 'Quit',width = 15, command = self.destroy).pack(side = RIGHT,padx = 5,pady = 5)
        
        #définition de la taille, couleur et postionnement de la Zone de Affichage du Dessin
        self.__zoneAffichage = ZoneAffichage(self, 800, 800, 'white')
        self.__zoneAffichage.pack(padx = 5,pady = 5)  
        
        #Liste de routes
        self.__routes = []
        
        #Création des villes. Elles n'ont pas encore ses aretes
        self.__vA = Ville('A',100,400,[],'nid',self.__zoneAffichage)
        self.__vB = Ville('B',200,300,[],'int',self.__zoneAffichage)
        self.__vC = Ville('C',200,600,[],'int',self.__zoneAffichage)
        self.__vD = Ville('D',400,400,[],'int',self.__zoneAffichage)
        self.__vE = Ville('E',400,700,[],'int',self.__zoneAffichage)
        self.__vF = Ville('F',100,200,[],'int',self.__zoneAffichage)
        self.__vG = Ville('G',500,500,[],'food',self.__zoneAffichage)
        self.__vH = Ville('H',600,600,[],'int',self.__zoneAffichage)
        self.__vI = Ville('I',400,200,[],'int',self.__zoneAffichage)
        self.__vJ = Ville('J',750,300,[],'int',self.__zoneAffichage)       
        
        #Création des routes.
        self.__routes.append(Route([self.__vA,self.__vB],self.__zoneAffichage))
        self.__routes.append(Route([self.__vA,self.__vC],self.__zoneAffichage))
        self.__routes.append(Route([self.__vB,self.__vD],self.__zoneAffichage))
        self.__routes.append(Route([self.__vC,self.__vE],self.__zoneAffichage))
        self.__routes.append(Route([self.__vC,self.__vD],self.__zoneAffichage))
        self.__routes.append(Route([self.__vE,self.__vH],self.__zoneAffichage))
        self.__routes.append(Route([self.__vA,self.__vF],self.__zoneAffichage))
        self.__routes.append(Route([self.__vD,self.__vG],self.__zoneAffichage))
        self.__routes.append(Route([self.__vF,self.__vI],self.__zoneAffichage))
        self.__routes.append(Route([self.__vI,self.__vB],self.__zoneAffichage))
        self.__routes.append(Route([self.__vI,self.__vD],self.__zoneAffichage))
        self.__routes.append(Route([self.__vI,self.__vJ],self.__zoneAffichage))
        self.__routes.append(Route([self.__vD,self.__vJ],self.__zoneAffichage))
        self.__routes.append(Route([self.__vJ,self.__vG],self.__zoneAffichage))
        
        #Nombre de Fourmis initial
        self.__numF = 2

        #Liste de fourmis
        self.__fourmis = []

        #Mis en place de la quantité initiale de phéromone dans chaque route       
        for routeI in self.__routes:
            routeI.set_phero(self.__numF/routeI.get_taille())
         
        #Création des fourmis au début       
        for i in range(self.__numF):
            self.__fourmis.append(Ant(self.__vA,(i+1),self.__zoneAffichage)) 
        
        self.__iter = 0 #Counter de iterações
        
        self.__qo = 0.5 #Paramètre q0 de l'environnment

        #Choix aléatoire des meilleurs travailleurs et explorateurs       
        self.__bestTravs = [self.__fourmis[0],self.__fourmis[1]]
        self.__bestExps = [self.__fourmis[0],self.__fourmis[1]]
        
        #Counter avant prochaine selection naturelle
        self.__selectionNaturelle = len(self.__fourmis)
        
        #Plus petit chemin entre tous
        self.__allShort = []

        #Taille du plus petit chemin entre tous        
        self.__minTaille = math.inf
        
        #Variable boolénne que décide si la simulation continue ou non
        self.__go = 1
        
        #Counter de cycles évolutifs
        self.__cycles = 0
        
    #Fonction qui simule l'environnment            
    def simulation(self):
        #Pour chaque fourmi
        for fourmi in self.__fourmis:
            if fourmi.get_cond() == 'ville': #Si dans une ville
                if fourmi.get_where().get_cond() == 'food': #Si dans la source
                    if fourmi.get_food() == 0: #Si n'a pas encore pris la nourriture
                        fourmi.prendre_nourriture() #Si non, prende la nourriture
                    else:
                        fourmi.getTendance(self.__qo) #Si oui, decide prochaine route
            
                elif fourmi.get_where().get_cond() == 'nid': #Si dans le nid
                    if fourmi.get_food() == 1: #Si n'a pas encore laissé la nourriture
                        if fourmi.get_qteNou() == 0: #Si premiere fois dans le cycle
                            self.__selectionNaturelle = self.__selectionNaturelle - 1 #Réduire counter de fourmis retournées
                        fourmi.add_qteNou() #Ajoute 1 à la quantité de nouriture aporté au nid 
                        fourmi.set_tailleT(0) # Reset la taille du chemin actuel
                        fourmi.set_chemin() #reset le chemin actuel
                        fourmi.memoryLost(self.__vA)  #reset la memoire de la fourmi
                        fourmi.laisser_nourriture() #laisse la nourriture 
                    else:
                        fourmi.memoryLost(self.__vA) #Si non, reset memoire et 
                        fourmi.getTendance(self.__qo) #choisi la prochaine route
                else:
                    fourmi.getTendance(self.__qo) #Si dans une ville intermediaire
            else:
                fourmi.marcher() #Si dans une route, il faut just marcher
        
        #Si tous les fourmis on déjà retourner au nid au moins une fois
        if self.__selectionNaturelle == 0:
            
            counter = 0 #Counter de combien ont pris le plus petit chemin actuel
            
            #Pour chaque fourmi
            for fourmi in self.__fourmis:
                taille = 0
                for route in fourmi.get_shortest(): #On voit la taille du plus petit chemin trouvé 
                    taille = taille + route.get_taille() #pendant le cycle actuel
                if taille < self.__minTaille: #Si taille plus petite que la plus petite taille actuel
                    self.__minTaille = taille #Nouveau plus petit chemin trouvé
                    self.__allShort =[]
                    
                    for route in self.__routes: #On reset le couleur du plus petit chemin ancienne 
                        route.reset_couleur() # dans le dessin
                    
                    for route in fourmi.get_shortest(): #On copie le nouveau plus petit chemin
                        self.__allShort.append(route)
                    
                    for route in fourmi.get_shortest(): #On affiche en jeune le nouveau plus petit
                        route.set_couleur()             #chemin dans le dessin
             
            #On compte combien de fourmis ont pris le plus petit chemin dans le cycle actuel       
            for fourmi in self.__fourmis:
                if fourmi.get_shortest() == self.__allShort:
                    counter = counter + 1
                else:
                    if(len(self.__fourmis)>2):
                        fourmi.extinct()
                        self.__fourmis.remove(fourmi)
            
            #On choix un critère d'arrète pour la simulation
            if (counter/len(self.__fourmis)) >= 0.95:
                self.__go = 0
            else:
                self.__go = 1
              
            #On evapore le pheromone dans toutes les routes
            for route in self.__routes:
                route.evaporation()
            
            #On depose le pheromone sur les plus petit chemins
            for fourmi in self.__fourmis:
                fourmi.deposer_pheromone_global()
            
            #On selectione les meilleurs travaileurs et explorateurs
            for fourmi in self.__fourmis:
                if (self.__bestExps[0].get_timesR(self.__routes) < self.__bestExps[1].get_timesR(self.__routes)):
                    aux = self.__bestExps[0]
                    self.__bestExps[0] = self.__bestExps[1]
                    self.__bestExps[1] = aux
                
                else:
                    if fourmi.get_timesR(self.__routes) > self.__bestExps[0].get_timesR(self.__routes):
                        self.__bestExps[1] = self.__bestExps[0]
                        self.__bestExps[0] = fourmi
                    elif fourmi.get_timesR(self.__routes) > self.__bestExps[1].get_timesR(self.__routes) and fourmi != self.__bestExps[0]:
                        self.__bestExps[1] = fourmi
                
                if (self.__bestTravs[0].get_qteNou() < self.__bestTravs[1].get_qteNou()):
                    aux = self.__bestTravs[0]
                    self.__bestTravs[0] = self.__bestTravs[1]
                    self.__bestTravs[1] = aux
                
                else:
                    if fourmi.get_qteNou() > self.__bestTravs[0].get_qteNou():
                        self.__bestTravs[1] = self.__bestTravs[0]
                        self.__bestTravs[0] = fourmi
                    elif fourmi.get_qteNou() > self.__bestTravs[1].get_qteNou() and fourmi != self.__bestTravs[0]:
                        self.__bestTravs[1] = fourmi  
            
            #On reset les valeurs de nourriture apportée au nid et le vecteur de routes utilisées        
            for fourmi in self.__fourmis:
                fourmi.set_qteNou(0) 
                fourmi.set_timesR()
        
            #Crossover - Création de deux nouvelles fourmis
            self.__fourmis.append(newAnt(self.__bestTravs[0],self.__bestTravs[1],self.__vA,self.__iter+self.__numF+1,self.__zoneAffichage))
            self.__fourmis.append(newAnt(self.__bestExps[0],self.__bestExps[1],self.__vA,self.__iter+self.__numF+2,self.__zoneAffichage))
        
            #Chance de migration de une fourmi aleatoire 
            mig = random.randint(1,100)
            if mig <= 10:
                self.__fourmis.append(Ant(self.__vA,(self.__iter),self.__zoneAffichage))
            
            #On reset le competeur pour la prochaine selection naturelle
            self.__selectionNaturelle = len(self.__fourmis)
            
            #On ajoute un au nombre de cycles évolutifs
            self.__cycles = self.__cycles + 1
        
        #On Ajoute un au nombre de iterations general 
        self.__iter = self.__iter +1    
        
        #On verifie si les criteres d'arrrete sont atteintes
        if self.__go == 1 or len(self.__fourmis) < 100: #Si non, continue
            self.__zoneAffichage.after(1,self.simulation)
        
        #Si oui, affiche les résultats trouvés
        else:
            print("Debut Alive =",self.__numF,", NOW = ",len(self.__fourmis))
            print("PCC Trouvé = ")
            for route in self.__allShort:
                print(route.get_ft()[0].get_nom(),'-',route.get_ft()[1].get_nom())
            print("Taille PCC = ",self.__minTaille)
            print("Num de Iter = ",self.__iter)
            print("Num de Cycles = ",self.__cycles)
            print("Alpha Trav = ",self.__bestTravs[0].get_alpha())
            print("Beta Trav = ", self.__bestTravs[0].get_beta())
            print("Alpha Exp = ", self.__bestExps[0].get_alpha())
            print("Beta Exp = ", self.__bestExps[0].get_beta())
                    
# Création de la fenêtre principale
Civ = Civilisation()
Civ.mainloop()
