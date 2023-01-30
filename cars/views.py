from django.shortcuts import render, redirect

from .models import CarModel
from .forms import CarForm

# Create your views here.

from django.db.models import F, Max, Min, Q


def newindex(request):
    if request.method == 'GET':
        query = request.GET.get('data')

    if query == "Blue":
        qs = CarModel.objects.filter(color='blue')
    elif query == "Red":
        qs = CarModel.objects.filter(color='red')
    else:
        qs = CarModel.objects.all()

    context = {'cars': qs}
    return render(request, 'cars/base.html', context)


def createCar(request):
    form = CarForm()
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            CarModel.handle_number_create(CarModel)

            return redirect('index')
    context = {'form': form}
    return render(request, 'cars/form.html', context)


def updateCar(request, pk):
    car = CarModel.objects.get(id=pk)
    form = CarForm(request.POST, instance=car)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'cars/form.html', context)


def deleteCar(request, pk):
    car = CarModel.objects.get(id=pk)
    car.delete()
    CarModel.objects.filter(seq_number__gt=car.seq_number).update(
        seq_number=F("seq_number")-1)
    return redirect('index')


def MoveCar(pk, movement):
    car = CarModel.objects.get(id=pk)
    if movement == -1:
        lowest = CarModel.objects.aggregate(Min("seq_number"))[
            "seq_number__min"]
        data = lowest
    if movement == 1:
        highest = CarModel.objects.aggregate(Max("seq_number"))[
            "seq_number__max"]
        data = highest
    if data is not None:
        new = car.seq_number + movement
        old = car.seq_number
        if new != (data+movement):
            CarModel.objects.filter(seq_number=new).update(seq_number=old)
            CarModel.objects.filter(id=pk).update(
                seq_number=new)

    return redirect('index')


def up(request, pk):
    return MoveCar(pk, -1)


def down(request, pk):
    return MoveCar(pk, 1)
