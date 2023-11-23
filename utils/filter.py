from utils.constants import *


def get_filter(macs_array, filter_type, optional_filter=None):
    filter_mapping = {
        LOCAL_USERS: '{"%s":[%s]}'
        % (FILTER[LOCAL_USERS], ",".join('"{0}"'.format(elem) for elem in macs_array)),
        ENDPOINTS: '{"%s":[%s]}'
        % (FILTER[ENDPOINTS], ",".join('"{0}"'.format(elem) for elem in macs_array)),
        ENDPOINTS_ROLE: '{"%s":[%s]}'
        % (FILTER[ENDPOINTS], ",".join('"{0}"'.format(elem) for elem in macs_array)),
        NAS_SESSION: '{"acctstoptime":{"$exists": false},"nasipaddress":"%s"}'
        % optional_filter,
        ACTIVE_SESSION: '{"acctstoptime":{"$exists": false}, "%s":[%s]}'
        % (FILTER[ENDPOINTS], ",".join('"{0}"'.format(elem) for elem in macs_array)),
    }

    try:
        return filter_mapping[filter_type]
    except KeyError:
        raise ValueError(f"Tipo de filtro no encontrado: {filter_type}")
