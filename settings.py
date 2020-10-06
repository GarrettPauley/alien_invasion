
class Settings: 
    """A class to store all of the game settings"""

    def __init__(self): 
        """initialize the game's settings"""
        self.screen_width = 900
        self.screen_height = 500
        self.bg_color = (230,230,230)
        #bullet speed 
        self.bullet_speed = 1.5 
        self.bullet_width = 400
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        #Alien settings 
        self.alien_speed = .3
        self.fleet_advance_speed = 15
        
        #Ship settings 
        self.ship_speed = 1
        self.ship_limit = 3
        #How quickly the game speeds up 
        self.speedup_scale = 1.1
        #How quickly the alien point values increase 
        self.score_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self): 
        """Initialize settings that change throughout the game.""" 
        self.ship_speed = 1
        self.bullet_speed = 1.5 
        self.alien_speed = .3
        #fleet_direction of 1 represets righ; flee_direction of -1 means left 
        self.fleet_direction = 1
        #Scoring 
        self.alien_points = 50 

    def increase_speed(self):
        """Increase speed settings.""" 
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
    