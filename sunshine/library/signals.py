
from django.dispatch import Signal

book_post_processed = Signal(providing_args=['book'])
