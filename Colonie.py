#Pedro Pinheiro
#Colonie de Fourmis - Classes

from tkinter import * #importation de tkinter
import random
import math


# Classe Ville
class Ville:
    def __init__(self,name,x,y,arretes,cond,can):
        
        #Set condition choisie
        self.__cond = cond
        
        #Set la couleur qui correspond à sa condition
        if cond == 'nid':
            self.__c ='blue'
        
        elif cond == 'food':
            self.__c ='green'       
        
        else:
            self.__c = 'black'
          
        #Affiche à côte de son dessin dans l'environnement  
        can.create_text(x + 30, y + 30, text = name)
        
        #Set le nom, la position et les arretes
        self.__nom = name
        self.__xc = x
        self.__yc = y
        self.__mesArretes = arretes
        
        #Affiche son dessin dans l'environnement. Un Cercle
        self.__dessin = can.create_oval(self.__xc-30,self.__yc-30,self.__xc+30,self.__yc+30,fill=self.__c)
    
    #Retourne les arretes de cette ville    
    def get_arretes(self):
        return self.__mesArretes
    
    #Determine les arretes de cette ville
    def set_arretes(self,route):
        self.__mesArretes.append(route)
       
    #Retourne se la ville est une source de nourriture, le nid ou une ville intermediaire 
    def get_cond(self):
        return self.__cond
    
    #retourne la position de la ville dans l'environnement    
    def get_centre(self):
        return self.__xc,self.__yc
	 
    #retoune le nom de la ville   
    def get_nom(self):
        return self.__nom

#Classe Route     
class Route:
    def __init__(self,ft,can):
        self.__qtPhe = 0 #Quantité de phéromone
        self.__c = 'black' #Couleur
        self.__x1,self.__y1=ft[0].get_centre() #Coordonnées de ville 1
        self.__x2,self.__y2=ft[1].get_centre() #Coordonnées de ville 1
        #Taille de la route
        self.__taille = math.floor(math.sqrt((self.__x1-self.__x2)**2+(self.__y1-self.__y2)**2))
        #Son dessin
        self.__dessin = can.create_line(self.__x1,self.__y1,self.__x2,self.__y2,fill=self.__c)
        self.__evap = 0.5 #taux d'évaporation
        self.__fromTo = ft #Villes adjacents
        self.__can = can #Zone de affichage
        
        #Label avec sa taille
        can.create_text((self.__x1+self.__x2)/2, (self.__y1+self.__y2)/2 +20, text = self.__taille)
        
        #label avec sa quantité de phéromone
        self.__label = can.create_text((self.__x1+self.__x2)/2, (self.__y1+self.__y2)/2 - 20, text = math.floor(self.__qtPhe*10))
        
        #S'ajoute à les aretes des villes adjacents
        ft[0].set_arretes(self)
        ft[1].set_arretes(self)
     
    #Retourne sa taille   
    def get_taille(self):
        return self.__taille
     
    #Retourne ses villes adjacents   
    def get_ft(self):
        return self.__fromTo

    #Retourne les coordonnées de ville 1    
    def get_debut(self):
        return self.__fromTo[0].get_centre()
    
    #Retourne les coordonnées de ville 2 
    def get_fin(self):
        return self.__fromTo[1].get_centre()
    
    #Retourne sa quantité de phéromone à l'instant
    def get_phero(self):
        return self.__qtPhe

    #Defini sa quantité de phéromone à partir de la valeu INI et l'affiche dans le dessin    
    def set_phero(self,INI):
        self.__qtPhe = INI
        self.__can.itemconfig(self.__label,text = math.floor(self.__qtPhe*10))
    
    #Ajoute phéromone et l'affiche dans le dessin
    def add_phero(self,add):
        self.__qtPhe += add
        self.__can.itemconfig(self.__label,text = math.floor(self.__qtPhe*10))
    
    #Evapore le phéromone en utilizant le taux de évaporation   
    def evaporation(self):
        self.__qtPhe = (1-self.__evap)*self.__qtPhe
        
        #Pour pas générer les problemes de calcul
        if(self.__qtPhe < 1e-20):
            self.__qtPhe = 1e-20
        self.__can.itemconfig(self.__label,text = math.floor(self.__qtPhe*10))
    
    #Change sa couleur dans le dessin	
    def set_couleur(self):
        self.__can.itemconfig(self.__dessin,fill='yellow',width = 10)
    
    #Redefinit sa couleur comme noir 
    def reset_couleur(self):
        self.__can.itemconfig(self.__dessin,fill='black',width = 1)
  
#Classe Ant      
class Ant:
    def __init__(self,nid,number,can):
        self.__antN = number #Numero de la Fourmi dans la colonie
        self.__alpha = random.uniform(-5,5) #Paramètre alpha qui pondere le pheromone
        self.__beta = random.uniform(-5,5) #Parametre beta qui pondere la distance
        self.__food = 0    # Amene la norriture(1 = oui)
        self.__posx,self.__posy = nid.get_centre()  #position initiale = nid      
        self.__v = 15 #Velocité des fourmis en pixels
        self.__choix = 0 #Choix de prochaine route
        self.__c = 'red' # Couleur dans le dessin
        self.__chemin = [] #Chemin actuel jusqu'à la norriture
        self.__cond = 'ville' #Condition initial = nid -> dans une ville
        self.__where = nid #Ville de dernier localization
        #Son dessin, un carre
        self.__dessin = can.create_rectangle(self.__posx-5,self.__posy-5,self.__posx+5,self.__posy+5,fill=self.__c)
        self.__can = can #Zone de affichage
        self.__memory =[nid] #Memoire local
        self.__tailleT = 0 #Taille du chemin actuel
        self.__qteNou = 0 #Quantité de nourriture ammene au nid pendant ce cycle
        self.__timesR = [] #Routes visité dans ce cycle 
        self.__shortest = [] #Plus petit Chemin couvert
        self.__minT = math.inf #Taille du plus petit chemin couvert

    #Retourne combien de routes la fourmi a visité pendant ce cycle        
    def get_timesR(self,routes):
        len = 0
        
        for route in routes:
            if route in self.__timesR:
                len = len + 1
        
        return len
    
    #Reset les routes couvertes
    def set_timesR(self):
        self.__timesR = []
      
    #Set la quantité de nourriture déjà ammené au nid  
    def set_qteNou(self,ini):
        self.__qteNou = ini
       
    #Ajoute 1 à la quantité de nourriture ammenné au nid dans le cycle
    def add_qteNou(self):
        self.__qteNou = self.__qteNou + 1
       
    #Retourne la quantité de nourriture ammenné au nid dans le cycle 
    def get_qteNou(self):
        return self.__qteNou
    
    #Efface la fourmi du dessin
    def extinct(self):
        self.__can.delete(self.__dessin)
     
    #Retourne si la fourmi apporte la nourriture   
    def get_food(self):
        return self.__food
      
    #Efface la memorie de villes de la fourmi  
    def memoryLost(self,nid):
        self.__memory =[nid]
    
    #Retourne le dessin de la fourmi   
    def get_dessin(self):
        return self.__dessin 
    
    #Retourne le chemin actuel de la Fourmi
    def get_chemin(self):
        return self.__chemin
    
    #Reset le chemin de la Fourmi
    def set_chemin(self):
        self.__chemin = []
    
    #Retourne la derniere Ville visite par la fourmi
    def get_where(self):
        return self.__where
    
    #Retourne la taille du dernier chemin couvert par la fourmi
    def get_tailleT(self):
        return self.__tailleT
    
    #Set la taille du chemin couvert
    def set_tailleT(self,ini):
        self.__tailleT = ini
    
    #Retourne le plus petit chemin couvert par la fourmi    
    def get_shortest(self):
        return self.__shortest
    
    #Retourne se la fourmi est dans une ville ou dans une route 
    def get_cond(self):
         return self.__cond
    
    #Retourne la position de la fourmi dans le dessin
    def set_centre(self,x,y):
        self.__posx = x
        self.__posy = y
    
    #La fourmi apporte de la nourriture
    def prendre_nourriture (self):
        self.__food = 1
    
    #La fourmi n'apporte plus de la nourriture
    def laisser_nourriture(self):
        self.__food = 0
    
    #Deposer pheromone en retour
    def deposer_pheromone_local(self):
        self.__chemin[-1].add_phero(0.0003)
    
    #Deposer pheromone a chaque cycle
    def deposer_pheromone_global(self):
        for route in self.__shortest:
            route.add_phero(1/self.__minT)
    
    #Reourne le parametre alpha de la fourmi    
    def get_alpha(self):
        return self.__alpha
    
    #Reourne le parametre beta de la fourmi  
    def get_beta(self):
        return self.__beta
     
    #Choix de prochaine route   
    def getTendance(self,qo):
        maxTendance = -500
        checkPhero = 0
        possible_choices = []
        q = random.uniform(0,1) #Parametre q pour rendre la decision plus aleatoire

        #Se la fourmi est dans la source de nourriture        
        if self.__where.get_cond() == 'food':
            self.__choix = self.__chemin[-1] #Retoune dans son propre chemin
            
            for route in self.__chemin: #Mesure la taille du chemin actuel
                self.__tailleT = self.__tailleT + route.get_taille()
            
            #Regarde si c'est le plus petit chemin trouvé par la fourmi
            if (len(self.__shortest)==0 or self.__tailleT < self.__minT):
                self.__minT = self.__tailleT
                self.__shortest = [] #Si oui, met a jour le plus petit chemin
                for route in self.__chemin:
                    self.__shortest.append(route) 
        
        #Se la fourmi est en train de retourner vers le nid           
        elif (self.__where.get_cond() == 'int' and self.__food == 1):
            self.__choix = self.__chemin[-1] #Retoune dans son propre chemin
        
        #Si non, elle cherche la norriture
        else:
            for route in self.__where.get_arretes(): #Pour chaque arrete
                if q <= qo or route.get_phero() == 0: #Choix de l'équation de tendance basé sur q et qo
                    tendance = route.get_phero()/(route.get_taille()**(self.__beta))
                else:
                    tendance = (route.get_phero()**self.__alpha)/(route.get_taille()**(self.__beta))
                
                #Regarde si la route ammene a une ville dejà visitée             
                if (self.__where == route.get_ft()[0] and route.get_ft()[1] in self.__memory) or (self.__where == route.get_ft()[1] and route.get_ft()[0] in self.__memory):
                    tendance = -501
                else:
                    possible_choices.append(route) #Si non, ville visitable
                
                if tendance > maxTendance: #Choix basée sur la tendance
                    maxTendance = tendance
                    self.__choix = route
            
            #Regarde si toutes les villes adjacentes ont été déjà visitées                       
            if maxTendance == -500:
                self.__choix = self.__chemin[-1] #Si oui, retourne dans ce propre chemin
            
            #Au moins une ville n'a pas été visitée   
            else:            
                self.__chemin.append(self.__choix) #Ajoute la route au chemin
                self.__timesR.append(self.__choix) #Ajoute la ville à les routes couvertes dans le cycle
            
        self.__cond = 'route' #Change la condition de la fourmi
            
        if (self.get_food()==1): #Si fourmi en train de retourner vers le nid
            self.deposer_pheromone_local() #Depose pheromone dans la route courant
    
    #Mouvement de la formi dans le dessin                                        
    def marcher(self):
        route = self.__chemin[-1] #Route analysée
        
        #Regrade le sense du mouvement
        if self.__where == route.get_ft()[0]:
            x1,y1 = route.get_debut() #Coordonnées de la route
            x2,y2 = route.get_fin()
        
            self.__posx += ((x2-x1)/route.get_taille()*self.__v) #Nouvelle position
            self.__posy += ((y2-y1)/route.get_taille()*self.__v)
        
            #Si la fourmi a arrivé dans une ville
            if abs(self.__posx - x1) > abs(x2-x1) or abs(self.__posy - y1) > abs(y2-y1) or (abs(self.__posy - y1) == abs(y2-y1) and abs(self.__posx - x1) == abs(x2-x1)):
                #Si fourmi en train de chercher norriture
                if(self.__food == 0):
                    self.__posx = x2 #Position de la fourmi = position de la ville 
                    self.__posy = y2
                    self.__cond = 'ville' #Change la condition de la fourmi
                    self.__where = route.get_ft()[1]
                    if self.__where in self.__memory: #Si ville dejá visité
                        self.__chemin.pop(-1); #Ne prendre pas chemin en compte
                    self.__can.coords(self.__dessin,x2-5,y2-5,x2+5,y2+5) #Change coordonnées de la fourmi dans le dessin
                    self.__memory.append(self.__where) #Ajoute la ville à la memoire

                #Fourmi retourne au nid
                else:
                    self.__posx = x2
                    self.__posy = y2
                    self.__cond = 'ville'
                    self.__where = route.get_ft()[1]
                    self.__chemin.pop(-1); #Efface le chemin quand retourne
                    self.__can.coords(self.__dessin,x2-5,y2-5,x2+5,y2+5) #Change coordonnées de la fourmi dans le dessin                   
            else:
                #Si encore en train de marcher: Change la position de la fourmi dans le dessin
                self.__can.move(self.__dessin, ((x2-x1)/route.get_taille()*self.__v), ((y2-y1)/route.get_taille()*self.__v))
         
        #Pareil dans l'autre direction       
        else:
            x1,y1 = route.get_debut()
            x2,y2 = route.get_fin()
        
            self.__posx += ((x1-x2)/route.get_taille()*self.__v)
            self.__posy += ((y1-y2)/route.get_taille()*self.__v)
            
            if abs(self.__posx - x2) > abs(x1-x2) or abs(self.__posy - y2) > abs(y1-y2) or (abs(self.__posx - x2) > abs(x1-x2) == abs(x1-x2) and abs(self.__posy - y2) == abs(y1-y2)):
                if ((self.__food == 0)):
                    self.__posx = x1
                    self.__posy = y1
                    self.__cond = 'ville'
                    self.__where = route.get_ft()[0]
                    if self.__where in self.__memory:
                        self.__chemin.pop(-1);
                    self.__can.coords(self.__dessin,x1-5,y1-5,x1+5,y1+5)
                    self.__memory.append(self.__where)
                else:
                    self.__posx = x1
                    self.__posy = y1
                    self.__cond = 'ville'
                    self.__where = route.get_ft()[0]
                    self.__chemin.pop(-1);
                    self.__can.coords(self.__dessin,x1-5,y1-5,x1+5,y1+5)
            else:
                self.__can.move(self.__dessin, ((x1-x2)/route.get_taille()*self.__v), ((y1-y2)/route.get_taille()*self.__v))

#Classe newAnt
class newAnt(Ant):
    def __init__(self,mother,father,nid, number, can):
        Ant.__init__(self, nid, number, can)
        
        self.__beta = father.get_beta() #Prendre le beta de le pere
        self.__alpha = mother.get_alpha() #Prendre le alpha de la mere
        
        #Regarde si il y a multation
        mut = random.randint(1,100)
        if mut <= 10:
            self.mutation() 

    #fonction de mutation qui altere un des parametres de la fourmi            
    def mutation(self):
        cara = random.randint(1,2) #Prendre un parametre au hasard pour changer
        if cara == 1:
            self.__alpha = self.__alpha + random.uniform(-0.03,0.03)
        elif cara ==2:
            self.__beta = self.__beta +random.uniform(-0.03,0.03)          