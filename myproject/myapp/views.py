from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from myproject import settings
from .models import Post, Category
from .forms import PostForm


from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    title = 'Статьи'
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    posts = Post.objects.all().order_by(('-created_at'))
    if category_id:
        posts = posts.filter(category_id=category_id)

    context = {'title': title, 'categories': categories, 'posts': posts}
    return render(request,'index.html', context)



def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})


@login_required(login_url='/login/')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})



@login_required(login_url='/login/')
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user and not request.user.is_superuser:
        return render(request, 'action_prohibited.html')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})




@login_required(login_url='/login/')
def delete_post(request, id):
    title = 'Подтверждение удаления'
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return render(request, 'action_prohibited.html')
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'delete_confirmation.html', {'post': post})





def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # сразу авторизуем пользователя
            return redirect('products')  # редирект на список товаров
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

#
# def send_email(request):
#     if request.method == 'POST':
#         subject = 'Приветствие от нашего сервиса!'  # Тема письма
#         message = f'Пользователь {request.user} хочет приобрести услугу' # Сообщение
#         recipient_list = ['alex.ponomarov@mail.ru']  # Получатель
#
#         try:
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=recipient_list,
#                 fail_silently=False
#             )
#             return render(request, 'email_sent_successfully.html')  # Рендер страницы успеха
#         except Exception as e:
#             return render(request, 'email_error.html', {'error_message': str(e)})  # Рендер страницы ошибки
#     else:
#         return render(request, 'send_email.html')  # Страница отправки письма


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