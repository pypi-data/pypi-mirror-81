
import requests
import json
import pickle
import re
from getpass import getpass
from bs4 import BeautifulSoup
import html2markdown


class accessConfluence:
    """
    Facilitate Access to Confluence Cloud via their REST API. 
    """
    def __init__(self):
        """
        Set the URL and load API token from .token; if .token not found
        give the option to run saveToken().
        """

        self.url = "https://tarifica-telefonica.atlassian.net/wiki/rest/api/content"

        #recursive question, loops if answer is not in {y,n}
        def question():
            answer = input("Would you like to save your Confluence Cloud API token now? [y/n] ")
            if answer == 'y':
                self.saveToken()
            elif answer == 'n':
                print('No problem! Run `insightful confluence savetoken` when you are ready.')
            else:
                print('Answer must be one of {y,n} !')
                question()

        # if file exists open it, otherwise ask to save
        try:
            with open('.token', 'rb') as pfile:
                self.auth = pickle.load(pfile)
        except FileNotFoundError:
            print('Error: .token not found')
            question()
            

    def saveToken(self):
        """
        In terminal, Python will ask for your email and Confluence Cloud API token
        and save them to .token as a tuple.
        """
        with open('.token', 'wb') as pfile:
            email = input("Enter the email associated with your Atlassian cccount: ")
            token = getpass("Enter your Atlassian API token: ")
            auth = (email, token)
            pickle.dump(auth, pfile)
            print('Saved to .token')

            self.auth = auth

    def format_output(self, x):
        """
        Format python dictionary for pretty JSON-style printing.

        Args:
            x (dict): A dictionary

        Returns:
            str: Nicely formatted dictionary
        """
        return json.dumps(x, sort_keys=True, indent=4, separators=(",", " : "))

    def listPages(self, limit = 25):
        """
        Print and assign to self.pages a list of pages in Confluence Cloud.
        Output has the format:
        {
            PROJECT 0: {
                {ID 0: TITLE 0},
                ...,
                {ID N: TITLE N},
            },
            ...,
            PROJECT N: {
                {ID 0: TITLE 0},
                ...,
                {ID N: TITLE N},
            }
        }

        Args:
            limit (int, optional): Number of pages to return. Defaults to 25.

        Returns:
            dict: dictionary defined above.

        Raises:
            Exception: Raise error if the API reponse code is not 200.
        """
        headers = {
            "Accept": "application/json"
        }

        payload = {
            'expand': 'space',
            'limit': limit
        }

        response = requests.get(
            self.url,
            headers=headers,
            params=payload,
            auth=self.auth
        )
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        results = json.loads(response.text)['results']

        out = {}
        for r in results:
            id = r['id']
            title = r['title']
            space = r["space"]['name']
            if space not in out.keys():
                out[space] = {}
            
            out[space][id] = title

        self.pages = out
        return out

    def download(self, title = None, space = None, id = None):
        """
        Download page from Confluence Cloud.

        Args:
            title (str, optional): Page title. Defaults to None.
            space (str, optional): Page space. Defaults to None.
            id ([type], optional): Page id. Defaults to None.

        Raises:
            ValueError: At least one of <title>, <space>, or <id> must
            not be None.
            Exception: If API response code is not 200.

        Returns:
            str: Body of page, with line breaks.
        """
        if all(x is None for x in [space, title, id]):
            raise ValueError("Error: one of title, space, id must not be None")

        headers = {
            "Accept": "application/json"
        }

        payload = {
            'expand': 'body.storage'
        }
        if space is not None:
            payload['space'] = space
        if id is not None:
            payload['id'] = id
        if title is not None:
            payload['title'] = title

        response = requests.get(
            self.url,
            headers=headers,
            params=payload,
            auth=self.auth
        )
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        result = json.loads(response.text)['results'][0]
        html = result['body']['storage']['value']
        soup = BeautifulSoup(html, features="lxml")
        text = soup.get_text('\n')

        self.title = title
        self.html = html
        self.text = text

        return text

    def saveAs(self, type = 'md'):
        """
        Save downloaded page to local file.

        Args:
            type (str, optional): File extension, one of {md, html, txt}. Defaults to 'md'.

        Raises:
            ValueError: Raise if type file extension is not supported.
        """
        if type == 'md':
            content = html2markdown.convert(self.html)
        elif type == 'html':
            content = self.html
        elif type == 'txt':
            content = self.text
        else:
            raise ValueError('Error: type must be one of {md, html, txt}')

        filename = re.sub(' ', '_', f'{self.title}.{type}')
        with open(filename, 'w') as f:
            f.write(content)

        print('Saved content to', filename)


if __name__ == '__main__':
    API = accessConfluence()
    # API.listPages()
    out = API.download(id = '241893377')
    print(out)




