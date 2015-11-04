import getopt
import os
import types
import sys
from exts.module_util import import_module_by_path, find_module

COPY_SETTINGS_FUNC_IGNORED_VALUE = object()

def set_setting_obj():
    """
    set setting obj from -c or from settings.py and settings_init.py
    """
    # getopt.getopt(sys.argv[1:],"hp:i:",["help","ip=","port="])
    opts, args = getopt.getopt(sys.argv[1:], "c:d:")
    specified_path = None
    for opt, value in opts:
        # conf file replace
        if opt == "-c" and os.path.exists(value):
            specified_path = value
    current_path = sys.path[0]
    settings_path = os.path.join(current_path, "settings") if not specified_path else specified_path
    src_module_obj = import_module_by_path(settings_path)

    # must use find module ,then ,after copy settings ,refresh in cache
    dest_module_obj = find_module("app.settings_init")
    copy_settings(src_module_obj, dest_module_obj)


def copy_settings(src_module, dst_module,
    args_obj=None,
    extra_items=None,
    ignoring_attributes=[],
    ignoring_attributes_in_obj=None
    ):
    """
    Copy settings from |dst_module| to |src_module|.
    
    An attribute in |dst_module| is considered as "setting" only if:
        Its name also exists in |src_module|.
        Its name not starts or ends with '__'.
        It is not a module.
    """
    #/ 
    vars_dict = vars(src_module).copy()

    #/
    if args_obj:
        #/
        args_obj_vars_dict = vars(args_obj).copy()
        
        #/
        for key, value in args_obj_vars_dict.items():
            if value is not None:
                vars_dict[key] = value
    
    #/
    if extra_items:
        vars_dict.update(extra_items)

    #/
    for key in sorted(vars_dict.keys()):
        #/
        if key in ignoring_attributes:
            continue

        #/
        if ignoring_attributes_in_obj is not None and hasattr(ignoring_attributes_in_obj, key):
            continue

        #/
        if key.startswith('_') and key.endswith('_'):
            continue

        #/
        if not hasattr(dst_module, key):
            continue

        #/
        value = vars_dict[key]

        #/
        if value is COPY_SETTINGS_FUNC_IGNORED_VALUE:
            continue

        #/
        if isinstance(value, types.ModuleType):
            continue

        #/
        setattr(dst_module, key, value)
