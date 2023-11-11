from playwright.sync_api import sync_playwright
import config
import pandas as pd
import launch_orders
import occurrences_orders


def orders_process():
    # Concatena caminho do arquivo excel
    path_file_xlsx = config.FOLDER_FILE_XLSX + config.NAME_FILE_XLSX

    # Abre o arquivo excel na primeira aba
    df = pd.read_excel(path_file_xlsx, sheet_name='Sheet1')

    with sync_playwright() as p:
        # Abre página do formulário no edge
        browser = p.chromium.launch(channel='msedge', headless=False)
        page = browser.new_page()
        page.goto(config.LINK_FORMS)

        # Abre página da tabela com os dados no edge
        page2 = browser.new_page()
        page2.goto(config.LINK_PROCUREMENT)

        # Digita login e senha no site da tabela
        page2.locator('#inputEmail').fill(config.NAME_USER)
        page2.locator('#inputPassword').fill(config.PASSWORD_USER)

        # Aguarda até que apareça o botão do cookie e realiza o click
        elementCookie = page2.wait_for_selector(
            '#onetrust-accept-btn-handler', timeout=5000)
        try:
            page2.locator('#onetrust-accept-btn-handler').click()
        except:
            print("Botão de cookie não existe")

        # Clica no botão para logar
        page2.locator('button.btn-primary').click()

        # Pega o retorno de quantas ordens de pedidos foi encontrada na página do formulário
        occurrences = occurrences_orders.count_item_occurrences()

        # Itera o loop sobre a quantidade de ordens de pedidos encontradas
        numberOrder = 1
        while numberOrder <= int(occurrences):

            # Captura o número de Ordem do pedido na página do formulário
            fild_numberOrder = page.input_value(
                f'#PONumber{numberOrder}')

            # Preenche o campo de pesquisar o número da ordem de pedido na página da tabela
            page2.locator('#dtBasicExample_filter > label > input[type=search]').fill(
                fild_numberOrder)

            # Captura os valores das colunas: Ship Date, Ordert Total e State
            shipDate = page2.locator(
                '#dtBasicExample > tbody > tr > td:nth-child(7)').text_content()

            orderTotal = page2.locator(
                '#dtBasicExample > tbody > tr > td:nth-child(8)').text_content()
            orderTotal = orderTotal.replace('$', '').replace(' ', '')

            state = page2.locator(
                '#dtBasicExample > tbody > tr > td:nth-child(5)').text_content()

            # Encontre a posição da célula onde o valor está localizado na coluna A
            posicao = df[df['State'] == state].index
            linha = posicao[0]

            # Pega o nome da pessoa que fez o pedido na coluna B "Full Name"
            fullName = df.loc[linha, 'Full Name']

            # Preenche os valores nos campos correspondentes na página do formulário
            page.locator(f'#shipDate{numberOrder}').fill(shipDate)

            page.locator(f'#orderTotal{numberOrder}').fill(orderTotal)

            page.select_option(f'#agent{numberOrder}', value=fullName)

            # incremente no contador
            numberOrder += 1

        # Clica no botão "Submit" na página do formulário para enviar todas as ordens preenchidas
        page.locator('#submitbutton').click()

        input('STOP para poder ver o resultado. Pressione qualquer tecla para finalizar.')


if __name__ == '__main__':
    occurrences_orders.count_item_occurrences()
    launch_orders.orders_process()
