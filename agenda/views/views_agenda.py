from django.shortcuts import render, redirect, get_object_or_404
from ..models import AgendaEvento
from ..forms import AgendaEventoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def agenda_list(request):
    agendas = AgendaEvento.objects.select_related('turma').order_by('-data')
    return render(request, 'agenda/list.html', {'agendas': agendas})

@login_required
def agenda_create(request):
    if request.method == 'POST':
        form = AgendaEventoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('cal:agenda_list')
    else:
        form = AgendaEventoForm()
    return render(request, 'agenda/form.html', {'form': form, 'titulo': 'Novo Evento'})

@login_required
def agenda_update(request, pk):
    agenda = get_object_or_404(AgendaEvento, pk=pk)
    if request.method == 'POST':
        form = AgendaEventoForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('cal:agenda_list')
    else:
        form = AgendaEventoForm(instance=agenda)
    return render(request, 'agenda/form.html', {'form': form, 'titulo': 'Editar Evento'})

@login_required
def agenda_delete(request, pk):
    agenda = get_object_or_404(AgendaEvento, pk=pk)
    if request.method == 'POST':
        agenda.delete()
        messages.success(request, 'Evento excluído com sucesso!')
        return redirect('cal:agenda_list')
    return render(request, 'agenda/confirm_delete.html', {'agenda': agenda})
