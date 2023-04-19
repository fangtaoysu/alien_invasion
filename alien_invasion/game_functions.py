import sys
import pygame
import json

from bullet import Bullet
from alien import Alien
from time import sleep


def get_number_aliens_x(ai_settings, alien_width):
	'''计算每行可以容纳多少外星人'''
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (3 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	'''计算屏幕可容纳多少行ufo'''
	available_space_y = ai_settings.screen_height - (5 * alien_height) - ship_height
	number_rows = int(available_space_y / (3 * alien_height))
	return number_rows
	
def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
	'''创建一个外星人并加入当前行'''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	'''创建ufo舰队'''
	# 创建一个外星人，计算一行可容纳多少外星人
	# 外星人间距为外星人宽度
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	for row_number in range(number_rows):
		# 创建一行外星人
		for alien_number in range(number_aliens_x):
			creat_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_keydown_events(event, ai_settings, stats, screen, ship, bullets):
	'''按下按键响应事件'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, stats, screen, ship, bullets)
	elif event.key == pygame.K_q:
		write_max_file(stats.high_score)
		sys.exit()
		
def check_keyup_events(event, ship):
	'''松开按键响应事件'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False

def check_events(ai_settings, stats, sb, screen, play_button, ship, aliens, bullets):
	'''响应按键和鼠标事件'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			write_max_file(stats.high_score)
			sys.exit()
			
		# 检测鼠标按下，返回鼠标位置元组
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
		
		# 按下按键
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, stats, screen, ship, bullets)
			
		# 抬起按键	
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
	'''更新屏幕上的图像，并切换到新屏幕'''

	# 每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color) # 将背景色赋给屏幕
	ship.blitme()
	# 组编调用draw，每个元素自动绘制
	aliens.draw(screen)
	
	# 显示得分
	sb.show_score()
	
	# 如果游戏处于非活动状态，就显示play按钮
	if not stats.game_active:
		play_button.draw_button()
	
	# 重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
			
	# pygame.display.flip() 更新整个待显示的Surface对象到屏幕上
	pygame.display.flip()
	
def fire_bullet(ai_settings, stats, screen, ship, bullets):
	'''若未到达限制，发射一颗子弹'''
	# 创建一颗子弹，并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed and stats.game_active:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
				
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''响应被外星人撞到飞船 || 外星人到达底端'''
	if stats.ships_left > 1:
		# 将ships_left - 1
		stats.ships_left -= 1
		
		# 更新记分牌
		sb.prep_ships()
		
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新的外星人，并将飞船放到屏幕底端中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		sleep(0.5)
	
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''检查是否有外星人位于屏幕边缘，并更新整群外星人位置'''
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	# 检测外星人和飞船直接有碰撞
	if pygame.sprite. spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
		
	# 检查是否有外星人到达屏幕底端
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
	
def change_fleet_direction(ai_settings,aliens):
	'''整群ufo下移，并改变方向'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
	'''有外星人到达边缘，采取措施'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	# 检查是否子弹是否击中ufo，若击中，删除对应子弹和外星人
	# 第三[bullets]第四[aliens]个参数：是否删除对象
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:
		# 删除现有子弹并新建一群外星人
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		
		# 提高等级
		stats.level += 1
		sb.prep_level()
		# 提高难度
		ai_settings.increase_speed()

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''检查是否有外星人到达屏幕底端'''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被外星人撞到一样处理
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break
			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	'''单击“开始游戏”开始'''
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# 隐藏光标
		pygame.mouse.set_visible(False)
		
		# 重置游戏基本信息
		stats.reset_stats()
		stats.game_active = True
		ai_settings.initialize_dynamic_settings()
		
		# 重置记分牌图形
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		# 创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	'''更新子弹位置，并删除已消失的子弹'''
	bullets.update()
	
	# 删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
	'''检查是否产生了最高分'''
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def read_max_file(cur_high_score):
	'''从文件"maxScore.json"中读历史最高分'''
	try:
		with open('maxScore.json') as f_obj:
			high_score = json.load(f_obj)
			
	except FileNotFoundError:
		with open('maxScore.json', 'w') as f_obj:
			json.dump(cur_high_score, f_obj)
		return cur_high_score
	
	else:
		return high_score
		
	
def write_max_file(cur_high_score):
	'''向"maxScore.json"写当前最高分'''
	with open('maxScore.json', 'w') as f_obj:
		json.dump(cur_high_score, f_obj)

