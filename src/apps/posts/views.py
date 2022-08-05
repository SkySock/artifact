from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.posts.models.post import Post
from apps.posts.serializers.posts import PreviewPostSerializer



