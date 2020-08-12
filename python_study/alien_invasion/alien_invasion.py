import sys
import pygame
import game_functions as gf

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats


def run_game():
    pygame.init()
    # define the screen
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # create an instance to store game statistics
    stats = GameStats(ai_settings)
    # make a ship
    ship = Ship(ai_settings, screen)
    # make a group to store the bullets in
    bullets = Group()
    aliens = Group()

    # create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


if __name__ == '__main__':
    run_game()
