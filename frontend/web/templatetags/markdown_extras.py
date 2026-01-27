from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def markdown(value):
    """Converte texto Markdown básico para HTML"""
    if not value:
        return ""
    
    # Negrito **texto**
    value = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', value)
    
    # Itálico *texto*
    value = re.sub(r'\*(.*?)\*', r'<em>\1</em>', value)
    
    # Quebras de linha duplas para parágrafos
    value = value.replace('\r\n\r\n', '</p><p>')
    value = value.replace('\n\n', '</p><p>')
    
    # Quebras de linha simples para <br>
    value = value.replace('\r\n', '<br>')
    value = value.replace('\n', '<br>')
    
    # Envolver em parágrafo se não estiver vazio
    if value.strip():
        if not value.startswith('<p>'):
            value = f'<p>{value}</p>'
    
    return mark_safe(value)

@register.filter
def parse_component_name(component_str):
    """Extrai o nome do componente removendo a quantidade"""
    if not component_str:
        return ""
    if '(x' in component_str:
        return component_str.split(' (x')[0].strip()
    return component_str.strip()

@register.filter
def parse_component_quantity(component_str):
    """Extrai a quantidade do componente"""
    if not component_str:
        return "1"
    if '(x' in component_str and ')' in component_str:
        try:
            qty_part = component_str.split('(x')[1].split(')')[0]
            return qty_part
        except:
            return "1"
    return "1"