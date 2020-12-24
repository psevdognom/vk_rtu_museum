from django import forms
from django.core.exceptions import ValidationError
from музей.models import Place, Item, Category
from django.shortcuts import reverse

class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = [
            'name',
            'parentId',
            'description',
        ]
        parentId = forms.ModelChoiceField(queryset = Category.objects.all(), to_field_name='parentId')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Описание'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['parentId'].required = False
        
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError("slug may not be create")
        if Category.objects.filter(slug__iexact = new_slug).count():
            raise ValidationError('Slug is not unique. We alredy have "{}" slug '.format(new_slug))
        return new_slug

class PlaceForm(forms.ModelForm):
    class Meta():
        model = Place
        fields = [
            'name',
            'parentId',
            'description',
        ]
        parentId = forms.ModelChoiceField(queryset = Place.objects.all(), to_field_name='parentId')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Описание'}),
        }

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['parentId'].required = False
        
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError("slug may not be create")
        if Place.objects.filter(slug__iexact = new_slug).count():
            raise ValidationError('Данное имя уже существует. We alredy have "{}" slug '.format(new_slug))
        return new_slug

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'mark',
            'image',
            'description',
            'category',
            'place',
            'state',
            'getting',
            'material',
            'year',
        ]

        category = forms.ModelChoiceField(queryset = Category.objects.all(), to_field_name='category')
        place = forms.ModelChoiceField(queryset = Place.objects.all(), to_field_name='place')

        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя'}),
            'mark':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя'}),
            'image': forms.ClearableFileInput(),
            'description':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Состояние'}),
            'getting': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Получение'}),
            'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Материал'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Год выпуска'}),

        }
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['place'].required = False
        self.fields['description'].required = False
        self.fields['image'].required = False
        self.fields['category'].initial = Category.objects.all()[0]