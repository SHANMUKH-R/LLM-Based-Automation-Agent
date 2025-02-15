import requests
from bs4 import BeautifulSoup
url = 'https://pypi.org/simple/'

def getpackages(url):
    responce = requests.get(url)
    if responce.status_code == 200:
        soup = BeautifulSoup(responce.text,"html.parser")
        packages = [a.text.strip() for a in soup.find_all('a')]
        with open("packages.txt","w+") as file:
            for pkg in packages:
                file.write(str(pkg)+" ")
            file.close()
    else:
        print("We cant fetch the right url")

getpackages(url)