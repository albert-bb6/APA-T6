"""
Módulo para la normalización de expresiones horarias en textos en castellano.

Descripción: Lee un archivo de texto, identifica las expresiones de hora
tanto en formatos digitales como coloquiales y las transforma a formato HH:MM
únicamente si son válidas según las reglas del idioma.
"""

import re


def procesar_match(match):
    """
    Función auxiliar que analiza una coincidencia de expresión horaria
    y devuelve la cadena normalizada HH:MM o la original si es inválida.
    """
    cadena_original = match.group(0)
    
    # 1. Caso Formato Estándar (HH:MM)
    if match.group('std_h') is not None:
        h = int(match.group('std_h'))
        m_str = match.group('std_m')
        
        # Validación estricta: minutos siempre deben ser de 2 dígitos
        if len(m_str) != 2:
            return cadena_original
        
        m = int(m_str)
        if 0 <= h <= 23 and 0 <= m <= 59:
            return f"{h:02d}:{m:02d}"
        return cadena_original

    # 2. Caso Formato con letras y expresiones coloquiales
    h_str = match.group('txt_h')
    h = int(h_str)
    
    m = 0
    if match.group('txt_m') is not None:
        m = int(match.group('txt_m'))
    elif match.group('en_punto'):
        m = 0
    elif match.group('y_cuarto'):
        m = 15
    elif match.group('y_media'):
        m = 30
    elif match.group('menos_cuarto'):
        m = -15

    periodo = match.group('periodo')

    if periodo:
        # Reloj con franja horaria explícita siempre está en rango 1-12
        if h < 1 or h > 12:
            return cadena_original
        
        h_mod = 0 if h == 12 else h
        
        if "mañana" in periodo and (4 <= h <= 12):
            h_final = h
        elif "mediodía" in periodo and (h == 12 or 1 <= h <= 3):
            h_final = h
        elif "tarde" in periodo and (3 <= h <= 8):
            h_final = h_mod + 12
        elif "noche" in periodo and (8 <= h <= 12 or 1 <= h <= 4):
            h_final = 0 if h == 12 else (h_mod + 12 if h >= 8 else h)
        elif "madrugada" in periodo and (1 <= h <= 6):
            h_final = h
        else:
            return cadena_original
            
    else:
        # Formatos de 12h sin periodo explícito (rango de 00:00 a 11:59)
        if match.group('en_punto') or match.group('y_cuarto') or match.group('y_media') or match.group('menos_cuarto'):
            if h < 1 or h > 12:
                return cadena_original
            h_final = 0 if h == 12 else h
        else:
            # Caso "8h27m" sin periodo (admite formato 24h directo)
            h_final = h

    if match.group('menos_cuarto'):
        m = 45
        h_final = (h_final - 1) % 24

    if 0 <= h_final <= 23 and 0 <= m <= 59:
        return f"{h_final:02d}:{m:02d}"
        
    return cadena_original


def normalizaHoras(ficText, ficNorm):
    """
    Busca expresiones horarias en ficText, las normaliza y guarda el
    resultado en ficNorm.
    """
    re_estandar = r'\b(?P<std_h>\d{1,2}):(?P<std_m>\d+)\b'
    
    re_texto = (
        r'\b(?P<txt_h>\d{1,2})\s*'
        r'(?:'
        r'h(?P<txt_m>\d+)?m?|'
        r'h\b|'
        r'(?P<en_punto>\s+en\s+punto)\b|'
        r'(?P<y_cuarto>\s+y\s+cuarto)\b|'
        r'(?P<y_media>\s+y\s+media)\b|'
        r'(?P<menos_cuarto>\s+menos\s+cuarto)\b'
        r')'
        r'(?:\s+de\s+la\s+(?P<periodo>mañana|tarde|noche|madrugada)|\s+del\s+(?P<periodo_m>mediodía))?'
    )
    
    patron_completo = re.compile(f'({re_estandar}|{re_texto})')

    with open(ficText, 'r', encoding='utf-8') as f_in, \
         open(ficNorm, 'w', encoding='utf-8') as f_out:
         
        for linea in f_in:
            linea_normalizada = patron_completo.sub(
                lambda m: procesar_match(m) if m.group('periodo') or not m.group('periodo_m') 
                else procesar_match_mediodia(m), 
                linea
            )
            f_out.write(linea_normalizada)


def procesar_match_mediodia(match):
    """
    Wrapper auxiliar para canalizar 'del mediodía' junto al grupo general de periodos.
    """
    class MatchWrapper:
        def __init__(self, original_match):
            self._m = original_match
        def group(self, name):
            if name == 'periodo' and self._m.group('periodo_m'):
                return 'mediodía'
            return self._m.group(name)
    return procesar_match(MatchWrapper(match))
