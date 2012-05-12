

from django.db import models

class AuthorManager(models.Manager):
    
    def get_authors(self, authors, separator=u','):
        #TODO: no case sensitive
        if authors is not None:
            for author_name in authors.split(separator):
                author, _ = self.get_or_create(name=author_name.strip())
                yield author
