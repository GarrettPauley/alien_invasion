
class Settings: 
    """A class to store all of the game settings"""

    def __init__(self): 
        """initialize the game's settings"""
        self.screen_width = 900
        self.screen_height = 500
        self.bg_color = (230,230,230)
        self.ship_speed = 1.5
        #bullet speed 
        self.bullet_speed = 1.0 
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        self.alien_speed = 1.0 