from click import *
import requests

@command()
@argument('commit')
def get_email(commit):
    echo(get_email_using_commit(commit))

def get_email_using_commit(commit):
    url = f"{commit}.patch"
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        return html
    else:
        return ("Erreur :", response.status_code)

if __name__ == "__main__":
    get_email()