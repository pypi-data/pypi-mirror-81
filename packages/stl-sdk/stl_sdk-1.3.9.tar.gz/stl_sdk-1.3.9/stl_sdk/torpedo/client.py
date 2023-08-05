import requests
from requests.exceptions import HTTPError
from stl_sdk.torpedo.exceptions import TorpedoClientHTTPError


class TorpedoClient:
    """Cliente HTTP para comunicação com Torpedo

    :param str url: Endereço da API do serviço Torpedo
    :param str product_name: Nome do produto requisitando o envio do email,
        esse parâmetro será usado em conjunto com o ``template_name`` para encontrar o template do email
    """
    url = None
    product_name = None

    def __init__(self, url, product_name):
        self.url = url.strip('/')
        self.product_name = product_name

    def send_email(self, email, subject, template_name, data=None):
        """Envia email com um template pré-definido do Torpedo através da API do `Mailgun <https://www.mailgun.com/>`_.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import TorpedoClient

            client = TorpedoClient('https://notifications.spacetimeanalytics.com', 'waves')
            response = client.send_email('pedro@gmail.com', 'Bem-vindo!', 'welcome', { 'name': 'Pedro' })

        :param email: Email do destinatário
        :type email: str
        :param subject: Assunto do email
        :type subject: str
        :param template_name: Nome do template do Torpedo
            (`Veja os templates disponíveis <http://notifications.spacetimeanalytics.com>`_).
        :type template_name: str
        :param data: Dicionário de dados para popular o email
        :type data: dict, optional
        :return: Resposta da requisição para o Mailgun
        :rtype: requests.Response
        """
        try:
            response = requests.post(
                    '{}/api/send-email'.format(self.url),
                    json={
                        'to_email': email,
                        'subject': subject,
                        'template_name': template_name,
                        'data': data,
                        'product': self.product_name,
                    }
                )
            response.raise_for_status()
            return response
        except HTTPError as error:
            raise TorpedoClientHTTPError(error) from error
