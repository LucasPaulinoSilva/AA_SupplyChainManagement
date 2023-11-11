import config
import httpx
from bs4 import BeautifulSoup


def count_item_occurrences():
    # Obtem o html da página do formulário dos pedidos
    response = httpx.get(config.LINK_FORMS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Verifica a quantidades de vezes que o item foi encontrado na página
        occurrences = str(soup).count('PONumber')
        print(f'Total itens encontrados: {occurrences}')
        return occurrences

    else:
        raise Exception(
            f'Erro no get do URL: {config.LINK_FORMS}. Status code: {response.status_code}')


if __name__ == '__main__':
    count_item_occurrences()
