import os
import json
import requests
from .Fork import Fork
from .types import Actions
from .ErrorMs import ErrorMs
from .loggs import Loggs


class ForkHttp(Fork):
    """
        Clase para el control de operaciones de bifurcaciones
        basada en peticiones http.
    """
    topic = None

    forks = []

    # Logs de la aplicacion
    logs = Loggs('ForkHttpLogic')

    def __init__(self, topic):
        self.topic = topic

    def confForks(self, conf):
        self.forks = conf

    def process(self, span, data, fnc_class, params=[]):
        """
            Metodo para el procesamiento de las peticiones.
        """
        # Data anterior
        response = None

        # Headers
        headers = {}

        # Headers
        if not data["headers"].get("Authorizacion", None) is None:
            headers.update({
                "Authorizacion": data["headers"].get("Authorizacion", None)
            })

        for wk in self.forks:
            # Respuesta de la peticion.
            resp_rest = None

            # Url base
            url_endp = os.environ.get('URL_ENDPOINT_SERVICES', None)

            # Conf base
            conf_int = wk.get('conf')

            # App
            app = conf_int.get('App')

            # Version
            ver = conf_int.get('Version')

            # Services
            ser = conf_int.get('Name')

            # Url de la peticion
            url_pet = f'{url_endp}/{app}/api/{ver}/{ser}'

            # Data Send
            data_send = data.get('data', {})

            # Validar si se paso una funcion
            if hasattr(wk.get('fnc_call', None), '__call__'):
                # Recuperar la funcion a ejecutar
                fnc = wk.get('fnc_call')

                try:
                    # Dar formato a la data
                    data_send = fnc(
                        data.get('data', {}),
                        response
                    )
                except Exception as err:
                    self.logs.error(err)

            # Action
            act = wk.get('action')

            try:
                self.logs.info(f'SALIDA [{url_pet}]: {data_send}')
                # Define el estado
                if act == Actions.CREATE:
                    resp_rest = requests.post(
                        url_pet,
                        data=json.dumps(data_send),
                        headers=headers
                    )
                elif act == Actions.DELETE:
                    resp_rest = requests.delete(url_pet, headers=headers)
                elif act == Actions.GET:
                    resp_rest = requests.get(url_pet, headers=headers)
                elif act == Actions.LIST:
                    resp_rest = requests.get(url_pet, headers=headers)
                elif act == Actions.UPDATE:
                    resp_rest = requests.put(
                        url_pet, data=json.dumps(data_send), headers=headers)
                else:
                    pass
            except Exception as err:
                self.logs.error(err)
                raise ErrorMs(
                    message="Ocurrio un error al consumir los workers")

            # Generar el diccionario http
            htpp_resp = {
                "code": resp_rest.status_code,
                "message": url_pet,
                "headers": []
            }

            # Actualizar el registro de http
            data['metadata']['http'] = htpp_resp

            # Ver si ocurrio un error.
            if resp_rest.status_code == requests.codes.ok:
                response = {}

                # Almacenar la respuesta el servicio
                rp = resp_rest.json()
                if not rp.get('data', {}) is None:
                    if not rp.get('response', {}) is None:
                        response = rp['data']['response']

                data['response'] = {}

                if not response.get('code', None) is None:

                    msg = response.get('userMessage', '')

                    # Asignar un codigo de error
                    if data['metadata']['http']['code'] == 200:
                        data['metadata']['http'].update({
                            "code": 500
                        })

                    # response['userMessage'] = f'{app}:{ser}({ver}): {msg}'

                    self.logs.error(f'{app}:{ser}({ver}): {msg}')

                    data['response'].update({
                        "data": {
                            "response": response
                        }
                    })

                    return self.formatResponse(
                        data,
                        # Enviar el resultado correcto
                        self.get_http_data(data['metadata']),
                        self.getErrorCode(data),
                        self.getErrorMeta(data)
                    )
                else:
                    data['response'].update({
                        "data": response.get('data', {})
                    })

            else:
                rp = resp_rest.json()
                data['response'] = {}
                data['response'].update({
                    "data": rp.get('data', {})
                })
                return self.formatResponse(
                    data,
                    # Enviar el resultado correcto
                    self.get_http_data(data['metadata']),
                    self.getErrorCode(data),
                    self.getErrorMeta(data)
                )

        # Parametros
        paramsInject = self.getParams(span, data, params)
        # Ejecutar la funciona final
        RESP = fnc_class(*paramsInject)
        # Regresar la respuesta con el formato correcto
        return self.formatResponse(data, RESP)
