from django.shortcuts import render, redirect, get_object_or_404
from ..models import Conexao
from ..forms import ConexaoForm
from django.contrib.auth.decorators import login_required

@login_required
def conexao_list(request):
    conexaos = Conexao.objects.all()  # Removido o filtro por usuário
    return render(request, 'cal/conexao_list.html', {'conexaos': conexaos})

@login_required
def conexao_create(request):
    if request.method == 'POST':
        form = ConexaoForm(request.POST)
        if form.is_valid():
            conexao = form.save(commit=False)
            # conexao.user = request.user  # Removido: conexaos são globais
            conexao.save()
            return redirect('cal:conexao_list')
    else:
        form = ConexaoForm()
    return render(request, 'cal/conexao_form.html', {'form': form, 'title': 'Novo Conexao'})

@login_required
def conexao_update(request, pk):
    conexao = get_object_or_404(Conexao, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        form = ConexaoForm(request.POST, instance=conexao)
        if form.is_valid():
            form.save()
            return redirect('cal:conexao_list')
    else:
        form = ConexaoForm(instance=conexao)
    return render(request, 'cal/conexao_form.html', {'form': form, 'title': 'Editar Conexao'})

@login_required
def conexao_delete(request, pk):
    conexao = get_object_or_404(Conexao, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        conexao.delete()
        return redirect('cal:conexao_list')
    return render(request, 'cal/conexao_confirm_delete.html', {'conexao': conexao})
