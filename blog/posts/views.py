from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import Post, Comment
from blog.forms import SignUpForm  # <- formulario de registro

def post_list(request):
    posts = (Post.objects
                  .filter(published=True, published_date__lte=timezone.now())
                  .order_by('-published_date', '-created_date'))
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(active=True).order_by('created_date')
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
    })

@require_http_methods(["GET", "POST"])
def login_view(request):
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
        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'blog/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # crea el usuario
            messages.success(request, 'Cuenta creada. Ahora inicia sesión.')
            return redirect('blog:login')  # te manda al login
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = SignUpForm()

    return render(request, 'blog/register.html', {'form': form})
