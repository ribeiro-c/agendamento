import time
import logging
import traceback
from collections import defaultdict

from agenda.models import AgendaEvento, Aluno, WhatsAppEnvio, Turma
from agenda.integrations.whatsapp_client import montar_mensagem
from evolution.app import enviar_texto

logger = logging.getLogger(__name__)


def _eventos_novos_por_turma():
    """
    Retorna um dict { turma: [eventos] } contendo apenas eventos
    que ainda não foram registrados em WhatsAppEnvio.
    """
    eventos_pendentes = (
        AgendaEvento.objects
        .filter(enviado_whatsapp=False)
        .select_related("turma")
        .order_by("data")
    )

    agrupados = defaultdict(list)

    for evento in eventos_pendentes:

        if evento.turma is None:
            logger.warning(f"⚠ Evento '{evento.titulo}' sem turma. Ignorando.")
            continue

        ja_enviado = WhatsAppEnvio.objects.filter(
            turma=evento.turma,
            hash_evento=evento.hash
        ).exists()

        if ja_enviado:
            # Já enviado em execução anterior — apenas sincroniza a flag
            evento.enviado_whatsapp = True
            evento.save(update_fields=["enviado_whatsapp"])
            continue

        agrupados[evento.turma].append(evento)

    return agrupados


def _registrar_envios(turma, eventos):
    """Salva WhatsAppEnvio para cada evento da turma e marca a flag."""
    for evento in eventos:
        WhatsAppEnvio.objects.get_or_create(
            turma=turma,
            hash_evento=evento.hash
        )
        evento.enviado_whatsapp = True
        evento.save(update_fields=["enviado_whatsapp"])

    logger.info(
        f"📝 {len(eventos)} envio(s) registrado(s) — turma: {turma}"
    )


def enviar_tarefas():

    logger.info("📲 Iniciando envio WhatsApp")

    agrupados = _eventos_novos_por_turma()

    if not agrupados:
        logger.info("📭 Nenhum evento novo para enviar")
        return

    logger.info(f"🏫 Turmas com eventos novos: {len(agrupados)}")

    for turma, eventos in agrupados.items():

        logger.info(
            f"📤 Turma '{turma}' — {len(eventos)} evento(s) a enviar"
        )

        alunos = Aluno.objects.filter(turma=turma)

        if not alunos.exists():
            logger.warning(f"⚠ Nenhum aluno na turma '{turma}'. Registrando e seguindo.")
            _registrar_envios(turma, eventos)
            continue

        # Monta UMA mensagem com todos os eventos da turma
        mensagem = montar_mensagem(eventos)

        logger.info(f"💬 Mensagem montada com {len(eventos)} evento(s)")

        for aluno in alunos:

            numero = aluno.telefone

            if not numero:
                logger.warning(f"⚠ Aluno '{aluno.nome_aluno}' sem telefone. Pulando.")
                continue

            try:

                response = enviar_texto(numero, mensagem)

                if response.status_code in [200, 201]:
                    logger.info(f"✅ Mensagem enviada para {aluno.nome_aluno} ({numero})")
                else:
                    logger.warning(
                        f"⚠ API retornou {response.status_code} para {numero}. "
                        f"Resposta: {response.text[:200]}"
                    )

                time.sleep(4)

            except Exception as e:
                logger.error(f"❌ Erro ao enviar para {numero}: {e}")
                traceback.print_exc()

        # Registra sempre após a tentativa — evita reenvio infinito
        _registrar_envios(turma, eventos)

    logger.info("✅ Envio finalizado")
