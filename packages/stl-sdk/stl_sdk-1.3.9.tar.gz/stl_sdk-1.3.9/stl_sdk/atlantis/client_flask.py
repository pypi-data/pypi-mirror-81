from stl_sdk.exceptions import InvalidInitParameters
from stl_sdk.atlantis.client import AtlantisClient


class AtlantisClientFlask(AtlantisClient):
    """Cliente Flask para comunicação com Atlantis.
        Ao iniciar o cliente ele irá buscar as variaveis de ambiente
        `ATLANTIS_URL`, `ATLANTIS_CLIENT_ID` e `ATLANTIS_CLIENT_SECRET`.

        Para pular a chamada inicial de configuração do openId em seus teste, defina a variavel de ambiente `FLASK_ENV=testing`.

    Exemplo:

        .. code-block:: python

            from stl_sdk.atlantis import AtlantisClientFlask

            atlantis = AtlantisClientFlask()

            def init_app(app):
                atlantis.init_app(app)

    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app.config['ATLANTIS_URL'] is None:
            raise InvalidInitParameters('Missing ATLANTIS_URL on AtlantisClientFlask initialization.')

        if app.config['ATLANTIS_CLIENT_ID'] is None:
            raise InvalidInitParameters('Missing ATLANTIS_CLIENT_ID on AtlantisClientFlask initialization.')

        super().__init__(
            app.config['ATLANTIS_URL'],
            app.config['ATLANTIS_CLIENT_ID'],
            client_secret=app.config.get('ATLANTIS_CLIENT_SECRET'),
            skip_openid_configuration=app.config.get('FLASK_ENV') == 'testing'
        )
