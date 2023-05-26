from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View

from Feedback.models import Feedback
from Petsitter.settings import animal_choice, size_choice

from .forms import PetsitForm, PetsitSearchForm
from .helpers import count_rating
from .models import PetsitUser


class PetStart(View):
    def get(self, request):
        return render(request, "petsitter_start.html")


class PetForm(LoginRequiredMixin, View):
    def get(self, request):
        form = PetsitSearchForm()
        return render(request, "petsit_form.html", {"form": form})

    def post(self, request):
        animal = request.POST.get("animal")
        animal_size = request.POST["size"]
        city = request.POST["city"]
        place = request.POST["place_type"]
        transport = request.POST.get("transport")
        user = self.request.user.id

        animal = animal_choice[animal]

        if transport == "on":
            transport = True
        else:
            transport = False

        search_result = PetsitUser.objects.filter(
            city=city,
            place_type=place,
            transport=transport,
            animals=animal,
            size=animal_size,
        ).exclude(user=user)

        search_result_1 = list(map(lambda el: el.id, search_result))
        request.session["search_results"] = search_result_1

        return redirect("result")


class PetResultView(LoginRequiredMixin, View):
    def get(self, request):
        search_results = request.session["search_results"]

        result = []
        all_ratings = []

        for num in search_results:
            person = PetsitUser.objects.get(id=num)
            result.append(person)
            user = User.objects.get(username=person.user)

            feedback = Feedback.objects.filter(pet_sitter=user.id)
            for stars in feedback:
                all_ratings.append(int(stars.rating))

        rating = count_rating(all_ratings)

        return render(
            request, "petsit_result.html", {"result": result, "rating": rating}
        )


class PetsitLogView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user

        try:
            pet = PetsitUser.objects.get(user=user)
        except PetsitUser.DoesNotExist:
            return redirect("petsit-form")
        else:
            feedback = Feedback.objects.filter(pet_sitter=user)
            all_animals = pet.animals.all()
            animals = ""

            for animal in all_animals:
                animals += animal.name + " "

            return render(
                request,
                "petsit_logview.html",
                {"petsitter": pet, "feedback": feedback, "animals": animals},
            )


class PetsitLogForm(LoginRequiredMixin, View):
    def get(self, request):
        form = PetsitForm()
        return render(request, "login_form.html", {"form": form})

    def post(self, request):
        form = PetsitForm(request.POST)

        if form.is_valid():
            obj1 = form.save(commit=False)
            obj1.user = User.objects.get(pk=request.user.id)
            obj1.save()
            form.save_m2m()
            return redirect("petsit-view")
        return render(request, "login_form.html", {"form": form})


class UpdateInfoView(View):
    def get(self, request, id):
        user = self.request.user
        id = user.id
        person = PetsitUser.objects.get(user_id=id)
        animals = person.animals.all()
        sizes = person.size.all()
        animals_list = []
        size_list = []

        for animal in animals:
            animals_list.append(animal.name)

        for size in sizes:
            size_list.append(size.size)

        return render(
            request,
            "update.html",
            {"person": person, "animals": animals_list, "size": size_list},
        )

    def post(self, request, id):
        person = PetsitUser.objects.get(user_id=id)
        user = User.objects.get(id=id)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        city = request.POST["city"]
        address = request.POST["address"]
        about = request.POST.get("about")
        animals = request.POST.getlist("animal")
        sizes = request.POST.getlist("size")
        animal_list = []
        size_list = []

        for animal in animals:
            animal = animal_choice[animal]
            animal_list.append(animal)

        for size in sizes:
            size = size_choice[size]
            size_list.append(size)

        # if user.first_name != first_name:
        #     user.first_name = first_name
        #     user.save(update_fields=['first_name'])
        # elif: ...

        user.first_name = first_name
        user.last_name = last_name
        person.city = city
        person.address = address
        person.about = about
        person.animals.set(animal_list)
        person.size.set(size_list)
        person.save()
        user.save()

        return redirect("petsit-view")
