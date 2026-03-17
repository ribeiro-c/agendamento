from django.shortcuts import render, redirect, get_object_or_404
from ..models import Whats
from ..forms import WhatsForm
from django.contrib.auth.decorators import login_required

@login_required
def whats_list(request):
    whatss = Whats.objects.all()  # Removido o filtro por usuário
    return render(request, 'cal/whats_list.html', {'whatss': whatss})

@login_required
def whats_create(request):
    if request.method == 'POST':
        form = WhatsForm(request.POST)
        if form.is_valid():
            whats = form.save(commit=False)
            # whats.user = request.user  # Removido: whatss são globais
            whats.save()
            return redirect('cal:whats_list')
    else:
        form = WhatsForm()
    return render(request, 'cal/whats_form.html', {'form': form, 'title': 'Novo Whats'})

@login_required
def whats_update(request, pk):
    whats = get_object_or_404(Whats, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        form = WhatsForm(request.POST, instance=whats)
        if form.is_valid():
            form.save()
            return redirect('cal:whats_list')
    else:
        form = WhatsForm(instance=whats)
    return render(request, 'cal/whats_form.html', {'form': form, 'title': 'Editar Whats'})

@login_required
def whats_delete(request, pk):
    whats = get_object_or_404(Whats, pk=pk)  # Removido filtro por usuário
    if request.method == 'POST':
        whats.delete()
        return redirect('cal:whats_list')
    return render(request, 'cal/whats_confirm_delete.html', {'whats': whats})
