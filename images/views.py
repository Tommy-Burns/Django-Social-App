from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign user to new image
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.xhtml', {
        'section': 'images',
        'form': form,
    })


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.xhtml', {
        'section': 'images',
        'image': image,
    })


def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({
                'status': 'ok',
            })
        except Image.DoesNotExist:
            pass
    return JsonResponse({
        'status': 'error',
    })


def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Return first page if page isn't an integer
        images = paginator.page(1)
    except EmptyPage:
        # Return an empty page if AJAX request and page are out of range
        if images_only:
            return HttpResponse('')
        # Return last page of results if page is out of range
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'images/image/list_images.xhtml', {
            'section': 'images',
            'images': images,
        })
    return render(request, 'images/image/list.xhtml', {
        'section': 'images',
        'images': images,
    })
