from django.shortcuts import render, redirect, get_object_or_404
from ..models import Turma
from ..forms import TurmaForm
from django.contrib.auth.decorators import login_required

@login_required
def turma_list(request):
    turmas = Turma.objects.all()  # Removido o filtro por usuário
    return render(request, 'cal/turma_list.html', {'turmas': turmas})

@login_required
def turma_create(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            # turma.user = request.user  # Removido: turmas são globais
            turma.save()
            return redirect('cal:turma_list')
    else:
        form = TurmaForm()
    return render(request, 'cal/turma_form.html', {'form': form, 'title': 'Novo Turma'})

@login_required
def turma_update(request, pk):
    turma = get_object_or_404(Turma, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('cal:turma_list')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'cal/turma_form.html', {'form': form, 'title': 'Editar Turma'})

@login_required
def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        turma.delete()
        return redirect('cal:turma_list')
    return render(request, 'cal/turma_confirm_delete.html', {'turma': turma})
