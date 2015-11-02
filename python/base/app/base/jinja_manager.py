import os
from jinja2 import Environment, PrefixLoader, FileSystemLoader
from jinja2.ext import loopcontrols, autoescape
from app.dashboard.templates import DASHBOARD_DIR_NAME
from app.settings_init import PROJECT_SRC_DIR

__author__ = 'jiang'

TEMPLATE_PLATFORM_V_DEFAULT = 'default'
TEMPLATE_PLATFORM_SEP = '#'
CACHE_SIZE = 500  # default 400

EXTENSION_S = [loopcontrols, autoescape]

_SECTION_DIR_NAME_S = [
    DASHBOARD_DIR_NAME,
]


def make_template_prefix(platform, dir_name):
    return '{}{}{}'.format(
        platform,
        TEMPLATE_PLATFORM_SEP,
        dir_name,
    )

# /
JINJA2_ENV = Environment(
    loader=PrefixLoader(
        dict(
            [(
                 make_template_prefix(TEMPLATE_PLATFORM_V_DEFAULT, dir_name),
                 FileSystemLoader(os.path.join(PROJECT_SRC_DIR, dir_name, 'templates')),
             ) for dir_name in _SECTION_DIR_NAME_S
             ]
        )
    ),
    extensions=EXTENSION_S,
    cache_size=CACHE_SIZE,
)


class JinjaManager(object):
    """jinja manager
    Method of first inherited class will overwrite class behind.
    """
    template_platform = TEMPLATE_PLATFORM_V_DEFAULT

    def render_string(self, template_name, **kwargs):
        """Rewrite. Use jinja2"""
        template = JINJA2_ENV.get_template(template_name)
        return template.render(
            **kwargs)

    def render_template(self, template_dir_name, template_name, **kwargs):
        return self.render('{}{}/{}'.format(
            self.template_platform + TEMPLATE_PLATFORM_SEP,
            template_dir_name,
            template_name
        ),
            **kwargs
        )

    def render_dashboard_template(self, template_name, **kwargs):
        return self.render_template(
            template_dir_name=DASHBOARD_DIR_NAME,
            template_name=template_name,
            **kwargs
        )
