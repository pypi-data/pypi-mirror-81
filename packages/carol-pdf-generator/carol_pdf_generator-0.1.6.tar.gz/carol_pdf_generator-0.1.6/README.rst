carol\_pdf\_generator
=====================

carol\_pdf\_generator is a Python library for creating PDF Files from
images (png, jpg) file. Base64 encoded is also supported.

Installation
------------

Use the package manager `pip <https://pip.pypa.io/en/stable/>`__ to
install foobar.

.. code:: bash

    pip install carol_pdf_generator

Usage
-----

.. code:: python

    from carol_pdf_generator import get_from_file_list, get_from_base64_list
    from urllib import request

    file_list = [
        'jpgfile.jpg',
        'pngfile.png'
    ]

    base64_images.append(request.urlopen('https://pastebin.com/raw/k3VZeNHW').read().decode('latin1'))
    base64_images.append(request.urlopen('https://pastebin.com/raw/CaZJ7n6s').read().decode('latin1'))
    base64_images.append(request.urlopen('https://pastebin.com/raw/7Asb2iMJ').read().decode('latin1'))

    from_file = get_from_file_list(file_list)

    base64 = get_from_base64_list(base64_images, 'test.pdf')  # Returns the PDF base64 encoded data uri and saves the PDF to test.pdf

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
