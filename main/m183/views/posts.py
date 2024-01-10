from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Post, Comment
from ..forms import CommentForm
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)


def home(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'home.html', {'posts': posts})


@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).exclude(status='deleted')
    return render(request, 'posts/dashboard.html', {'user_posts': user_posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    statuses = ['published', 'hidden', 'deleted']
    if request.method == 'POST':
        if not request.user.is_authenticated:
            logger.warning('User not authenticated: %s' % request.user)
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            logger.info('Comment created: %s by user: %s' % (comment, request.user))
            return redirect('post_detail', post_id=post.id)
        elif 'status' in request.POST and (request.user == post.author or request.user.is_staff):
            post.status = request.POST['status']
            post.save()
            logger.info('Post status changed: %s by user: %s' % (post, request.user))
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    if post.status == 'published' or (post.status == 'hidden' and (request.user == post.author or request.user.is_staff)) or (post.status == 'deleted' and request.user.is_staff):
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        return render(request, 'posts/post.html', {'post': post, 'comments': comments, 'form': form, 'statuses': statuses})
    else:
        logger.info('User: %s tried to access Post: %s which is not found or not accessible.' % (request.user, post))
        return redirect('home')
