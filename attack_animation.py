import arcade

from enum import Enum


class AttackType(Enum):
    """
    Classe de type énumération pour les différentes types d'attaques.
    """
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class AttackAnimation(arcade.Sprite):
    """
    Classe pour animer une séquence de sprite.
    Paramètre:
        - arcade.Sprite : classe Sprite de la librairie Arcade.
    """
    ATTACK_SCALE = 0.25
    ANIMATION_SPEED = 5.0

    def __init__(self, attack_type):
        super().__init__()
        self.animation_update_time = 1.0 / AttackAnimation.ANIMATION_SPEED
        self.time_since_last_swap = 0.0

        self.attack_type = attack_type
        if self.attack_type == AttackType.ROCK:
            self.textures = [
                arcade.load_texture("assets/srock.png"),
                arcade.load_texture("assets/srock-attack.png"),
            ]
        elif self.attack_type == AttackType.PAPER:
            self.textures = [
                arcade.load_texture("assets/spaper.png"),
                arcade.load_texture("assets/spaper-attack.png"),
            ]
        else:
            self.textures = [
                arcade.load_texture("assets/scissors.png"),
                arcade.load_texture("assets/scissors-close.png"),
            ]

        self.scale = self.ATTACK_SCALE
        self.current_texture = 0
        self.set_texture(self.current_texture)

    def on_update(self, delta_time: float = 1 / 60):
        """
        La logique pour animer les sprites.
        Invoquer la méthode "update()" sur les sprites.
        Paramètre:
            - delta_time : le nombre de millisecondes depuis le dernier update.
        """
        self.time_since_last_swap += delta_time
        if self.time_since_last_swap > self.animation_update_time:
            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:
                self.current_texture = 0
                self.set_texture(self.current_texture)
            self.time_since_last_swap = 0.0
