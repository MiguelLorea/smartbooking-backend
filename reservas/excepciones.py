import logging

from rest_framework.views import exception_handler

logger = logging.getLogger("seguridad")


def manejar_error(exc, context):
    response = exception_handler(exc, context)
    if response is not None and response.status_code == 403:
        request = context.get("request")
        usuario = "anonimo"
        if request is not None and request.user.is_authenticated:
            usuario = request.user.username
        path = ""
        metodo = ""
        if request is not None:
            path = request.path
            metodo = request.method
        logger.warning(
            "acceso denegado usuario=%s accion=%s recurso=%s resultado=denegado",
            usuario,
            metodo,
            path,
        )
    return response
