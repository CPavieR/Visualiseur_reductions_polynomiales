from modele_2SAT import *
from modele_3SAT import *
from modele_Karp import *
from modele_personnalise import *
import view
import os

largeur_programme = os.get_terminal_size().columns


def formatage_print(string):
    return "|"+string+" " * (largeur_programme-2-len(string))+"|"


def choix():

    print_entete()
    print(formatage_print("Choississez l'algorithme !"))
    print(formatage_print("1 : 2SAT -> algorithme de Tarjan"))
    print(formatage_print("2 : 3SAT -> VertexCover"))
    print(formatage_print(
        "3 : Cycle Hamiltonien -> Voyageur de commerce (Reduction de Karp)"))
    print(formatage_print("4 : Transformation personnalise"))

    choix = input("|")
    # diff : 0 : entrer utilisateur, 1 : petite instance, 2 : moyenne instance, 3 : grande instance
    difficulte = 0
    inst = "default"
    entree_par_fichier = ""
    while (inst != "1" and inst != "2" and inst != "3"):
        print(formatage_print("Souhaitez vous"))
        print(formatage_print("1 : Entrée aléatoire"))
        print(formatage_print("2 : Lire un fichier"))
        print(formatage_print("3 : Entrer manuellement une instance"))
        inst = input("|")
    if (inst == "1"):
        entrer = "4"
        while (not entrer.isnumeric() or int(entrer) not in [1, 2, 3]):
            print(formatage_print(
                "Rentrez un niveau de difficulté valide. 1, 2 ou 3"))
            entrer = input("|")
        difficulte = int(entrer)
    else:
        difficulte = 0
    if (inst == "2"):
        entree_par_fichier = lecture_fichier()

    print(formatage_print("Choissez quel type d'affichage vous souhaitez"))

    print(formatage_print("1 : une fenêtre par étape"))
    print(formatage_print("2 : tout en une fenêtre"))
    print(formatage_print("3 : une fenêtre par étape avec les variable du programme"))
    print(formatage_print("4 : pas de visuel"))
    mode = input("|")
    if mode.isnumeric and int(mode) in [1, 2, 3, 4]:
        view.type_de_visu = int(mode)
        # print(view.type_de_visu)
    else:
        print(formatage_print("mode invalide, affichage par défaut"))
    entree_3d = ""

    print(formatage_print("Souhaiter vous une visualisation en 3D ? O/n"))
    entree_3d = input("|")
    if (entree_3d.lower() == "o" or entree_3d == ""):
        view.visu_3d = True
    else:
        view.visu_3d = False
    print("─"*75)
    if (choix == "1"):
        # bon exemple : h h nl na nq nq nj nz q nh
        # e k nc u r g l nx v j
        # "v g nq c h h nl na nq nq nj nz q nh"
        # (v \vee g) \wedge (-q \vee c) \wedge (h \vee h) \wedge (y)\wedge(-l \vee -a) \wedge (-q \vee -j) \wedge (-j \vee -z) \wedge (q \vee -h) \wedge (-k \vee g) \wedge (l \vee -m)
        # -k g l -m
        if (entree_par_fichier == ""):
            ent = ""
            if (difficulte != 0):
                nb_lit = [3, 6, 9]
                nb_clause = [8, 12, 17]
                ent = entree_hasard_2SAT(
                    nb_lit[difficulte-1], nb_clause[difficulte-1])
        else:
            ent = entree_par_fichier
        resolvSAT2(ent)

    elif (choix == "2"):
        # (-c \vee c \vee -e)  \wedge (-d \vee -c \vee c)  \wedge (-c \vee -c \vee -d)  \wedge (-a \vee d \vee -e)  \wedge (-c \vee b \vee -g)  \wedge (d \vee -h \vee f)
        # (b \vee g \vee -c)  \wedge (-d \vee -g \vee -c)  \wedge (-b \vee -g \vee g)  \wedge (d \vee d \vee -d)  \wedge (-h \vee -e \vee -f)  \wedge (a \vee -g \vee f)
        # (-c \vee -d \vee b)  \wedge (e \vee g \vee b)  \wedge (-d \vee -g \vee -d)  \wedge (-a \vee b \vee -d)  \wedge (e \vee -d \vee d)  \wedge (-b \vee c \vee -a)
        # (f \vee -f \vee -h)  \wedge (-c \vee -a \vee -h)  \wedge (b \vee d \vee g)  \wedge (b \vee h \vee f)  \wedge (d \vee d \vee -c)  \wedge (g \vee -e \vee c)
        # "(-b \vee -c \vee b)  \wedge (-b \vee -e \vee -a)  \wedge (-c \vee -d \vee -c)  \wedge (-a \vee -b \vee c)  \wedge (-c \vee c \vee -c)  \wedge (-d \vee e \vee c)"
        # ent
        if (entree_par_fichier == ""):
            ent = ""
            if (difficulte != 0):
                nb_lit = [4, 6, 9]
                nb_clause = [3, 5, 7]
                ent = entree_hasard_3SAT(
                    nb_lit[difficulte-1], nb_clause[difficulte-1])
        else:
            ent = entree_par_fichier
        resolvSAT3(ent)
    elif (choix == "3"):
        # (1,2);(2,3);(3,4);(4,5);(5,1);(1,6)
        # "(1,2);(2,3);(3,4);(4,5);(5,1);(1,6);(5,6)"
        #
        if (entree_par_fichier == ""):
            ent = ""
            if (difficulte != 0):
                nb_sommet = [3, 6, 9]
                nb_arete = [6, 15, 21]
                ent = entree_hasard_KARP(
                    nb_sommet[difficulte-1], nb_arete[difficulte-1])
        else:
            ent = entree_par_fichier
        karp(ent)
    elif (choix == "4"):
        # (1,2);(2,3);(3,4);(4,5);(5,1);(1,6)
        # "(1,2);(2,3);(3,4);(4,5);(5,1);(1,6);(5,6)"
        #
        entree_aleatoire = False
        entree_utilisateur=False
        entree_fichier=False
        if (entree_par_fichier == ""):
            ent = entree_par_fichier
            entree_fichier=True
        elif (difficulte != 0):
            entree_aleatoire = True
        else:
            entree_utilisateur=True
        transformation_personnalise(ent, entree_aleatoire, entree_fichier, entree_utilisateur)
    else:
        print("erreur")
        exit(0)
    if (view.type_de_visu == 2):
        if (view.visu_3d):
            if(choix=="1"):
                oriente=True
            else:
                oriente=False
            affichage_visu_type_2_3d(oriente)
        else:
            affichage_visu_type_2()
    exit(0)


def print_entete():
    print("─"*largeur_programme)
    print(formatage_print(" █████╗ ██╗      ██████╗  ██████╗")) 
    print(formatage_print("██╔══██╗██║     ██╔════╝ ██╔═══██╗")) 
    print(formatage_print("███████║██║     ██║  ███╗██║   ██║")) 
    print(formatage_print("██╔══██║██║     ██║   ██║██║   ██║")) 
    print(formatage_print("██║  ██║███████╗╚██████╔╝╚██████╔╝")) 
    print(formatage_print("╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ")) 
    print("─"*largeur_programme)


def resolvSAT2(ent):
    """fonction principale
    entrée : ent = liste des clauses, ou "" si l'on souhaite l'entrer a la main
    sortie :
    affiche si la formule est satisfiable ou non
    """

    if (ent == ""):
        print("le format d'entrée des formules est le LaTeX, exemple : (v \\vee g) \wedge (-q \\vee c) \wedge (h \\vee h) \wedge (y)\wedge(-l \\vee -a)")
        ent = input("entrez la formule (v \\vee g) \wedge (-q \\vee c)\n")

    valide, li_symbole, li_sommet_en_ordre = traitement_entree_utilisateur_SAT2(
        ent)
    while (not valide):
        print("entrée non valide, un charactere par symbole")
        print("le format d'entrée des formules est le LaTeX, exemple : (v \\vee g) \wedge (-q \\vee c) \wedge (h \\vee h) \wedge (y)\wedge(-l \\vee -a)")
        ent = input("entrez la formule (v \\vee g) \wedge (-q \\vee c)\n")
        valide, li_symbole, li_sommet_en_ordre = traitement_entree_utilisateur_SAT2(
            ent)
    # on transforme le codage en string par int
    if (len(li_symbole) > 12):
        view.type_de_visu = 4
        print("Instance trop grande, Visualisation desactivé")
    li_couple = traitement_entree_int_SAT2(li_sommet_en_ordre, li_symbole)

    # on construie l'instance du graphe correspondant
    li_graphe = transfo_en_graphe_int_SAT2(li_couple, li_symbole)

    # test que l'instance du graphe à bien était créée

    # li_test_transfo_int=to_graph_format_netw(li_graphe,li_symbole)
    # on applique l'algo de tarjan
    graphe_adja = li_graphe_to_li_adja_SAT2(li_graphe, len(li_symbole))
    composante, ordre_decouverte = algo_tarjan(
        len(li_symbole), graphe_adja, li_symbole)

    # on renverse l'ordre de découverte du parcours en profondeur afin d'obtenir un ordre topologique

    ordreTopo = triTopo(graphe_adja, li_symbole, composante)
    # on teste dans l'ordre topologique si un symbole est dans la même composante connexe que son négatif
    satis = True

    for compo in ordreTopo:
        for element in compo:
            if (element < (len(li_symbole)//2)-1):
                if (element+(len(li_symbole)//2) in compo):
                    satis = False

    print("la formule est elle satisfiable :", satis)
    if (satis):
        vals = propagation(graphe_adja, li_symbole)
        print("exemple vrai :")
        for i in range(len(li_symbole)):
            print(li_symbole[i]+" : "+str(vals[i]))

    # G = nx.DiGraph()
    # print(composante)
    # print(li_symbole)

    # G.add_nodes_from(li_symbole)
    # , cmap = plt.get_cmap('jet')
    # G.add_edges_from(li_test_transfo_int)
    # nx.draw(G,pos=nx.spring_layout(G, k=1/sqrt(10)*3),node_color=composante , with_labels=True)

    # plt.text(0,0,'axes title')
    # plt.show()
    return satis


def resolvSAT3(ent):
    if (ent == ""):
        print("le format d'entrée des formules est le LaTeX, exemple : (v \\vee g) \wedge (-q \\vee c \\vee g) \wedge (h \\vee h \\vee h) \wedge (y)\wedge(-l \\vee -a)")
        ent = input("entrez la formule\n")

    valide, li_symbole, triplet_en_ordre = traitement_entree_utilisateur_SAT3(
        ent)
    while (not valide):
        print("Erreur entrée non valide")
        ent = input(
            "entrez la formule (v \\vee g) \wedge (-q \\vee c \\vee g) \wedge (h \\vee h \\vee h) \wedge (y)\wedge(-l \\vee -a)\n")
        valide, li_symbole, triplet_en_ordre = traitement_entree_utilisateur_SAT3(
            ent)
        print(li_symbole)
    if (len(li_symbole) > 12):
        view.type_de_visu = 4
        print("Instance trop grande, Visualisation desactivé")
    # print(valide, li_symbole, triplet_en_ordre)
    triplet_int = traitement_entree_int_SAT3(triplet_en_ordre, li_symbole)
    # print(triplet_int)
    graphe, graphe_ng, pos, labels, taille, nouveux_triplet = creation_graphe_SAT3(
        li_symbole, triplet_int)

    """print(graphe)
    G=nx.Graph()
    li_sommet = []
    for i in range(taille):
        li_sommet.append(i)
    print(li_sommet)
    G.add_nodes_from(li_sommet)
    G.add_edges_from(graphe)
    print(labels)
    nx.draw(G, pos=pos,labels=labels,
                    with_labels=True)
    plt.show()"""
    #

    mini = minimal_vertex_cover(graphe, nouveux_triplet, labels, len(
        li_symbole), (len(li_symbole)//2+(len(triplet_int)*2)), taille, pos)

    if (len(mini) <= (len(li_symbole)//2+(len(triplet_int)*2))+1):
        print("La formule est Satisfiable")
        print("solution :")
        for e in mini:
            print(labels[e]+" : Vrai")
    else:
        print("la formule est non satisfiable")
    return len(mini) <= (len(li_symbole)//2+(len(triplet_int)*2))+1


def karp(ent):
    # (1,2);(2,3);(3,4);(4,5);(5,1);(1,6);(5,6)

    if (ent == ""):
        print("le format d'entrée du graphe est une liste d'aretes, exemple : (4,5);(6,9);(2,4);(8,3)")
        ent = input("entrez la liste d'arêtes\n")
    valide, li_symb, li_arete, label = traitement_entree_utilisateur_karp(ent)
    while (not valide):
        print("Erreur, entrée non valide")
        ent = input("entrez la liste d'arêtes\n")
        valide, li_symb, li_arete, label = traitement_entree_utilisateur_karp(
            ent)
    if (len(li_symb) > 12):
        view.type_de_visu = 4
        print("Instance trop grande, Visualisation desactivé")
    visualisation_graphe(li_symb, liste_doublet_int_vers_liste_nom_karp(
        li_arete, li_symb), type_g="simple", li_var={"description": "Voici le graphe de départ"})

    graphe = completion_graphe(li_arete, len(li_symb), li_symb, label)

    cout, parc = tsp(graphe, len(li_symb))
    if (cout != len(li_symb)):
        print("Il n'y as pas de cycle hamiltonien")
        return False
    else:
        print("Il y as un cycle hamiltonien :",
              liste_int_vers_liste_nom(parc, li_symb))
        li_arete_cycle = []
        for i in range(len(parc)-1):
            li_arete_cycle.append([parc[i], parc[i+1]])
        li_arete_cycle.append([parc[0], parc[-1]])
        print(liste_doublet_int_vers_liste_nom(li_arete_cycle, li_symb))
        li_arete_totale = []

        for i in range(len(li_symb)):
            for y in range(len(li_symb)):
                if (i != y and [y, i]not in li_arete_totale):
                    li_arete_totale.append([i, y])
        visualisation_graphe([i for i in range(len(li_symb))], li_arete_totale, labels=label,
                             type_g="simple", arete_colore=li_arete_cycle, texte="Le cycle hamiltonien trouvé est en rouge", li_var={"description": "On génère toutes les permutations possibles des sommets du graphe et on calcule le cout de ce parcours, si le cout du parcours est supérieur au nombre de sommets, cela signifie que l'on est passé par une arête n'appartenant pas au graphe d'origine, ce n'est donc pas un cycle hamiltonien. Si le parcours a un cout égal au nombre de sommets, alors on en déduit que le parcours ne passe que par des arêtes appartenant au graphe d'origine. On a donc un cycle hamiltonien"})

        return True




def lecture_fichier():
    chemin = ""
    while (not os.path.isfile(chemin)):
        print(formatage_print("Quel est le chemin du fichier ?"))
        chemin = input("|")
    f = open(chemin, "r")
    lines = f.readlines()
    return (lines[0])


if __name__ == '__main__':
    choix()
