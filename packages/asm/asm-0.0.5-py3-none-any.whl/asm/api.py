#This file is part of asm. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from asm.utils import asm_url
from xml.dom.minidom import parseString
from urllib import request
import socket
import os
import genshi
import genshi.template
from random import randint

loader = genshi.template.TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'template'),
    auto_reload=True)


class API(object):
    """
    Generic API to connect to ASM
    """
    __slots__ = (
        'url',
        'username',
        'timeout',
    )

    def __init__(self, username, timeout=None, debug=False):
        """
        This is the Base API class which other APIs have to subclass. By
        default the inherited classes also get the properties of this
        class which will allow the use of the API with the `with` statement

        Example usage ::

            from asm.api import API

            with API(username) as asm_api:
                return asm_api.test_connection()

        :param username: ASM API username
        :param timeout: int number of seconds to lost connection.
        """
        self.url = asm_url(debug)
        self.username = username
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def connect(self, xml):
        """
        Connect to the Webservices and return XML data from ASM

        :param xml: XML data.

        Return XML object
        """
        headers = {
            'Content-Type': 'application/soap+xml; charset=utf-8',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(xml),
            }
        rqst = request.Request(self.url, bytes(xml.encode('utf-8')), headers)
        try:
            response = request.urlopen(rqst, timeout=self.timeout)
            return response.read()
        except socket.timeout as err:
            return
        except socket.error as err:
            return

    def test_connection(self):
        """
        Test connection to ASM webservices
        Send XML to ASM and return error send data
        """
        tmpl = loader.load('test_connection.xml')

        vals = {
            'referencia_c': randint(1000, 2000),
            }
        xml = tmpl.generate(**vals).render()
        result = self.connect(xml)
        if not result:
            return 'Error connection to ASM'

        dom = parseString(result)
        Envio = dom.getElementsByTagName('Envio')

        if not Envio:
            return 'Error connection to ASM'

        Errores = Envio[0].getElementsByTagName('Errores')
        if Errores:
            Error = Errores[0].getElementsByTagName('Error')
            if Error:
                error = Error[0].firstChild.data
                return error

        reference = Envio[0].getAttribute('codbarras')
        if reference:
            return 'Succesfully send a test to ASM with tracking "%s"' % (reference)
