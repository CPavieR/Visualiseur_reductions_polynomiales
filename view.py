from math import sqrt
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy
from mpl_toolkits.mplot3d import Axes3D
# permet de stocker les donnees a visu pour affichage en une seule fenetre
# global stockage_donnee_visu
stockage_donnee_visu = []
# variable globale type_de_visu
# permet a l'utilisateur le type de visuel voulue
# global type_de_visu
type_de_visu = 1
visu_3d = False


def bar_progression(progression, total, taille_de_la_barre=20):
    fraction = progression / total

    fleche = int(fraction * taille_de_la_barre - 1) * '-' + '>'

    espacement = int(taille_de_la_barre - len(fleche)) * ' '
    if (progression == total):
        ending = '\n'
    else:
        ending = '\r'

    print(
        f'On dessine les figures: [{fleche}{espacement}] {int(fraction*100)}%', end=ending)


def affichage_visu_type_2_3d(oriente=False):
    print("Patientez cela peut prendre quelques secondes...")

    taille = len(stockage_donnee_visu)
    largeur = int(sqrt(taille)) + \
        ((taille-(int(sqrt(taille))**2))//int(sqrt(taille))+1)
    hauteur = int(sqrt(taille))
    # print("hauteur : ",hauteur)
    # print("largeur : ", largeur)
    # print("nombre de plot", taille)

    # print(li_posi)

    for i in range(taille):
        posi = {}

        li = stockage_donnee_visu[i][1].items()
        # print(li)
        # print(len(li))
        # print(li)

        for ele in li:
            # print(ele)
            # print(ele)
            # ele[1].append(1)

            nouvelle_co = ele[1]
            posi[ele[0]] = nouvelle_co+[2]

        # print(stockage_donnee_visu[i][0])
        ax = plt.subplot2grid((hauteur, largeur), (i //
                                                   largeur, i % largeur), projection="3d")
        node_xyz = np.array([posi[v] for v in posi])
        ax.grid(False)
        ax.axis('off')
        ax.set_zlim(0, 4)
        arete_xyz = np.array([(posi[u], posi[v])
                            for u, v in stockage_donnee_visu[i][0].edges()])
        # print(stockage_donnee_visu[i][3])
        ax.scatter(*node_xyz.T, s=40, ec="w",
                c=stockage_donnee_visu[i][3], depthshade=False)

        y = 0
        for viarete in arete_xyz:
            if(not oriente):
                ax.plot(*viarete.T, color="tab:"+stockage_donnee_visu[i][2][y])
                
            elif(oriente):
                if(sqrt((viarete[1][0]-viarete[0][0])**2+(viarete[1][1]-viarete[0][1])**2+(viarete[1][2]-viarete[0][2])**2) != 0):
                    #ax.quiver(viarete[0][0], viarete[0][1], viarete[0][2], viarete[1][0]-viarete[0][0], viarete[1][1]-viarete[0][1], viarete[1][2]-viarete[0][2], arrow_length_ratio=0.06/sqrt((viarete[1][0]-viarete[0][0])**2+(viarete[1][1]-viarete[0][1])**2+(viarete[1][2]-viarete[0][2])**2), color="tab:"+stockage_donnee_visu[i][2][y])
                    ax.plot(*viarete.T, color="tab:"+stockage_donnee_visu[i][2][y])
                    tete_de_fleche=creation_fleche(viarete[0],viarete[1])

                    ax.plot3D([tete_de_fleche[0][0],tete_de_fleche[1][0] ],[ tete_de_fleche[0][1],tete_de_fleche[1][1]],[tete_de_fleche[0][2],tete_de_fleche[1][2] ], color="tab:"+stockage_donnee_visu[i][2][y])
                    ax.plot3D([tete_de_fleche[2][0],tete_de_fleche[3][0] ],[ tete_de_fleche[2][1],tete_de_fleche[3][1]],[tete_de_fleche[2][2],tete_de_fleche[3][2]], color="tab:"+stockage_donnee_visu[i][2][y])
                    
                else:
                    #A fAIRE
                    pass
            y = y+1

        if (len(stockage_donnee_visu[i]) >= 5):
            for n in posi:
                ax.text(posi[n][0], posi[n][1], posi[n]
                        [2], stockage_donnee_visu[i][4][n])
        else:
            for n in posi:
                # print(n)
                # print(stockage_donnee_visu[i][4])
                ax.text(posi[n][0], posi[n][1], posi[n][2], n)

        bar_progression(i, taille)

    bar_progression(taille, taille)
    print("Les dessins on été fait, matplotlib vas maintenant les afficher...")
    plt.show()
    # [g, pos, edge color, node_color, label]

def creation_fleche(pos1,pos2):
    taille_tronc_fleche=sqrt((pos2[0]-pos1[0])**2+(pos2[1]-pos1[1])**2+(pos2[2]-pos1[2])**2)
    longueur_tete_fleche=1
    rapport_long_tete_tronc=longueur_tete_fleche/taille_tronc_fleche
    taille_x=pos2[0]-pos1[0]
    taille_y=pos2[1]-pos1[1]
    coordonnee_x_tete=pos2[0]-taille_x*rapport_long_tete_tronc
    coordonnee_y_tete=pos2[1]-taille_y*rapport_long_tete_tronc
    return [coordonnee_x_tete,coordonnee_y_tete,pos2[2]+0.22],[pos2[0],pos2[1],pos2[2]],[coordonnee_x_tete,coordonnee_y_tete,pos2[2]-0.22],[pos2[0],pos2[1],pos2[2]]



def visu_3d_general(G, pos, edge_color,
                    node_color, labels=[], with_labels=True, texte="", descrip={},oriente=False):
    # , fig=plt.figure()
    posi = {}

    li = pos.items()
    # print(li)
    # print(len(li))
    # print(li)
    #print(li)
    for ele in li:
        # print(ele)
        # ele[1].append(1)

        nouvelle_co = ele[1]
        posi[ele[0]] = nouvelle_co+[2]
    #print(posi)
    # print(stockage_donnee_visu[i][0])
    # fig=plt.figure()
    # ax=fig.add_subplot(projection='3d')
    if (descrip != {}):
        ax = plt.figure().add_subplot(121, projection='3d')
    else:
        ax = plt.figure().add_subplot(projection='3d')
    plt.grid(False)
    plt.axis('off')
    ax.set_zlim(0, 4)
    sommet_xyz = np.array([posi[v] for v in posi])
    #print(labels)
    if (labels == []):
        for n in posi:
            ax.text(posi[n][0], posi[n][1], posi[n][2], n)
    else:
        for n in posi:
            ax.text(posi[n][0], posi[n][1], posi[n][2], labels[n])
    arete_xyz = np.array([(posi[u], posi[v]) for u, v in G.edges()])

    # print(stockage_donnee_visu[i][3])
    ax.scatter(*sommet_xyz.T, s=40, ec="w", c=node_color, depthshade=False)

    y = 0
    for viarete in arete_xyz:
        if(not oriente):
            ax.plot(*viarete.T, color="tab:"+edge_color[y])
            
        elif(oriente):
            if(viarete[1][0]!=viarete[0][0] or viarete[1][1]!=viarete[0][1] or viarete[1][2]!=viarete[0][2]):
                #ax.quiver(viarete[0][0], viarete[0][1], viarete[0][2], viarete[1][0]-viarete[0][0], viarete[1][1]-viarete[0][1], viarete[1][2]-viarete[0][2], arrow_length_ratio=0.06/sqrt((viarete[1][0]-viarete[0][0])**2+(viarete[1][1]-viarete[0][1])**2+(viarete[1][2]-viarete[0][2])**2), color="tab:"+edge_color[y])
                ax.plot(*viarete.T, color="tab:"+edge_color[y])
                tete_de_fleche=creation_fleche(viarete[0],viarete[1])

                ax.plot3D([tete_de_fleche[0][0],tete_de_fleche[1][0] ],[ tete_de_fleche[0][1],tete_de_fleche[1][1]],[tete_de_fleche[0][2],tete_de_fleche[1][2] ], color="tab:"+edge_color[y])
                ax.plot3D([tete_de_fleche[2][0],tete_de_fleche[3][0] ],[ tete_de_fleche[2][1],tete_de_fleche[3][1]],[tete_de_fleche[2][2],tete_de_fleche[3][2]], color="tab:"+edge_color[y])
            
            else:
                theta = np.linspace(0, 2 * np.pi, 201)
                x = 0.35*np.cos(theta)
                y_deux = np.sin(theta)
                phi = np.pi/9
                print(x)
                ax.plot(x*np.sin(phi)+ viarete[0][0],
                        y_deux*np.sin(phi)+viarete[0][1],x*np.cos(phi)+viarete[0][2]+0.35, color="tab:"+edge_color[y])
                #, color="tab:"+edge_color[y]
        y = y+1
    # return fig
    if (texte != ""):
        #print("texte")
        plt.figtext(0.5, 0.01, texte, wrap=True,
                    horizontalalignment='center', fontsize=12)
    if (descrip != {}):
        plt.subplot(122)
        axis = plt.gca()
        axis.set_xlim([0, 10])
        axis.set_ylim([0, 7])
        ind = 0
        for key in descrip:
            plt.text(0, ind, key+" : \n"+str(descrip[key]), wrap=True)
            ind = ind+1
            if (key == "description"):
                ind = ind+1
        plt.axis('off')




def affichage_visu_type_2():
    print("Patientez cela peut prendre quelques secondes...")

    taille = len(stockage_donnee_visu)
    largeur = int(sqrt(taille)) + \
        ((taille-(int(sqrt(taille))**2))//int(sqrt(taille))+1)
    hauteur = int(sqrt(taille))
    # print("hauteur : ",hauteur)
    # print("largeur : ", largeur)
    # print("nombre de plot", taille)
    for i in range(taille):
        # print(stockage_donnee_visu[i])
        plt.subplot2grid((hauteur, largeur), (i //
                         largeur, i % largeur))
        if (len(stockage_donnee_visu[i]) == 5):

            nx.draw(stockage_donnee_visu[i][0], pos=stockage_donnee_visu[i][1], edge_color=stockage_donnee_visu[i][2],
                    node_color=stockage_donnee_visu[i][3], labels=stockage_donnee_visu[i][4], with_labels=True)
        else:

            nx.draw(stockage_donnee_visu[i][0], pos=stockage_donnee_visu[i][1], edge_color=stockage_donnee_visu[i][2],
                    node_color=stockage_donnee_visu[i][3], with_labels=True)
        bar_progression(i, taille)
    bar_progression(taille, taille)
    print("Les dessins on été fait, matplotlib vas maintenant les afficher...")
    plt.show()
    # [g, pos, edge color, node_color, label]


def visualisation_graphe(li_symb, li_graph, couleur=[], texte="", li_var={}, pos={}, labels={}, type_g="bigraph", arete_colore=[]):
    """
    entree : li_symb : liste des symboles
                li_graph : liste des aretes
                couleur : liste des couleurs des sommets
                texte : texte a afficher en bas de l'écran
                li_var : dictionnaire des variables a afficher
                pos : dictionnaire des positions des sommets
                labels : dictionnaire qui permet de passer du codage en int utiliser par le programme au nom donnee par l'utilisateur
                type_g : type de graphe "simple" = non oriente, oriente par defaut
                arete_colore : liste des aretes a colorier en rouge
    """
    # couleurs peut etre soit des str, soit des int, si c'est des int
    # on les multiplie pour mieux differencier les couleurs
    # sinon on fait rien
    if (couleur == []):
        couleur = ["blue"]*len(li_symb)
    couleur_arete = []

    oriente =False
    if type_g == "simple":
        G = nx.Graph()
    else:
        G = nx.DiGraph()
        oriente=True
    
    G.add_nodes_from(li_symb)
    G.add_edges_from(li_graph)
        # pos=nx.circular_layout(G)
        # print(labels)
    li_arete = G.edges()
    for a in li_arete:
        # print(a)
        # print(type(a[0]))
        # print(li_symb[int(a[0])],li_symb[int(a[1])])
        # print(arete_colore)
        # print([a[0],a[1]])
        # print([a[1],a[0]])
        if [a[1], a[0]] in arete_colore or [a[0], a[1]] in arete_colore:
            couleur_arete.append("red")
            # print("rouge")
        else:
            couleur_arete.append("gray")
            # print("gris")
        # print("--------------------")
    
    if pos == {}:
        pos = nx.circular_layout(G)
        for e in pos:
            pos[e] = pos[e].tolist()
    if (type_de_visu == 1):

        #G.add_nodes_from(li_symb)
        #G.add_edges_from(li_graph)
        # for i in range(len(li_graph)):
        #    print(str(li_graph[i])+" : ", couleur_arete[i])
        # print(labels)
        # print(li_graph)
        # print(couleur_arete)
        # pos=nx.circular_layout(G)
        # edge_color=[[labels[i],labels[y]] for i,y in arete_colore],edge_color=arete_colore,
        #print(texte)
        #if pos == {}:
        #    pos = nx.circular_layout(G)
        #    for e in pos:
        #        pos[e] = pos[e].tolist()
        print(couleur_arete)
        if (labels == {}):
            if (visu_3d):
                visu_3d_general(G, pos=pos, edge_color=couleur_arete,
                                node_color=couleur, with_labels=True, texte=texte,oriente=oriente)
            else:
                nx.draw(G, pos=pos, edge_color=couleur_arete,
                        node_color=couleur, with_labels=True)
                plt.figtext(0.5, 0.01, texte, wrap=True,
                            horizontalalignment='center', fontsize=12)
        else:
            if (visu_3d):
                visu_3d_general(G, pos=pos, edge_color=couleur_arete,
                                node_color=couleur, labels=labels, with_labels=True, texte=texte,oriente=oriente)
            else:
                nx.draw(G, pos=pos, edge_color=couleur_arete,
                        node_color=couleur, labels=labels, with_labels=True)
                plt.figtext(0.5, 0.01, texte, wrap=True,
                            horizontalalignment='center', fontsize=12)

        plt.show()
    if (type_de_visu == 2):
        """plt.subplot2grid((5, 6), (parametre.num_plot //
                         6, parametre.num_plot % 6))"""

        #G.add_nodes_from(li_symb)
        #G.add_edges_from(li_graph)
        # pos=nx.circular_layout(G)
        # print(labels)
        #if pos == {}:
        #    pos = nx.circular_layout(G)
        #    for e in pos:
        #        pos[e] = pos[e].tolist()
        if (labels == {}):
            stockage_donnee_visu.append([G, pos, couleur_arete, couleur])
            """nx.draw(G, pos=pos,edge_color=couleur_arete,
                node_color=couleur, with_labels=True)"""
        else:
            stockage_donnee_visu.append(
                [G, pos, couleur_arete, couleur, labels])
            """nx.draw(G, pos=pos,edge_color=couleur_arete,
                node_color=couleur,labels=labels ,with_labels=True)"""
        # [g, pos, edge color, node_color, label]
        # parametre.num_plot = parametre.num_plot+1
    if (type_de_visu == 3):

        #G.add_nodes_from(li_symb)
        #G.add_edges_from(li_graph)
        # print(nx.circular_layout(G))

        #if pos == {}:
        #    pos = nx.circular_layout(G)
        #    for e in pos:
        #        pos[e] = pos[e].tolist()
        if (labels == {}):
            if (visu_3d):

                visu_3d_general(G, pos=pos, edge_color=couleur_arete,
                                node_color=couleur, with_labels=True, descrip=li_var,oriente=oriente)
            else:
                plt.subplot(121)
                nx.draw(G, pos=pos, edge_color=couleur_arete,
                        node_color=couleur, with_labels=True)
        else:
            if (visu_3d):

                visu_3d_general(G, pos=pos, edge_color=couleur_arete,
                                node_color=couleur, labels=labels, with_labels=True, descrip=li_var,oriente=oriente)
            else:
                plt.subplot(121)
                nx.draw(G, pos=pos, edge_color=couleur_arete,
                        node_color=couleur, labels=labels, with_labels=True)
        if (not visu_3d):
            plt.subplot(122)
            # fig.xlim(0, 10)
            # fig.ylim(0, len(li_var)+1)
            ind = 0
            for key in li_var:
                plt.text(0, ind, key+" : \n"+str(li_var[key]), wrap=True)
                ind = ind+1
                if (key == "description"):
                    ind = ind+1
            plt.axis('off')
        plt.show()
