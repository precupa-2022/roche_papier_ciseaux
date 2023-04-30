"""
Nom: Alexander Precup
Groupe: 402
Date de remise: 2023-04-29
Description du programme: TP6 - Jeu de style roche, papier, ciseaux.
"""
import arcade
import random

from game_state import GameState
from attack_animation import AttackType
from attack_animation import AttackAnimation

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
SPRITE_SCALING_PLAYER = 0.20
SPRITE_SCALING_OBJECTS = 0.25


class MyGame(arcade.Window):
    """
    La classe principale de l'application roche, papier, ciseaux
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Dessiner l'arrière-plan
        arcade.set_background_color(arcade.color.AMAZON)

        # Initialiser les variables du jeu
        self.player = None
        self.computer = None
        self.rock = None
        self.paper = None
        self.scissors = None
        self.computer_attack = None
        self.player_attack_type = None
        self.computer_attack_type = None
        self.game_state = GameState.NOT_STARTED
        self.player_score = 0
        self.computer_score = 0
        self.player_attacked = False
        self.player_wins_round = False
        self.ronde_nulle = False

    def setup(self):
        """
        Configurer les variables du jeu
        Cette méthode est appelée chaque fois qu'une nouvelle partie commence
        """

        # self.player_score = 0
        # self.computer_score = 0
        # self.game_state = GameState.NOT_STARTED

        """  Créer le sprite joueur """
        self.player = arcade.Sprite("assets/faceBeard.png", SPRITE_SCALING_PLAYER)
        self.player.center_x = 200
        self.player.center_y = 225
        """  Créer le sprite ordinateur """
        self.computer = arcade.Sprite("assets/compy.png")
        self.computer.center_x = 600
        self.computer.center_y = 225
        """  Créer les sprites roche, papier, ciseaux """
        self.rock = arcade.Sprite("assets/srock.png", SPRITE_SCALING_OBJECTS)
        self.paper = arcade.Sprite("assets/spaper.png", SPRITE_SCALING_OBJECTS)
        self.scissors = arcade.Sprite("assets/scissors.png", SPRITE_SCALING_OBJECTS)

    def on_draw(self):
        """
        Méthode qu'Arcade invoque à chaque "frame" pour afficher les éléments du jeu à l'écran.
        """

        """
        Effacer l'écran avant de dessiner.
        Dessiner l'arrière-plan selon la couleur spécifiée avec la méthode "set_background_color".
        """
        arcade.start_render()

        """ Afficher les textes """
        arcade.draw_text("Roche, papier, ciseaux",
                         0, 500, arcade.csscolor.DARK_MAGENTA, 50, width=SCREEN_WIDTH, align="center")
        arcade.draw_text(f"Le pointage du joueur est {self.player_score} ",
                         100, 100, arcade.csscolor.HONEYDEW, 10, width=SCREEN_WIDTH, align="left")
        arcade.draw_text(f"Le pointage de l'ordinateur est {self.computer_score}",
                         500, 100, arcade.csscolor.HONEYDEW, 10, width=SCREEN_WIDTH, align="left")

        """ Afficher les sprites joueur et ordinateur """
        self.player.draw()
        self.computer.draw()

        """ Afficher les éléments nécessaires pour chaque état du jeu courant """
        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text("Appuyer sur une image pour faire une attaque !",
                             0, 450, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
            """ Afficher le sprite roche dans un rectangle rouge """
            arcade.draw_rectangle_outline(125, 150, 50, 50, arcade.color.SIENNA)
            self.rock.center_x = 125
            self.rock.center_y = 150
            self.rock.draw()
            """ Afficher le sprite papier dans un rectangle rouge """
            arcade.draw_rectangle_outline(200, 150, 50, 50, arcade.color.SIENNA)
            self.paper.center_x = 200
            self.paper.center_y = 150
            self.paper.draw()
            """ Afficher le sprite ciseaux dans un rectangle rouge """
            arcade.draw_rectangle_outline(275, 150, 50, 50, arcade.color.SIENNA)
            self.scissors.center_x = 275
            self.scissors.center_y = 150
            self.scissors.draw()

            """ Afficher le rectangle rouge pour le sprite choix ordinateur """
            arcade.draw_rectangle_outline(600, 150, 50, 50, arcade.color.SIENNA)

        elif self.game_state == GameState.ROUND_ACTIVE:
            arcade.draw_text("Appuyer sur une image pour faire une attaque !",
                             0, 450, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
            """ Afficher le sprite roche dans un rectangle rouge """
            arcade.draw_rectangle_outline(125, 150, 50, 50, arcade.color.SIENNA)
            self.rock.center_x = 125
            self.rock.center_y = 150
            self.rock.draw()
            """ Afficher le sprite papier dans un rectangle rouge """
            arcade.draw_rectangle_outline(200, 150, 50, 50, arcade.color.SIENNA)
            self.paper.center_x = 200
            self.paper.center_y = 150
            self.paper.draw()
            """ Afficher le sprite ciseaux dans un rectangle rouge """
            arcade.draw_rectangle_outline(275, 150, 50, 50, arcade.color.SIENNA)
            self.scissors.center_x = 275
            self.scissors.center_y = 150
            self.scissors.draw()

            """ Afficher le rectangle rouge pour le sprite choix ordinateur """
            arcade.draw_rectangle_outline(600, 150, 50, 50, arcade.color.SIENNA)

        elif self.game_state == GameState.ROUND_DONE:
            arcade.draw_text("Appuyer sur 'ESPACE' pour commencer une nouvelle ronde !",
                             0, 450, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
            if self.player_wins_round:
                arcade.draw_text("Vous avez gagné la ronde !",
                                 0, 350, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
            else:
                if self.ronde_nulle:
                    arcade.draw_text("Match nul !",
                                     0, 350, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
                else:
                    arcade.draw_text("L'ordinateur a gagné la ronde !",
                                     0, 350, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")

            """ Afficher le sprite roche animé dans un rectangle rouge si le joueur a choisi roche """
            arcade.draw_rectangle_outline(125, 150, 50, 50, arcade.color.SIENNA)
            if self.player_attack_type == AttackType.ROCK:
                self.rock.center_x = 125
                self.rock.center_y = 150
                self.rock.draw()
            """ Afficher le sprite papier animé dans un rectangle rouge si le joueur a choisi papier """
            arcade.draw_rectangle_outline(200, 150, 50, 50, arcade.color.SIENNA)
            if self.player_attack_type == AttackType.PAPER:
                self.paper.center_x = 200
                self.paper.center_y = 150
                self.paper.draw()
            """ Afficher le sprite ciseaux animé dans un rectangle rouge si le joueur a choisi ciseaux """
            arcade.draw_rectangle_outline(275, 150, 50, 50, arcade.color.SIENNA)
            if self.player_attack_type == AttackType.SCISSORS:
                self.scissors.center_x = 275
                self.scissors.center_y = 150
                self.scissors.draw()
            """ Afficher le sprite ordinateur (généré aléatoire) animé dans un rectangle rouge """
            arcade.draw_rectangle_outline(600, 150, 50, 50, arcade.color.SIENNA)
            self.computer_attack.center_x = 600
            self.computer_attack.center_y = 150
            self.computer_attack.draw()

        elif self.game_state == GameState.GAME_OVER:
            if self.player_score == 3:
                arcade.draw_text("Vous avez gagné la partie !",
                                 0, 350, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
            elif self.computer_score == 3:
                arcade.draw_text("Vous avez perdu la partie !",
                                 0, 350, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")

            arcade.draw_text("La partie est terminée.",
                             0, 400, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
            arcade.draw_text("Appuyer sur 'ESPACE' pour débuter une nouvelle partie.",
                             0, 450, arcade.csscolor.HONEYDEW, 20, width=SCREEN_WIDTH, align="center")
            """ Afficher le sprite roche animé dans un rectangle rouge si le joueur a choisi roche """
            arcade.draw_rectangle_outline(125, 150, 50, 50, arcade.color.SIENNA)
            if self.player_attack_type == AttackType.ROCK:
                self.rock.center_x = 125
                self.rock.center_y = 150
                self.rock.draw()
            """ Afficher le sprite papier animé dans un rectangle rouge si le joueur a choisi papier """
            arcade.draw_rectangle_outline(200, 150, 50, 50, arcade.color.SIENNA)
            if self.player_attack_type == AttackType.PAPER:
                self.paper.center_x = 200
                self.paper.center_y = 150
                self.paper.draw()
            """ Afficher le sprite ciseaux animé dans un rectangle rouge si le joueur a choisi ciseaux """
            arcade.draw_rectangle_outline(275, 150, 50, 50, arcade.color.SIENNA)
            if self.player_attack_type == AttackType.SCISSORS:
                self.scissors.center_x = 275
                self.scissors.center_y = 150
                self.scissors.draw()

            """ Afficher le sprite ordinateur (généré aléatoire) animé dans un rectangle rouge """
            arcade.draw_rectangle_outline(600, 150, 50, 50, arcade.color.SIENNA)
            self.computer_attack.center_x = 600
            self.computer_attack.center_y = 150
            self.computer_attack.draw()

    def on_update(self, delta_time):
        """
        La logique pour simuler la logique du jeu.
        Invoquer la méthode "update()" sur les sprites.
        Paramètre:
            - delta_time : le nombre de millisecondes depuis le dernier update.
        """

        """ Si le joueur a attaqué, anime le sprite choisi par le joueur """
        if self.player_attacked:
            self.rock.on_update()
            self.paper.on_update()
            self.scissors.on_update()
        """ Si la partie est active et le joueur a attaqué """
        if self.game_state == GameState.ROUND_ACTIVE and self.player_attacked:
            """ Générer l'attaque d'ordinateur """
            pc_attack = random.randint(0, 2)
            """ Appliquer les règles du jeu et calculer le pointage """
            if pc_attack == 0:
                self.computer_attack_type = AttackType.ROCK
                self.computer_attack = arcade.Sprite("assets/srock-attack.png", SPRITE_SCALING_OBJECTS)
                if self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK:
                    self.player_score += 1
                    self.player_wins_round = True
                elif self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.ROCK:
                    self.computer_score += 1
                else:
                    self.ronde_nulle = True
            elif pc_attack == 1:
                self.computer_attack_type = AttackType.PAPER
                self.computer_attack = arcade.Sprite("assets/spaper-attack.png", SPRITE_SCALING_OBJECTS)
                if self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.PAPER:
                    self.computer_score += 1
                elif self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER:
                    self.player_score += 1
                    self.player_wins_round = True
                else:
                    self.ronde_nulle = True
            else:
                self.computer_attack_type = AttackType.SCISSORS
                self.computer_attack = arcade.Sprite("assets/scissors-close.png", SPRITE_SCALING_OBJECTS)
                if self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS:
                    self.player_score += 1
                    self.player_wins_round = True
                elif self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.SCISSORS:
                    self.computer_score += 1
                else:
                    self.ronde_nulle = True
            """ Afficher le sprite d'ordinateur """
            self.computer_attack.on_update()
            """ Si le joueur ou l'ordinateur ont un pointage de 3, le jeu est fini """
            if self.player_score < 3 and self.computer_score < 3:
                self.game_state = GameState.ROUND_DONE
            else:
                self.game_state = GameState.GAME_OVER

    def on_key_press(self, key, key_modifiers):
        """
        Cette méthode est invoquée à chaque fois que l'usager tape une touche 'ESPACE'
        sur le clavier.
        Paramètres:
            - key: la touche enfoncée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """

        """ Changer l'état du jeu avec la touche 'ESPACE' """
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.ROUND_ACTIVE
            elif self.game_state == GameState.ROUND_DONE:
                self.game_state = GameState.ROUND_ACTIVE
                # Initialiser les variables du jeu
                self.player_attack_type = None
                self.computer_attack_type = None
                self.player_attacked = False
                self.player_wins_round = False
                self.ronde_nulle = False
            elif self.game_state == GameState.GAME_OVER:
                self.game_state = GameState.NOT_STARTED
                # Initialiser les variables du jeu et le pointage
                self.player_attack_type = None
                self.computer_attack_type = None
                self.player_attacked = False
                self.player_wins_round = False
                self.ronde_nulle = False
                self.player_score = 0
                self.computer_score = 0

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Méthode invoquée lorsque l'usager clique un bouton de la souris.
        Paramètres:
            - x, y: coordonnées où le bouton a été cliqué
            - button: le bouton de la souris appuyé
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """
        if self.game_state == GameState.NOT_STARTED:
            self.game_state = GameState.ROUND_ACTIVE
        """ 
        Valider si le joueur attaque (clique sur un des sprites)
        Indiquer le type d'attaque choisi par le joueur, indiqué que le joueur a attaqué et animé le sprite choisi
        """
        if self.rock.collides_with_point((x, y)):
            self.player_attack_type = AttackType.ROCK
            self.player_attacked = True
            self.rock = AttackAnimation(AttackType.ROCK)
        elif self.paper.collides_with_point((x, y)):
            self.player_attack_type = AttackType.PAPER
            self.player_attacked = True
            self.paper = AttackAnimation(AttackType.PAPER)
        elif self.scissors.collides_with_point((x, y)):
            self.player_attack_type = AttackType.SCISSORS
            self.player_attacked = True
            self.scissors = AttackAnimation(AttackType.SCISSORS)


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
