import json
import logging

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from ..models import Aluno, AgendaEvento, TarefaCompleta

logger = logging.getLogger(__name__)


def listar_tarefas(request, aluno_id):
    """
    Lista todas as tarefas da turma do aluno,
    indicando quais ele já marcou como concluídas.
    """
    aluno = get_object_or_404(Aluno, pk=aluno_id)

    eventos = (
        AgendaEvento.objects
        .filter(turma=aluno.turma)
        .order_by("data")
    )

    # Monta um set de IDs de eventos já concluídos por este aluno
    concluidos_ids = set(
        TarefaCompleta.objects
        .filter(aluno=aluno, concluida=True)
        .values_list("evento_id", flat=True)
    )

    tarefas = []
    for evento in eventos:
        tarefas.append({
            "evento": evento,
            "concluida": evento.id in concluidos_ids,
        })

    return render(request, "tarefas/lista.html", {
        "aluno": aluno,
        "tarefas": tarefas,
    })


@require_POST
def marcar_concluida(request):
    """
    Endpoint AJAX para marcar/desmarcar uma tarefa como concluída.
    Payload JSON: { "evento_id": int, "aluno_id": int }
    Resposta JSON: { "status": "ok", "concluida": bool }
    """
    try:
        data = json.loads(request.body)
        evento_id = int(data.get("evento_id"))
        aluno_id = int(data.get("aluno_id"))
    except (TypeError, ValueError, json.JSONDecodeError) as e:
        logger.warning(f"Payload inválido em marcar_concluida: {e}")
        return JsonResponse({"status": "erro", "mensagem": "Dados inválidos."}, status=400)

    aluno = get_object_or_404(Aluno, pk=aluno_id)
    evento = get_object_or_404(AgendaEvento, pk=evento_id)

    tarefa, criado = TarefaCompleta.objects.get_or_create(
        aluno=aluno,
        evento=evento,
        defaults={"concluida": False}
    )

    # Toggle
    tarefa.concluida = not tarefa.concluida
    tarefa.save()

    logger.info(
        f"{'✅' if tarefa.concluida else '⬜'} "
        f"Aluno {aluno} — {evento.titulo} — concluida={tarefa.concluida}"
    )

    return JsonResponse({"status": "ok", "concluida": tarefa.concluida})
