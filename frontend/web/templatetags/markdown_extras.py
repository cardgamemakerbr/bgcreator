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