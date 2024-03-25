class FNC:
    formule = []
    li_symbole = []
    def __init__(self, formule=""):
        if(formule != ""):
            self.depuis_entree_utilisateurs(formule)
        else:
            self.formule = []


    def __str__(self):
        return str(self.formule)
    def depuis_entree_utilisateurs(self, entree):
        if(self.formule == []):
            entree = entree.replace(" ", "")
            # print(entree)
            li_clause_en_ordre = entree.split(")\wedge(")
            li_li_litteraux = []
            for element in li_clause_en_ordre:
                element = element.replace("(", "")
                element = element.replace(")", "")
                element = element.replace(" ", "")
                li_li_litteraux.append(element.split("\\vee"))
            valide = True
            li_symbole = []
            for d in li_li_litteraux:
                for e in d:
                    if len(e) >= 1 and e[0] != '-' and e not in li_symbole:
                        li_symbole.append(e)
                        li_symbole.append('-'+e)
                        if (len(e) != 1):
                            valide = False
                    elif (len(e) >= 1 and e[1:] not in li_symbole and e[1:] != ""):

                        li_symbole.append(e[1:])
                        li_symbole.append(e)
                        if (len(e[1:]) != 1):
                            valide = False

            if(valide):
                self.formule = li_li_litteraux
                self.li_symbole = li_symbole
            else:
                print("Erreur, l'entree n'est pas valide")
                print("Les symboles doivent etre des lettres")
                print(li_li_litteraux)
            return valide
        else:
            print("Erreur, la formule n'est pas vide")
            return False


    def taille_de_conversion_min(self):
        if(len(self.formule)==0):
            return 0
        taille_mini=len(self.formule[0])
        for clause in self.formule:
            if(len(clause)>taille_mini):
                taille_mini=len(clause)
        return taille_mini
    
    def get_formule(self):
        return self.formule
    def get_li_symbole(self):
        return self.li_symbole
    def to_clauses_taille(self, taille):
        if(self.taille_de_conversion_min()<=taille):
            fnc_final=[]
            for clause in self.formule:
                if(len(clause)<taille):
                    nouvelle_clause=[]
                    for i in range(len(clause)):
                        nouvelle_clause.append(clause[i])
                        
                    for i in range(len(clause)-1,taille):
                        nouvelle_clause.append(clause[len(clause)-1])

                    fnc_final.append(nouvelle_clause)
                else:
                    fnc_final.append(clause)
            return fnc_final
        else:
            print("Erreur, la taille minimum des clauses est superieur a la taille demandee")
            return None
    def transformation_int(self, taille_clause=0):
        if(taille_clause==0):
            taille_clause=self.taille_de_conversion_min()
        
        formule_bonne_taille=self.to_clauses_taille(taille_clause)
        tous_int=True
        for clause in formule_bonne_taille:
            for litteral in clause:
                if(litteral[0]=='-'):
                    if(litteral[1:].isnumeric()==False):
                        tous_int=False
                else:
                    if(litteral.isnumeric()==False):
                        tous_int=False
        fnc_int=[]
        if(tous_int):
            for clause in formule_bonne_taille:
                nouvelle_clause=[]
                for litteral in clause:
                    if(litteral[0]=='-'):
                        nouvelle_clause.append(-int(litteral[1:]))
                    else:
                        nouvelle_clause.append(int(litteral))
                fnc_int.append(nouvelle_clause)
            return fnc_int
        else:
            index=1
            dict_symbole={}
            for clause in formule_bonne_taille:
                nouvelle_clause=[]
                for litteral in clause:
                    if(litteral[0]=='-'):
                        if(litteral[1:] in dict_symbole):
                            nouvelle_clause.append(-dict_symbole[litteral[1:]])
                        else:
                            dict_symbole[litteral[1:]]=index
                            nouvelle_clause.append(-index)
                            index+=1
                    else:
                        if(litteral in dict_symbole):
                            nouvelle_clause.append(dict_symbole[litteral])
                        else:
                            dict_symbole[litteral]=index
                            nouvelle_clause.append(index)
                            index+=1
                fnc_int.append(nouvelle_clause)
            return fnc_int
    
    def ajout_clause(self, clause):
        self.formule.append(clause)
        for litteral in clause:
            if(litteral[0]=='-'):
                if(litteral[1:] not in self.li_symbole):
                    self.li_symbole.append(litteral[1:])
                    self.li_symbole.append(litteral)
            else:
                if(litteral not in self.li_symbole):
                    self.li_symbole.append(litteral)
                    self.li_symbole.append('-'+litteral)
