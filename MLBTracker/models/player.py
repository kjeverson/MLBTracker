from django.db import models
from datetime import datetime
from .team import Team


class Player(models.Model):
	id = models.IntegerField(primary_key=True, null=False)
	name_first = models.CharField(max_length=25, null=False)
	name_use = models.CharField(max_length=25, null=False)
	name_last = models.CharField(max_length=25, null=False)
	name_short = models.CharField(max_length=27)
	name_full = models.CharField(max_length=51)
	team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
	birth_date = models.DateField()
	height_feet = models.IntegerField(null=False)
	height_inches = models.IntegerField(null=True, blank=True)
	weight = models.IntegerField(null=False)
	throws = models.CharField(max_length=2, null=False)
	bats = models.CharField(max_length=2, null=False)
	position = models.CharField(max_length=3, null=True, blank=True)

	def __repr__(self):
		return f"{self.name_full}-{self.team}"

	def get_position(self):
		POSITIONS = ["P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]
		if not self.position:
			return None
		elif self.position not in ['O', 'D', 'H', '1']:
			return POSITIONS[int(self.position)-1]
		elif self.position == '1':
			return f'{self.throws}HP'
		else:
			if not self.position:
				return "NONE"
			if self.position == 'O':
				return "OF"
			if self.position == 'D':
				return "DH"
			if self.position == 'H':
				return "PH"

	def bats_long(self):
		if self.throws == "R":
			return "Right"
		elif self.throws == "L":
			return "Left"
		else:
			return "Switch"

	def throws_long(self):
		if self.throws == "R":
			return "Right"

		if self.throws == "L":
			return "Left"

	def get_age(self):
		current_date = datetime.now()
		birth_date = datetime.combine(self.birth_date, datetime.min.time())
		age = current_date.year - birth_date.year

		if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
			age -= 1

		return age
