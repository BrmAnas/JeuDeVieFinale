import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
from game import Game
import matplotlib.pyplot as plt



class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de la Vie")
        self.root.geometry("1000x700")
        self.root.config(bg="#2e3b4e")
        self.size_var = tk.IntVar(value=50)  
        self.game = Game(size=self.size_var.get())
        self.cell_size = 10
        self.offset_x = 0
        self.offset_y = 0
        self.cellule_color_vivante = "red"  
        self.cell_color_dead = "#FFFFFF"  
        self.create_accueil()
        self.liste_graph = []


    def create_accueil(self):
        #Ecran d'accueil
        self.clear_screen()
        title_label = tk.Label(self.root, text="Jeu de la Vie", font=("Helvetica", 40, "bold"), fg="#EEE6D8", bg="#2e3b4e")
        title_label.pack(pady=50)
        
        start_button = self.create_button(self.root, "Démarrer le Jeu", self.start_game)
        start_button.pack(pady=20)
        
        regles_button = self.create_button(self.root, "Règles du Jeu", self.affiche_regle)
        regles_button.pack(pady=20)
        
        taille_label = tk.Label(self.root, text="Taille de la grille :", font=("Helvetica", 12), bg="#2e3b4e", fg="white")
        taille_label.pack(pady=10)
        
        taille_entry = tk.Entry(self.root, textvariable=self.size_var, width=5, font=("Helvetica", 14))
        taille_entry.pack(pady=5)
        
        taille_button = self.create_button(self.root, "Appliquer", self.taille_grid)
        taille_button.pack(pady=10)

    def taille_grid(self):
        #Permet de prendre en compte la nouvelle taille de la grille
        new_size = self.size_var.get()
        self.game = Game(size=new_size)
        self.start_game()

    def start_game(self):
        #Affiche l'interface de jeu
        self.clear_screen()
        self.is_running = False
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="#1e2b34", highlightthickness=0)
        self.canvas.grid(row=0, column=1, padx=20, pady=20)
        self.canvas.bind("<ButtonPress-2>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Button-1>", self.changement_cellule)

        
        self.panel = tk.Frame(self.root, bg="#2e3b4e")
        self.panel.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        self.create_buttons()
        
        self.save_load_panel = tk.Frame(self.root, bg="#2e3b4e")
        self.save_load_panel.grid(row=0, column=2, padx=10, pady=10, sticky="ne")
        self.create_button_droite()
        
        back_button = self.create_button(self.root, "Retour au menu", self.create_accueil, width=15, font_size=10)
        back_button.grid(row=1, column=1, pady=20)
        
        self.aleatoire_grid()
        self.update_grid_display()

    def changement_cellule(self, event):
        #Donne à l'utilisateur la possibilité de changer l'état d'une cellule
        row = (event.y - self.offset_y) // self.cell_size
        col = (event.x - self.offset_x) // self.cell_size

        if 0 <= row < self.game.size and 0 <= col < self.game.size:
            self.game.grid[row][col] = 1 - self.game.grid[row][col]
            self.update_grid_display()


    def create_buttons(self):
        #Permet de créer les boutons
        self.start_stop_button = self.create_button(self.panel, "Lancer", self.play_stop)
        self.start_stop_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        next_button = self.create_button(self.panel, "Étape suivante", self.run_single)
        next_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        random_button = self.create_button(self.panel, "Aléatoire", self.aleatoire_grid)
        random_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        reset_button = self.create_button(self.panel, "Réinitialiser", self.reset_grid)
        reset_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        color_button = self.create_button(self.panel, "Choix couleurs", self.change_cellule_color)
        color_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        zoom_in_button = self.create_button(self.panel, "Zoom +", self.zoom_in)
        zoom_in_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        zoom_out_button = self.create_button(self.panel, "Zoom -", self.zoom_out)
        zoom_out_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        graph_button = self.create_button(self.panel, "Graphique", self.evolution_vie)
        graph_button.grid(row=7, column=0, padx=5, pady=5, sticky="ew")


    def create_button_droite(self):
        #Permet de créer les boutons de sauvegarde
        sauvegarde_button = self.create_button(self.save_load_panel, "Sauvegarder", self.sauvegarder, width=15, font_size=10)
        sauvegarde_button.grid(row=0, column=0, padx=5, pady=5, sticky="ne")

        charge_button = self.create_button(self.save_load_panel, "Charger", self.charger, width=15, font_size=10)
        charge_button.grid(row=1, column=0, padx=5, pady=5, sticky="ne")

    def create_button(self, container, text, command, width=20, font_size=14):
        return tk.Button(container, text=text, font=("Helvetica", font_size), fg="black", bg="lightgray", width=width, command=command, bd=2)


    def play_stop(self):
        #Permet de lancer ou de mettre en pause le jeu
        if not self.is_running:
            self.is_running = True
            self.start_stop_button.config(text="Stop")
            self.run_game()
        else:
            self.is_running = False
            self.start_stop_button.config(text="Lancer")

    def run_game(self):
        #Met a jour la grille
        if self.is_running:
            self.game.update()
            self.update_grid_display()
            self.root.after(100, self.run_game)
            self.liste_graph.append(self.game.count_cellule_vivante())                

    def run_single(self):
        #Avance d'une seule étape
         
        self.game.update()
        self.update_grid_display()
        self.liste_graph.append(self.game.count_cellule_vivante())   

    def aleatoire_grid(self):
        #Initialise la grille aléatoirement
        self.game.aleatoire()
        self.update_grid_display()

    def reset_grid(self):
        #Renitialise le jeu
        self.game.reset()
        self.is_running = False
        self.start_stop_button.config(text="Lancer")
        self.update_grid_display()

    def sauvegarder(self):
        #Sauvegarde le jeu
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            self.game.sauvegarder(filename)
            messagebox.showinfo("Sauvegarde", "Grille sauvegardée !")

    def charger(self):
        #Charge le jeu
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.game.charger(filename)
            self.update_grid_display()
            messagebox.showinfo("Chargement", "Grille chargée !")

    def change_cellule_color(self):
        #Permet de changer la couleur des cellules
        color = colorchooser.askcolor()[1]
        if color:
            self.cellule_color_vivante = color
            self.update_grid_display()

    def update_grid_display(self):
        #Met à jour l'affichage de la grille
        self.canvas.delete("all")
        for i in range(self.game.size):
            for j in range(self.game.size):
                color = self.cellule_color_vivante if self.game.grid[i][j] else self.cell_color_dead
                self.canvas.create_rectangle(
                    j * self.cell_size + self.offset_x,
                    i * self.cell_size + self.offset_y,
                    (j + 1) * self.cell_size + self.offset_x,
                    (i + 1) * self.cell_size + self.offset_y,
                    fill=color, outline="black"
                )
        cellule_vivante_count = self.game.count_cellule_vivante()
        self.cellule_vivante_label = tk.Label(self.root, text=f"Cellules vivantes : {cellule_vivante_count}", font=("Helvetica", 12), bg="#2e3b4e", fg="white")
        self.cellule_vivante_label.grid(row=2, column=1, pady=10)

    def start_drag(self, event):
        #Démarre le déplacement de la grille
        self.drag_data = {"x": event.x, "y": event.y}

    def drag(self, event):
        #Déplace la grille lors du clic-glisser
        self.offset_x += event.x - self.drag_data["x"]
        self.offset_y += event.y - self.drag_data["y"]
        self.update_grid_display()
        self.drag_data = {"x": event.x, "y": event.y}

    def zoom_in(self):
        #Augmente la taille des cellules (Zoom avant)
        self.cell_size = min(self.cell_size + 2, 20)
        self.update_grid_display()

    def zoom_out(self):
        #Diminue la taille des cellules (Zoom arrière)
        self.cell_size = max(self.cell_size - 2, 5)
        self.update_grid_display()

    def affiche_regle(self):
        #Affiche les règles du jeu
        regles = """
        Les règles sont les suivantes:
        - Une cellule vivante avec moins de 2 voisines vivantes meurt (sous-population).
        - Une cellule vivante avec 2 ou 3 voisines vivantes survit.
        - Une cellule vivante avec plus de 3 voisines vivantes meurt (surpopulation).
        - Une cellule morte avec exactement 3 voisines vivantes devient vivante (reproduction).
        """
        messagebox.showinfo("Règles du jeu", regles)

    def clear_screen(self):
        #Efface le contenu de l'écran actuel
        for widget in self.root.winfo_children():
            widget.destroy()

    def evolution_vie(self):
        #Affiche un graphique du nombre de cellules vivantes en fonction du temps
        plt.figure(figsize=(10, 5))
        plt.plot(self.liste_graph, marker='o')
        plt.title("Évolution des cellules vivantes au cours du temps")
        plt.xlabel("Etapes")
        plt.ylabel("Nombre de cellules vivantes")
        plt.show()



