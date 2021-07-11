from app import app


@app.template_filter('zfill')
def zfill(value, width):
    """ Zfill filter for ansible """
    return str(value).zfill(width)
