from django import template

register = template.Library()


@register.filter
def column(dict,key):
    return dict,key

@register.filter
def row(dict_key,row):
    dict,column = dict_key
    if column in dict and row in dict[column]:
        string = '<ul style="padding:0;list-style-type: none">'
        for entity in dict[column][row]:
            reagent,conc,unit = entity
            string += '<li>%s %s %s</li><hr>' % (conc,unit,reagent)
        string += '</ul>'
        return string
    else:
        return ''

@register.filter
def alphabet(value):
    return chr(value+64)

register.filter('column',column)
register.filter('row',row)