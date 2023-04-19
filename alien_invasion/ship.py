import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		''' 初始化飞船并设置其位置'''
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# 加载飞船图像并获取其外界矩形
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect() # ship转化为矩形元素
		self.screen_rect = screen.get_rect() # 屏幕转化为矩形元素
		
		# 移动标志
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		
		# 初始化飞船位置
		self.rect.centerx = self.screen_rect.centerx # 屏幕中心赋给ship中心
		self.rect.bottom = self.screen_rect.bottom # 屏幕底部赋给ship底部
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		'''根据移动标志调整飞船位置'''
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.centerx += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > self.screen_rect.left:
			self.centerx -= self.ai_settings.ship_speed_factor			
		if self.moving_up and self.rect.top > self.screen_rect.top:
			self.centery -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.centery += self.ai_settings.ship_speed_factor
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery

	def blitme(self):
		'''在指定位置绘制飞船'''
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		'''让飞船在屏幕上居中'''
		self.centerx = self.screen_rect.centerx
		self.centery = self.screen_rect.bottom - 40
