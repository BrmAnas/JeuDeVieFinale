import numpy as np

class Game:
    def __init__(self, size=50):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)


    def update(self):
        #Met à jour l'état de la grille
        new_grid = np.zeros_like(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                alive_neighbors = self.count_cellule_voisine(i, j)
                if self.grid[i][j] == 1:
                    if alive_neighbors == 2 or alive_neighbors == 3:
                        new_grid[i][j] = 1
                elif alive_neighbors == 3:
                    new_grid[i][j] = 1
        self.grid = new_grid

    def count_cellule_voisine(self, x, y):
        #Compte le nombre de voisins que possède une cellule
        voisins = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        alive_count = 0
        for dx, dy in voisins:
            nx, ny = (x + dx) % self.size, (y + dy) % self.size 
            alive_count += self.grid[nx, ny]
        return alive_count


    def count_cellule_vivante(self):
        #Compte le nombre de cellule
        return np.sum(self.grid)
        
    def aleatoire(self):
        #Initialise la grille aléatoirement
        self.grid = np.random.randint(2, size=(self.size, self.size))

    def reset(self):
        #Réinitialise la grille
        self.grid = np.zeros((self.size, self.size), dtype=int)


    def sauvegarder(self, filename):
        #Enregistre l'état actuel de la grille dans un fichier texte
        with open(filename, 'w') as file:
            for row in self.grid:
                file.write("".join(map(str, row)) + "\n")

    def charger(self, filename):
        #Charge l'état de la grille à partir d'un fichier texte
        with open(filename, 'r') as file:
            self.grid = np.array(
                [[int(char) for char in line.strip()] for line in file.readlines()],
                dtype=int
            )

