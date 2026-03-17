from django.shortcuts import render, redirect, get_object_or_404
from ..models import ConexaoAgenda
from ..forms import ConexaoAgendaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def conexao_list(request):
    conexaos = ConexaoAgenda.objects.select_related('turma').all()
    return render(request, 'conexao/list.html', {'conexaos': conexaos})

@login_required
def conexao_create(request):
    if request.method == 'POST':
        form = ConexaoAgendaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conexão criada com sucesso!')
            return redirect('cal:conexao_list')
    else:
        form = ConexaoAgendaForm()
    return render(request, 'conexao/form.html', {'form': form, 'titulo': 'Nova Conexão'})

@login_required
def conexao_update(request, pk):
    conexao = get_object_or_404(ConexaoAgenda, pk=pk)
    if request.method == 'POST':
        form = ConexaoAgendaForm(request.POST, instance=conexao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conexão atualizada com sucesso!')
            return redirect('cal:conexao_list')
    else:
        form = ConexaoAgendaForm(instance=conexao)
    return render(request, 'conexao/form.html', {'form': form, 'titulo': 'Editar Conexão'})

@login_required
def conexao_delete(request, pk):
    conexao = get_object_or_404(ConexaoAgenda, pk=pk)
    if request.method == 'POST':
        conexao.delete()
        messages.success(request, 'Conexão excluída com sucesso!')
        return redirect('cal:conexao_list')
    return render(request, 'conexao/confirm_delete.html', {'conexao': conexao})
