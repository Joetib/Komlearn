from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .forms import CommentForm, QuestionForm, GroupForm
from .models import Question, Group


@login_required
def home(request):
    """ The home page containing followed groups and recent questions """
    comment_form = CommentForm()
    return render(request, 'group/home.html', {'comment_form': comment_form})


@login_required
def group_list(request):
    """ Show all groups and allow the user to join them"""

    user_groups = request.user.group_set.all()
    unfollowed_groups = Group.objects.exclude(id__in=user_groups)
    return render(request, 'group/list.html', {'user_groups': user_groups, 'unfollowed_groups': unfollowed_groups})


@login_required
def create_group(request):
    """ Handles the creation of new groups """
    if request.method == "POST":
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            new_group = group_form.save()
            new_group.created_by = request.user
            new_group.members.add(request.user)
            new_group.save()
            return redirect('group:home')
    group_form = GroupForm()
    return render(request, 'group/creategroup.html', {'form': group_form,})


@login_required
def edit_group(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user != group.created_by:
        return redirect('group:home')
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group:group_page', group_name=group.name, group_id=group.id)
    group_edit_form = GroupForm()
    return render(request, 'group/edit_group.html', {'form': group_edit_form, 'group': group})


@login_required
def group(request, group_name, group_id):
    group = Group.objects.get(id=group_id)
    if request.user not in group.members.all():
        return redirect('group:home')
    questions_list = group.questions.all()
    paginator = Paginator(questions_list, 10)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    comment_form = CommentForm()
    return render(request, 'group/group.html', {'group': group, 'questions': questions, 'comment_form': comment_form})


@login_required
def follow(request, group_id):
    group = Group.objects.get(id=group_id)
    group.members.add(request.user)
    return redirect('group:group_list')


@login_required
def unfollow(request, group_id):
    group = Group.objects.get(id=group_id)
    group.members.remove(request.user)
    return redirect('group:group_list')


@login_required
def create_question(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user not in group.members.all():
        return redirect('group:home')
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.user = request.user
            new_question.group = group
            new_question.save()
            return redirect('group:group_page', group_name=group.name, group_id=group.id)
    question_form = QuestionForm()
    return render(request, 'group/create_question.html', {'question_form': question_form, 'group': group})


@login_required
def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    group = question.group
    if request.user not in group.members.all():
        return redirect('group:home')
    comment_form = CommentForm()
    return render(
        request,
        'group/question_detail.html',
        {'group': group, 'question': question, 'comment_form': comment_form}
    )

@require_POST
def add_comment(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.user not in question.group.members.all():
        return redirect('group:home')
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(question, request.user)
    return redirect('group:question_detail', question_id=question_id)

