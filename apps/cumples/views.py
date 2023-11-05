from django.shortcuts import render
from .models import Cumpleañero
from .forms import CumpleañeroForm
import calendar
from django.contrib import messages  # Importa el módulo de mensajes



def index(request):
    # Lógica para manejar el formulario de carga de cumpleaños
    if request.method == 'POST':
        form = CumpleañeroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El cumpleaño se ha cargado exitosamente.')

    else:
        form = CumpleañeroForm()

    # Obtener cumpleaños mes a mes con nombres de los meses
    cumpleaños_por_mes = {}
    for mes in range(1, 13):
        nombre_mes = calendar.month_name[mes]  # Obtén el nombre del mes
        cumpleaños_por_mes[nombre_mes] = Cumpleañero.objects.filter(mes_cumpleaños=mes)

    return render(request, 'index.html', {'form': form, 'cumpleaños_por_mes': cumpleaños_por_mes})
