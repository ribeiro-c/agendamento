import hashlib


def gerar_hash(evento):
    """
    Generates a stable deduplication key for an event.

    Uses inicio (datetime) when available, falling back to the legacy data
    field, so hashes remain consistent across old and new records.
    """
    inicio = evento.get("inicio") or evento.get("data") or ""

    texto = "\n".join([
        str(inicio),
        str(evento.get("titulo", "")),
        str(evento.get("tipo", "")),
        str(evento.get("descricao", "")),
    ])

    return hashlib.sha256(texto.encode("utf-8")).hexdigest()
