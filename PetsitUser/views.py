from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from PetsitUser.models import PetsitUser
from Feedback.models import Feedback
from PetsitUser.forms import PetsitForm, PetsitSearchForm


class PetStart(View):
    def get(self, request):
        return render(request, 'petsitter_start.html')


class PetForm(LoginRequiredMixin, View):
    def get(self, request):
        form = PetsitSearchForm()
        return render(request, 'petsit_form.html', {'form': form})

    def post(self, request):
        animal = request.POST.get('animal')
        animal_size = request.POST['size']
        city = request.POST['city']
        # district = request.POST['district']
        place = request.POST['place_type']
        transport = request.POST.get('transport')
        user = self.request.user.id

        if animal == 'PIES':
            animal = 1
        elif animal == 'KOT':
            animal = 3
        elif animal == 'KRÓLIK':
            animal = 2
        elif animal == 'CHOMIK':
            animal = 5
        elif animal == "FRETKA":
            animal = 4

        if transport == 'on':
            transport = True
        else:
            transport = False

        search_result = PetsitUser.objects.filter(city=city,
                                                  place_type=place,
                                                  transport=transport,
                                                  animals=animal,
                                                  size=animal_size).exclude(user=user)

        search_result_1 = [el.id for el in search_result]
        request.session['search_results'] = search_result_1

        return redirect('result')


class PetResultView(LoginRequiredMixin, View):
    def get(self, request):
        search_results = request.session['search_results']

        result = []
        summ = []

        for num in search_results:
            person = PetsitUser.objects.get(id=num)
            result.append(person)
            u = User.objects.get(username=person.user)
            try:
                feedback = Feedback.objects.filter(pet_sitter=u.id)
                for f in feedback:
                    summ.append(int(f.rating))
            except:
                continue

        if len(summ) != 0:
            rating = sum(summ)/len(summ)
        else:
            rating = 0
        return render(request, 'petsit_result.html', {'result': result, 'rating': rating})


class PetsitLogView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user

        try:
            pet = PetsitUser.objects.get(user=user)
            feedback = Feedback.objects.filter(pet_sitter=user)
            an = pet.animals.all()
            animals = ''

            for a in an:
                animals += a.name + ' '

            return render(request, 'petsit_logview.html', {'petsitter': pet, 'feedback': feedback, 'animals': animals})
        except PetsitUser.DoesNotExist:
            return redirect('petsit-form')


class PetsitLogForm(LoginRequiredMixin, View):

    def get(self, request):
        form = PetsitForm()
        return render(request, 'login_form.html', {'form': form})

    def post(self, request):
        form = PetsitForm(request.POST)

        if form.is_valid():
            obj1 = form.save(commit=False)  # Return an object without saving to the DB
            obj1.user = User.objects.get(pk=request.user.id)  # Add an author field which will contain current user's id
            obj1.save()
            form.save_m2m()
            return redirect('petsit-view')
        return render(request, 'login_form.html', {'form': form})


class UpdateInfoView(View):
    def get(self, request, id):
        user = self.request.user
        id = user.id
        person = PetsitUser.objects.get(user_id=id)
        animals = person.animals.all()
        size = person.size.all()
        animals_list = []
        size_list = []
        for a in animals:
            animals_list.append(a.name)

        for s in size:
            size_list.append(s.size)

        return render(request, 'update.html', {"person": person, 'animals': animals_list, 'size': size_list})

    def post(self, request, id):
        person = PetsitUser.objects.get(user_id=id)
        pers = User.objects.get(id=id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        address = request.POST['address']
        about = request.POST.get('about')
        animal = request.POST.getlist('animal')
        size = request.POST.getlist('size')
        animal_list = []
        size_list = []

        for i in animal:
            if i == 'PIES':
                i = 1
                animal_list.append(i)
            elif i == 'KOT':
                i = 3
                animal_list.append(i)
            elif i == 'KRÓLIK':
                i = 2
                animal_list.append(i)
            elif i == 'CHOMIK':
                i = 5
                animal_list.append(i)
            elif i == "FRETKA":
                i = 4
                animal_list.append(i)

        for s in size:
            if s == 'BARDZO MAŁY - do 2 kg':
                s = 1
                size_list.append(s)
            elif s == 'MAŁY - 2-5 kg':
                s = 2
                size_list.append(s)
            elif s == 'ŚREDNI - 5-12 kg':
                s = 3
                size_list.append(s)
            elif s == 'DUŻY - 12-20 kg':
                s = 4
                size_list.append(s)
            elif s == "BARDZO DUŻY - powyżej 20 kg":
                s = 5
                size_list.append(s)

        pers.first_name = first_name
        pers.last_name = last_name
        person.city = city
        person.address = address
        person.about = about
        person.animals.set(animal_list)
        person.size.set(size_list)
        person.save()
        pers.save()

        return redirect('petsit-view')