from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import UserRegisterForm, PostForm

# 1. Home - List all posts
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'posts': posts})

# 2. Post Detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# 3. Register User
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# 4. Create Post (Login Required)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'New Post'})

# 5. Update Post (Login Required + Author Check)
@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('post-detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post-detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Update Post'})

# 6. Delete Post (Login Required + Author Check)
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post-detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('blog-home')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})