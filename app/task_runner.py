from django_rq import job


@job('default')
def default_handler():
    pass


default_handler.delay()  # Enqueue function with a timeout of 3600 seconds.


@job('stir_fry')
def stir_fry_handler():
    pass


stir_fry_handler.delay()
