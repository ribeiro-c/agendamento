from django.shortcuts import render, redirect, get_object_or_404
from ..models import Aluno
from ..forms import AlunoForm
from django.contrib.auth.decorators import login_required

@login_required
def aluno_list(request):
    alunos = Aluno.objects.all()  # Removido o filtro por usuário
    return render(request, 'cal/aluno_list.html', {'alunos': alunos})

@login_required
def aluno_create(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            # aluno.user = request.user  # Removido: alunos são globais
            aluno.save()
            return redirect('cal:aluno_list')
    else:
        form = AlunoForm()
    return render(request, 'cal/aluno_form.html', {'form': form, 'title': 'Novo Aluno'})

@login_required
def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('cal:aluno_list')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'cal/aluno_form.html', {'form': form, 'title': 'Editar Aluno'})

@login_required
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        aluno.delete()
        return redirect('cal:aluno_list')
    return render(request, 'cal/aluno_confirm_delete.html', {'aluno': aluno})
