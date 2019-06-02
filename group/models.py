from django.db import models
from django.conf import settings


class Group(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='groups_created', null=True, blank=True)
    about = models.TextField(max_length=5120, blank=True)
    picture = models.ImageField(upload_to='group_profiles', blank=True, null=True)

    def latest_questions(self):
        return self.questions.all()[:3]


class Question(models.Model):
    """ The Question Models """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-posted_date',)

    def __str__(self):
        return f"{self.user.username}'s question"

    def get_absolute_url(self):
        pass


class Comment(models.Model):
    """ The comments Models """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-comment_date',)

