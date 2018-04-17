from django import template

register = template.Library()


@register.filter
def column(dict,key):
    return dict,key

@register.filter
def row(dict_key,row):
    dict,column = dict_key
    string = ''
    if row in dict[column] and dict[column][row]:
        for entity in dict[column][row]:
            reagent,conc,unit = entity
            string += '<li>%s at %s %s</li>' % (reagent,conc,unit)
        return string
    else:
        return ''

register.filter('column',column)
register.filter('row',row)