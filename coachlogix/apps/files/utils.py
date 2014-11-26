import io
import os
import uuid
import magic
 
from PIL import Image as PILImage
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from wand.image import Image
from mimetypes import guess_extension, guess_type


def get_uuid_name():
    """Return a new uuid name."""
    return str(uuid.uuid4())[:100]


def get_file_name(fobj):
    """
    Returns a file name and extension.

    :fobj: Either a base64 encoded string or a file object.
    """
    ext = os.path.splitext(str(fobj.name))[1][1:]
    return "{}.{}".format(get_uuid_name(), ext)


def get_b64_extension(fobj):
    """Return extension of base64 file."""
    if isinstance(fobj, basestring):
        ext = guess_extension(guess_type(fobj)[0]).strip('.')
        ext = "jpg" if ext == "jpeg" or ext == "jpe" else ext
        return ext


def valid_file_extension(fname, extension_list):
    """Determine if the file has a valid extension."""
    return any([fname.endswith(e) for e in extension_list])


def get_mimetype(fobj):
    """Return the mimetype for the file."""    
    mime = magic.Magic(mime=True)
    mimetype = mime.from_buffer(fobj.read(1024))
    fobj.seek(0)
    return mimetype


def strip_ext(fname):
    """Strip the file extension from the name."""
    return os.path.splitext(fname)[0]


def valid_file_mimetype(fobj, mimetype_list):
    """Determine if the file has a valid mimetype."""
    mimetype = get_mimetype(fobj)
    return any([mimetype.startswith(m) for m in mimetype_list]) if mimetype else False

 
def pdf_generator(source, **options):
    """
    Take the raw source file and try to convert it to a PIL image.
    """
    if not source:
        return
    
    path = source.path
    pages = 0 # 0-Indexed for first page only.
    output = 'jpg'

    # Attempt to open the file using wand.image.Image and output as blob, otherwise return.
    try:
        raw = io.StringIO(Image(filename='{}[{}]'.format(source.path, pages)).make_blob(output))
        raw.seek(0)
        image = PILImage.open(raw)
    except Exception:
        return
 
    return image
