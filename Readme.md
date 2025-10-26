# ChessBot

Un jeu d'échecs en Python utilisant **Pygame** pour l'interface graphique et **Stockfish** comme moteur d'IA.

---

## 📋 Description

Ce projet permet de jouer aux échecs contre une IA basée sur le moteur **Stockfish**. L'interface graphique est développée avec **Pygame**, et le jeu propose plusieurs niveaux de difficulté pour s'adapter à tous les joueurs.

---

## 🎮 Fonctionnalités

- Jouez contre une IA avec **20 niveaux de difficulté**.
- Surlignage des **mouvements possibles** pour la pièce sélectionnée.
- Interface graphique intuitive avec affichage des pièces et des cases.
- Gestion des **promotions de pions**.
- Affichage des messages de l'IA et des résultats de partie.

---

## 📥 Prérequis

- **Python 3.8 ou supérieur**


- Stockfish (moteur d'échecs) : à télécharger depuis le site officiel et placer dans le dossier stockfish.


## 🛠 Installation

- Clonez ce dépôt :

    ```bash
    https://github.com/Archange75019/chessBot.git
    cd chessBot-main
    ```

- Créer un environnement virtuel :
    ```bash
  python -m venv venv
  source venv/bin/activate
- Installez les dépendances :
    ```bash
  pip install -r requirements.txt

- Téléchargez Stockfish et placez l'exécutable dans un dossier stockfish.
  https://stockfishchess.org/download/
- Assurez-vous que les images des pièces sont dans le dossier images :

Les images doivent être nommées selon le format : chess_piece_2_{couleur}_{type}.png.
Exemple : chess_piece_2_white_knight.png pour un cavalier blanc.




## 🚀 Utilisation


Lancez le jeu :
```bash
python main.py
```
- Sélectionnez le niveau de difficulté de l'IA (de 1 à 20).
- Jouez en cliquant sur les pièces et les cases de destination :

Les mouvements possibles sont surlignés en bleu clair.
Les messages de l'IA s'affichent en bas de l'écran.




## 📂 Structure du projet
```bash
Copierechecs-ia/
│
├── main.py          # Code principal du jeu
├── stockfish/             # Dossier contenant l'exécutable de Stockfish
│   └── stockfish-windows-x86-64-avx2.exe
│
├── images/                # Dossier contenant les images des pièces
│   ├── chess_piece_2_white_pawn.png
│   ├── chess_piece_2_white_knight.png
│   ├── ...
│   └── chess_piece_2_black_king.png
│
└── README.md              # Ce fichier
```
## ⚠️ Problèmes courants


- "Mouvement non permis" :

Vérifiez que la pièce sélectionnée est bien blanche.
Assurez-vous que la case de destination est bien surlignée (mouvement légal).
Si le problème persiste, vérifiez que les coordonnées de la souris sont correctement converties en coordonnées de case.



- Stockfish non trouvé :

Assurez-vous que l'exécutable de Stockfish est dans le dossier stockfish et que le chemin est correct dans le code.




