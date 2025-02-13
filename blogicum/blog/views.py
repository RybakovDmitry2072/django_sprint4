from django.http import Http404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, FormView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentsForm, DynamicPostForm
from .models import Comments, Post, Category
from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class IndexListView(ListView):
    model = Post
    ordering = ['-date']
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        now = timezone.now()
        return Post.objects.filter(
            pub_date__lte=now,
            is_published=True,
            category__is_published=True
        )


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'  

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.get_object().pk)
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.get_object().pk)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.get_object().author.username})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DynamicPostForm(instance=self.get_object())
        return context
    

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comments
    template_name = 'blog/comment.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.get_object().post.pk)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.get_object().post.pk})



class CreateCommentView(LoginRequiredMixin, FormView):
    form_class = CommentsForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})
        

class EditCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comments
    form_class = CommentsForm
    pk_url_kwarg = 'comment_id'  # Указываем, что параметр для получения объекта - это comment_id
    template_name = 'blog/comment.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.get_object().post.pk)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.get_object().post.pk})

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    pk_url_kwarg = 'post_id'
    paginate_by = 10 

    def get_queryset(self):
        now = timezone.now()
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.objects.filter(
            category=category,
            pub_date__lte=now,
            is_published=True
        )
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = self.object.comments.all()  
        return context
        
        

    def get_object(self, queryset=None):
        now = timezone.now()
        post = super().get_object(queryset)
        if (post.pub_date > now
                or not post.is_published
                or not post.category.is_published):
            raise Http404("Post not found")
        return post
    

class ProfileDetailView(DetailView):
    model = User  
    template_name = 'blog/profile.html'  
    context_object_name = 'profile'  

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['page_obj'] = Post.objects.filter(author=user).order_by('-created_at')[:10]
        return context
    

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model  = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        return self.request.user.is_authenticated
    

class PasswordChangeView(PasswordChangeView):
    template_name = 'blog/password_change.html'




