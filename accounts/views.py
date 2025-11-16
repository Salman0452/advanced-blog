from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    """User registration view"""
    
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to home
        if request.user.is_authenticated:
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Account created successfully! You can now log in as {form.cleaned_data["username"]}.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Please correct the errors below.'
        )
        return super().form_invalid(form)


class LoginView(View):
    """User login view"""
    
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to home
        if request.user.is_authenticated:
            return redirect('blog:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Set session expiry based on remember_me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to next parameter or home
                next_url = request.GET.get('next', 'blog:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """User logout view"""
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        return render(request, 'accounts/logout_confirm.html')
    
    def post(self, request):
        username = request.user.username
        logout(request)
        messages.success(request, f'Goodbye, {username}! You have been logged out.')
        return redirect('blog:home')
