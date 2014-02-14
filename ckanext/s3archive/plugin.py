import os
from logging import getLogger

from pylons import request
from genshi.input import HTML

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurable
from ckan.plugins import IRoutes

log = getLogger(__name__)


class s3archivePlugin(SingletonPlugin):
    implements(IConfigurable, inherit=True)
    implements(IRoutes, inherit=True)

    def configure(self, config):
        self.access_key = config.get('ckanext.s3archive.access_key')
        self.secret_key = config.get('ckanext.s3archive.secret_key')

    def before_map(self, map):

        map.connect('/dataset/{id}/resource/{resource_id}/download',
                    action='resource_download', controller='ckanext.s3archive.controller:S3Downloader')

        map.connect('/dataset/{id}/resource/{resource_id}/download/{filename}',
                    action='resource_download', controller='ckanext.s3archive.controller:S3Downloader')

        return map
