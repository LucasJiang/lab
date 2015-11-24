import traceback
import binascii
from tornado.web import RequestHandler
from app.base.jinja_manager import JinjaManager, TEMPLATE_PLATFORM_SEP
from app.database.session_maker import get_new_session
from app.exception.error_log import ErrorLog
from app.settings_init import AES_KEY, LOGIN_COOKIE_NAME, LOGIN_COOKIE_DOMAIN, LOGIN_COOKIE_EXPIRE_DAYS, ENCRYPT_ZFILL, \
    AES_IV, HMAC_KEY1, HMAC_KEY2
from app.user.models.user import User
from exts.crypto_util import encrypt_bytes, decrypt_bytes

__author__ = 'jiang'


class RequestHandlerBase(JinjaManager, RequestHandler, ErrorLog):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        self.sqlalchemy_session = None
        self.login_user = None
        RequestHandler.__init__(self, application, request, **kwargs)

    @property
    def db_session(self):
        """
        create sqlalchemy sql obj
        """
        if not self.sqlalchemy_session:
            self.sqlalchemy_session = get_new_session()
        return self.sqlalchemy_session

    def render_template(self, template_dir_name, template_name, **kwargs):
        """
        override to set k-v
        """
        return self.render('{}{}/{}'.format(
            self.template_platform + TEMPLATE_PLATFORM_SEP,
            template_dir_name,
            template_name
        ),
            # Add public k-v here to give template var.
            **kwargs
        )

    def prepare(self):
        """override to run before get/post etc method
        """
        self.login_user = self._get_login_user()

    def _get_login_user(self):
        """
        Get user obj from cookie
        """
        login_cookie_value = self.get_cookie(LOGIN_COOKIE_NAME)
        if login_cookie_value:
            str_user_id = decrypt_bytes(
                data=binascii.unhexlify(login_cookie_value),
                raw_len=ENCRYPT_ZFILL,
                aes_iv=AES_IV,
                aes_key=AES_KEY,
                hmac_key1=HMAC_KEY1,
                hmac_key2=HMAC_KEY2,
            )
            return self.db_session.query(User).filter(User.id == int(str_user_id)).first()
        else:
            return None

    def clear_login_cookie(self):
        self.clear_cookie(LOGIN_COOKIE_NAME,
                          domain=LOGIN_COOKIE_DOMAIN
                          )

    def set_login_cookie(self, user_id):
        """
        set login cookie
        """
        zfill_user_id = str(user_id).zfill(ENCRYPT_ZFILL)
        cookie_value = encrypt_bytes(zfill_user_id.encode(encoding="utf-8"),
                                     AES_IV, AES_KEY, HMAC_KEY1, HMAC_KEY2)
        cookie_value = binascii.hexlify(cookie_value)
        self.set_cookie(LOGIN_COOKIE_NAME, cookie_value,
                        domain=LOGIN_COOKIE_DOMAIN,
                        expires_days=LOGIN_COOKIE_EXPIRE_DAYS,
                        )

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages and to add logs
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback

            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()

        else:
            self.add_error_log_to_db(
                self.db_session,
                exc_info=kwargs["exc_info"],
                code=status_code,
                info=self._reason,
            )

            # use any wanted page instead of these code
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                        })
