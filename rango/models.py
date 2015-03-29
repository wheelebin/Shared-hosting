from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=200)
	url = models.URLField()
	views = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Page, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	ftp = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username

class Plan(models.Model):
	domain = models.CharField(max_length=200, unique=True)
	owner = models.ForeignKey(User)
	directory = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.domain