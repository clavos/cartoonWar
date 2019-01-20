from django import forms
from forum.models import Article, Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Votre commentaire',
        }
    ))

    class Meta:
        model = Comment
        fields = (
            'content',
        )

    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.content = self.cleaned_data['content']

        if commit:
            comment.save()

        return comment


class ArticleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'title',
            'placeholder': 'Le titre de votre post',
        }
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'content',
            'placeholder': 'Le contenu de votre post',
        }
    ))

    class Meta:
        model = Article
        fields = (
            'title',
            'content',
        )

    def save(self, commit=True):
        article = super(ArticleForm, self).save(commit=False)
        article.content = self.cleaned_data['content']
        article.title = self.cleaned_data['title']

        if commit:
            article.save()

        return article
