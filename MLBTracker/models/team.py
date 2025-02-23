from django.db import models


class Team(models.Model):

	id = models.CharField(max_length=3, primary_key=True)
	location = models.CharField(max_length=25)
	name = models.CharField(max_length=20)
	full_name = models.CharField(max_length=45)
	primary_color = models.CharField(max_length=7)
	secondary_color = models.CharField(max_length=7)
	league = models.CharField(max_length=2)
	division = models.CharField(max_length=7)

	def __repr__(self):
		return f"{self.full_name}"


