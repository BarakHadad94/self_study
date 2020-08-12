import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, ship, bullets):

    for event in pygame.event.get():
        # if exits
        if event.type == pygame.QUIT:
            sys.exit()
        # if press right or left or space
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        # if releases right or left
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    # create new bullet and add to bullet group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, aliens, bullets):
    # set background color
    screen.fill(ai_settings.bg_color)
    # redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # draw ship
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()
    # get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    # check if bullets hit aliens, and delete both bullet and alien if so
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # destroy existing bullets and create new fleet
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def create_fleet(ai_settings, screen, ship, aliens):
    # create a full fleet of aliens
    # create an alien and find the number of aliens in a row
    # spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_alien_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # determine the number of rows of aliens that fit in the screen
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
    aliens.add(alien)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    # respond to ship being hit by alien
    if stats.ships_left > 0:
        # dec ships_left
        stats.ships_left -= 1
        # empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    # check if fleet is at edge, then update positions
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # look for aliens hitting the bottom
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    # check if any aliens have reached the bottom of the screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat the same way as when an alien hit a ship
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def check_fleet_edges(ai_settings, aliens):
    # respond if any aliens has reached the edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # drop the fleet and change it's direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
