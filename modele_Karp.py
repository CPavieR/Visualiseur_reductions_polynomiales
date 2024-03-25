from control import *
from view import *
from itertools import permutations
from random import randint

def traitement_entree_utilisateur_karp(entree):
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

    return valide, li_symb, li_arete, labels


def liste_int_vers_liste_nom_karp(li_int, li_symb):
    """
    entre : liste int
    liste symbole
    sortie liste symbole
    permet de passer du codage en int utiliser par le programme
    au codage en symbole utiliser par l'utilisateur
    """
    li_final = []
    for el in li_int:
        li_final.append(li_symb[el])
    return li_final


def liste_doublet_int_vers_liste_nom_karp(li_int, li_symb):
    """
    entre : liste de couple de int
    liste symbole
    sortie liste de couple de symboles
    permet de passer du codage en int utiliser par le programme
    au codage en symbole utiliser par l'utilisateur
    """
    li_final = []
    for el in li_int:
        li_final.append([li_symb[el[0]], li_symb[el[1]]])
    return li_final


def completion_graphe(li_graphe, nombre_de_sommets, li_symb, labels):
    """
    entree : liste arete
    sortie : graphe pondéré complété sous forme d'une matrice d'ajacence
    """
    matrice = [[-1 for i in range(nombre_de_sommets)]
               for y in range(nombre_de_sommets)]
    li_arete_visu = []
    liarete_a_colorer = []
    for i in range(nombre_de_sommets):
        for y in range(nombre_de_sommets):
            if (i != y):
                if ([y, i] not in li_arete_visu):
                    li_arete_visu.append([i, y])
                if ([i, y] in li_graphe or [y, i] in li_graphe):
                    matrice[i][y] = 1
                    matrice[y][i] = 1

                    # li_arete_visu.append([i,y])
                    if ([y, i] not in liarete_a_colorer):

                        liarete_a_colorer.append([i, y])
                else:
                    matrice[i][y] = 2
                    matrice[y][i] = 2
                    # liarete_a_colorer.append("gray")
    visualisation_graphe([i for i in range(len(li_symb))], li_arete_visu, texte="On complète le graphe, les aretes appartenant au graphe d'origine sont en rouges est ont un poids de 1, les autres sont en gris et ont un poids de 2",
                         labels=labels, type_g="simple", arete_colore=liarete_a_colorer, li_var={"description": "On complète le graphe, les aretes appartenant au graphe d'origine sont en rouges est ont un poids de 1, les autres sont en gris et ont un poids de 2"})
    return matrice


def tsp(graphe, taille):
    sommets = []
    for i in range(taille):
        sommets.append(i)
    cout_mini = taille*2
    li_permutation = permutations(sommets)
    permu_mini = []
    for i in li_permutation:
        # print(i)
        cout = 0
        k = i[0]
        # print(i[1:])
        for j in i[1:]:

            cout += graphe[k][j]
            k = j

        cout += graphe[k][i[0]]
        if (cout < cout_mini):
            permu_mini = i
        cout_mini = min(cout_mini, cout)
    # print(cout_mini)
    # print(permu_mini)
    return cout_mini, permu_mini


def entree_hasard_KARP(nb_sommet, nb_arete):
    str_final = ""
    arete_deja_faite = []

    for i in range(nb_arete):
        t1 = 1
        t2 = 1
        while (t1 == t2 and [t1, t2] not in arete_deja_faite and [t2, t1] not in arete_deja_faite):
            t1 = randint(0, nb_sommet)
            t2 = randint(0, nb_sommet)
        arete_deja_faite.append([t1, t2])
        str_final = str_final + "(" + \
            str(t1)+" , " + \
            str(t2)+") "
        if (nb_arete-i > 1):
            str_final = str_final + " ; "

    print("la formule choisie est : ", str_final)
    return str_final
