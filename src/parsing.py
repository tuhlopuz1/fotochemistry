import requests
from lxml import html
from bs4 import BeautifulSoup

def moreinfo(v11):

    if v11[0] == ' ':
        v11 = v11[1:len(v11)]

    if v11[-1] == ' ':
        v11 = v11[0:len(v11)-1]



    v11 = v11.replace(' ', '_')

    url = f'https://ru.wikipedia.org/wiki/{v11}'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')


    ses = requests.Session()

    log = ses.post(url, data={"search": v11})



    htc = log.text

    tree = html.fromstring(htc)

    element = tree.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/p[1]')
    if element != []:
        element = element[0]


    else:
        return 'error'

    eltt = element.text_content()

    element = tree.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/p[2]')
    if element != []:
        element = element[0]
        eltt += element.text_content()



    return eltt



def reaction(a):
    if a == 'H2O':
        return 'Вода'

    url = 'https://chemequations.com/ru/'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.text

    ses = requests.Session()

    log = ses.post(url, data={'s': a})

    htc = log.text

    tree = html.fromstring(htc)

    element = tree.xpath('/html/body/div[1]/section/div[1]/div/h1')
    if element != []:
        element = element[0]

    else:
        return 'error'

    eltt = element.text_content()

    if not '?' in eltt:
        if eltt != f'\n{a}':

            eltt = eltt.replace('(g)', '')
            eltt = eltt.replace('(l)', '')
            eltt = eltt.replace('(al)', '')
            eltt = eltt.replace('(aq)', '')
            eltt = eltt.replace('(s)', '')
            return eltt

        else:
            element = tree.xpath('/html/body/div[1]/section/div[1]/div/ul/li[1]/em')
            if element != []:
                element = element[0]
            else:
                return 'error'
            eltt = element.text_content()
            eltt = eltt.replace('(g)', '')
            eltt = eltt.replace('(l)', '')
            eltt = eltt.replace('(al)', '')
            eltt = eltt.replace('(aq)', '')
            eltt = eltt.replace('(s)', '')
            return eltt
    else:
        if '?' in eltt:
            element = tree.xpath(
                '/html/body/div[1]/section/div[1]/div/table/tbody/tr[1]/td[2]/a')[0]

            eltt = element.text_content()
            eltt = eltt.replace('(g)', '')
            eltt = eltt.replace('(l)', '')
            eltt = eltt.replace('(al)', '')
            eltt = eltt.replace('(aq)', '')
            eltt = eltt.replace('(s)', '')

            return eltt