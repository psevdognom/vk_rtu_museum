from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import *

class ObjectDetailMixin:
    model = None
    template = None
    def get(self, request, slug):
        places = Place.objects.all()
        categories = Category.objects.all()
        obj = get_object_or_404(self.model, slug__iexact = slug)
        return render(request, self.template, context ={self.model.__name__.lower():obj, 'admin_object':obj, 'detail': True, 'places':places, 'categories':categories})

class ObjectCreateMixin:

    form_model = None
    template = None

    def get(self, request):
        form = self.model_form()
        places = Place.objects.all()
        categories = Category.objects.all()
        return render(request, self.template, context = {'form': form, 'places':places, 'categories':categories})

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template, context={'form':bound_form, 'categories':Category.objects.all(), 'places':Place.objects.all()})

class ObjectDeleteMixin:

    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        places = Place.objects.all()
        categories = Category.objects.all()
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'places':places, 'categories':categories})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))

class ObjectUpdateMixin:

    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact = slug)
        bound_form = self.model_form(instance = obj)
        places = Place.objects.all()
        categories = Category.objects.all()
        return render(request, self.template, context={'form':bound_form, self.model.__name__.lower():obj, 'places':places, 'categories':categories})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact = slug)
        bound_form = self.model_form(request.POST, instance= obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context= {'form':bound_form, self.model.__name__.lower(): obj})