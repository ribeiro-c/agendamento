def montar_mensagem(eventos):
    """
    Monta uma mensagem única com todos os eventos agrupados por data.
    Recebe uma lista de objetos AgendaEvento.
    """

    mensagem = "📚 *Agenda Escolar — Novas atividades*\n"
    mensagem += "━━━━━━━━━━━━━━━━━━━━━━\n"

    data_atual = None

    for evento in eventos:

        if data_atual != evento.data:
            data_atual = evento.data
            mensagem += f"\n📅 *{evento.data.strftime('%d/%m/%Y')}*\n\n"

        mensagem += f"📌 *{evento.titulo}*\n"
        mensagem += f"📂 {evento.tipo}\n"

        if evento.descricao and evento.descricao.strip():
            mensagem += f"{evento.descricao.strip()}\n"

        mensagem += "────────────────────\n"

    return mensagem.strip()
