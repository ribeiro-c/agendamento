from django.shortcuts import render, redirect, get_object_or_404
from ..models import WhatsAppEnvio
from ..forms import WhatsAppEnvioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def whats_list(request):
    whatss = WhatsAppEnvio.objects.select_related('turma').order_by('-enviado_em')
    return render(request, 'whats/list.html', {'whatss': whatss})

@login_required
def whats_create(request):
    if request.method == 'POST':
        form = WhatsAppEnvioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de envio criado com sucesso!')
            return redirect('cal:whats_list')
    else:
        form = WhatsAppEnvioForm()
    return render(request, 'whats/form.html', {'form': form, 'titulo': 'Novo Envio WhatsApp'})

@login_required
def whats_update(request, pk):
    whats = get_object_or_404(WhatsAppEnvio, pk=pk)
    if request.method == 'POST':
        form = WhatsAppEnvioForm(request.POST, instance=whats)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de envio atualizado com sucesso!')
            return redirect('cal:whats_list')
    else:
        form = WhatsAppEnvioForm(instance=whats)
    return render(request, 'whats/form.html', {'form': form, 'titulo': 'Editar Envio WhatsApp'})

@login_required
def whats_delete(request, pk):
    whats = get_object_or_404(WhatsAppEnvio, pk=pk)
    if request.method == 'POST':
        whats.delete()
        messages.success(request, 'Registro de envio excluído com sucesso!')
        return redirect('cal:whats_list')
    return render(request, 'whats/confirm_delete.html', {'whats': whats})
