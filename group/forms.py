from django import forms
from .models import Comment, Question, Group


class GroupForm(forms.ModelForm):
    """ Form for handling creation of groups """

    class Meta:
        model = Group
        fields = ('name', 'about', 'picture')


class QuestionForm(forms.ModelForm):
    """ Form for handling addition of questions """

    class Meta:
        model = Question
        fields = ('text',)


class CommentForm(forms.Form):
    """ Form for adding Comments """

    text = forms.CharField(label="Comment", widget=forms.Textarea)

    def save(self, question, user):
        """ custom save method to create comment """

        comment = Comment.objects.create(text=self.cleaned_data.get('text', None), question=question, user=user)