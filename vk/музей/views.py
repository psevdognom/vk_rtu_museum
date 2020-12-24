from django.shortcuts import render
from django.shortcuts import get_object_or_404
from музей.models import Item, Place, Category
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import redirect
from музей.utils import ObjectCreateMixin, ObjectDetailMixin, ObjectDeleteMixin, ObjectUpdateMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from музей.forms import ItemForm, CategoryForm, PlaceForm
from django.db.models import Q

base_context = {
    'categories': Category.objects.all(),
    'places': Place.objects.all(),
}

def main_view(request):
    places = Place.objects.all()
    categories = Category.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        items = Item.objects.filter(Q(name__icontains = search_query) 
        | Q(description__icontains = search_query) 
        | Q(mark__icontains = search_query) 
        | Q(place__name__icontains = search_query) 
        | Q(category__name__icontains = search_query)
        | Q(getting__icontains = search_query) 
        | Q(year__icontains = search_query))
    else:
        items = Item.objects.all()
    return render(request, 'музей/main_view.html', context = {'places':places, 'categories':categories, 'items':items})

def place_detail(request, slug):
    categories = Category.objects.all()
    places = Place.objects.all()
    current_place = get_object_or_404(Place, slug__iexact = slug)
    if current_place.has_childs():
        childs = current_place.get_childs()
        items = current_place.item.all()
    else:
        childs = None
        items = current_place.item.all()
    return render(request, 'музей/place_detail.html', context={'place':current_place, 'childs':childs, 'items':items, 'categories':categories, 'places':places, 'admin_object':current_place, 'detail':True})

def category_detail(request, slug):
    current_category = get_object_or_404(Category, slug__iexact = slug)
    if current_category.parentId == None:
        parent = None
    else:
        parent = current_category.parentId
    if current_category.has_childs():
        childs = current_category.get_childs()
        items = None
    else:
        items = current_category.item.all()
        childs = current_category.get_childs()
    return render(request, 'музей/category_detail_template.html', context={'parent':parent, 'category':current_category, 'childs':childs, 'items':items, 'categories': Category.objects.all(), 'places':Place.objects.all(), 'detail':True, 'admin_object':current_category})

class PlaceCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PlaceForm
    template = 'музей/place_create_form.html'
    raise_exception = True

class PlaceUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Place
    model_form = PlaceForm
    template = 'музей/place_update_form.html'
    raise_exception = True

class PlaceDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Place
    template = 'музей/place_delete_form.html'
    redirect_url = 'main'
    raise_exception = True

class CategoryUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Category
    model_form = CategoryForm
    template = 'музей/category_update_form.html'
    raise_exception = True

class CategoryDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Category
    template = 'музей/category_delete.html'
    redirect_url = 'main'
    raise_exception = True

class ItemCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = ItemForm
    temlate = 'музей/item_create_form.html'
    raise_exception = True

class CategoryCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = CategoryForm
    template = 'музей/category_create_form.html'
    raise_exception = True

class ItemDetail(ObjectDetailMixin, View):
    model = Item
    template = 'музей/item_detail.html'

class ItemDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Item
    template = 'музей/item_delete.html'
    redirect_url = 'main'
    raise_exception = True

class ItemUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Item
    model_form = ItemForm
    template = 'музей/item_update_form.html'
    raise_exception = True

def item_create(request, slug):
    categories = Category.objects.all()
    places = Place.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = ItemForm()
    base_context['form'] = form
    return render(request, 'музей/item_create_form.html',context = base_context)


def new_item_create(request):
    categories = Category.objects.all()
    places = Place.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = ItemForm()
    base_context['form'] = form
    return render(request, 'музей/item_create_form.html',context = base_context)

