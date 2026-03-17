from django.shortcuts import render, get_object_or_404, redirect
from agenda.models import Escola
from agenda.forms import EscolaForm  # você precisa criar esse form
from django.contrib import messages


from django.contrib.auth.decorators import login_required

@login_required
def escola_list(request):
    escolas = Escola.objects.filter(user=request.user)
    return render(request, 'cal/escola_list.html', {'escolas': escolas})

@login_required
def escola_nova(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            escola = form.save(commit=False)
            escola.user = request.user
            escola.save()
            messages.success(request, 'Escola criada com sucesso!')
            return redirect('cal:escolas')
    else:
        form = EscolaForm()
    return render(request, 'cal/escola_form.html', {'form': form})

@login_required
def escola_update(request, pk):
    escola = get_object_or_404(Escola, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EscolaForm(request.POST, instance=escola)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escola atualizada com sucesso!')
            return redirect('cal:escolas')
    else:
        form = EscolaForm(instance=escola)
    return render(request, 'cal/escola_form.html', {'form': form})

@login_required
def escola_delete(request, pk):
    escola = get_object_or_404(Escola, pk=pk, user=request.user)
    if request.method == 'POST':
        escola.delete()
        messages.success(request, 'Escola excluída com sucesso!')
        return redirect('cal:escolas')
    return render(request, 'cal/escola_confirm_delete.html', {'escola': escola})


# # LISTAR CATEGORIAS
# def escola_list(request):
#     # escolas = Escola.objects.filter(user=request.user)
#     escolas = Escola.objects.all()
#     return render(request, 'cal/escola_list.html', {'escolas': escolas})

# # CRIAR NOVA CATEGORIA
# def escola_nova(request):
#     if request.method == 'POST':
#         form = EscolaForm(request.POST)
#         if form.is_valid():
#             escola = form.save(commit=False)
#             escola.user = request.user  # associar ao usuário logado
#             escola.save()
#             messages.success(request, 'Escola criada com sucesso!')
#             return redirect('cal:escolas')
#     else:
#         form = EscolaForm()
#     return render(request, 'cal/escola_form.html', {'form': form})

# # ATUALIZAR CATEGORIA
# def escola_update(request, pk):
#     escola = get_object_or_404(Escola, pk=pk)
#     if request.method == 'POST':
#         form = EscolaForm(request.POST, instance=escola)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Escola atualizada com sucesso!')
#             return redirect('cal:escolas')
#     else:
#         form = EscolaForm(instance=escola)
#     return render(request, 'cal/escola_form.html', {'form': form})

# # EXCLUIR CATEGORIA
# def escola_delete(request, pk):
#     escola = get_object_or_404(Escola, pk=pk)
#     if request.method == 'POST':
#         escola.delete()
#         messages.success(request, 'Escola excluída com sucesso!')
#         return redirect('cal:escolas')
#     return render(request, 'cal/escola_confirm_delete.html', {'escola': escola})



# @login_required
# def escola_list(request):
#     escola = Escola.objects.all()  # Removido o filtro por usuário
#     return render(request, 'cal/escola_list.html', {'escola': escola})



# @login_required
# def tipo_list(request):
#     tipos = Tipo.objects.all()  # Removido o filtro por usuário
#     return render(request, 'cal/tipo_list.html', {'tipos': tipos})

# @login_required
# def tipo_create(request):
#     if request.method == 'POST':
#         form = TipoForm(request.POST)
#         if form.is_valid():
#             tipo = form.save(commit=False)
#             # tipo.user = request.user  # Removido: tipos são globais
#             tipo.save()
#             return redirect('cal:tipo_list')
#     else:
#         form = TipoForm()
#     return render(request, 'cal/tipo_form.html', {'form': form, 'title': 'Novo Tipo'})

# @login_required
# def tipo_update(request, pk):
#     tipo = get_object_or_404(Tipo, pk=pk)  # Removido filtro por usuário
#     if request.method == 'POST':
#         form = TipoForm(request.POST, instance=tipo)
#         if form.is_valid():
#             form.save()
#             return redirect('cal:tipo_list')
#     else:
#         form = TipoForm(instance=tipo)
#     return render(request, 'cal/tipo_form.html', {'form': form, 'title': 'Editar Tipo'})

# @login_required
# def tipo_delete(request, pk):
#     tipo = get_object_or_404(Tipo, pk=pk)  # Removido filtro por usuário
#     if request.method == 'POST':
#         tipo.delete()
#         return redirect('cal:tipo_list')
#     return render(request, 'cal/tipo_confirm_delete.html', {'tipo': tipo})
