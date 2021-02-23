import pygame, time
from typing import Tuple
# Initialisation de Pygame
pygame.init()

# Quelques variables publiques
fenetre = None
centre = 0
joueur = 1
score = [0,0]
police = pygame.font.SysFont('Chiller', 72)
tableu_en_cours = [2] * 9
'''
 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8
'''

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
gris = (200, 200, 200)
gris_clair = (240, 240, 240)
rouge = (255, 0, 0)
bleu = (0, 0, 255)
orange = (255, 165, 0)
aqua = (102, 255, 255)
violet = (153, 51, 255)

# Images
taille_du_x = 10  # taille de l'image du x ou le 0
taille_image = 620 # taille de l'image de fond
X_IMAGE = pygame.image.load("x.png")
O_IMAGE = pygame.image.load("o.png")
M_IMAGE = pygame.image.load("morpion.png")

def debut():
	global fenetre, centre, tableu_en_cours
	# Fenêtre seule vide
	taille = 700 # 700 pixels
	fenetre = pygame.display.set_mode((taille, taille)) # un carré de 700 pixels
	pygame.display.set_caption("   *** Morpion ***")               # Titre de la fenêtre
	fenetre.fill(gris_clair)                            # couleur du fond
	# image de fond centrée dans la fenêtre
	centre = fenetre.get_width() // 2 # déclare le point au centre de la fenêtre
	fenetre.blit(M_IMAGE, (centre - (M_IMAGE.get_width() // 2),centre - (M_IMAGE.get_width() // 2)))
	pygame.display.flip()
	tableu_en_cours = [2] * 9
debut()

# détermine les neuf positions des images X ou O
taille_trait = 40 # épaisseur du trait noir
taille_xo = X_IMAGE.get_width() # get_width() = obtient la largeur, vu que c'est un carré la hauteur est la même
moitie_xo = X_IMAGE.get_width() // 2 # pourquoi '// 2' ? => éssaiez 'print(11 / 2)' et 'print(11 // 2)'
gauche = centre - moitie_xo - taille_trait - taille_xo
droite = centre + moitie_xo + taille_trait
case_centre = centre - moitie_xo
haut = centre - moitie_xo - taille_trait - taille_xo
bas = centre + moitie_xo + taille_trait
positions = [[gauche, haut],
             [case_centre, haut], 
             [droite, haut], 
             [gauche, case_centre], 
             [case_centre, case_centre], 
             [droite, case_centre], 
             [gauche, bas], 
             [case_centre, bas], 
             [droite, bas]]

def affiche_le_gagnant(x, combi):
	image_actuelle = fenetre.copy()
	image = pygame.image.load('win_' + x + '.png')
	emplacement = [centre - (image.get_width() // 2),centre - (image.get_width() // 2)]
	pygame.display.flip()
	touche = False
	while touche == False:
		for action in pygame.event.get():
			if action.type == pygame.KEYDOWN:
				touche = True
		sec = (int(str(time.time()).split('.')[0]))
		if sec % 2 == 0:
			fenetre.blit(image, (emplacement))
			pygame.display.flip()
		else:
			fenetre.blit(image_actuelle, (0,0))
			pygame.display.flip()
	debut()
	texte1 = police.render('Score X : ' + str(score[0]), True, bleu)
	texte2 = police.render('Score O : ' + str(score[1]), True, rouge)
	fenetre.blit(texte1, (10, fenetre.get_height() - 70))
	fenetre.blit(texte2, (400, fenetre.get_height() - 70))
	pygame.display.update()

def verifie_gagnant():
	global tableu_en_cours
	combinaisons = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [2,4,6], [0,4,8]]
	for combi in combinaisons:
		if tableu_en_cours[combi[0]] == 1 and tableu_en_cours[combi[1]] == 1 and tableu_en_cours[combi[2]] == 1:
			score[0] += 1
			affiche_le_gagnant('x', combi)
		if tableu_en_cours[combi[0]] == 0 and tableu_en_cours[combi[1]] == 0 and tableu_en_cours[combi[2]] == 0:
			score[1] += 1
			affiche_le_gagnant('o', combi)
	tableau_plein = True
	for x in tableu_en_cours:
		if x == 2: tableau_plein = False
	if tableau_plein == True:
		nouvelle_police = pygame.font.SysFont('Algerian', 90)
		pygame.font.Font.set_bold
		texte = nouvelle_police.render('PARTIE NULLE', True, violet)
		fenetre.blit(texte, (80, fenetre.get_height() // 2))
		pygame.display.update()
		pygame.time.delay(5000)
		debut()

def verifie_click(position_souris, point_haut_gauche):
	point_bas_droite = [point_haut_gauche[0] + taille_xo, point_haut_gauche[1] + taille_xo]
	if position_souris[0] >= point_haut_gauche[0] and position_souris[1] >= point_haut_gauche[1]:
		if position_souris[0] <= point_bas_droite[0] and position_souris[1] <= point_bas_droite[1]:
			return True
		else:
			return False
	else:
		return False

def dessine_xo(position_souris):
	global joueur
	for i in range(9):
		x = positions[i]
		if verifie_click(position_souris, x) == True:
			if tableu_en_cours[i] > 1:
				tableu_en_cours[i] = joueur
				if joueur == 1:
					fenetre.blit(X_IMAGE, x)
					joueur = 0
				else:
					fenetre.blit(O_IMAGE, x)
					joueur = 1
				pygame.display.flip()
				verifie_gagnant()
				break

while True: #boucle sans fin (sauf si on appuye sur 'Echap', ou fermé avec la souris)
	# on lit ce qui se passe sur le clavier et la souris
	for action in pygame.event.get():         # pour chaque évènement qui se passe
		if action.type == pygame.KEYDOWN:     # si sur le clavier une touche a été appuyée
			if action.key == pygame.K_ESCAPE: # si cette touche est le 'Echap' :
				print("\nTouche 'ECHAP' appuyée => Fin du jeu...")
				quit()
		if action.type == pygame.QUIT:        # si la souris a fermé la fenêtre
			print("\nFenêtre fermée avec la souris => Fin du jeu...")
			quit()
		if action.type == pygame.MOUSEBUTTONDOWN: # si une touche de la souris est appuyée
			dessine_xo(pygame.mouse.get_pos())                           # on appelle la fonction 'click'

