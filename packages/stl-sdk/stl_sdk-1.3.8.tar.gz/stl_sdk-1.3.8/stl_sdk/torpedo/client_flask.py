from stl_sdk.torpedo.client import TorpedoClient
from stl_sdk.exceptions import InvalidInitParameters


class TorpedoClientFlask(TorpedoClient):
    """Cliente Flask para comunicação com Torpedo.
        Ao iniciar o cliente ele irá buscar as variaveis de ambiente
        `TORPEDO_URL` e `TORPEDO_PRODUCT_NAME`

    Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClientFlask

            torpedo = TorpedoClientFlask()

            def init_app(app):
                torpedo.init_app(app)

    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app.config['TORPEDO_URL'] is None:
            raise InvalidInitParameters('Missing TORPEDO_URL on TorpedoClientFlask initialization.')

        if app.config['TORPEDO_PRODUCT_NAME'] is None:
            raise InvalidInitParameters('Missing TORPEDO_PRODUCT_NAME on TorpedoClientFlask initialization.')

        super().__init__(app.config['TORPEDO_URL'], app.config['TORPEDO_PRODUCT_NAME'])
