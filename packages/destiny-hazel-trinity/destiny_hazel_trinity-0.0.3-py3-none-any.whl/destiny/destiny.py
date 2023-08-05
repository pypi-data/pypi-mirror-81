import asyncio
import aiohttp

from . import api
from . import manifest

class Destiny:
    """Main class including manifest data and api.

    :param api: a file or string containing only the API key for the Bungie API
    :type api: file-like object or string
    :param loop: asynchronous event loop to use, defaults to None
    :type loop: class:`asyncio.selector_events.BaseSelectorEventLoop`, optional
    :param contactInfo: Contact information to be provided to Bungie via User Agent, defaults to {'appID': '', 'appName': '', 'version': '', 'url': '', 'contactEmail': ''}
    :type contactInfo: dict, optional
    """
    def __init__(self, apiKey, *, loop=None, contactInfo=None):
        try:
            with apiKey as f:
                apiKey = f.read()
        except:
            pass
    
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self._loop)

        if contactInfo is None:
            contactInfo = {
                'appID': '',
                'appName': '',
                'version': '',
                'url': '',
                'contactEmail': ''
            }

        self.api = api.API(apiKey, self._session, **contactInfo)
        self.manifest = manifest.Manifest(self.api)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *_):
        await self.close()
    
    async def close(self):
        await self._session.close()