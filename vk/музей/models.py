from django.db import models
from django.shortcuts import reverse
from time import time


def gen_translit_slug(s):
    abs = {'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'e', 'ж':'zh', 'з':'z', 'и':'i', 'й':'i', 'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch', 'ш':'sh', 'щ':'sch', 'ъ':'', 'ы':'i', 'ь':'', 'э':'e', 'ю':'u', 'я':'ya', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9', '0':'0'}
    new_slug = ''
    for lit in s:
        if lit != ' ' and lit != '-' and lit != '/':
            new_slug += abs[lit.lower()]
    return new_slug

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=150, blank = True, unique = True)
    parentId = models.ForeignKey("self", on_delete = models.CASCADE, null = True, blank = False, related_name='children')
    description = models.TextField(blank = False, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_translit_slug(self.name) + str(time())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail_url", kwargs = {'slug': self.slug})

    def get_delete_url(self):
        return reverse('category_delete_url', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('category_update_url', kwargs={'slug':self.slug})
    
    def get_childs(self):
        if Category.objects.filter(parentId = self):
            return Category.objects.filter(parentId = self)
        else:
            return False

    def has_childs(self):
        if self.get_childs() == False:
            return False
        else:
            return True

class Place(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=150, blank = True, unique = True)
    parentId = models.ForeignKey("self", on_delete = models.CASCADE, null = True, blank = False, related_name='children_place')
    description = models.TextField(blank = False, default='')

    def __str__(self):
        if self.parentId:
            return self.parentId.name + '/' + self.name
        else:
            return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_translit_slug(self.name) + str(time())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("place_detail_url", kwargs = {'slug': self.slug})

    def get_delete_url(self):
        return reverse('place_delete_url', kwargs= {'slug':self.slug} )

    def get_update_url(self):
        return reverse('place_update_url', kwargs= { 'slug':self.slug })
    
    def get_childs(self):
        if Place.objects.filter(parentId = self):
            return Place.objects.filter(parentId = self)
        else:
            return False
    
    def get_items(self):
        return self.item.all()

    def has_childs(self):
        if self.get_childs() == False:
            return False
        else:
            return True
        
    
class Item(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length = 50, unique=True, blank=True)
    mark = models.CharField(max_length=150, db_index=True)
    image = models.ImageField(upload_to='images/items')
    description = models.TextField(blank=False, default='')
    category = models.ManyToManyField(Category, blank = True, related_name='item')
    place = models.ManyToManyField(Place, blank = True, related_name='item')
    state = models.CharField(max_length=400, blank=False, default='')
    getting = models.CharField(max_length=400, blank=False, default='')
    material = models.CharField(max_length=50, blank=False, default='')
    year = models.CharField(max_length=50, blank=False, default='')
    
    class Meta:
        ordering = ['mark']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_translit_slug(self.mark)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("item_detail_url", kwargs = {'slug': self.slug})

    def get_update_url(self):
        return reverse('item_update_url', kwargs= {'slug':self.slug})

    def get_delete_url(self):
        return reverse('item_delete_url', kwargs= {'slug':self.slug})