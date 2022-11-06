from django.shortcuts import render, redirect
from django.views import View
from PetsitUser.models import Animal, AnimalSize
from Services.models import Services
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from Services.forms import ServicesForm


class ServicesFormView(LoginRequiredMixin, View):
    def get(self, request):
        form = ServicesForm()
        return render(request, 'services_form.html', {'form': form})

    def post(self, request):
        form = ServicesForm(request.POST)
        pet_sit = request.POST['pet-sit']
        pet_type = request.POST['pet-type']
        pet_size = request.POST['pet-size']
        print(pet_sit)
        a = User.objects.get(username=pet_sit)
        print(a.id)

        if pet_type == "PIES":
            pet_type = 1
        elif pet_type == "KOT":
            pet_type = 3
        elif pet_type == "KRÓLIK":
            pet_type = 2
        elif pet_type == "CHOMIK":
            pet_type = 5
        else:
            pet_type = 4

        if form.is_valid():
            obj = form.save(commit=False)  # Return an object without saving to the DB
            obj.owner = User.objects.get(pk=request.user.id)  # Add an author field which will contain current user's id
            obj.pet_sitter = User.objects.get(username=pet_sit)
            obj.animal = Animal.objects.get(id=pet_type)
            obj.size = AnimalSize.objects.get(id=pet_size)
            obj.save()

            return redirect('petsit-view')
        return render(request, 'services_form.html', {'form': form})


class ServicesAllView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user.id

        try:
            results_done = Services.objects.filter(pet_sitter=user).order_by('-id')
            results_ordered = Services.objects.filter(owner=user).order_by('-id')
            msg = ''
            return render(request, 'services_all.html',
                          {'results_done': results_done, 'results_ordered': results_ordered, 'msg': msg})

        except:
            msg = 'Nie masz jeszcze żadnych usług'
            return render(request, 'services_all.html', {'msg': msg})

    def post(self, request):
        result = request.POST.get('btn-appr')
        service_to_approve = Services.objects.get(id=result)
        service_to_approve.is_approved = True
        service_to_approve.save()
        print(result)
        user = self.request.user.id
        results_done = Services.objects.filter(pet_sitter=user)
        results_ordered = Services.objects.filter(owner=user)
        return render(request, 'services_all.html',
                      {'results_done': results_done, 'results_ordered': results_ordered})

