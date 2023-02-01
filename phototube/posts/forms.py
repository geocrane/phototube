from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    def is_edit(self):
        return self.instance.id is not None

    class Meta:
        model = Post
        fields = ("image", "text", "group")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
