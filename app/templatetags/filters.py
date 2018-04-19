from django import template

register = template.Library()


@register.filter
def column(dict,key):
    return dict,key

@register.filter
def row(dict_key,row):
    dict,column = dict_key
    if  column in dict and row in dict[column]:
        string = '<ul style="list-style-type: none">'
        for entity in dict[column][row]:
            reagent,conc,unit = entity
            string += '<li>%s at %s %s</li><hr>' % (reagent,conc,unit)
        string += '</ul>'
        return string
    else:
        return ''

register.filter('column',column)
register.filter('row',row)