import sys 
from time import sleep
import pygame
from settings import Settings
from game_stats import Stats
from button import Button
from ship import Ship 
from bullet import Bullet
from aliens import Alien
from scoreboard import Scoreboard



class AlienInvasion: 
    """Class structure to manage game assests and behavior"""
    def __init__(self): 
        """ Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.stats = Stats(self)
        self.scoreboard = Scoreboard(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        #Make the Button to start the game 
        self.play_button = Button(self, 'Start')
        
    def run_game(self): 
        """ Set the main loop for the game"""
        while True: 
            self._check_events()
            if self.stats.game_active == True:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()        
            self._update_screen()
            
    def _check_events(self):
        #Watch for keyboad and mouse activity
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP: 
                self._check_keyup_events(event)

            elif event.type == pygame.K_SPACE: 
                self._fire_bullets()
    
    def _check_play_button(self, mouse_pos): 
        """Start a new game when the player clicks play.""" 
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active: 
            #Reset the game stats 
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True 
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            #Hid the mouse cursor. 
            pygame.mouse.set_visible(False)

            #get rid of remaining aliens and bullets 
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship 
            self._create_fleet()
            self.ship.center_ship()
            
            
             
    

    def _check_keydown_events(self, event): 

        if event.key == pygame.K_RIGHT: 
                #Respond to key presses
                self.ship.moving_right = True
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = True

        elif event.key == pygame.K_q: 
            sys.exit()
        
        elif event.key == pygame.K_SPACE: 
            self._fire_bullets()

    def _check_keyup_events(self, event): 
        #Respond to key release
            if event.key == pygame.K_RIGHT: 
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT: 
                self.ship.moving_left = False
    
    def _fire_bullets(self):
        """Creates a bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed: 
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self): 
        """update the position of the bullets and get rid of old bullets. They missed their target so they are clearly faulty."""
        for bullet in self.bullets.copy(): 
                if bullet.rect.bottom <= 0: 
                    self.bullets.remove(bullet)
        self._check_for_bullet_collision()
        
    def _check_for_bullet_collision(self):
        """Check for bullets that have hit aliens, if they hit the alien, get rid of it!
        when the fleet is cleared, create another one!""" 
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions: 
            for aliens in collisions.values(): 
                self.stats.score += self.settings.alien_points * len(aliens)
                self.scoreboard.prep_score()
                self.scoreboard.check_high_scores()

        if not self.aliens: 
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level

    def _update_aliens(self): 
        """Check if the fleet is at an edge, then
        Update the positions of all aliens in the fleet.""" 
        self._check_fleet_edges()
        self.aliens.update()
        #Check to see is an alien ship hits the players ship 
        if pygame.sprite.spritecollideany(self.ship, self.aliens): 
            self._ship_hit()
        #Watch out for the alien ships hitting the players ship
        self._check_aliens_bottom()

    def _ship_hit(self): 
        #decrement ships_left. 
        if self.stats.ships_left > 0: 
            self.stats.ships_left -=1
            self.scoreboard.prep_ships()
            #Get rid of any remaining aliens and bullets. 
            self.aliens.empty() 
            self.bullets.empty()
        else: 
            self.stats.game_active = False 
            pygame.mouse.set_visible(True)


        #Create a new fleet and center the ship 
        self._create_fleet()
        self.ship.center_ship() 
        #Pause for .5 seconds 
        sleep(0.5)


    def _create_fleet(self): 
        """Create the fleet of aliens""" 
        
        #Create an alien and find the number of aliens in a row. 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width) 
        number_aliens_x = available_space_x // (2 * alien_width)
        #Determine the number of rows of aliens that fit on the screen 
        ship_height = self.ship.rect.height 
        available_space_y = self.settings.screen_height-(3 * alien_height - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        #Create the fleet of aliens 
        for row_number in range(number_rows): 
            for alien_number in range(number_aliens_x): 
                self._create_alien(alien_number, row_number)
                #create an alien and place it in the row

    def _check_fleet_edges(self): 
        """If the fleet reaches the edge of the screen, move them down and change the direction """ 
        for alien in self.aliens.sprites(): 
            if alien.check_edges(): 
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self): 
        """Drop the entire fleet and change the fleet's direction.""" 
        for aliens in self.aliens.sprites(): 
            aliens.rect.y += self.settings.fleet_advance_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number): 
        "Create an alien and place it in the row"
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
        self.aliens.add(alien)

    def _check_aliens_bottom(self): 
        """Check if any alins have reached the bottom of the screen.""" 
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites(): 
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as the ship getting hit by an alien. 
                self._ship_hit()
                break 

        

    def _update_screen(self):
        # Redraw the sceen with each pass of the loop 
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()
        #draw the aliens group to the screen 
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()

        if not self.stats.game_active: 
            self.play_button.draw_button()
    
        pygame.display.flip()

    



if __name__ == '__main__': 
    #make an instance of the game and run it
    ai  = AlienInvasion()
    ai.run_game()
    
    