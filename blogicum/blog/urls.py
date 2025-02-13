from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.IndexListView.as_view(),
         name='index'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'),
     path('accounts/profile/<str:username>/',
          views.ProfileDetailView.as_view(),
          name='profile'),
     path('edit_profile/',
          views.ProfileUpdateView.as_view(),
          name='edit_profile'
          ),
     path('posts/create/',
          views.CreatePostView.as_view(),
          name='create_post'      
          ),
     path('posts/<int:post_id>/edit/',
          views.PostUpdateView.as_view(),
          name='edit_post'
          ),
     path('posts/<int:post_id>/delete/',
          views.DeletePostView.as_view(),
          name='delete_post'),
     path('posts/<int:post_id>/comment/',
          views.CreateCommentView.as_view(),
          name='add_comment'
          ),
     path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
          views.EditCommentView.as_view(),
          name='edit_comment'),
     path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
           views.DeleteCommentView.as_view(),
           name='delete_comment'),

]
