import logging

import paste.fileapp
import mimetypes
import os
from pylons import config
import boto.s3.connection as s3connection

import ckan.logic as logic
import ckan.lib.base as base
from ckan.common import c, response, request, _
import ckan.model as model
import ckan.lib.uploader as uploader

log = logging.getLogger(__name__)

from ckan.controllers.package import PackageController

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
render = base.render
abort = base.abort
redirect = base.redirect
get_action = logic.get_action


class S3Downloader(PackageController):

    def resource_download(self, id, resource_id, filename=None):
        """
        Provides a direct download by either redirecting the user to the url stored
         or downloading an uploaded file directly.
        """
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj}

        try:
            rsc = get_action('resource_show')(context, {'id': resource_id})
            pkg = get_action('package_show')(context, {'id': id})
        except NotFound:
            abort(404, _('Resource not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read resource %s') % id)

        if rsc.get('url_type') == 'upload':
            upload = uploader.ResourceUpload(rsc)
            filepath = upload.get_path(rsc['id'])

            #### s3archive new code
            access_key = config.get('ckanext.s3archive.access_key')
            secret_key = config.get('ckanext.s3archive.secret_key')
            bucket_name = config.get('ckanext.s3archive.bucket')

            if not os.path.exists(filepath):
                content_type, content_enc = mimetypes.guess_type(rsc.get('url',''))
                key_name = filepath[len(filepath)-39:]

                conn = s3connection.S3Connection(access_key, secret_key)
                bucket = conn.get_bucket(bucket_name)

                key = None
                for key in bucket.list(prefix=key_name.lstrip('/')):
                    pass
                if not key:
                    abort(404, _('Resource data not found'))

                headers = {}
                if content_type:
                    headers['response-content-type'] = content_type
                url = key.generate_url(300, method='GET', response_headers=headers)
                redirect(url)
            #### code finish

            fileapp = paste.fileapp.FileApp(filepath)

            try:
               status, headers, app_iter = request.call_application(fileapp)
            except OSError:
               abort(404, _('Resource data not found'))
            response.headers.update(dict(headers))
            content_type, content_enc = mimetypes.guess_type(rsc.get('url',''))
            response.headers['Content-Type'] = content_type
            response.status = status
            return app_iter
        elif not 'url' in rsc:
            abort(404, _('No download is available'))
        redirect(rsc['url'])

