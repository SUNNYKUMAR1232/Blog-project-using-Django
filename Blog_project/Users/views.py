from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from .forms import UserRegisterForm ,UserUpdateForm,ProfileUpdateForm    
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # save the user
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def log_out(request):
    logout(request)
    return redirect('login')

def profile(request):
    if request.method=='POST':
        u_from=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_from.is_valid() and p_form.is_valid():
            u_from.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')
    else:
        u_from=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form':u_from,
        'p_form':p_form
    }
    return render(request, 'users/profile.html',context)
def reset_password(request):
    if request.method=='POST':
        form=AuthenticationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f'You are now logged in as {username}')
                return redirect('home')
            else:
                messages.error(request,'Invalid username or password')
        else:
            messages.error(request,'Invalid username or password')
    form=AuthenticationForm()
    return render(request,'users/login.html',{'form':form}) 

""" 
message.debug
message.info
message.success
message.warning
message.error

 """