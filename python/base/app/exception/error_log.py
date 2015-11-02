import json
from pprint import pformat
import traceback
from tornado.web import HTTPError
from app.exception.models.error_log import ErrorLog300, ErrorLog400, ErrorLog500, LoggableError

__author__ = 'jiang'


class ErrorLog(object):
    HTTP_METHOD_TO_LETTER_DICT = {
        'GET': 'G',
        'POST': 'P',
        'PUT': 'M',
        'DELETE': 'D',
        'HEAD': 'H',
        'OPTIONS': 'O',
        'TRACE': 'T',
        'CONNECT': 'C',
    }

    def add_error_log_to_db(self,
                            session,
                            user_id=0,
                            exc_info=None,
                            code=None,
                            info=None,
                            table=None,
                            ):
        # /
        exc_obj = exc_info[1] if exc_info else None

        # /
        table_class = table

        if isinstance(exc_obj, HTTPError):
            if table_class is None:
                status_code = exc_obj.status_code

                if 300 <= status_code <= 399:
                    table_class = ErrorLog300
                elif 400 <= status_code <= 499:
                    table_class = ErrorLog400
                else:
                    table_class = ErrorLog500

            if code is None:
                code = exc_obj.status_code

        elif isinstance(exc_obj, LoggableError):
            if table_class is None and exc_obj.table is not None:
                table_class = exc_obj.table

            if code is None and exc_obj.code is not None:
                code = exc_obj.code

        # /
        if table_class is None:
            table_class = ErrorLog500

        # /
        if code is None:
            code = 500

        # /
        errorlog_obj = table_class()

        # /
        errorlog_obj.user_id = user_id

        errorlog_obj.user_ip = self.request.remote_ip or ''

        errorlog_obj.agent = self.request.headers.get('User-Agent', '')

        # /
        method_upper = self.request.method.upper()

        method_letter = self.HTTP_METHOD_TO_LETTER_DICT.get(method_upper, None)

        if method_letter is None:
            method_letter = method_upper[0]

            if method_letter in self.HTTP_METHOD_TO_LETTER_DICT.values():
                method_letter = 'Z'

        errorlog_obj.method = method_letter

        errorlog_obj.code = code

        errorlog_obj.url = self.request.full_url()

        errorlog_obj.args = json.dumps(self.request.arguments,
                                       ensure_ascii=False, encoding='utf-8') if self.request.arguments \
            else ''

        # /
        headers_dict_copy = self.request.headers.copy()
        headers_dict_copy.pop('Cookie', None)
        headers_dict_copy.pop('User-Agent', None)
        headers_dict_copy.pop('X-Real-Ip', None)
        headers_dict_copy.pop('X-Scheme', None)
        errorlog_obj.headers = pformat(headers_dict_copy, indent=4, width=1)

        if self.request.cookies:
            errorlog_obj.headers += '\n\n'
            errorlog_obj.headers += self.request.cookies.output(header="CK:")

        # /
        if info is None:
            info_text = ''
        elif isinstance(info, (dict, list, tuple)):
            info_text = pformat(info, indent=4, width=1)
        else:
            info_text = info

        # /
        if exc_info is not None:
            info_text += make_exception_traceback_text(exc_info)

        errorlog_obj.info = info_text

        # /
        session.add(errorlog_obj)
        session.commit()
        return errorlog_obj


def make_exception_traceback_text(exc_info):
    text_frame_s = traceback.format_exception(*exc_info)

    text = ''.join(text_frame_s)

    return text
