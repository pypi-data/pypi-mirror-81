from . import errors

import os
import zipfile

import aiosqlite
import sqlite3

import async_timeout
import json

import inspect

class Manifest:
    """Interfaces with the Destiny 2 manifest.

    :param api: An API instance. Automatically created when initializing a Destiny instance.
    :type api: destiny.API
    """

    def __init__(self, api):
        self.api = api
        self.manifests = {
            'en': '',
            'fr': '',
            'es': '',
            'de': '',
            'it': '',
            'ja': '',
            'pt-br': '',
            'es-mx': '',
            'ru': '',
            'pl': '',
            'zh-cht': ''
        }
    
    async def decodeHash(self, hash, definition, language):
        """Decodes a given hash.
        
        :param hash: The hash ID of the entity to decode
        :type hash: str,int
        :param definition: The type of entity.
        :type definition: str
        :param language: The language to decode in
        :type language: str
        :raises KeyError: invalid language
        """

        if language not in self.manifests:
            raise KeyError(f'{language} is not a valid language')

        if not self.manifests[language]:
            await self.update(language)

        # Honestly no clue but it's in pydest and probably right
        if definition == 'DestinyHistoricalStatsDefinition':
            hash = f'"{hash}"'
            identifier = 'key'
        else:
            hash = int(hash)
            if hash & 0x80000000 != 0:
                hash = hash - 0x100000000
            identifier = 'id'

        try:
            async with aiosqlite.connect(self.manifests[language]) as db:
                async with db.execute(f'SELECT json FROM {definition} WHERE {identifier} = {hash}') as cursor: # <- FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE FUCK THIS LINE
                    result = await cursor.fetchall()
        except sqlite3.OperationalError as e:
                if e.args[0].startswith('no such table'):
                    raise ValueError(f'Invalid definition: {definition}')
                else:
                    raise e
        
        if result:
            return json.loads(result[0][0])
        else:
            raise ValueError(f'No entry for id: {hash}')
            
    
    async def update(self, language):
        """Updates the manifest from Bungie
        
        :param language: language of manifest to update
        :type language: str
        :raises KeyError: invalid language
        """

        if language not in self.manifests:
            raise KeyError(f'{language} is not a valid language')

        response = await self.api.getDestinyManifest()

        url = response['mobileWorldContentPaths'][language]
        fp = url.split('/')[-1]

        await self._download('https://www.bungie.net' + url, 'manifestZip')
        zipRef = zipfile.ZipFile('manifestZip', 'r')
        zipRef.extractall('.')
        zipRef.close()
        os.remove('manifestZip')
        
        self.manifests[language] = fp
    
    async def _download(self, url, name):
        with async_timeout.timeout(10):
            async with self.api.session.get(url) as response:
                filename = os.path.basename(name)
                with open(filename, 'wb') as f_handle:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f_handle.write(chunk)
                return await response.release()