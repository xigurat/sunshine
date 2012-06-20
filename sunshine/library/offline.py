

from tasks import task

from .models import Book


#~ @task(ignore=(Book.DoesNotExist,))
def post_process(book_id):
    #~ book = Book.objects.get(id=book_id)
    #~ book.post_process()
    pass
