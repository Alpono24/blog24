from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.template.defaultfilters import title
from django.core.paginator import Paginator


from myproject import settings
from .models import Post, Category, ShopProduct,  ShopCategory, MusicGenre, MusicArtist, MusicAlbum, MusicSong

from .forms import PostForm


from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.


def posts(request):
    title = 'Статьи'
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    query = request.GET.get('q') #111
    posts = Post.objects.all().order_by(('-created_at'))
    if category_id:
        posts = posts.filter(category_id=category_id)
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        ).distinct()
    # Пагинация


    paginator = Paginator(posts, 10)  # показать по 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'title': title, 'categories': categories, 'page_obj': page_obj}
    return render(request, 'posts.html', context)



@login_required(login_url='/login/')
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})


@login_required(login_url='/login/')
def add_post(request):
    title = 'Страница добавления статьи'
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form, 'title': title})



@login_required(login_url='/login/')
def edit_post(request, id):
    title = 'Страница редактирования статьи'
    post = get_object_or_404(Post, id=id)
    if post.author != request.user and not request.user.is_superuser:
        return render(request, 'action_prohibited.html')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post, 'title': title})




@login_required(login_url='/login/')
def delete_post(request, id):
    title = 'Подтверждение удаления'
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return render(request, 'action_prohibited.html')
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    return render(request, 'delete_confirmation.html', {'post': post})





def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # сразу авторизуем пользователя
            return render(request, 'successful_registration.html')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')
def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')  # Получаем тему письма из формы
        message = request.POST.get('message')  # Получаем тело письма из формы
        recipient_list = ['alex.ponomarov@mail.ru']

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False
            )
            return render(request, 'email_sent_successfully.html')
        except Exception as e:
            return render(request, 'email_error.html', {'error_message': str(e)})
    else:
        return render(request, 'send_email.html')



##Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop

def products_view(request):
    title = 'Товары'
    categories = ShopCategory.objects.all()
    category_id = request.GET.get('category_Shop')
    query = request.GET.get('q')
    products = ShopProduct.objects.all()
    if category_id:
        products = products.filter(category_Shop_id=category_id)

    if query:
        products = ShopProduct.objects.filter(
            Q(name_Shop__icontains=query)
        ).distinct()
    paginator = Paginator(products, 7)  # показать по 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'title': title,
        'page_obj': page_obj
    })



def product_detail(request, pk):
    product = get_object_or_404(ShopProduct, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    """Добавить товар в корзину (через сессию)."""
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    request.session['cart'] = cart
    return redirect('cart_view')

@login_required(login_url='/login/')
def remove_from_cart(request, product_id):
    """Удалить товар из корзины."""
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('cart_view')


@login_required(login_url='/login/')
def cart_view(request):
    """Показать корзину."""
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'cart.html', {'products': products, 'total': total})






#music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music
@login_required(login_url='/login/')
def music(request):
    title = "Музыка"
    genres = MusicGenre.objects.all()
    genre_id = request.GET.get('genre_music')
    query = request.GET.get('q')
    songs = MusicSong.objects.all()
    if genre_id:
        songs = songs.filter(genre_music_id=genre_id)

    if query:
        # Поиск по названию песни, имени исполнителя, альбому и жанру
        songs = MusicSong.objects.filter(
            Q(title_music__icontains=query) |  # — поиск по названию песни.
            Q(artist_music__name_music__icontains=query) |  # — поиск по имени исполнителя.
            Q(album_music__title_music__icontains=query) |  # — поиск по названию альбома.
            Q(genre_music__name_music__icontains=query)  # — поиск по жанру.
        ).distinct()  # distinct(), чтобы избежать дублирования результатов





    return render(request, 'music.html', {
        'songs': songs,
        'genres': genres,
        'selected_genre': genre_id,
        'title': title
    })


