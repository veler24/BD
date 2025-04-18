from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from api.models import Forum, Theme, Message
from django.utils import timezone
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from .forms import RegisterForm, ForumForm, ThemeForm


def index(request):
    forums = Forum.objects.all()
    return render(request, 'main/forums.html', {'forums': forums})


class ThemesOfForumView(ListView):
    model = Forum
    template_name = 'main/forums.html'
    context_object_name = 'forums'


class ThemesView(ListView):
    model = Theme
    template_name = 'main/themes.html'
    context_object_name = 'themes'
    paginate_by = 10

    def get_queryset(self):
        forum_id = self.kwargs['forum_id']
        return Theme.objects.filter(forum_id=forum_id).order_by('-name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forum'] = Forum.objects.get(id=self.kwargs['forum_id'])
        return context


class MessageView(ListView):
    model = Message
    template_name = 'main/message.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        theme_id = self.kwargs['theme_id']
        return Message.objects.filter(theme_id=theme_id).order_by('-msg_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = Theme.objects.get(id=self.kwargs['theme_id'])
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            theme_id = self.kwargs['theme_id']
            message_text = request.POST.get('message')

            if message_text:
                Message.objects.create(
                    msg_txt=message_text,
                    msg_time=timezone.now(),
                    theme_id=theme_id,
                    sender=request.user
                )

            return redirect('message', theme_id=theme_id)


def themes(request):
    theme = Theme.objects.all()
    return render(request, 'main/themes.html', {'theme': theme})


@login_required
def profile_view(request):
    return render(request, 'main/profile.html')


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required
def create_forum(request):
    error = ''
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['creator'] = request.user.id

        form = ForumForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'
    else:
        form = ForumForm(initial={'creator': request.user.id})

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'main/createForum.html', data)


@login_required
def create_theme(request, forum_id=None):
    error = ''

    if forum_id:
        forum = get_object_or_404(Forum, id=forum_id)
    else:
        # Альтернативный вариант, если forum_id не передается
        # Например, можно получить из сессии или другого параметра
        forum = get_object_or_404(Forum, id=request.session.get('current_forum_id'))
        # или вернуть ошибку, если форум не указан
        # return HttpResponseBadRequest("Forum not specified")

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['start_usr'] = request.user.id
        form_data['forum'] = forum.id  # Используем текущий форум

        form = ThemeForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('themes', forum_id=forum.id)  # Перенаправляем в форум
        else:
            error = 'Форма была неверной'
    else:
        form = ThemeForm(initial={
            'creator': request.user.id,
            'forum': forum.id  # Используем текущий форум
        })

    data = {
        'form': form,
        'error': error,
        'forum': forum  # Передаем форум в контекст
    }

    return render(request, 'main/createTheme.html', data)
