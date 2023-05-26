from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View

from Petsitter.settings import animal_choice
from PetsitUser.models import Animal, AnimalSize

from .forms import ServicesForm
from .models import Services


class ServicesFormView(LoginRequiredMixin, View):
    def get(self, request):
        form = ServicesForm()
        return render(request, "services_form.html", {"form": form})

    def post(self, request):
        form = ServicesForm(request.POST)
        pet_sit = request.POST["pet-sit"]
        pet_type = request.POST["pet-type"]
        pet_size = request.POST["pet-size"]

        pet_type = animal_choice[pet_type]

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = User.objects.get(pk=request.user.id)
            obj.pet_sitter = User.objects.get(username=pet_sit)
            obj.animal = Animal.objects.get(id=pet_type)
            obj.size = AnimalSize.objects.get(id=pet_size)
            obj.save()

            return redirect("petsit-view")
        return render(request, "services_form.html", {"form": form})


class ServicesAllView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user.id

        results_done = Services.objects.filter(pet_sitter=user).order_by("-id")
        results_ordered = Services.objects.filter(owner=user).order_by("-id")

        if results_done.exists() or results_ordered.exists():
            msg = ""
            return render(
                request,
                "services_all.html",
                {
                    "results_done": results_done,
                    "results_ordered": results_ordered,
                    "msg": msg,
                },
            )
        else:
            msg = "Nie masz jeszcze żadnych usług"
            return render(request, "services_all.html", {"msg": msg})

    def post(self, request):
        result = request.POST.get("btn-appr")
        service_to_approve = Services.objects.get(id=result)
        service_to_approve.is_approved = True
        service_to_approve.save()
        user = self.request.user.id
        results_done = Services.objects.filter(pet_sitter=user)
        results_ordered = Services.objects.filter(owner=user)
        return render(
            request,
            "services_all.html",
            {"results_done": results_done, "results_ordered": results_ordered},
        )
