from django.shortcuts import render, redirect, get_object_or_404
from ..models import AgendaEvento
from ..forms import AgendaEventoForm
from django.contrib.auth.decorators import login_required

@login_required
def agenda_list(request):
    agendas = AgendaEvento.objects.all()  # Removido o filtro por usuário
    return render(request, 'cal/agenda_list.html', {'agendas': agendas})

@login_required
def agenda_create(request):
    if request.method == 'POST':
        form = AgendaEventoForm(request.POST)
        if form.is_valid():
            agenda = form.save(commit=False)
            # agenda.user = request.user  # Removido: agendas são globais
            agenda.save()
            return redirect('cal:agenda_list')
    else:
        form = AgendaEventoForm()
    return render(request, 'cal/agenda_form.html', {'form': form, 'title': 'Novo Agenda'})

@login_required
def agenda_update(request, pk):
    agenda = get_object_or_404(AgendaEvento, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        form = AgendaEventoForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            return redirect('cal:agenda_list')
    else:
        form = AgendaEventoForm(instance=agenda)
    return render(request, 'cal/agenda_form.html', {'form': form, 'title': 'Editar Agenda'})

@login_required
def agenda_delete(request, pk):
    agenda = get_object_or_404(AgendaEvento, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        agenda.delete()
        return redirect('cal:agenda_list')
    return render(request, 'cal/agenda_confirm_delete.html', {'agenda': agenda})
