from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import Post, Comment

def post_list(request):
    # Solo posts publicados hasta ahora
    posts = (Post.objects
                  .filter(published=True, published_date__lte=timezone.now())
                  .order_by('-published_date', '-created_date'))
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    # Muestra solo publicados; si quieres ver borradores como admin, quita el filter published
    post = get_object_or_404(
        Post,
        slug=slug,
        published=True
    )
    comments = post.comments.filter(active=True).order_by('created_date')
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
    })

@require_http_methods(["GET", "POST"])
def login_view(request):
    # Si ya está logueado, redirige a la lista
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Has iniciado sesión.')
            return redirect('blog:post_list')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'blog/login.html')
