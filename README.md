Casse-Brique — Tkinter
Auteurs : Stéphane Urbon, Rayane Zidane 3ETI

 1. Règles du jeu
– Détruire toutes les briques pour gagner.  
– La raquette se déplace en continu; Gauche/Droite changent simplement le sens.  
– Si la balle sort par le bas, la raquette rétrécit d’un niveau (3 niveaux → défaite).  
– Briques spéciales malus (délai temporaire) :
Rouge = accélère fortement la balle 
Violette = plateau et contrôles inversés  
Verte = raquette qui est ralentit.  
– Chaque brique vaut 10 points.

2. Lancement
Exécuter : `python main.py`

3. Commandes
Gauche : partir vers la gauche. 
Droite : partir vers la droite. 
Bouton: Rejouer : relance une partie. 
Bouton Quitter : ferme l’application (menu et fin de partie).

4. Architecture
- `main.py` : point d’entrée (fenêtre + lancement du menu)  
- `menu.py` : classe `InterfaceAccueil` (écran titre, Jouer, Quitter)  
- `game.py` : classe `InterfaceJeu` (canvas, briques, raquette, balle, collisions, score, effets)  
 


5. Structures de données 
- Liste : `self.briques` (toutes les briques du canvas).  
- Pile : `self.pile_vitesses` (vitesses pendant le boost rouge; on dépile à la fin).  
- File : `self.file_messages` (messages temporaires au centre; affichage séquentiel).  

6. Spécificités d’implémentation 
- Contrôle dans le style "arcade" : mouvement continu, touches = changement de sens.  
- Hitbox élargie de la raquette : Cela évite que la balle , avec une certaine trajectoire, rentre dans la raquette , rebondit a l'interieur pour ressortir de l'autre coté.  
- Anti-couloir latéral : murs virtuels accolés aux bords du mur de briques cela empêche de passer derrière la première rangée de brique et casser les briques derriere .  
- Effets temporisés : rouge (vitesse), violette (inversion), verte (lourdeur); timers dédiés.  
- Fin de partie : message central, score permanent, boutons Rejouer/Quitter dans la zone de jeu.

7. Paramètres principaux (dans `game.py`)
- Vitesse balle : valeurs de départ et `vitesse_max`.  
- Durées effets : rouge, violette, verte (timers `after`).  
- Hitbox raquette : `hitbox_pad_x`, `hitbox_pad_y`.  
- Fluidité : intervalle d’update (`after(20)`) (ajustabilité non testé).

8. Dépôt Git

https://github.com/stephaneurbon-hue/projetPython

## 9. Contenu de l’archive
Code complet (tous les fichiers ci-dessus), ce `README.md` , URL du dépôt et le rappel des emplacements Liste/Pile/File .
