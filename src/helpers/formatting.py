def format_duration(ms: int) -> str:
    """Formatea duración en milisegundos a formato minutos:segundos.

    :param ms: Duración en milisegundos.
    :return: Cadena con formato mm:ss.
    """
    minutes, seconds = divmod(int(ms / 1000), 60)
    return f"{minutes}:{seconds:02d}"
