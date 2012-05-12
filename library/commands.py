#!/usr/bin/env python
#-*- coding:utf-8 -*-


from datetime import datetime
from os import path, listdir
from commands_common import get_output, call
from dateutil.parser import parser as dateutil_parser


def get_pdf_info(pdf_file_path):
    """
    pdfinfo command prints an output like this:

      Creator:        Adobe InDesign CS2 (4.0.2)
      Producer:       PDFlib PLOP 2.0.0 (FreeBSD)/Adobe PDF Library 7.0
      CreationDate:   Mon Mar 26 10:27:26 2007
      ModDate:        Mon Apr 30 23:33:39 2007
      Tagged:         yes
      Pages:          270
      Encrypted:      no
      Page size:      612 x 792 pts (letter)
      File size:      5670000 bytes
      Optimized:      yes
      PDF version:    1.6

    from where n_pages and is_encrypted is extracted
    """
    params = []
    for line in get_output('pdfinfo', [u'"%s"' % pdf_file_path]):
        double_dot_pos = line.find(':')
        param_name = line[:double_dot_pos].strip().lower().replace(' ', '_')
        data = line[double_dot_pos + 1:].strip()
        params.append((param_name, data))
    return _PdfInfo(**dict(params))


def pdf2png(pdf_file_path, first=1, last=None):
    #preparing command
    args = ['-f %d' % first]
    if last is not None:
        args.append('-l %d' % last)
    args.extend(['-png', u'"%s"' % pdf_file_path, u'"%s"' % pdf_file_path])
    call('pdftoppm', args)

    #retrieving pages image paths
    working_directory = path.dirname(pdf_file_path)
    images_root_name = path.basename(pdf_file_path)
    pages_image_paths = {}
    for file_path in listdir(working_directory):
        file_name = path.basename(file_path)
        if file_name.startswith(images_root_name + '-'):
            number = file_name[len(images_root_name) + 1:-4]
            pages_image_paths[int(number)] = path.join(
                    working_directory, file_path)
    return pages_image_paths


def _parse_date(date):
    if date is None:
        return None
    try:
        return dateutil_parser().parse(date)
    except:
        return None


class _PdfInfo(object):
    """PDF file information representation"""
    def __init__(self, pages, encrypted, creationdate=None,
                 moddate=None, **kw):
        """Constructor"""
        self.n_pages = int(pages)
        self.is_encrypted = encrypted == 'yes'
        self.last_modification = (
            _parse_date(moddate)
            or _parse_date(creationdate)
            or datetime.now()
)
