from graph import *
from view import *
from control import *
from fnc import * 

def transformation_personnalise(entree, entree_aleatoire, entree_fichier, entree_utilisateur):
    """
    entree : string de l'instance d'entree, n'est defini que si on lit l'entree depuis un fichier
    entree_aleatoire : booleen, l'utilisateur souhaite une entree aleatoire
    entree_fichier : booleen, l'utilisateur souhaite une entree depuis un fichier
    entree_utilisateur : booleen, l'utilisateur souhaite une entree depuis l'interface
    """
    print("Transformation personnalise")
    print("Ce module vous permet de facilier creer votre propre transformation")
    print("Pour cela on mets a votre disposition la classe Graphe")
    print("Vous trouverez un exemple d'operation simple si dessous")

    exemple()


def exemple():
    """
    print("on cree un graphe non orienter")
    nouveau_graphe=Graphe(oriente=False)
    print("on demande a l'utilisateur de rentrer un graphe")
    print("le graphe doit etre de la forme (sommet 1, sommet 2);(sommet 3, sommet 4); etc")
    print("les sommets sont de type libre")
    entree = input("entrer le graphe")
    print("la fonction traitement_entree_utilisateur permet de creer le graphe correspondant a l'entree fournie")
    print("elle renvoie un booleen qui indique si l'entree est valide")
    print("si l'entree n'est pas valide, le graphe ne sera pas modifier")
    if(nouveau_graphe.traitement_entree_utilisateur(entree)):
        print("on affiche le graphe")
        nouveau_graphe.visualiser()
    else:
        print("l'entree n'est pas valide")
    print("on cree un nouveau graphe oriente")
    nouveau_graphe_2=Graphe(oriente=True)
    print("on genere un graphe aleatoire")
    if(nouveau_graphe_2.graphe_au_hasard(5,8)):

        print("on affiche le graphe")
        nouveau_graphe_2.visualiser()"""
    nouveau_graphe_3=Graphe()
    print("on ajoute un sommet au graphe")
    nouveau_graphe_3.ajout_sommet("a")
    print("on ajoute un autre sommet au graphe")
    nouveau_graphe_3.ajout_sommet("tarte aux pommes")
    nouveau_graphe_3.ajout_sommet(35)
    

    print("on ajoute une arete au graphe")
    nouveau_graphe_3.ajout_arete(["a",35])
    print("on affiche le graphe")
    nouveau_graphe_3.visualiser()
    print("on complete le graphe")
    nouveau_graphe_3.completer_le_graphe()
    print("on affiche le graphe")
    nouveau_graphe_3.visualiser()


"""liste des methodes de la classe Graphe:

    ajout_sommet(sommet) : ajoute un sommet au graphe
    ajout_arete(arete) : ajoute une arete au graphes
    ajout_liste_arete(liste_arete) : ajoute une liste d aretes au graphe
    ajout_liste_sommet(liste_sommet) : ajoute une liste de sommets au graphe
    supprimer_sommet(sommet) : supprime un sommet du graphe
    supprimer_arete(arete) : supprime une arete du graphe
    traitement_entree_utilisateur(entree) : permet de creer un graphe a partir d une entree utilisateur
    graphe_aleatoire(nb_sommet, nb_arete) : genere un graphe aleatoire
    completer_le_graphe() : complete le graphe
    visualiser(arete_a_colorier=[], dictionnaire_couleur_sommet_par_nom={}, legende="", dictionnaire_variable={}, dictionnaire_position={}) : affiche le graphe
        arete_a_colorier : liste des aretes a colorier
        dictionnaire_couleur_sommet_par_nom : dictionnaire qui a chaque sommet associe une couleur
        legende : string qui sera affiche en dessous du graphe
        dictionnaire_variable : dictionnaire qui a chaque variable associe une valeur
        dictionnaire_position : dictionnaire qui a chaque sommet associe une position"""

"""liste des methodes de la classe FNC:
    get_formule() : renvoie la formule
    get_li_symbole() : renvoie la liste des symboles
    depuis_entree_utilisateurs(entree) : permet de creer une formule a partir d une entree utilisateur
    sous la forme : (a \vee b) \wedge (c \vee d) \wedge (e \vee f)
    ATTENTION : les symboles doivent etre des lettres
    ATTENTION : \v est un symbole special en python, il faut donc le doubler
    ATTENTION : si la string est definie dans le programme, 
    ATTENTION : cela ne devrait pas etre necessaire si elle est saisie avec un input.
    taille_de_conversion_min() : renvoie la taille de la plus grande clause
    cela indique la taille de clause maximum a laquelle on peut convertir la formule
    to_clauses_taille(taille) : renvoie la formule sous la forme de clauses de taille = taille
    transformation_int(taille) : renvoie la formule sous la forme d une liste de liste d int, on peut specifier la taille des clauses
    ajouter_clause(clause) : ajoute une clause a la formule







"""