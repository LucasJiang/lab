import traceback
from tornado.web import RequestHandler
from app.base.jinja_manager import JinjaManager, TEMPLATE_PLATFORM_SEP
from app.database.session_maker import get_new_session
from app.exception.error_log import ErrorLog

__author__ = 'jiang'


class RequestHandlerBase(JinjaManager, RequestHandler, ErrorLog):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        self.sqlalchemy_session = None
        RequestHandler.__init__(self, application, request, **kwargs)

    @property
    def db_session(self):
        if not self.sqlalchemy_session:
            self.sqlalchemy_session = get_new_session()
        return self.sqlalchemy_session

    def render_template(self, template_dir_name, template_name, **kwargs):
        return self.render('{}{}/{}'.format(
            self.template_platform + TEMPLATE_PLATFORM_SEP,
            template_dir_name,
            template_name
        ),
            # Add public k-v here to give template var.
            **kwargs
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
