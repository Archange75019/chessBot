import chess
import chess.engine
import pygame
import os
import sys

# === CONSTANTES ===
TAILLE_CASE = 80  # Taille d'une case de l'échiquier en pixels
MARGE_BORD = 30   # Marge à gauche pour les chiffres des lignes
MARGE_BAS = 40    # Marge en bas pour les lettres des colonnes et les messages
TAILLE_FENETRE = 8 * TAILLE_CASE + MARGE_BORD + MARGE_BAS
COULEUR_BLANC = (255, 255, 255)
COULEUR_NOIR = (128, 128, 128)
COULEUR_SELECTION = (173, 216, 230)  # Couleur de surbrillance pour la case sélectionnée

def obtenir_mouvements_legaux(board, case_depart):
    """
    Retourne la liste des cases d'arrivée possibles pour une pièce donnée,
    en coordonnées d'affichage (x, y).

    Args:
        board (chess.Board): L'état actuel de l'échiquier.
        case_depart (tuple): Coordonnées (x, y) de la case de départ en affichage.

    Returns:
        list: Liste des coordonnées (x, y) des cases d'arrivée possibles.
    """
    x_depart, y_depart = case_depart
    depart = chess.square(x_depart, 7 - y_depart)  # Conversion en case chess
    mouvements_legaux = []

    for move in board.legal_moves:
        if move.from_square == depart:
            x_arrivee = chess.square_file(move.to_square)
            y_arrivee = 7 - chess.square_rank(move.to_square)  # Conversion en coordonnées d'affichage
            mouvements_legaux.append((x_arrivee, y_arrivee))

    return mouvements_legaux

def charger_images_pieces():
    """
    Charge les images des pièces d'échecs depuis le dossier 'images'.
    Les images doivent être nommées selon le format : 'chess_piece_2_{couleur}_{type}.png'.

    Returns:
        dict: Dictionnaire associant chaque symbole de pièce à son image.
    """
    pieces = {}
    roles = {'P': 'pawn', 'N': 'knight', 'B': 'bishop', 'R': 'rook', 'Q': 'queen', 'K': 'king'}
    couleurs = {chess.WHITE: 'white', chess.BLACK: 'black'}

    for symbole, role in roles.items():
        for couleur_code, couleur_nom in couleurs.items():
            nom_fichier = f"images/chess_piece_2_{couleur_nom}_{role}.png"
            if os.path.exists(nom_fichier):
                image = pygame.image.load(nom_fichier).convert_alpha()
                image = supprimer_fond_blanc(image)
                piece_nom = symbole if couleur_code == chess.WHITE else symbole.lower()
                pieces[piece_nom] = image
            else:
                print(f"⚠️ Image manquante : {nom_fichier}")

    return pieces

def supprimer_fond_blanc(image):
    """
    Rend transparent les pixels blancs d'une image.

    Args:
        image (pygame.Surface): Image à modifier.

    Returns:
        pygame.Surface: Image avec le fond blanc transparent.
    """
    image = image.copy()
    image.lock()
    largeur, hauteur = image.get_size()

    for x in range(largeur):
        for y in range(hauteur):
            couleur = image.get_at((x, y))
            if couleur.r > 240 and couleur.g > 240 and couleur.b > 240:
                image.set_at((x, y), (0, 0, 0, 0))

    image.unlock()
    return image

def choisir_promotion(fenetre, couleur):
    """
    Affiche une interface pour choisir la pièce de promotion d'un pion.

    Args:
        fenetre (pygame.Surface): Fenêtre principale du jeu.
        couleur (chess.Color): Couleur du joueur (BLACK ou WHITE).

    Returns:
        str: Symbole de la pièce choisie ('q', 'r', 'b', 'n').
    """
    options = ['q', 'r', 'b', 'n']
    font = pygame.font.SysFont(None, 40)
    selection = None

    while selection is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                index = x // (TAILLE_CASE * 2)
                if 0 <= index < 4:
                    selection = options[index]

        fenetre.fill((50, 50, 50))
        for i, p in enumerate(options):
            texte = font.render(p.upper(), True, (255, 255, 255))
            fenetre.blit(texte, (i * TAILLE_CASE * 2 + 20, TAILLE_FENETRE // 2 - 20))
        pygame.display.flip()

    return selection if couleur == chess.WHITE else selection.lower()

def dessiner_echiquier(fenetre, board, selectionnee=None, pieces_images=None, message_ia=""):
    """
    Dessine l'échiquier, les pièces, les cases sélectionnées et les mouvements possibles.

    Args:
        fenetre (pygame.Surface): Fenêtre principale du jeu.
        board (chess.Board): L'état actuel de l'échiquier.
        selectionnee (tuple): Coordonnées (x, y) de la case sélectionnée.
        pieces_images (dict): Dictionnaire des images des pièces.
        message_ia (str): Message à afficher en bas de l'écran.
    """
    font = pygame.font.SysFont(None, 24)

    # Vider la surface
    fenetre.fill((200, 200, 200))

    # Dessiner les cases
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(MARGE_BORD + x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            couleur = COULEUR_BLANC if (x + y) % 2 == 0 else COULEUR_NOIR
            pygame.draw.rect(fenetre, couleur, rect)

            # Surligner la case sélectionnée
            if selectionnee and (x, y) == selectionnee:
                pygame.draw.rect(fenetre, COULEUR_SELECTION, rect)

    # Surligner les mouvements possibles
    if selectionnee:
        mouvements_possibles = obtenir_mouvements_legaux(board, selectionnee)
        for (mx, my) in mouvements_possibles:
            rect = pygame.Rect(MARGE_BORD + mx * TAILLE_CASE, my * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            s = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
            s.fill((127, 255, 212, 128))  # Couleur semi-transparente
            fenetre.blit(s, rect)

    # Dessiner les pièces
    for y in range(8):
        for x in range(8):
            piece = board.piece_at(chess.square(x, 7 - y))
            if piece and pieces_images and piece.symbol() in pieces_images:
                image = pieces_images[piece.symbol()]
                img_rect = image.get_rect()
                pos_x = MARGE_BORD + x * TAILLE_CASE + (TAILLE_CASE - img_rect.width) // 2
                pos_y = y * TAILLE_CASE + (TAILLE_CASE - img_rect.height) // 2
                fenetre.blit(image, (pos_x, pos_y))

    # Dessiner chiffres et lettres
    for i in range(8):
        chiffre = str(8 - i)
        texte_chiffre = font.render(chiffre, True, (0, 0, 0))
        fenetre.blit(texte_chiffre, (5, i * TAILLE_CASE + TAILLE_CASE // 2 - 8))

    for i in range(8):
        lettre = chr(ord('a') + i)
        texte_lettre = font.render(lettre, True, (0, 0, 0))
        fenetre.blit(texte_lettre, (MARGE_BORD + i * TAILLE_CASE + TAILLE_CASE // 2 - 6, 8 * TAILLE_CASE + 10))

    # Afficher le message de l'IA
    texte_ia = font.render(message_ia, True, (255, 0, 0))
    fenetre.blit(texte_ia, (MARGE_BORD, 8 * TAILLE_CASE + 25))

def get_case_from_mouse(pos):
    """
    Convertit les coordonnées de la souris en coordonnées de case (x, y).

    Args:
        pos (tuple): Coordonnées (x, y) de la souris.

    Returns:
        tuple: Coordonnées (x, y) de la case.
    """
    x, y = pos
    return x // TAILLE_CASE, y // TAILLE_CASE

def choisir_niveau_interface():
    """
    Affiche une interface pour choisir le niveau de difficulté de l'IA.

    Returns:
        int: Niveau de difficulté sélectionné (1 à 20).
    """
    fenetre_niveau = pygame.display.set_mode((800, 200))
    pygame.display.set_caption("Choisis la difficulté")
    font = pygame.font.SysFont(None, 30)
    clock = pygame.time.Clock()
    boutons = []
    nb_niveaux = 20
    largeur_bouton = 35
    hauteur_bouton = 50
    marge = 10
    start_x = marge
    start_y = 80

    for i in range(nb_niveaux):
        rect = pygame.Rect(start_x + i * (largeur_bouton + marge), start_y, largeur_bouton, hauteur_bouton)
        boutons.append((rect, i + 1))

    niveau_selectionne = None
    while niveau_selectionne is None:
        fenetre_niveau.fill((50, 50, 50))
        texte = font.render("Clique sur le niveau IA désiré", True, (255, 255, 255))
        fenetre_niveau.blit(texte, (20, 30))

        for rect, numero in boutons:
            pygame.draw.rect(fenetre_niveau, (100, 100, 200), rect)
            txt = font.render(str(numero), True, (255, 255, 255))
            txt_rect = txt.get_rect(center=rect.center)
            fenetre_niveau.blit(txt, txt_rect)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for rect, numero in boutons:
                    if rect.collidepoint(pos):
                        niveau_selectionne = numero
                        break

    pygame.display.quit()
    return niveau_selectionne

def jouer_contre_ia(niveau=10):
    """
    Lance une partie d'échecs contre l'IA avec le niveau de difficulté spécifié.

    Args:
        niveau (int): Niveau de difficulté de l'IA (1 à 20).
    """
    board = chess.Board()
    chemin_stockfish = os.path.join("stockfish", "stockfish-windows-x86-64-avx2.exe")

    if not os.path.exists(chemin_stockfish):
        print(f"Erreur : Stockfish non trouvé à {chemin_stockfish}")
        return

    with chess.engine.SimpleEngine.popen_uci(chemin_stockfish) as engine:
        fenetre = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
        pygame.display.set_caption("♟️ Échecs contre IA")
        clock = pygame.time.Clock()
        pieces_images = charger_images_pieces()
        selectionnee = None
        message_ia = "Sélectionne un pion blanc pour jouer..."
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = get_case_from_mouse(event.pos)
                    case = chess.square(x, 7 - y)
                    piece = board.piece_at(case)

                    if selectionnee is None:
                        if piece and piece.color == chess.WHITE:
                            selectionnee = (x, y)
                            message_ia = f"Pièce sélectionnée : {piece.symbol()}"
                    else:
                        sx, sy = selectionnee
                        depart = chess.square(sx, 7 - sy)
                        arrivee = chess.square(x, 7 - y)
                        move = chess.Move(depart, arrivee)

                        # Promotion
                        if board.piece_at(depart).piece_type == chess.PAWN and chess.square_rank(arrivee) in [0, 7]:
                            promotion_piece = choisir_promotion(fenetre, board.turn)
                            move = chess.Move(depart, arrivee, promotion=chess.PIECE_SYMBOLS.index(promotion_piece.lower()))

                        if move in board.legal_moves:
                            board.push(move)
                            selectionnee = None
                            message_ia = "L'IA réfléchit..."

                            # IA joue
                            limit = chess.engine.Limit(time=0.1 * (21 - niveau))
                            result = engine.play(board, limit)
                            board.push(result.move)
                            message_ia = f"L'IA joue : {result.move.uci()}"
                        else:
                            selectionnee = None
                            message_ia = "Mouvement non légal. Recommence."

            dessiner_echiquier(fenetre, board, selectionnee, pieces_images, message_ia)
            pygame.display.flip()
            clock.tick(30)

            # Fin de partie
            if board.is_game_over():
                font = pygame.font.SysFont(None, 40)
                resultat = board.result()
                fenetre.fill((50, 50, 50))
                texte_fin = font.render(f"Partie terminée : {resultat}", True, (255, 255, 255))
                fenetre.blit(texte_fin, (TAILLE_FENETRE//2 - 150, TAILLE_FENETRE//2 - 20))
                pygame.display.flip()
                pygame.time.wait(3000)

                # Relancer une nouvelle partie
                jouer_contre_ia(niveau)
                running = False
                break

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    niveau = choisir_niveau_interface()  # Fenêtre de sélection
    jouer_contre_ia(niveau)              # Lancer le jeu
