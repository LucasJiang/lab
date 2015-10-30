# coding: utf-8
from collections import deque
import imp
import os
import os.path
import sys

def find_module(name, or_none=False):
    #/
    module_obj = sys.modules.get(name, None)

    #/
    if module_obj is not None:
        return module_obj

    #
    if or_none:
        try:
            __import__(name)
        except Exception:
            return None
    else:
        __import__(name)
        ## raise ImportError if not exist
        ## raise any error caused in the imported module
        ##
        ## Module object created by |__import__| will contain the module's sub modules
        ## as attribute objects. While module object created by |import| statement does not

    #/
    return sys.modules[name]

def find_module_or_error(name):
    assert isinstance(name, str) and name != ''
    try:
        return sys.modules[name]
    except KeyError:
        pass
    #
    __import__(name)
    ## raise ImportError if not exist
    ## raise any error caused in the imported module
    ## 
    ## Module object created by |__import__| will contain the module's sub modules
    ## as attribute objects. While module object created by |import| statement does not
    
    return sys.modules[name]

def get_dir_path_by_module(module):
    """
    Given a module instance, get the module file's dir path.
    Note if the module name is actually a package name, e.g. "tkinter", then the
    module file is actually "tkinter.__init__".
    """
    the_dir_path = os.path.dirname(module.__file__)
    
    return the_dir_path

def get_module_tree_by_package(package):
    the_module_s = []

    def the_handle(package, level, parent, index, is_before_children):
        if not is_before_children: return

        the_module_s.extend(get_sibling_module_s_by_module(package,
            is_package=True
            )
        )

    tree_traverse_depth_first(
        root=package,
        get_children=get_child_package_s_by_module,
        handle=the_handle,
    )

    return the_module_s

def get_module_tree_by_package_name(package):
    #/
    the_module_object = find_module_or_error(package)

    #/
    return get_module_tree_by_package(the_module_object)

def get_parent_module_by_module(module):
    the_parent_module_name = get_parent_module_name_by_module(module)
    if the_parent_module_name == '': return None
    the_parent_module = find_module_or_error(the_parent_module_name)
    return the_parent_module

def get_parent_module_file_path_by_module(module):
    the_parent_module = get_parent_module_by_module(module)
    the_parent_module_file_path = the_parent_module.__file__
    return the_parent_module_file_path

def get_parent_module_name_by_module(module):
    assert hasattr(module, '__name__')
    the_module_name = module.__name__
    the_parent_module_name = get_parent_module_name_by_module_name(the_module_name)
    return the_parent_module_name

def get_parent_module_name_by_module_name(module_name):
    #/
    if not has_parent_module_name_by_module_name(module_name):
        return ''

    #/
    the_last_dot_index = module_name.rfind('.')
    assert the_last_dot_index != -1

    #/
    return module_name[0:the_last_dot_index]

def get_sibling_dir_name_s_by_module(module):
    the_dir_path = get_dir_path_by_module(module)
    the_sibling_name_s = os.listdir(the_dir_path)
    the_sibling_dir_name_s = [x for x in the_sibling_name_s
        if os.path.isdir(os.path.join(the_dir_path, x))
    ]
    return the_sibling_dir_name_s

def get_sibling_package_dir_name_s_by_module(module):
    the_dir_path = get_dir_path_by_module(module)
    the_sibling_name_s = os.listdir(the_dir_path)
    the_sibling_dir_name_s = [x for x in the_sibling_name_s
        if os.path.isfile(os.path.join(the_dir_path, x, '__init__.py')) \
    ]
    return the_sibling_dir_name_s

def get_sibling_package_dir_path_s_by_module(module):
    the_dir_path = get_dir_path_by_module(module)
    the_sibling_name_s = os.listdir(the_dir_path)
    the_sibling_dir_name_s = [os.path.join(the_dir_path, x) for x in the_sibling_name_s
        if os.path.isfile(os.path.join(the_dir_path, x, '__init__.py')) \
    ]
    return the_sibling_dir_name_s

def get_sibling_package_module_s_by_module(module):
    module_s = []
    
    for name in get_sibling_package_dir_name_s_by_module(module):
        m = find_module('{}.{}'.format(module.__name__, name), or_none=True)
        if m is not None:
            module_s.append(m)

    return module_s

def get_sibling_package_modules_z_one_sub_module_by_module(module, name):
    module_s = []

    for n in get_sibling_package_dir_name_s_by_module(module):
        m = find_module('{}.{}.{}'.format(module.__name__, n, name), or_none=True)
        if m is not None:
            module_s.append(m)

    return module_s

def get_sibling_file_name_s_by_module(module):
    """ Files here mean regular files, not including directories. """
    the_dir_path = get_dir_path_by_module(module)
    the_sibling_name_s = os.listdir(the_dir_path)
    the_sibling_file_name_s = [x for x in the_sibling_name_s
        if os.path.isfile(os.path.join(the_dir_path, x))
    ]
    return the_sibling_file_name_s

def get_sibling_module_name_s_by_module(module, is_package=False):
    if is_package:
        the_parent_module_name = module.__name__
    else:
        the_parent_module_name = get_parent_module_name_by_module(module)

    #/
    the_py_name_s = get_sibling_py_file_name_s_by_module(module)

    #/
    the_py_name_s_noext = [x[0:-3] for x in the_py_name_s]

    #/
    the_sibling_module_name_s = ['{}.{}'.format(the_parent_module_name, x)  for x in the_py_name_s_noext]

    #/
    return the_sibling_module_name_s

def get_sibling_module_name_s_by_module_name(module, is_package=False):
    #/
    the_module_object = find_module_or_error(module)

    #/
    return get_sibling_module_name_s_by_module(the_module_object, is_package=is_package)

def get_sibling_module_s_by_module(module, is_package=False):
    the_sub_module_name_s = get_sibling_module_name_s_by_module(module, is_package=is_package)

    the_sub_module_s = []
    
    for the_sub_module_name in the_sub_module_name_s:
        try:
            the_sub_module = find_module_or_error(the_sub_module_name)
        except ImportError:
            sys.stderr.write('Ignored {}\n'.format(the_sub_module_name))
        else:
            the_sub_module_s.append(the_sub_module)

    return the_sub_module_s

def get_sibling_module_s_by_module_name(module, is_package=False):
    #/
    the_module_object = find_module_or_error(module)

    return get_sibling_module_s_by_module(the_module_object, is_package=is_package)

def get_child_package_name_s_by_package(package):
    #/
    the_dir_path = get_dir_path_by_module(package)

    #/
    the_child_name_s = os.listdir(the_dir_path)

    #/
    the_child_dir_name_s = [x for x in the_child_name_s
        if os.path.isdir(os.path.join(the_dir_path, x))
    ]

    #/
    the_child_dir_path_s = [os.path.join(the_dir_path, x)
        for x in the_child_dir_name_s
    ]

    #/
    the_child_package_name_s = []

    assert len(the_child_dir_name_s) == len(the_child_dir_path_s)
    for dir_name, dir_path in zip(the_child_dir_name_s, the_child_dir_path_s):
        the_init_file_path = os.path.join(dir_path, '__init__.py')
        if os.path.isfile(the_init_file_path):
            the_child_package_name_s.append('{}.{}'.format(package.__name__, dir_name))

    return the_child_package_name_s

def get_child_package_name_s_by_package_name(package):
    #/
    the_module_object = find_module_or_error(package)

    #/
    return get_child_package_name_s_by_package(the_module_object)

def get_child_package_s_by_module(package):
    #/
    the_child_package_name_s = get_child_package_name_s_by_package(package)
    
    #/
    the_child_package_s = []
    
    for the_sibling_package_name in the_child_package_name_s:
        the_sibling_package = find_module_or_error(the_sibling_package_name)
        the_child_package_s.append(the_sibling_package)

    #/
    return the_child_package_s

def get_child_package_s_by_module_name(module):
    #/
    the_module_object = find_module_or_error(module)

    #/
    return get_child_package_s_by_module(the_module_object)

def get_sibling_py_file_name_s_by_module(module):
    the_sibling_file_name_s = get_sibling_file_name_s_by_module(module)
    the_sibling_file_name_s_with_py_ext = [x for x in the_sibling_file_name_s if x.lower().endswith('.py')]
    return the_sibling_file_name_s_with_py_ext

def has_parent_module_name_by_module_name(module_name):
    #/ Ensure the module name does not start or end with dot.
    ## Because such a name is considered as invalid.
    assert not module_name.startswith('.')
    assert not module_name.endswith('.')

    #/
    return module_name.find('.') != -1

def tree_traverse_depth_first(root, get_children, handle,
    reverse_child_order=False):
    """ This function is copy-and-pasted from AoiU.Algorithm in order to
    eliminate the dependency.
    It is used by function get_module_tree_by_package above.
    """
    #//
    the_item_queue = deque()
    the_item_queue.append((root, 0, None, None))
    ## |0| is the level.

    the_pending_parent_item_s = []
    ## assumne items are unique

    while(the_item_queue):
        the_item, the_level, the_parent, the_index = the_item_queue.popleft()

        #//
        if any(x is the_item for x in the_pending_parent_item_s):
            handle(the_item, the_level, the_parent, the_index, False)
            the_pending_parent_item_s.remove(the_item)
            continue
        else:
            handle(the_item, the_level, the_parent, the_index, True)
            the_item_queue.appendleft((the_item, the_level, the_parent, the_index))
            the_pending_parent_item_s.append(the_item)

        #//
        the_child_item_s = get_children(the_item)

        #//
        if the_child_item_s:

            #//
            if reverse_child_order:
                the_child_item_s = reversed(the_child_item_s)

            #//
            the_child_item_tuple_s = []

            for the_child_item_index, the_child_item in enumerate(the_child_item_s):
                the_child_item_tuple = (the_child_item, the_level+1, the_item, the_child_item_index)
                the_child_item_tuple_s.append(the_child_item_tuple)

            #//
            the_child_item_tuple_s.reverse()
            the_item_queue.extendleft(the_child_item_tuple_s)

def import_module_in_namespace(namespace_path, module_fullname,
    __import__sub_modules=True):
    #/
    module_file_barename_s = module_fullname.split('.')
    parent_module_fullname = '' ## change in each iteration
    module_file_dir_path = namespace_path ## change in each iteration

    for module_file_barename in module_file_barename_s:
        if parent_module_fullname == '':
            parent_module_obj = None
            module_fullname = module_file_barename
        else:
            parent_module_obj = sys.modules[parent_module_fullname]
            module_fullname = parent_module_fullname + '.' + module_file_barename

        if parent_module_obj and __import__sub_modules:
            __import__(module_fullname)
            module_obj = sys.modules[module_fullname]
        else:
            file_handle = None
            try:
                #/
                tup = imp.find_module(module_file_barename, [module_file_dir_path])
                ## raise ImportError

                #/
                module_obj = imp.load_module(module_fullname, *tup)
                ## raise exceptions

                #/
                if parent_module_obj:
                    setattr(parent_module_obj, module_file_barename, module_obj)
                ## If do not do this, then importing sub module using
                ## "import a.b" will fail because if top module "a" is imported,
                ## "import a.b" will find sub-module "a.b" by "getattr(a, 'b')".
                ## This is fine if the top module is imported using "import a"
                ## (internally using "__import__"), because in this case,
                ## "__import__" will somehow make sub-module "a.b" accessible
                ## using "getattr(a, 'b')". However, if the top module is
                ## imported using "imp.load_module", then sub-module "a.b" is
                ## not accessible using "getattr(a, 'b')".

                #/
                file_handle = tup[0]
            finally:
                if file_handle is not None:
                    file_handle.close()

        #/
        parent_module_fullname = module_fullname
        module_file_dir_path = os.path.join(module_file_dir_path, module_file_barename)

        #/
    return module_obj

def import_module_by_path(module_path):
    """
    |module_path| should not contain ".py" extension part.
    """
    #/
    namespace_path, module_file_name = os.path.split(module_path)
#    assert os.path.isdir(namespace_path)

    #/
    if module_file_name.endswith('.py'):
        module_file_name = module_file_name[:-3]

    assert module_file_name.find('.') == -1

    #/
    module_obj = import_module_in_namespace(namespace_path, module_file_name)

    #/
    return module_obj

def find_module_attribute(attr_path, attr_sep=':'):
    """
    Deprecated.
    Use |load_module_attr| instead.
    """
    #/
    module_dot_path, sep, attr_name = attr_path.rpartition(attr_sep)

    #/
    module_obj = find_module_or_error(module_dot_path)
    ## raise error

    #/
    attr_obj = getattr(module_obj, attr_name)
    ## raise error

    #/
    return attr_obj

def find_module_attribute_by_path(attr_path, attr_sep=':'):
    """
    Deprecated.
    Use |load_module_attr| instead.
    """
    #/
    module_file_path, sep, attr_name = attr_path.rpartition(attr_sep)

    #/
    module_obj = import_module_by_path(module_file_path)
    ## raise error

    #/
    attr_obj = getattr(module_obj, attr_name)
    ## raise error

    #/
    return attr_obj

def getattr_chain(obj, attr_chain, sep='.'):
    #/
    if sep is None:
        sep = '.'

    #/
    attr_name_s = attr_chain.split(sep)

    #/
    new_obj = obj

    for attr_name in attr_name_s:
        new_obj = getattr(new_obj, attr_name)

    #/
    return new_obj

def load_module_attr(obj_uri, module_attr_sep='::', attr_chain_sep='.'):
    """
    #/ obj_uri
    e.g. |/a/b/c.py:x.y.z| or |a.b.c:x.y.z|

    #/ module_uri
    |/a/b/c.py| or |a.b.c| is the |module_uri| part.
    Can be either a file path or a namespace path.
    Whether it is a file path is determined by whether it ends with |.py|.

    #/ attr_chain
    |x.y.z| is attribute chain on the module obj to be loaded.

    #/ module_attr_sep
    If |module_attr_sep| is not present in |obj_uri|,
    consider |obj_uri| as module obj uri (i.e. without attribute chain),
    return module obj loaded.
    """
    #/
    module_uri, sep, attr_chain = obj_uri.partition(module_attr_sep)

    #/
    if module_uri.endswith('.py'):
    ## This means it is a file path, e.g. |/a/b/c.py|
        #/
        module_file_path = module_uri

        #/
        module_obj = import_module_by_path(module_file_path)
        ## raise error

    else:
    ## This means it is a namespace path, e.g. |a.b.c|
        #/
        module_namespace = module_uri

        #/
        module_obj = find_module_or_error(module_namespace)
        ## raise error

    #/
    if not attr_chain:
        return module_obj

    #/
    attr_obj = getattr_chain(
        obj=module_obj,
        attr_chain=attr_chain,
        sep=attr_chain_sep,
    )
    ## raise error

    return attr_obj
