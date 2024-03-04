from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import UserRegisterForm,ContactForm,ProfilePictureForm
from .models import District,State,ContactAddress

# Create your views here.
class RegisterPage(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html',{'form':form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/register.html', {'form':form})

    
class LoginPage(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Give the right credentials!')
            return redirect('login')

class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'accounts/address.html',{'form':form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('home')
        else:
            return render(request, 'accounts/address.html', {'form':form})

def load_districs(request):
    state_id = request.GET.get('state_id')
    districts = District.objects.filter(state_id=state_id)
    return render(request, 'accounts/dropdown.html',{'districts':districts})

class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request,"accounts/account.html")
    
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfilePictureForm(instance=request.user)
        return render(request, "accounts/profile.html",{'form':form})
    
    def post(self, request):
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
        
class EditAddressView(LoginRequiredMixin, View):
    def get(self, request):
        ads_instance = ContactAddress.objects.get(user = request.user)
        form = ContactForm(instance=ads_instance)
        return render(request, 'accounts/edit_address.html',{'form':form})

    def post(self, request):
        ads_instance = ContactAddress.objects.get(user = request.user)
        form = ContactForm(request.POST, instance=ads_instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            # Redirect to a success page or do something else
            return redirect('account')

