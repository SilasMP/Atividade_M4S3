from requests_html import HTMLSession
import time
import sqlite3

def raspagemOlx():
    sessao = HTMLSession()
    url = 'https://www.olx.com.br/eletronicos-e-celulares/estado-sp?q=iphone'
    resposta = sessao.get(url)

    anuncios = []
    links = resposta.html.find('a[class="sc-dJjYzT dOvWTZ"]')
    time.sleep(1)
    for link in links:
        
        url_iphone = link.attrs['href']        
        resposta_iphone = sessao.get(url_iphone)
        titulo = resposta_iphone.html.find('h1', first=True).text
        preco = resposta_iphone.html.find('span[class="ad__sc-1wimjbb-1 hoHpcC sc-bZQynM hYqmow"]', first=True).text
        publicacao = resposta_iphone.html.find('span[class="ad__sc-1oq8jzc-0 dWayMW sc-bZQynM FSvbY"]', first=True).text
        
        if preco != 0 and preco !='':
            anuncios.append({
                'url': url_iphone,
                'titulo': titulo,
                'preco': int(preco.replace('R$','').replace('.','')),
                'publicacao': publicacao
            })
    print('Dados Coletados com sucesso!' if len(anuncios)>0 else 'Ocorreu um erro')
    print(anuncios)
    salvandoDadosNoBd(anuncios)

def salvandoDadosNoBd(dados):
    conn = sqlite3.connect('anuncios.sqlite3')
    cursor = conn.cursor()
    sql = '''
        INSERT INTO anuncios (url, titulo, preco, publicacao)
        VALUES (?, ?, ?, ?)
    '''
    for anuncio in dados:
        valores = [anuncio['url'], anuncio['titulo'], anuncio['preco'], anuncio['publicacao']]
        print(valores)
        cursor.execute(sql, valores)
    
    conn.commit()
    conn.close()
    print('Dados Salvos no Banco de Dados')

if __name__ == '__main__':
    raspagemOlx()