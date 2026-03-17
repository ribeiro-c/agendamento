from django.shortcuts import render, redirect, get_object_or_404
from ..models import Turma
from ..forms import TurmaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def turma_list(request):
    turmas = Turma.objects.select_related('escola').all()
    return render(request, 'turma/list.html', {'turmas': turmas})

@login_required
def turma_create(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma criada com sucesso!')
            return redirect('cal:turma_list')
    else:
        form = TurmaForm()
    return render(request, 'turma/form.html', {'form': form, 'titulo': 'Nova Turma'})

@login_required
def turma_update(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('cal:turma_list')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'turma/form.html', {'form': form, 'titulo': 'Editar Turma'})

@login_required
def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        return redirect('cal:turma_list')
    return render(request, 'turma/confirm_delete.html', {'turma': turma})
