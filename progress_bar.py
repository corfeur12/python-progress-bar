class ProgressBar():
	
	def __init__(self, foreground_colour=(0, 0, 0), background_colour=(255, 255, 255), length=40, decimals=2, start_bar="[", end_bar="]", percent_character="%", fill_character=" "):
		# store params as attributes
		self.foreground_colour = foreground_colour
		self.background_colour = background_colour
		self.terminal_filled_colour = "".join([self.ansi_text_colour(foreground_colour), self.ansi_background_colour(background_colour)])
		self.terminal_unfilled_colour = "".join([self.ansi_text_colour(background_colour), self.ansi_background_colour(foreground_colour)])
		self.length = length
		self.decimals = decimals
		self.start_bar = start_bar
		self.end_bar = end_bar
		self.percent_character = percent_character
		self.fill_character = fill_character
		
		self.check_params()
		
		# initialise other attributes
		self.percent = 0
		self.drawn_percent = None
		self.bar = None
		
		# e.g. "{:.2f}{}"
		self.percentage_format = "".join(["{:.", str(self.decimals), "f}{}"])
		# e.g. "{}{: >38s}{}"
		self.percentage_bar_format = "".join(["{}{:", self.fill_character, ">", str(self.length - len(self.start_bar) - len(self.end_bar)), "s}{}"])
	
	
	def __repr__(self):
		return "<ProgressBar percent:{} length:{}>".format(self.percent, self.length)
	
	
	def __str__(self):
		if not self.percent == self.drawn_percent:
			self.redraw()
		return self.bar
	
	
	def check_params(self):
		assert len(self.foreground_colour) == 3, "foreground_colour must be a tuple in form (r, g, b)"
		assert max(self.foreground_colour) <= 255 and min(self.foreground_colour) >= 0, "foreground_colour values must be in range 0-255"
		assert all(isinstance(val, int) for val in self.foreground_colour), "foreground_colour values must be ints"
		assert len(self.background_colour) == 3, "background_colour must be a tuple in form (r, g, b)"
		assert max(self.background_colour) <= 255 and min(self.background_colour) >= 0, "background_colour values must be in range 0-255"
		assert all(isinstance(val, int) for val in self.background_colour), "background_colour values must be ints"
		assert self.decimals >= 0, "decimals must be greater than or equal to 0"
		assert isinstance(self.decimals, int), "decimals must be an int"
		assert len(self.fill_character) == 1, "fill_character must have len 1"
		# len(100) + whther there's a decimal
		max_percent_length = 3 + int(self.decimals > 0)
		assert sum([len(self.start_bar), len(self.end_bar), len(self.percent_character), self.decimals, max_percent_length]) <= self.length, "length too short for other parameters"
	
	
	def update(self, percent):
		self.percent = percent / 100.0
	
	
	def redraw(self):
		partial_foreground = self.interpolate_colour()
		partial_background = tuple(back - value + fore for value, fore, back in zip(partial_foreground, self.foreground_colour, self.background_colour))
		partial_character = "".join([self.ansi_text_colour(partial_foreground), self.ansi_background_colour(partial_background)])
		complete_char_count = int(self.percent * self.length)
		percentage = self.percentage_format.format(self.percent * 100, self.percent_character)
		percentage_bar = self.percentage_bar_format.format(self.start_bar, percentage, self.end_bar)
		percentage_bar_filled = self.terminal_filled_colour + percentage_bar[:complete_char_count]
		if complete_char_count < self.length:
			percentage_bar_partial = partial_character + percentage_bar[complete_char_count]
			percentage_bar_unfilled = "".join([self.terminal_unfilled_colour, percentage_bar[complete_char_count + 1:], self.ansi_default_terminal_colour()])
		else:
			percentage_bar_partial = partial_character
			percentage_bar_unfilled = self.ansi_default_terminal_colour()
		self.drawn_percent = self.percent
		self.bar = "".join([percentage_bar_filled, percentage_bar_partial, percentage_bar_unfilled])
	
	
	def interpolate_colour(self):
		return tuple(self.interpolate_value(back, fore) for fore, back in zip(self.foreground_colour, self.background_colour))
	
	
	def interpolate_value(self, background, foreground):
		return int(self.percent * self.length % 1 * (foreground - background) + background)


	@staticmethod
	def ansi_default_terminal_colour():
		return "\x1b[0m"


	@staticmethod
	def ansi_text_colour(rgb):
		return "\x1b[38;2;{};{};{}m".format(*rgb)


	@staticmethod
	def ansi_background_colour(rgb):
		return "\x1b[48;2;{};{};{}m".format(*rgb)

