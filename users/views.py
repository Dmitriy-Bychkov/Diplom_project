import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (LoginView as BaseLoginView,
                                       PasswordResetDoneView)
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from django.urls import reverse_lazy, reverse
from users.email_sender import send_mail_task
from users.forms import UserRegisterForm, UserProfileForm, PasswordForm
from users.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login


class LoginView(BaseLoginView):
    """ Вход на сайт """

    template_name = "users/login.html"
    title = "Login"


class LogoutView(BaseLogoutView):
    """ Выход с сайта """

    template_name = "users/login.html"


class RegisterView(CreateView):
    """
    Регистрация нового пользователя и
    отправка подтверждения на его email
    """

    form_class = UserRegisterForm
    template_name = "users/registration/registration_form.html"
    success_url = reverse_lazy('users:registration_reset')
    title = "Регистрация нового пользователя"

    def form_valid(self, form):
        """
        Метод form_valid вызывается для проверки,
        когда форма валидна и готова к сохранению.
        Сохраняет данные пользователя, устанавливает
        его аккаунт как неактивный, генерирует токен и создает
        URL для подтверждения адреса электронной почты.
        Отправляет письмо с этой ссылкой на э
        лектронную почту пользователя
        """

        user = form.save()
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy(
            'users:confirm_email',
            kwargs={'uidb64': uid, 'token': token}
        )
        current_site = '127.0.0.1:8000'

        subject = 'Подтверждение адреса электронной почты'
        message = (f"Для подтверждения адреса электронной почты"
                   f"перейдите по ссылке:"
                   f" http://{current_site}{activation_url}")
        recipient_list = [user.email]

        # передаем сервисной функции переменные для отправки email пользователю
        # со ссылкой для подтверждения почты
        send_mail_task(subject, message, recipient_list)

        return redirect('users:email_confirmation_sent')


class UserConfirmationSentView(PasswordResetDoneView):
    """ Успешный первый этап регистрации """

    template_name = "users/registration/registration_sent_done.html"


class UserConfirmEmailView(View):
    """ Пользователь подтверждает свою регистрацию """

    def get(self, request, uidb64, token):
        """
        Метод get() обрабатывает GET-запрос,
        который содержит параметры uidb64 и token.
        Проверяет параметры uidb64 и token, и если они действительны,
        активирует аккаунт пользователя, выполняет вход в систему
        и перенаправляет на страницу подтверждения или возвращает ошибку
        """

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist
        ):
            user = None

        if (user is not None and
                default_token_generator.check_token(user, token)):
            user.is_active = True
            user.save()
            login(request, user)

            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class UserConfirmedView(TemplateView):
    """ Регистрация пользователя завершена, вывод информации об этом """

    template_name = 'users/registration/registration_confirmed.html'
    title = "Your email is activated."


class UserListView(LoginRequiredMixin, ListView):
    """
    Контроллер для просмотра списка пользователей
    """

    model = User
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        """
        Переопределяем метод get_context_data(),
        чтобы добавить дополнительный
        контекст teacher_list, содержащий только
        преподавателей (User с is_staff=True).
        Далее эта контекстная переменная teacher_list
        используется в шаблоне
        """

        context = super().get_context_data(**kwargs)
        context['teacher_list'] = User.objects.filter(is_staff=True)

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """ Профиль пользователя """

    model = User
    success_url = reverse_lazy("users:profile")
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        """
        Метод возвращает текущего пользователя,
        связанного с запросом, который может быть
        использован в других методах представления
        для доступа к данным или выполнения действий
        от имени этого пользователя.
        """

        return self.request.user


@login_required
def set_new_password(request):
    """ Установить новый пароль, введенный пользователем в его профиле """

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']

            subject = ('Смена пароля вашего '
                       'профиля на сайте EPS')
            message = (f"Пароль успешно изменен.\n"
                       f"Ваш новый пароль: {new_password}")
            recipient_list = [request.user.email]

            # передаем сервисной функции переменные
            # для отправки email с новым паролем
            send_mail_task(subject, message, recipient_list)

            request.user.set_password(new_password)
            request.user.save()

            return redirect(reverse("users:profile"))
    else:
        form = PasswordForm()

    return render(request, 'users/change_password.html', {'form': form})


def password_reset(request):
    """
    Сгенерировать новый пароль пользователя
    при входе на сайт, если забыли пароль
    """

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = "".join(
                [str(random.randint(0, 9)) for _ in range(12)]
            )
            user.set_password(new_password)
            user.save()

            subject = "Сброс пароля на сайте"
            message = (f"Пароль успешно сброшен.\n"
                       f"Ваш новый пароль: {new_password}")
            recipient_list = [user.email]

            # передаем сервисной функции переменные
            # для отправки email с новым паролем
            send_mail_task(
                subject,
                message,
                recipient_list
            )

            # Перенаправление на страницу входа
            return redirect(reverse("users:login"))

        except User.DoesNotExist:
            # Отображение формы с сообщением об ошибке
            return render(
                request,
                'users/registration/password_reset_form.html',
                {'error_message': 'User not found'}
            )

    # Вывод формы для ввода email
    return render(
        request,
        'users/registration/password_reset_form.html'
    )
