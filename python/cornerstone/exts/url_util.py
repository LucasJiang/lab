# coding: utf-8
import os
from urllib import urlencode
from urlparse import parse_qs
from urlparse import parse_qsl
from urlparse import urlsplit
from urlparse import urlunsplit

def url_parse(url,
    protocol_default='http',
    default=None,
    port_default=None,
    path_default=None,
    ):
    """
    ::guess_port:: if the "server" portion of the url does not include a port
     number, then guess a default port number according to the protocol. That
     means protocol "http" will get 80 and "https" will get 443. If set to
     False, then port is set to None.
    """
    #/
    protocol, server, path, query, fragment = urlsplit(url)

    #/ decide protocol
    if not protocol:
        if protocol_default:
            protocol = protocol_default
        else:
            raise ValueError(url, -1, 'No protocol in the url and no default protocol specified.')

    assert protocol

    #/ decide server
    if not server:
        if default:
            server = default
        else:
            raise ValueError(url, -2, 'No server in the url and no default server specified.')

    assert server

    #/ decide host and port
    if ':' in server:
        host, port = server.split(':')
        port = int(port)
    else:
        host = server
        port = port_default
        if port == -1:
        ## -1 means to guess port number according to protocol
            if protocol == 'http':
                port = 80
            elif protocol == 'https':
                port = 443
            else:
                assert False

    assert port is None or isinstance(port, int), port
    
    #/ decide path
    if not path:
        if path_default:
            path = path_default
        else:
            raise ValueError(url, -3, 'No path in the url and no default path specified.')

    #/ decide path2, i.e. path + query
    path2 = path
    if query:
        path2 = path2 + '?' + query

    #/ decide path3, i.e. path + query + fragment
    path3 = path2
    if fragment:
        path3 = path2 + '#' + fragment

    #/
    return protocol, server, host, port, path, query, fragment, path2, path3

def url_get_protocol(url):
    protocol, server, path, query, fragment = urlsplit(url)
    return protocol

def url_update_protocol(url, protocol):
    old_protocol, server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, query, fragment))
    return new_url

def url_get_server(url):
    protocol, server, path, query, fragment = urlsplit(url)
    return server

def url_get_server_url(url):
    protocol, server, path, query, fragment = urlsplit(url)
    return urlunsplit((protocol, server, '', '', ''))

def url_update_server(url, server):
    protocol, old_server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, query, fragment))
    return new_url

def url_get_path(url):
    protocol, server, path, query, fragment = urlsplit(url)
    return path

def url_get_path_trunk(url):
    protocol, server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, None, None))
    return new_url

def url_update_path(url, path):
    protocol, server, old_path, query, fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, query, fragment))
    return new_url

def url_get_path2(url):
    """
    path2 means path + query
    """
    protocol, server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit(('', '', path, query, ''))
    return new_url

def url_get_path2_trunk(url):
    protocol, server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, query, None))
    return new_url

def url_get_path3(url):
    """
    path3 means path + query + fragment
    """
    protocol, server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit(('', '', path, query, fragment))
    return new_url

def url_get_parent_url(url):
    protocol, server, path, query, fragment = urlsplit(url)
    parent_path = os.path.dirname(path)
    return '{}://{}{}'.format(protocol, server,
        parent_path if parent_path != '/' else '')

def url_get_query(url):
    protocol, server, path, query, fragment = urlsplit(url)
    return query

def url_get_query_dict(url):
    protocol, server, path, query, fragment = urlsplit(url)
    query_dict = dict(parse_qsl(query))
    return query_dict

def url_has_query_item(url, item_key):
    protocol, server, path, query, fragment = urlsplit(url)
    return query_has_item(query, item_key)

def url_get_query_item(url, item_key, default=None):
    protocol, server, path, query, fragment = urlsplit(url)
    return query_get_item(query, item_key, default)

def url_get_query_item0(url, item_key, default=None):
    protocol, server, path, query, fragment = urlsplit(url)
    return query_get_item0(query, item_key, default)

def url_update_query(url, query):
    protocol, server, path, old_query, fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, query, fragment))
    return new_url

def url_update_query_item(url, item, add=False):
    protocol, server, path, query, fragment = urlsplit(url)
    new_query = query_update_item(query, item, add=add)
    new_url = urlunsplit((protocol, server, path, new_query, fragment))
    return new_url

def url_remove_query_item(url, item_key):
    protocol, server, path, query, fragment = urlsplit(url)
    new_query = query_remove_item(query, item_key)
    new_url = urlunsplit((protocol, server, path, new_query, fragment))
    return new_url

def url_remove_query_items(url, item_keys):
    protocol, server, path, query, fragment = urlsplit(url)
    new_query = query_remove_items(query, item_keys)
    new_url = urlunsplit((protocol, server, path, new_query, fragment))
    return new_url

def url_remove_query_items_by_filter(url, filter):
    protocol, server, path, query, fragment = urlsplit(url)
    new_query = query_remove_items_by_filter(query, filter)
    new_url = urlunsplit((protocol, server, path, new_query, fragment))
    return new_url

def url_sort_query(url, key=None, reverse=False):
    protocol, server, path, query, fragment = urlsplit(url)
    new_query = query_sort(query)
    new_url = urlunsplit((protocol, server, path, new_query, fragment))
    return new_url

def url_get_fragment(url):
    protocol, server, path, query, fragment = urlsplit(url)
    return fragment

def url_update_fragment(url, fragment):
    protocol, server, path, query, old_fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, query, fragment))
    return new_url

def url_to_absolute_url(url, server_url, parent_url):
    if url.find(':/') != -1:
        absolute_url = url
    else:
        if url.startswith('/'):
            absolute_path = url
            absolute_url = server_url + absolute_path
        else:
            relative_path = url
            absolute_url = parent_url + '/' + relative_path

    return absolute_url

def url_append_query_item(url, item):
    protocol, server, path, query, fragment = urlsplit(url)
    new_query = query_append_item(query, item)
    new_url = urlunsplit((protocol, server, path, new_query, fragment))
    return new_url

def url_change_protocol(url, protocol):
    protocol_old, server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit((protocol, server, path, query, fragment))
    return new_url

def url_change_protocol_and_port(url, protocol, port):
    port_text = str(port)

    protocol_old, server_old, path, query, fragment = urlsplit(url)

    server, sep, port_old = server_old.partition(':')

    if not (
        port is None \
        or (protocol == 'http' and port_text == '80') \
        or (protocol == 'https' and port_text == '443')
    ):
        server += ':' + port_text
    
    new_url = urlunsplit((protocol, server, path, query, fragment))
    
    return new_url

def url_remove_protocol_and_server(url):
    protocol, server, path, query, fragment = urlsplit(url)
    new_url = urlunsplit(('', '', path, query, fragment))
    return new_url

def url_remove_query_and_fragment(url):
    protocol, server, path, query, fragment = urlsplit(url)
    return urlunsplit((protocol, server, path, '', ''))

def query_has_item(query, item_key):
    query_items_d = parse_qs(query)
    return item_key in query_items_d

def query_get_item(query, item_key, default=None):
    query_items_d = parse_qs(query)
    return query_items_d.get(item_key, default)

def query_get_item0(query, item_key, default=None):
    query_items_d = parse_qs(query)
    if item_key in query_items_d:
        return query_items_d[item_key][0]
    else:
        return default

def query_append_item(query, item):
    new_query_portion = urlencode([item])
    if query == '':
        new_query = new_query_portion
    else:
        new_query = query + '&' + new_query_portion
    return new_query

def query_remove_item(query, item_key):
    query_item_s = parse_qsl(query)
    new_query_item_s = []
    for query_item in query_item_s:
        if query_item[0] == item_key:
            continue
        else:
            new_query_item_s.append(query_item)
    new_query = urlencode(new_query_item_s)
    return new_query

def query_remove_items(query, item_keys):
    query_item_s = parse_qsl(query)
    new_query_item_s = []
    for query_item in query_item_s:
        if query_item[0] in item_keys:
            continue
        else:
            new_query_item_s.append(query_item)
    new_query = urlencode(new_query_item_s)
    return new_query

def query_remove_items_by_filter(query, filter):
    query_item_s = parse_qsl(query)
    new_query_item_s = []
    for query_item in query_item_s:
        if filter(query_item):
            continue
        else:
            new_query_item_s.append(query_item)
    new_query = urlencode(new_query_item_s)
    return new_query

def query_update_item(query, item, add=False):
    #/
    query_item_s = parse_qsl(query)
    #/
    new_query_item_s = []
    has_replaced = False
    for query_item in query_item_s:
        if query_item[0] == item[0]:
            new_query_item_s.append(item)
            has_replaced = True
        else:
            new_query_item_s.append(query_item)
    #/
    if not has_replaced and add:
        new_query_item_s.append(item)
    #/
    new_query = urlencode(new_query_item_s)
    #/
    return new_query

def query_sort(query, key=None, reverse=False):
    query_item_s = parse_qsl(query)
    query_item_s_sorted = sorted(query_item_s,
        key=key if key is not None else lambda x:x[0],
        reverse=reverse
    )
    new_query = urlencode(query_item_s_sorted)
    return new_query

def make_qs(params, flaten=False, exclude=None):
    """
    params is a dict
    """
    #/
    if not params:
        return ''

    #/
    if flaten:
        if exclude:
            params = dict(((x[0], x[1][0]) for x in params.iteritems() if x[0] not in exclude))
        else:
            params = dict(((x[0], x[1][0]) for x in params.iteritems()))
    else:
        if exclude:
            params = dict(((x[0], x[1]) for x in params.iteritems() if x[0] not in exclude))
        
    #/
    qs = urlencode(params)

    #/
    return qs
