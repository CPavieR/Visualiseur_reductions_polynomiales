import itertools
import copy
from control import *
from view import *
from random import randint


def traitement_entree_utilisateur_SAT3(entree):
    """
    entree : string de la forme "(-e) \wedge(e \vee f \vee g)\wedge(-g \vee -r)\wedge(t)"
    sortie : li_symbole : liste de tous les symboles nécessaires a la résolution du problème
            li_couple_en_ordre : liste de couples de string de la forme [[x,-v,b],[v,b,-e],[e, -b,][-e,-b]]
    Cette fonction prend les données fournies par l'utilisateur, la FNC avec des clauses de longueur maximum
    3 et transforme l'entrée de string à une liste de couple de symboles, on génère également la liste complète 
    des symboles nécessaire à résoudre le problème
    """
    entree = entree.replace(" ", "")
    # print(entree)
    li_couple_en_ordre = entree.split(")\wedge(")
    triplet_en_ordre = []
    for element in li_couple_en_ordre:
        element = element.replace("(", "")
        element = element.replace(")", "")
        element = element.replace(" ", "")
        triplet_en_ordre.append(element.split("\\vee"))
        # print(element.split("\\vee"))

    valide = True
    li_symbole = []
    # pour chacun des symboles on teste, si celui-ci est négatif ou pas
    # si non négatif, on teste ssi il existe déjà dans la liste des symboles
    # si il n'existe pas dedans on le rajoute
    # si négatif, on n'enlève le symbole négatif, teste si l'on connaît le symbole non négatif
    # et rajoute le symbole non négatif si on ne le connaît pas
    # print(doublet_en_ordre)
    for d in triplet_en_ordre:
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

    return valide, li_symbole, triplet_en_ordre


def traitement_entree_int_SAT3(li_triplet_e, li_sommet):
    """
    entree : string, liste de sring
    sortie : list de couple de string
    prends une string du type "x y nx y" représentant une FNC avec des clauses de au maximum 3 symboles
    avec la liste des symboles
    séparent les clauses de la FNC et remplace les symboles par leur index dans la liste des symboles  
    """
    li_triplet = []

    for clause in li_triplet_e:

        if (len(clause) == 3):
            li_triplet.append([li_sommet.index(clause[0]),
                              li_sommet.index(clause[1]), li_sommet.index(clause[2])])
        # si une clause ne contient pas deux litteraux, on dedouble ceux present pour en avoir trois
        elif (len(clause) == 2):
            li_triplet.append([li_sommet.index(clause[0]),
                               li_sommet.index(clause[1]), li_sommet.index(clause[1])])
        else:
            li_triplet.append([li_sommet.index(clause[0]),
                               li_sommet.index(clause[0]),
                               li_sommet.index(clause[0])])

    return li_triplet


def creation_graphe_SAT3(li_symb, triplets):
    """
    entree :  li_symb : liste des symbole utiliser de le graphe
    triplets : triplets correspondant aux clauses
    cette fonction cree le graphe, ainsi que tout les valeur nessecaire a la visualisation de celui ci
    """
    compteur_visu = 0
    nouveux_triplet = []
    labels = {}
    for e in range(len(li_symb)):
        labels[e] = li_symb[e]

    pos = {}
    graphe = []
    graphe_ng = []
    graphe_ng_deux = []
    for i in range(len(labels)):
        pos[i] = [i*5, 0]
        if (i % 2 == 1):
            graphe.append([i-1, i])
            graphe_ng.append([i-1, i])
    indice = len(labels)
    taille_debut = len(labels)
    for triplet in triplets:
        nouveux_triplet.append([indice, indice+1, indice+2])
        graphe.append([indice, indice+1])
        graphe.append([indice+2, indice+1])
        graphe.append([indice, indice+2])
        graphe.append([indice, triplet[0]])
        graphe.append([indice+1, triplet[1]])
        graphe.append([indice+2, triplet[2]])
        graphe_ng.append([triplet[2], triplet[0]])
        graphe_ng.append([triplet[1], triplet[0]])
        graphe_ng.append([triplet[1], triplet[2]])
        pos[indice] = [(indice-taille_debut)//3*8, -0.75]
        pos[indice+1] = [(indice-taille_debut)//3*8+4, -0.75]
        pos[indice+2] = [(indice-taille_debut)//3*8+2.25, -1]
        labels[indice] = li_symb[triplet[0]]
        labels[indice+1] = li_symb[triplet[1]]
        labels[indice+2] = li_symb[triplet[2]]
        if (compteur_visu < 10):
            visualisation_graphe([i for i in range(indice+3)], copy.deepcopy(graphe), labels=copy.deepcopy(labels), pos=copy.deepcopy(pos), type_g="simple", li_var={
                                 "description": "Dans cette partie, on prend chaque clause, on crée la partie du graphe correspondante et on relie les sommets littéraux au sommet des clauses correspondantes", })
            compteur_visu = compteur_visu+1
        indice = indice + 3

    # print(graphe)
    return graphe, graphe_ng, pos, labels, indice, nouveux_triplet


def couleur(couv, nb_sommet):
    couleur = []
    for i in range(nb_sommet):
        if (i in couv):
            couleur.append(("red"))
        else:
            couleur.append("lightblue")
    return couleur


def est_couverture(graph, sommet):
    for arete in graph:
        if arete[0] not in sommet and arete[1] not in sommet:
            # print(arete)
            return False

    # print(True)
    return True


def minimal_vertex_cover(graph, triplet, labels, nb_sommet_reel, maxi, nb_sommet, pos):
    compteur_visu = 0
    # print(nb_sommet_reel)
    # print(nb_sommet_reel,maxi)
    # on initialise solution
    solution = [i for i in range(nb_sommet)]
    # on recupere toutes les combinaison possible sur les etats correspondant aux litteraux
    cov_combinations = combinaison(nb_sommet_reel)
    # pour chacune des combinaison
    for covtuple in cov_combinations:
        cov_deux = []
        cov = []
        for e in covtuple:
            cov.append(e)
        # on calcule l'ensemble de sommet correspondant a la transfo polynomiale
        for el in cov:
            for trip in triplet:
                if (not trip[0] in cov_deux or not trip[1] in cov_deux):
                    if (labels[el] == labels[trip[0]]):
                        cov_deux.append(trip[1])
                        cov_deux.append(trip[2])
                    if (labels[el] == labels[trip[1]]):
                        cov_deux.append(trip[2])
                        cov_deux.append(trip[0])
                    if (labels[el] == labels[trip[2]]):
                        cov_deux.append(trip[1])
                        cov_deux.append(trip[0])
        # on verifie que l'on ne depasse pas la taille max que l'on cherche soit un sommet par doublet + deux sommet par triplet
        if (len(cov_deux+cov) <= maxi):
            # si la taille est assez petite, on teste si l'ensemble de sommet couvre le graphe
            if est_couverture(graph, cov_deux+cov):
                # print("OKKK")
                couv = cov+cov_deux
                # si oui, alors on as trouver une solution, pn la compare la solution precedente, si elle est plus petite on la remplce
                # if(compteur_visu<10):
                # on visualise
                # visualisation_graphe([i for i in range(nb_sommet)], graph, labels=labels, pos=pos, couleur=couleur(couv,nb_sommet), type_g="simple")
                # compteur_visu=compteur_visu+1
                if (len(couv) < len(solution)):
                    # on reconstruie la reponse pour afficher sa construction
                    cov_affichage = []
                    cov_deux_affichage = []
                    for el in cov:
                        cov_affichage.append(el)
                        for trip in triplet:
                            changement = False
                            if (not trip[0] in cov_deux_affichage or not trip[1] in cov_deux_affichage):
                                if (labels[el] == labels[trip[0]]):
                                    cov_deux_affichage.append(trip[1])
                                    cov_deux_affichage.append(trip[2])
                                    changement = True
                                if (labels[el] == labels[trip[1]]):
                                    cov_deux_affichage.append(trip[2])
                                    cov_deux_affichage.append(trip[0])
                                    changement = True
                                if (labels[el] == labels[trip[2]]):
                                    cov_deux_affichage.append(trip[1])
                                    cov_deux_affichage.append(trip[0])
                                    changement = True
                                if (compteur_visu < 10 and changement):
                                    # on visualise
                                    # print(labels)
                                    visualisation_graphe([i for i in range(nb_sommet)], copy.deepcopy(graph), labels=copy.deepcopy(labels), pos=copy.deepcopy(pos), couleur=copy.deepcopy(couleur(cov_affichage+cov_deux_affichage, nb_sommet)), type_g="simple", li_var={"description": "Pour chaque combinaison possible, on ajoute les sommets des doublets dans la couverture, puis si un sommet x et lié a un triplet (x, y, z), on rajoute les sommets y et z a la couverture, à la fin, si la couverture couvre tous les sommets, en ayant au max un sommet par doublet et deux sommets par triplet, on obtient une solution", "combinaison": [
                                        labels[i] for i in cov], "sommets de litteraux traite ou en cours de traitement": [labels[i] for i in cov_affichage], "sommet de triplet dans la couverture": [labels[i] for i in cov_deux_affichage], "sommet en cours": labels[el]})
                                    compteur_visu = compteur_visu+1
                    solution = cov
                    # print(solution)
    return solution


def combinaison(nb_sommet):
    """
    entree : nb_sommet : nombre de sommet parmis lesquels on peut choisir

    sortie : combinaison possible sur les sommets donné
    """
    # print()
    # print(nb_sommet)
    li_comb = []
    sommets = []
    for i in range(nb_sommet):
        sommets.append(i)

    for L in range(nb_sommet//2+1):

        # print(L)
        for subset in itertools.combinations([i for i in range(nb_sommet)], L):

            li_comb.append(subset)

    return li_comb

#
#
#


# Example usage:
# graph = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)]
# cover = minimal_vertex_cover(graph)
# print("Minimal Vertex Cover:", cover)(e \vee f \vee g)\wedge(-g \vee -r)\wedge(t)\wedge (-e)
# (f \vee -g \vee g)  \wedge (-e \vee -f \vee h)  \wedge (-h \vee e \vee f)  \wedge (-c \vee b \vee -b)  \wedge (-f \vee d \vee g)  \wedge (e \vee a \vee -f)


def entree_hasard_3SAT(nb_litteraux, nb_clauses):
    str_final = ""
    li_litt_choisi = []
    li_symb = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'g', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for n in range(nb_litteraux):
        indice = -1
        while (indice == -1 or li_symb[indice] in li_litt_choisi):
            indice = randint(0, len(li_symb)-1)
        li_litt_choisi.append(li_symb[indice])
        # print(n)
        # print(li_litt_choisi)
    # print(li_litt_choisi)
    taille = len(li_litt_choisi)
    for f in range(taille):
        li_litt_choisi.append('-'+li_litt_choisi[f])
    # print(li_litt_choisi)
    str_print = ""
    for i in range(nb_clauses):
        t1 = randint(0, len(li_litt_choisi)-1)
        t2 = randint(0, len(li_litt_choisi)-1)
        t3 = randint(0, len(li_litt_choisi)-1)
        # print(li_litt_choisi[t1],li_litt_choisi[t2])
        str_final = str_final + "(" + \
            li_litt_choisi[t1]+" \\vee " + \
            li_litt_choisi[t2]+" \\vee " + \
            li_litt_choisi[t3]+") "
        str_print = str_print + "(" + \
            li_litt_choisi[t1]+" \\vee " + \
            li_litt_choisi[t2]+" \\vee " + \
            li_litt_choisi[t3]+") "
        if (nb_clauses-i > 1):
            str_final = str_final + " \wedge "
            str_print = str_print + " \wedge "
    str_final = str_final[:len(str_final)-1]
    print("la formule choisie est : ", str_print)
    return str_final
