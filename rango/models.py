from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	
	# to make the plural categories instead of categorys
	class Meta:
		verbose_name_plural= "Categories"
		
	def save(self, *args, **kwargs):
			self.slug = slugify(self.name)
			super(Category, self).save(*args, **kwargs)
		
	def __unicode__(self):
		return self.name
		
class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.title
		
class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')
	
	def __unicode__(self):
		return self.title
		
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
		
