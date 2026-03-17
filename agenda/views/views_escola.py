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
