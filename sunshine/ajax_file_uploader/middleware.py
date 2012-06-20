
import os
from urllib import unquote

from django.http import HttpResponseBadRequest
from django.core.files.uploadedfile import TemporaryUploadedFile


class AjaxFileUploadSessionMiddleware(object):
    chunk_size = 64 * 2 ** 10  # The default chunk size is 64 KB.

    def process_request(self, request):
        file_name = request.META.get('HTTP_X_FILE_NAME')
        self.uploaded_file = None
        if ('application/octet-stream' in request.META.get('CONTENT_TYPE')
            and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
            and request.method == 'POST'
            and file_name):

            initial_size = request._stream.remaining
            self.uploaded_file = TemporaryUploadedFile(
                name=unquote(file_name),
                content_type='application/octet-stream',
                size=initial_size,
                charset=None)

            size = 0
            while True:
                chunk = request._stream.read(self.chunk_size)
                if not chunk:
                    break
                size += len(chunk)
                self.uploaded_file.write(chunk)

            if size != initial_size:
                raise HttpResponseBadRequest

            self.uploaded_file.seek(0)
            self.uploaded_file.size = size

            request.FILES['file'] = self.uploaded_file
            request.POST = request.GET

    def process_response(self, request, response):
        if hasattr(self, 'uploaded_file') and self.uploaded_file is not None:
            tmp_file_name = self.uploaded_file.file.name
            if os.path.exists(tmp_file_name):
                os.remove(tmp_file_name)
        return response
