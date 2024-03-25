from math import sqrt
from view import *
from random import randint


def pos_biparti(sommets):
    """
    entree : liste de sommets
    sortie : dictionnaire de position pour matplotlib
    prends une liste de sommets de longueur pair et calcule les coordonnées pour en faire un graphe biparti

    """
    nb_sommet = len(sommets)

    pos = {}
    indice = 0
    demi = nb_sommet//2
    taille = sqrt(demi)
    taille_int = int(taille) + 1
    # on construie la premiere moitie du graphe
    for i in range(taille_int):
        for y in range(taille_int):
            if (i*taille_int+y < demi):
                pos[sommets[indice]] = ([i*5, y*5+i*1.5])
                indice = indice+1
    # on construie la seconde moitie du graphe
    for i in range(taille_int):
        for y in range(taille_int):
            if (i*taille_int+y < demi):
                pos[sommets[indice]] = ([i*5+taille_int*5+5, y*5+i*1.5])
                indice = indice+1
    return pos


def traitement_entree_int_SAT2(li_clause, li_sommet):
    li_couple = []

    for clause in li_clause:

        if (len(clause) == 2):
            li_couple.append([li_sommet.index(clause[0]),
                              li_sommet.index(clause[1])])

        else:
            li_couple.append([li_sommet.index(clause[0]),
                              li_sommet.index(clause[0])])

    return li_couple


def texte_transfo_en_graphe(li_g, li_sommet, ind):
    str_fin = "clause déjà traiter"
    for i in range(len(li_g)):
        if (i == ind):
            str_fin = str_fin+" clause a traiter : "
        if (len(li_g[i]) > 1):
            str_fin = str_fin+"["+li_sommet[li_g[i][0]] + \
                ", "+li_sommet[li_g[i][1]]+"]"
        else:
            str_fin = str_fin+"["+li_sommet[li_g[i][0]]+"]"
    return str_fin


def transfo_en_graphe_int_SAT2(li_couples, li_sommet):
    """
    entree : liste de de couple de int, liste des symboles
    sortie : liste de couple de int
    prends en entre une FNC de clause de deux symboles max et construit
    une formule logique sur ce modèle (p ou q) -> (non p => q) en 
    les couples sont représenté sous forme de int représentant l'index du symbole
    dans la  liste de symbole, avec une liste de symbole de taille 6
    [[1,2]] devient [[4 , 2]] (voir format enregistrement des couples avec int)
    """
    taille_moitie = len(li_sommet)//2
    li_final = []
    compteur_visu = 0
    for ind in range(len(li_couples)):
        if (len(li_couples[ind]) > 1):
            if (li_couples[ind][0] > taille_moitie-1):
                li_final.append(
                    [li_couples[ind][0]-taille_moitie, li_couples[ind][1]])
            else:
                li_final.append(
                    [li_couples[ind][0]+taille_moitie, li_couples[ind][1]])
            if (li_couples[ind][1] > taille_moitie-1):
                li_final.append(
                    [li_couples[ind][1]-taille_moitie, li_couples[ind][0]])
            else:
                li_final.append(
                    [li_couples[ind][1]+taille_moitie, li_couples[ind][0]])
        else:
            li_final.append([li_couples[ind][0], li_couples[ind][0]])
        texte = texte_transfo_en_graphe(li_couples, li_sommet, ind+1)
        if (compteur_visu < 10):
            visualisation_graphe(li_sommet, to_graph_format_netw(li_final, li_sommet), texte=texte, pos=pos_biparti(li_sommet), li_var={
                                 "description": "Pour chaque clause de la formule logique, on créé deux arêtes, (p ou q) devient les arêtes (-p, q) et (-q, p)", "clauses": liste_doublet_int_vers_liste_nom(li_couples, li_sommet), "arrête": liste_doublet_int_vers_liste_nom(li_final, li_sommet), "index": ind})
            compteur_visu = compteur_visu + 1
    return li_final


def mat_adja_to_li(graph):
    li_final = []
    for e in range(len(graph)):
        for f in graph[e]:
            li_final.append([e, f])
    return li_final


def li_graphe_to_li_adja_SAT2(aretes, long):
    graph = [[] for _ in range(long)]
    for u, v in aretes:
        graph[u].append(v)
    return graph


def algo_tarjan(nombre_de_sommets, graph, li_symb):
    """
    entree : nombre_de_sommets : int, arrête : liste de couple de int
    sortie : ordre de parcours : liste de int
            composante : liste de int
    cet algorithme prend un graphe et calcule ses composantes fortement connexes
    on renvoie également l'ordre de découvertes car l'algo de tarjan effectue un parcours en profondeur 
    inverser ce parcours nous permet d'obtenir l'ordre topologique, dont nous aurout besoin plus tard
    """
    # on refais le graphe sous forme de matrice d'adjacence

    # on initialise les variables nécessaires au parcours ainsi que le tableau composante
    compteur_decouverte = 0
    pile = []
    decouverte = [-1] * nombre_de_sommets
    composante = [-1] * nombre_de_sommets
    dans_la_pile = [False] * nombre_de_sommets
    compteur_visu = 0
    # on définis une seconde fonction, celle qui va faire le le parcours

    def parcours_trajan(graph, v, li_symb):
        """
        entree : graph : liste de liste d'adjacence
        v : sommet en exploration
        parcours_trajan parcours le graphe en profondeur et mets à jour 
        la liste composante afin de trouver les composantes fortement connexes

        """

        # on récupère ces variables afin de les préserver lors des multiples appels de parcours_trajan
        nonlocal compteur_decouverte, pile, decouverte, composante, dans_la_pile, compteur_visu
        # à chaque appel de parcours_trajan on vérifie que v n'a pas déjà était découverts
        # on peut donc affecter découverte et composante
        if (compteur_visu < 10):
            visualisation_graphe(li_symb, to_graph_format_netw(mat_adja_to_li(graph), li_symb), pos=pos_biparti(li_symb), couleur=[i*15 for i in composante], li_var={"description": "L'algorithme de Tarjan permet de trouver les composantes fortement connexes d'un graphe.\nPour ce faire, on prend un sommet au hasard, et on le définit racine de sa composante fortement connexe, on parcourt tous les sommets de sa composante fortement connexe, soit v le sommet racine, on parcourt tous les x tels que (v, x) et (x, v) existent et on les empile. Quand notre parcours se termine, on dépile les sommets jusqu'à retrouver v, nous avons trouvé la composante fortement connexe de v. On recommence tant qu'il existe des sommets sans composantes fortement connexes.", "compteur parcours": compteur_decouverte, "parcours": liste_int_vers_dict_nom(
                decouverte, li_symb), "pile": liste_int_vers_liste_nom(pile, li_symb), "composante": liste_int_vers_dict_nom(composante, li_symb), "sommet courant": li_symb[v]})
            compteur_visu = compteur_visu + 1
        decouverte[v] = compteur_decouverte
        composante[v] = compteur_decouverte
        # un nouveau sommet a été découvert, on incrémente le compteur
        compteur_decouverte += 1
        # on rajoute ce nouveau sommet a la pile et on indique qui'il est dedans
        pile.append(v)
        dans_la_pile[v] = True
        # pour tous les voisins du sommet v
        for voisin in graph[v]:
            # si le sommet n'est pas connu, on l'explore
            if decouverte[voisin] == -1:
                parcours_trajan(graph, voisin, li_symb)
            # si le sommet est dans la pile, alors il est un "ancetre" de v
            # or v l'a dans ses voisins, on a donc un cycle et v et son ancêtre
            # font partie de la même composante connexe
            if dans_la_pile[voisin]:
                composante[v] = min(composante[v], composante[voisin])
        # si v est une racine
        if decouverte[v] == composante[v]:
            # tant que des "descendants" de v sont dans la pile
            trouver_v = False
            while not trouver_v:
                # on dépile et tous les sommets dépiler font partie de la composante de v
                sommet = pile.pop()
                dans_la_pile[sommet] = False
                composante[sommet] = decouverte[v]
                if sommet == v:
                    trouver_v = True
    # on parcours tous les sommets qui n'ont pas était découvert
    for v in range(nombre_de_sommets):
        if decouverte[v] == -1:
            parcours_trajan(graph, v, li_symb)

    return composante, decouverte


def traitement_entree_utilisateur_SAT2(entree):
    """
    entree : string de la forme "(-e) \wedge(e \vee f)\wedge(-g \vee -r)\wedge(t)"
    sortie : li_symbole : liste de tous les symboles nécessaires a la résolution du problème
            li_couple_en_ordre : liste de couples de string de la forme [[x,nv],[v,b],[e, nb][ne,nb]]
    Cette fonction prend les données fournies par l'utilisateur, la FNC avec des clauses de longueur maximum
    2 et transforme l'entrée de string à une liste de couple de symboles, on génère également la liste complète 
    des symboles nécessaire à résoudre le problème
    """
    entree = entree.replace(" ", "")
    # print(entree)
    li_couple_en_ordre = entree.split(")\wedge(")
    doublet_en_ordre = []
    for element in li_couple_en_ordre:
        element = element.replace("(", "")
        element = element.replace(")", "")
        element = element.replace(" ", "")
        doublet_en_ordre.append(element.split("\\vee"))

    valide = True
    li_symbole = []
    # pour chacun des symboles on teste, si celui-ci est négatif ou pas
    # si non négatif, on teste ssi il existe déjà dans la liste des symboles
    # si il n'existe pas dedans on le rajoute
    # si négatif, on n'enlève le symbole négatif, teste si l'on connaît le symbole non négatif
    # et rajoute le symbole non négatif si on ne le connaît pas
    # print(doublet_en_ordre)
    for d in doublet_en_ordre:
        for e in d:
            if len(e) >= 1 and e[0] != '-' and e not in li_symbole:
                li_symbole.append(e)
                if (len(e) != 1):
                    valide = False
            elif (len(e) >= 1 and e[1:] not in li_symbole and e[1:] != ""):

                li_symbole.append(e[1:])
                if (len(e[1:]) != 1):
                    valide = False

    longu = len(li_symbole)
    # seul les symboles non négatifs sont dans la liste, on rajoute les négatifs
    for i in range(longu):
        li_symbole.append('-'+li_symbole[i])

    return valide, li_symbole, doublet_en_ordre


def triTopo(li_adja, li_sommet, composante):
    """
    entree : graphe sous forme de listes d'adjacence
    liste des sommets
    les composantes de chaque sommet
    sorti : tri tropologique des composantes fortement connexes sous forme d'une liste
    d'une liste de composantes fortement connexes
    Cette fonction trie les composantes connexes d'un graphe en ordre topologique
    """
    # pour faire cela on effectue un parcours en profondeur du graphe
    parcours = []
    compteur = 0

    vue = [-1]*len(li_sommet)

    def dfs_Topo(li_adja, parcours, compteur, vue, v):
        parcours.append([v])
        vue[v] = 1
        # mais à chaque fois que l'on observe un sommet
        # on affecte a tout les sommets de sa composante fortement connexe
        # le même ordre de découverte
        # ainsi, on effectue un parcours en profondeur sur les composantes fortement connexes
        for i in range(len(composante)):
            if (composante[i] == composante[v] and i != v):
                parcours[-1].append(i)
                vue[i] = 1
        compteur = compteur+1
        for element in li_adja[v]:
            if (vue[element] != 1):
                dfs_Topo(li_adja, parcours, compteur, vue, element)
        for i in range(len(composante)):
            if (composante[i] == composante[v] and i != v):
                for element in li_adja[i]:
                    if (vue[element] != 1):
                        dfs_Topo(li_adja, parcours, compteur, vue, element)
    for i in range(len(li_sommet)):
        if (vue != 1):
            dfs_Topo(li_adja, parcours, compteur, vue, i)
    parcours.reverse()
    return parcours


def liste_int_vers_liste_nom(li_int, li_symb):
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


def liste_int_vers_dict_nom(li_int, li_symb):
    """
    entre : liste int
    liste symbole
    sortie dict symbole
    permet de passer du codage en int utiliser par le programme
    au codage en symbole utiliser par l'utilisateur
    """
    li_final = []
    for i in range(len(li_int)):
        li_final.append(li_symb[i]+" : "+str(li_int[i]))
    return li_final


def liste_doublet_int_vers_liste_nom(li_int, li_symb):
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


def to_graph_format_netw(li_graphe, li_symbole):
    """
    entree : graphe, li_symbole
    sortie : liste d'arete
    transforme le codage du graphe utiliser par le programme 
    au codage attendu par networkx pour l'affichage
    """
    li_test_transfo_int = []
    for e in li_graphe:
        if (len(e) > 1):
            li_test_transfo_int.append([li_symbole[e[0]], li_symbole[e[1]]])
        else:
            li_test_transfo_int.append([li_symbole[e[0]]])
    return li_test_transfo_int


def couleur_propagation(val_ver, vue):
    """
    prends les valeur de veritee de propagation ainsi que l'etat de parcours
    et renvoie une liste de couleur pour la visualisation
    """
    li_couleurs = []
    for i in range(len(vue)):
        if (vue[i] == -1):
            li_couleurs.append("gray")
        else:
            if (val_ver[i]):
                li_couleurs.append("green")
            else:
                li_couleurs.append("red")
    # print(li_couleurs)
    return li_couleurs


def propagation(graphe, li_sommet):
    """
    entre : graphe sous forme de liste d'adjacence
    liste_sommet
    sortie : tableau valeur
    renvoie un tableau de valeur rendant une expression logique vraie
    """
    # on initialise les valeurs de vérité à None
    val_ver = [True]*len(li_sommet)
    vue = [-1]*len(li_sommet)
    compteur_visu = 0
    # pour chaque sommet sans valeur de vérité
    for i in range(len(li_sommet)):
        if (vue[i] == -1):
            # print("on traite",i)
            # on crée une file pour accueillir tous les descendants du sommet et lui-même
            file = []
            # on rajoute dans la file le sommet choisi
            file.append(i)
            val_ver[i] = True
            vue[i] = 1
            if (i < (len(li_sommet)//2)-1):

                val_ver[i+(len(li_sommet)//2)] = False
                vue[i+(len(li_sommet)//2)] = 1
            else:
                val_ver[i-(len(li_sommet)//2)] = False
                vue[i-(len(li_sommet)//2)] = 1
            if (compteur_visu < 10):
                visualisation_graphe(li_sommet, to_graph_format_netw(mat_adja_to_li(graphe), li_sommet), pos=pos_biparti(li_sommet), couleur=couleur_propagation(val_ver, vue), li_var={
                    "description": "Afin de trouver les valeur de vérité a associé aux symboles, on choisit un symbole et on lui affecte la valeur Vrai et on affecte Faux a son opposé, puis on affecte Vrai a tous ses voisins si ils n'ont pas déjà etaient explorés et Faux aux opposé de ces voisins. On répète cette procédure sur les voisin du sommet et ainsi de suite, si on ne trouve plus de voisin, on reprends un nouveau sommet non exploré jusqu'a qu'il n'y ai plus de sommet non exploré.\n On affichera les sommet non explorés en gris, les sommet avec la valeur vrai en vert et ceux avec la valeur faux en rouge", "explorer": liste_int_vers_dict_nom(vue, li_sommet), "courant": li_sommet[i]})
                compteur_visu = compteur_visu+1
            # tqnt que la fille n'est pas vide
            while (file != []):
                # on parcours les voisins du sommet courant
                for voisin in graphe[i]:
                    # si ils n'ont pas de valeur, on leur attribue la valeur vraie
                    if (vue[voisin] == -1):
                        val_ver[voisin] = True
                        vue[voisin] = 1
                        # on rajoute ce voisin à la pile
                        file.append(voisin)
                        # et on affecte la valeur de vérité de l'inverse du voisin a False
                        if (voisin < (len(li_sommet)//2)-1):
                            val_ver[voisin+(len(li_sommet)//2)] = False
                            vue[voisin+(len(li_sommet)//2)] = 1
                        else:
                            val_ver[voisin-(len(li_sommet)//2)] = False
                            vue[voisin-(len(li_sommet)//2)] = 1
                        if (compteur_visu < 10):
                            visualisation_graphe(li_sommet, to_graph_format_netw(mat_adja_to_li(graphe), li_sommet), pos=pos_biparti(li_sommet), couleur=couleur_propagation(val_ver, vue), li_var={
                                                 "description": "Afin de trouver les valeur de vérité a associé aux symboles, on choisit un symbole et on lui affecte la valeur Vrai et on affecte Faux a son opposé, puis on affecte Vrai a tous ses voisins si ils n'ont pas déjà etaient explorés et Faux aux opposé de ces voisins. On répète cette procédure sur les voisin du sommet et ainsi de suite, si on ne trouve plus de voisin, on reprends un nouveau sommet non exploré jusqu'a qu'il n'y ai plus de sommet non exploré.\n On affichera les sommet non explorés en gris, les sommet avec la valeur vrai en vert et ceux avec la valeur faux en rouge", "explorer": liste_int_vers_dict_nom(vue, li_sommet), "courant": li_sommet[voisin]})
                            compteur_visu = compteur_visu+1
                # on défile le sommet courant et si la file n'est pas vide on change le sommet courant
                # pour le premier sommet dans la pile
                file.pop(0)
                if (len(file) > 0):
                    i = file[0]
                # print(file)
    return val_ver


def entree_hasard_2SAT(nb_litteraux, nb_clauses):
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
        # print(li_litt_choisi[t1],li_litt_choisi[t2])
        str_final = str_final + "(" + \
            li_litt_choisi[t1]+" \\vee " + \
            li_litt_choisi[t2]+") "
        str_print = str_print + "(" + \
            li_litt_choisi[t1]+" \\vee " + \
            li_litt_choisi[t2]+") "
        if (nb_clauses-i > 1):
            str_final = str_final + " \wedge "
            str_print = str_print + " \wedge "
    str_final = str_final[:len(str_final)-1]
    print("la formule choisie est : ", str_print)
    return str_final
