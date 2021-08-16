from django import forms
from .models import Author, Comment, Submission


class DataForm(forms.Form):

    choices = [
            ("Author", "Author"),
            ("Comment", "Comment"),
            ("Submission", "Submission"),
            ]

    model = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'onchange': 'submit()'}))

class AuthorForm(forms.ModelForm):
        class Meta:
                model = Author
                fields = "__all__"

class CommentForm(forms.ModelForm):
        class Meta:
                model = Comment
                fields = "__all__"

class SubmissionForm(forms.ModelForm):
        class Meta:
                model = Submission
                fields = "__all__"

class SubmissionQueryForm(forms.Form):
        subreddit = forms.CharField(label='subreddit', max_length=500)
        submission = forms.CharField(label='submission', max_length=500)
