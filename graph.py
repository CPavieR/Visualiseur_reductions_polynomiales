from view import *
from random import randint


class Graphe:

    def __init__(self, oriente=False):
        """
        entree : digraphe : booleen si vrai alors le graphe sera oriente
        """
        self.li_arete = []
        self.li_symb = []
        self.etiquettes = {}
        self.nb_sommet = 0
        self.nb_arete = 0
        self.digraphe = oriente

    def __str__(self):
        """
        permet d'afficher le graphe
        """
        string_retour = ""
        string_retour += "Liste des sommets :"+str(self.li_symb)+"\n"
        string_retour += "Liste des aretes :" + \
            str(self._transformation_liste_arete_int_en_arete_etiquette(
                self.li_arete))+"\n"
        return string_retour

    def graphe_au_hasard(self, nb_sommet, nb_arete):
        if (self.nb_sommet != 0 or self.nb_arete != 0):
            print("Erreur ce graphe est deja definie")
            return False
        self.ajout_liste_sommet([i for i in range(nb_sommet)])
        for i in range(nb_arete):
            t1 = 1
            t2 = 1
            bon = False
            while (not bon):
                t1 = randint(0, nb_sommet)
                t2 = randint(0, nb_sommet)
                if (self.digraphe):
                    bon = t1 != t2 and [t1, t2] not in self.li_arete
                else:
                    bon = t1 != t2 and [t1, t2] not in self.li_arete and [
                        t2, t1] not in self.li_arete
            self.ajout_arete([t1, t2])

        return True

    def ajout_sommet(self, nom):
        """
        entree : nom : type arbitraire
        permet d'ajouter un sommet au graphe
        """
        if (nom not in self.li_symb):
            self.li_symb.append(nom)
            
            self.etiquettes[self.nb_sommet] = nom
            self.nb_sommet += 1
            return True
        else:
            print("Le sommet existe deja")
            return False

    def ajout_liste_sommet(self, liste_sommet):
        """
        entree : liste_sommet : liste de type arbitraire
        permet d'ajouter une liste de sommet au graphe
        """
        erreur=False
        for sommet in liste_sommet:

            if( not self.ajout_sommet(sommet)):
                erreur=True
        return not erreur

    def ajout_arete(self, arete):
        """
        entree : arete : collection (liste, tuple, etc) de deux elements designer par leurs noms
        permet d'ajouter une arete au graphe
        """
        if (arete not in self.li_arete):
            if (len(arete) == 2 and arete[0] in self.li_symb and arete[1] in self.li_symb):
                self.li_arete.append(
                    [self.li_symb.index(arete[0]), self.li_symb.index(arete[1])])
                return True
            elif (len(arete) == 2 and arete[0] not in self.li_symb and arete[1] in self.li_symb):
                self.ajout_sommet(arete[0])
                self.li_arete.append(
                    [self.li_symb.index(arete[0]), self.li_symb.index(arete[1])])
                return True
            elif (len(arete) == 2 and arete[0] in self.li_symb and arete[1] not in self.li_symb):
                self.ajout_sommet(arete[1])
                self.li_arete.append(
                    [self.li_symb.index(arete[0]), self.li_symb.index(arete[1])])
                return True
            elif (len(arete) == 2 and arete[0] not in self.li_symb and arete[1] not in self.li_symb):
                self.ajout_sommet(arete[0])
                self.ajout_sommet(arete[1])
                self.li_arete.append(
                    [self.li_symb.index(arete[0]), self.li_symb.index(arete[1])])
                return True
            else:
                print("L'arete n'est pas valide")
                return False
        else:
            print("L'arete existe deja")
            return False

    def est_orientee(self):
        return self.digraphe

    def ajout_liste_arete(self, liste_arete):
        """
        entree : liste_arete : liste de collection (liste, tuple, etc) de deux elements designer par leurs noms
        permet d'ajouter une liste d'arete au graphe
        """
        erreur=False
        for arete in liste_arete:
            if(not self.ajout_arete(arete)):
                erreur=True
        return not erreur

    def get_liste_arete(self):
        li_arete_etiquette = self._transformation_liste_arete_int_en_arete_etiquette(
            self.li_arete)
        return li_arete_etiquette

    def get_etiquettes(self):
        return self.etiquettes

    def get_nb_sommet(self):
        return self.nb_sommet

    def get_liste_sommet(self):
        li_sommet_etiquette = self._transformation_liste_sommet_int_en_sommet_etiquette(
            self.li_symb)

        return li_sommet_etiquette

    def _transformation_liste_sommet_etiquette_en_sommet_int(self, liste_sommet):
        """
        INTERNE A LA CLASSE, NE PAS UTILISER
        """
        liste_sommet_int = []
        for sommet in liste_sommet:
            liste_sommet_int.append(self.li_symb.index(sommet))
        return liste_sommet_int

    def _transformation_liste_sommet_int_en_sommet_etiquette(self, liste_sommet):
        """
        INTERNE A LA CLASSE, NE PAS UTILISER
        """
        liste_sommet_etiquette = []
        for sommet in liste_sommet:
            liste_sommet_etiquette.append(self.etiquettes[sommet])
        return liste_sommet_etiquette

    def _transformation_liste_arete_int_en_arete_etiquette(self, liste_arete):
        """
        INTERNE A LA CLASSE, NE PAS UTILISER
        """
        liste_arete_etiquette = []
        for arete in liste_arete:
            liste_arete_etiquette.append(
                [self.etiquettes[arete[0]], self.etiquettes[arete[1]]])
        return liste_arete_etiquette

    def _transformation_liste_arete_etiquette_en_arete_int(self, liste_arete):
        """
        INTERNE A LA CLASSE, NE PAS UTILISER
        """
        liste_arete_int = []
        for arete in liste_arete:
            if(arete[0] in self.li_symb and arete[1] in self.li_symb):
                liste_arete_int.append(
                    [self.li_symb.index(arete[0]), self.li_symb.index(arete[1])])
        return liste_arete_int

    def visualiser(self, arete_a_colorier=[], dictionnaire_couleur_sommet_par_nom={}, legende="", dictionnaire_variable={}, dictionnaire_position={}):
        """
        entree : arete_a_colorier : liste des aretes a colorier
                    dictionnaire_couleur_sommet_par_nom : dictionnaire qui a chaque sommet associe une couleur
                    legende : string qui sera affiche en dessous du graphe
                    dictionnaire_variable : dictionnaire qui a chaque variable associe une valeur
                    dictionnaire_position : dictionnaire qui a chaque sommet associe une position
        cette fonction affichera le graphe conformement au type de visuel selectionne
        """
        
        arete_a_colorier_int = self._transformation_liste_arete_etiquette_en_arete_int(
            arete_a_colorier)
        print(arete_a_colorier_int)
        li_couleur_sommet = []
        for sommet in self.li_symb:
            if sommet in dictionnaire_couleur_sommet_par_nom:
                li_couleur_sommet.append(
                    dictionnaire_couleur_sommet_par_nom[sommet])
            else:
                li_couleur_sommet.append("blue")
        li_arete_int = self.li_arete
        print(self.etiquettes)
        print(li_arete_int)
        if (self.digraphe):
            type = "bigraph"
        else:
            type = "simple"
        position_sommets = {}
        if(len(dictionnaire_position) >= self.nb_sommet):
            
            for i in range(self.nb_sommet):
                if self.li_symb[i] in dictionnaire_position:
                    position_sommets[i] = dictionnaire_position[self.li_symb[i]]
                else:
                    print("erreur : Vous devez definir les positions de soit aucun sommet soit tous les sommets")
                    return False
        elif(len(dictionnaire_position)!=0):
            print("erreur : Vous devez definir les positions de soit aucun sommet soit tous les sommets")
            return False
        visualisation_graphe([i for i in range(self.nb_sommet)], li_arete_int, arete_colore=arete_a_colorier_int,
                             couleur=li_couleur_sommet, texte=legende, li_var=dictionnaire_variable, type_g=type, labels=self.etiquettes, pos= position_sommets)
        return True
    def _graphe_en_liste_adjacence_int(self):
        """
        INTERNE A LA CLASSE, NE PAS UTILISER
        """
        li_adjacence = []
        for i in range(self.nb_sommet):
            li_adjacence.append([])
        for arete in self.li_arete:
            li_adjacence[arete[0]].append(arete[1])
            if (self.digraphe == False):
                li_adjacence[arete[1]].append(arete[0])
        return li_adjacence

    def graphe_en_dict_adjacence(self):
        """
        sortie : dictionnaire d'adjacence
        permet de recuperer le graphe sous forme d'un dictionnaire dict[sommet]=[liste adjacence du sommet]
        """
        dict_adjacence = {}
        for i in range(self.nb_sommet):
            dict_adjacence[self.li_symb[i]] = []
        for arete in self.li_arete:
            dict_adjacence[self.li_symb[arete[0]]].append(
                self.li_symb[arete[1]])
            if (self.digraphe == False):
                dict_adjacence[self.li_symb[arete[1]]].append(
                    self.li_symb[arete[0]])
        return dict_adjacence

    def completer_le_graphe(self):
        """
        permet de completer le graphe
        """
        for i in range(self.nb_sommet):
            for j in range(self.nb_sommet):
                if (i != j and [i, j] not in self.li_arete):

                    self.li_arete.append([i, j])
                    self.nb_arete += 1
                    if(self.digraphe == True):
                        self.li_arete.append([j, i])
                        self.nb_arete += 1
    def traitement_entree_utilisateur(self,entree):
        """
        entree : string de la forme "(5,6);(3,8); etc"
        sortie : li_symbole 
                li_couple_en_ordre 
        """
        entree = entree.replace(" ", "")
        # print(entree)
        li_couple_en_ordre = entree.split(");(")
        doublet_en_ordre = []
        for element in li_couple_en_ordre:
            element = element.replace("(", "")
            element = element.replace(")", "")
            element = element.replace(" ", "")
            doublet_en_ordre.append(element.split(","))

        valide = True
        li_arete = []
        indice = 0
        li_symb = []
        labels = {}
        for d in doublet_en_ordre:
            if (len(d) == 2):
                if (d[0] not in li_symb):
                    li_symb.append(d[0])
                    labels[li_symb.index(d[0])] = d[0]
                if (d[1] not in li_symb):
                    li_symb.append(d[1])
                    labels[li_symb.index(d[1])] = d[1]
                li_arete.append([li_symb.index(d[0]), li_symb.index(d[1])])
            else:
                valide = False
        if(valide):
            self.li_symb=li_symb
            self.li_arete=li_arete
            self.etiquettes=labels
            return True
        else:
            return False
    def supprimer_arete(self, arete):
        """
        entree : arete : collection (liste, tuple, etc) de deux elements designer par leurs noms
        permet de supprimer une arete au graphe
        """
        if (arete in self.li_arete):
            if (len(arete) == 2):
                self.li_arete.remove(
                    [self.li_symb.index(arete[0]), self.li_symb.index(arete[1])])
                return True
            else:
                print("L'arete n'est pas valide")
                return False
        else:
            print("L'arete n'existe pas")
            return False
    def suprimer_sommet(self, sommet):
        """
        entree : sommet : type arbitraire
        permet de supprimer un sommet au graphe
        """
        if (sommet in self.li_symb):

            nouveau_li_symb=copy.deepcopy(self.li_symb)
            nouveau_li_arete=copy.deepcopy(self.li_arete)
            nouveau_li_symb.remove(sommet)
            for arete in self.li_arete:
                if(self.etiquettes[arete[0]]==sommet or self.etiquettes[arete[1]]==sommet):
                    nouveau_li_arete.remove(arete)
            nouvel_etiquette={}
            for i in range(len(nouveau_li_symb)):
                if(i<self.li_symb.index(sommet)):
                    nouvel_etiquette[i]=self.etiquettes[i]
                    print(1)
                else:
                    nouvel_etiquette[i]=self.etiquettes[i+1]
                    print(2)
            self.li_symb=nouveau_li_symb
            self.li_arete=nouveau_li_arete
            self.etiquettes=nouvel_etiquette
            print("nouvel eti :",nouvel_etiquette)
            self.nb_arete=len(self.li_arete)
            self.nb_sommet=len(self.li_symb)
            return True
        else:
            print("Le sommet n'existe pas")
            return False


