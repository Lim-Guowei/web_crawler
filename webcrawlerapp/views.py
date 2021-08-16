from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Author, Comment, Submission
from .forms import DataForm, AuthorForm, CommentForm, SubmissionForm, SubmissionQueryForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

import sys
import os
sys.path.append(os.path.join(os.getcwd(), "database"))
from database import add_data, delete_data

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

models = {
        'Author': Author,
        'Comment': Comment,
        'Submission': Submission,
    }   

def get_model_into_template_table(*argv, **kwargv):
    """ Return data (values) and field (column names) of database base table from the specified model (table name).
        *argv contain/s strings of table name/s to be removed from inherited child model from input model.
    """
    model = list(kwargv.values())[0]
    data = model.objects.all()
    field = [field.name for field in model._meta.get_fields(include_parents=True, include_hidden=False)]
    field_remove = [ele for ele in argv]
    field = [x for x in field if x not in field_remove]
    data = model.objects.all().values_list()
    data = sorted(data, key=lambda x: x[0]) # Always display table order by id in descending order
    unique_together = [ele for tupl in model._meta.unique_together for ele in tupl]
    return data, field, model.__name__, unique_together

# Create your views here.
def show(request, model_to_display="Submission"):
    if "model_to_display" in request.session:   # Retrieve and display back the same table after insert
        model_to_display = request.session["model_to_display"]

    intial_display = get_model_into_template_table("comment", "", model=models.get(model_to_display))
    print()
    data, field, model = intial_display[0], intial_display[1], intial_display[2]
    
    if 'model' in request.POST:
        form = DataForm(request.POST, initial={"model": model_to_display})
        if form.is_valid():
            model = form.cleaned_data['model']
            model = models[model]
            choicefield_display = get_model_into_template_table("comment", "", model=model)
            data, field, model = choicefield_display[0], choicefield_display[1], choicefield_display[2]
    else:
        form = DataForm(initial={"model": model_to_display})
    return render(request, "show.html", context={'data': data, 'form': form, 'field': field, 'model':model})

def add_new(request):
    return render(request, "insert.html")

def insert(request):
    if request.method == "POST":
        form = SubmissionQueryForm(request.POST)

        if form.is_valid():
            subreddit = form.cleaned_data["subreddit"]
            submission = form.cleaned_data["submission"]
            state = add_data(subreddit, submission)

            if state == "Data adding successful":
                messages.success(request, state)
            else:
                messages.warning(request, state + ". Check terminal output")
            return redirect("show")

        else:
            messages.error(request, "Data is not inserted correctly")
            next = request.POST.get('next', '/')
            return redirect(next)

def delete(request):
    if request.method == "POST":
        delete_data()
        messages.success(request, "All data has been deleted")
    return redirect("show")
