import math
from django.core.paginator import Paginator

def make_pagination_range(
        range_pagina,
        qtde_paginas,
        pagina_atual
):
    range_meio = math.ceil(qtde_paginas/2)
    range_inicial = pagina_atual - range_meio
    range_final = pagina_atual + range_meio
    total_paginas = len(range_pagina)
    range_inicial_offset = abs(range_inicial) if range_inicial<0 else 0

    if range_inicial<0:
        range_inicial = 0
        range_final += range_inicial_offset

    if range_final>=total_paginas:
        range_inicial = range_inicial + abs(total_paginas - range_final)

    paginacao = range_pagina[range_inicial:range_final]

    return{
        'paginacao': paginacao,
        'range_pagina': range_pagina,
        'qtde_paginas': qtde_paginas,
        'pagina_atual': pagina_atual,
        'total_paginas': total_paginas,
        'range_inicial': range_inicial,
        'range_final': range_final,
        'primeira_pagina_fora_do_range': pagina_atual>range_meio,
        'ultima_pagina_fora_do_range': range_final<total_paginas
    }

def make_pagination(request, query_photos, items_per_page, qtde_page = 4):
    #print(f'QUANTIDADE DE FOTOS: {items_per_page}')
    try:
        pagina_atual = int(request.GET.get('page',1))
    except ValueError:
        pagina_atual = 1

    paginador = Paginator(query_photos, items_per_page)
    pagina_objeto = paginador.get_page(pagina_atual)
    range_paginacao = make_pagination_range(
        paginador.page_range,
        qtde_page,
        pagina_atual,
    )
    return pagina_objeto, range_paginacao