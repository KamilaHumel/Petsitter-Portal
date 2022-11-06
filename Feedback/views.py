from django.shortcuts import render, redirect
from django.views import View
from Feedback.models import Feedback
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from Feedback.forms import FeedbackForm


class FeedbackFormView(LoginRequiredMixin, View):
    def get(self, request):

        form = FeedbackForm()
        return render(request, 'feedback_form.html', {'form': form})

    def post(self, request):
        form = FeedbackForm(request.POST)
        pet_sit = request.POST['pet-sit']
        print(pet_sit)
        a = User.objects.get(username=pet_sit)
        print(a.id)

        if form.is_valid():
            obj = form.save(commit=False)  # Return an object without saving to the DB
            obj.owner = User.objects.get(pk=request.user.id)  # Add an author field which will contain current user's id
            obj.pet_sitter = User.objects.get(username=pet_sit)
            obj.save()

            return redirect('petsit-view')
        return render(request, 'feedback_form.html', {'form': form})


class FeedbackDeleteView(View):
    def get(self, request):
        user = self.request.user
        comments = Feedback.objects.filter(owner=user)

        if comments.exists():
            print(comments)
            msg = 'Twoje komentarze'
            return render(request, 'feedback_delete.html', {'comments': comments, 'msg': msg})

        else:
            msg = 'Nie dodałeś jeszcze żadnych komentarzy'
            return render(request, 'feedback_delete.html', {'msg': msg})

    def post(self, request):
        result = request.POST.get('btn-delete')
        comment_to_delete = Feedback.objects.get(id=result)
        user = self.request.user

        if comment_to_delete.owner == user:
            comment_to_delete.delete()
        else:
            msg = 'Musisz być autorem komentarza, jeśli chcesz go usunąć!'
            return render(request, 'feedback_delete.html', {'msg': msg})

        try:
            comments = Feedback.objects.filter(owner=user)
            msg = 'Twoje komentarze:'
            return render(request, 'feedback_delete.html', {'comments': comments, 'msg': msg})

        except:
            msg = 'Nie dodałeś jeszcze żadnych komentarzy'
            return render(request, 'feedback_delete.html', {'msg': msg})
