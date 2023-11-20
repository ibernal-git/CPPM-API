from utils.constants import *
# Construccion de filtro para la consulta a Clearpass
def get_filter(macs_array, filter_type):

  if FILTER.get(filter_type) == None:
    print("Tipo de filtro no encontrado")
    return
  macs_string = ",".join('"{0}"'.format(elem) for elem in macs_array)
  return '{"%s":[%s]}' % (FILTER[filter_type], macs_string)