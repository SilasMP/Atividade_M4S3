from requests_html import HTMLSession
import time
import sqlite3

def raspagemOlx():
    sessao = HTMLSession()
    url = 'https://www.olx.com.br/celulares/estado-sp/sao-paulo-e-regiao?q=iphone'
    resposta = sessao.get(url)

    anuncios = []
    links = resposta.html.find('#ad-list li a')
    time.sleep(1)
    for link in links:
        
        url_iphone = link.attrs['href']
        resposta_iphone = sessao.get(url_iphone)
        titulo = resposta_iphone.html.find('h1', first=True).text
        preco = resposta_iphone.html.find('[data-testid="ad-price-wrapper"] span', first=True).text

        anuncios.append({
            'url': url_iphone,
            'titulo': titulo,
            'preco': int(preco.replace('R$','').replace('.',''))
        })
    print('Dados Coletados com sucesso!' if len(anuncios)>0 else 'Ocorreu um erro')
    salvandoDadosNoBd(anuncios)

def salvandoDadosNoBd(dados):
    conn = sqlite3.connect('anuncios.sqlite3')
    cursor = conn.cursor()
    sql = '''
        INSERT INTO anuncios (url, titulo, preco)
        VALUES (?, ?, ?)
    '''
    for anuncio in dados:
        valores = [anuncio['url'], anuncio['titulo'], anuncio['preco']]
        print(valores)
        cursor.execute(sql, valores)
    
    conn.commit()
    conn.close()
    print('Dados Salvos no Banco de Dados')

if __name__ == '__main__':
    raspagemOlx()