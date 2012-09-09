import mimetypes

from boto.s3.key import Key

from django.contrib.staticfiles.storage import CachedFilesMixin

from storages.backends.s3boto import S3BotoStorage


class FixedS3BotoStorage(S3BotoStorage):

    def _save(self, name, content):
        cleaned_name = self._clean_name(name)
        name = self._normalize_name(cleaned_name)
        headers = self.headers.copy()
        content_type = getattr(content, 'content_type',
            mimetypes.guess_type(name)[0] or Key.DefaultContentType)

        if self.gzip and content_type in self.gzip_content_types:
            content = self._compress_content(content)
            headers.update({'Content-Encoding': 'gzip'})

        content.name = cleaned_name
        encoded_name = self._encode_name(name)
        key = self.bucket.get_key(encoded_name)
        if not key:
            key = self.bucket.new_key(encoded_name)
        if self.preload_metadata:
            self._entries[encoded_name] = key

        key.set_metadata('Content-Type', content_type)
        key.set_contents_from_file(content, headers=headers, policy=self.acl,
                                 reduced_redundancy=self.reduced_redundancy, rewind=True)
        return cleaned_name


class CachedS3BotoStaticFileStorage(CachedFilesMixin, FixedS3BotoStorage):

    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStaticFileStorage, self).__init__(*args, **kwargs)

        self.location = "static/"
