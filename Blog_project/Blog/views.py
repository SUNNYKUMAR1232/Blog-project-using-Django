from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
posts = [
    {
        'author':'CoreyMS',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted':'August 27,2020'
    },
    {
        'author':'Jane Doe',
        'title':'Blog Post 2',
        'content':'Second post content',
        'date_posted':'August 28,2020'
    },

]
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        context = { # context is a dictionary
        'posts':Post.objects.all(),
        'title':'Home'
        }
        return render(request,'blog/Home.html',context)
    else:
        return redirect('login') 

def about(request):
    if request.user.is_authenticated:
        return render(request,'blog/About.html',{'title':'About'})
    else:
        return redirect('login') 

class PostListView(ListView):
    model=Post
    template_name='blog/Home.html'
    context_object_name='posts'
    ordering=['-date_post']
    paginate_by=5
    
class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False



