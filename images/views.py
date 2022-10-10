from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image

from django.http import JsonResponse
from django.views.decorators.http import require_POST



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
