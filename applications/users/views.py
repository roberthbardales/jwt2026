from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView

from .forms import AdminEditUserForm, AdminResetPasswordForm, LoginForm, UpdatePasswordForm, UserRegisterForm
from .mixins import AdministradorPermisoMixin
from .models import User


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('app_users:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['admin_mode'] = self.request.user.is_authenticated and self.request.user.occupation == User.ADMINISTRADOR
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_mode'] = self.request.user.is_authenticated and self.request.user.occupation == User.ADMINISTRADOR
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated and self.request.user.occupation == User.ADMINISTRADOR:
            occupation = form.cleaned_data['occupation']
        else:
            occupation = User.CLIENTE
        user = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            occupation=occupation,
            gender=form.cleaned_data['gender'],
            date_birth=form.cleaned_data['date_birth'],
            phone=form.cleaned_data.get('phone', ''),
        )
        if not self.request.user.is_authenticated:
            login(self.request, user)
        messages.success(self.request, 'Usuario registrado correctamente.')
        return super().form_valid(form)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('app_users:dashboard')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user is None:
            form.add_error(None, 'Email o contraseña incorrectos.')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('app_users:login'))


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/cambiar_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('app_users:login')
    login_url = reverse_lazy('app_users:login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )
        if user is None:
            form.add_error(None, 'La contraseña actual es incorrecta.')
            return self.form_invalid(form)

        usuario.set_password(form.cleaned_data['password2'])
        usuario.save()
        messages.success(self.request, 'Contraseña actualizada correctamente.')
        logout(self.request)
        return super().form_valid(form)


class ListaUsuariosView(AdministradorPermisoMixin, ListView):
    template_name = 'users/lista_usuarios.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)


class UserDetailView(AdministradorPermisoMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'usuario'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_superuser:
            raise Http404
        return obj


class AdminEditUserView(AdministradorPermisoMixin, UpdateView):
    model = User
    form_class = AdminEditUserForm
    template_name = 'users/admin_edit_user.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_superuser:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('app_users:user-detail', args=[self.object.pk])

    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado correctamente.')
        return super().form_valid(form)


class AdminResetPasswordView(AdministradorPermisoMixin, FormView):
    template_name = 'users/admin_reset_password.html'
    form_class = AdminResetPasswordForm

    def get_success_url(self):
        return reverse('app_users:user-detail', args=[self.kwargs['pk']])

    def get_usuario(self):
        try:
            usuario = User.objects.get(pk=self.kwargs['pk'])
        except User.DoesNotExist:
            raise Http404
        if usuario.is_superuser:
            raise Http404
        return usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.get_usuario()
        return context

    def form_valid(self, form):
        usuario = self.get_usuario()
        usuario.set_password(form.cleaned_data['password1'])
        usuario.save()
        messages.success(self.request, f'Contraseña restablecida para {usuario.first_name} {usuario.last_name}.')
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    login_url = reverse_lazy('app_users:login')