
from insightful.connection import get_mysql_conn, DATABASE, send_webhook
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import time
import markdown
from bs4 import BeautifulSoup
import docx

class insightful:
    """
    Read and write insights with the sandbox.insights table.
    """
    def __init__(self):
        """
        Setup the mysql connection and queries.
        """
        self.mysql_conn = get_mysql_conn(DATABASE)

    def _upload(self, project, copy):
        """
        Insert a new piece of copy into sandbox.insights.

        Args:
            project (str): Name of the project, maximum 255 characters
            insight (str): The copy, maximum 10000 characters
        """
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query_write = "INSERT INTO sandbox.insights (date, project, copy) VALUES ('{}', '{}', '{}');"
        query = query_write.format(now, project, copy)
        print(query)

        try:
            self.mysql_conn.execute(query)
            print('Row inserted into sandbox.insights')
        except SQLAlchemyError as e:
            print(e)

    def download(self, project, n = -1):
        """
        Get pieces of copy from sandbox.insights.

        Args:
            project (str): Name of the project
            n (int, optional): Number of the most recent insights to return.
                Defaults to -1, which returns all insights.

        Returns:
            dict: Dictionary with str(datetime) as keys and copy as values.
        """
        
        n = 9999 if n == -1 else n
        query_read = "SELECT date, copy FROM sandbox.insights WHERE project = '{}' ORDER BY 1 DESC LIMIT {};"
        query = query_read.format(project, n)
        print(query)

        try:
            results = self.mysql_conn.execute(query).fetchall()
            results = {str(k):v for k,v in results}
            print(f"\nLoaded {len(results)} row(s) from sandbox.insights")
        except SQLAlchemyError as e:
            print(e)

        return results

    def readText(self, filename):
        """
        Read text from filename.

        Args:
            filename (str): filepath of the file to read. Must be one of {.txt, .md, .docx, .doc}

        Returns:
            str: Text from filename
        """
        extension = os.path.splitext(filename)[1]

        if extension == '.txt':
            text = open(filename, 'r').readlines()
            text = "".join(text)
        elif extension == '.md':
            html = markdown.markdown(open(filename, 'r').read())
            text = BeautifulSoup(html, features="lxml").findAll(text=True)
            text = "".join(text)
        elif extension in ('.doc', '.docx'):
            doc = docx.Document(filename)
            text = [para.text for para in doc.paragraphs]
            text = "\n".join(text)
        else:
            raise ValueError(f'{extension} not recognized')

        return text

    def upload(self, project, copy = None, filename = None):
        """
        Wrapper arround _insertRow to handle files as well as strings for copy content.
        Specify just one of copy and filename; if both are specified then filename takes
        priority.

        Args:
            project (str): Name of the project, maximum 255 characters
            copy (str, optional): The copy, maxiumum 10000 characters. Defaults to None.
            filename (str, optional): The filename containing the copy, must a text file,
                markdown file, or word document. Defaults to None.

        Raises:
            ValuError: copy and filename cannot both be None, will raise an error if so.
        """

        self.project = project

        if copy is None and filename is None:
            raise ValuError('one of copy and filename must not be None')
        elif filename is not None:
            copy = self.readText(filename)
        else:
            pass

        # split copy that is too long
        copy_length = len(copy)
        if copy_length <= 10000:
            self._upload(project, copy)
        else:
            N = 9990 #chunk size leaving room for prefix ordering
            chunks = (-copy_length//N)*-1 # ceiling division
            for i in range(chunks, 0, -1): #backwards range
                copy_chunk = f"[{i+1}/{chunks}]\n" + copy[i*N:(i+1)*N] # add prefix with order
                self._upload(project, copy_chunk)
                time.sleep(1) # sleep so the copy is ordered properly

    def listProjects(self):
        """
        Prints a list of all projects in sandbox.insights
        """
        try:
            query = "select distinct project from sandbox.insights order by 1;"
            results = self.mysql_conn.execute(query).fetchall()
            print(f"\nThere are currently {len(results)} projects:")
            for i, r in enumerate(results):
                print(f"{i+1}. {r[0]}")
        except SQLAlchemyError as e:
            print(e)

    def slackNotification(self):
        """
        Sends a slack message to #insightful in Avengers-Priscilla, letting
        us know which project was just updated. Reads project from the upload()
        method.
        """
        message = f"Project: {self.project} updated."
        send_webhook(message)


if __name__ == '__main__':
    # I = insightful()
    # I.listProjects()
    # I.insertRow('setup', copy = 'and another one')
    # out = I.getRows('testing')
    # print(out)

    # I.readText('textfile.txt')
    # I.readText('markdown.md')
    # I.readText('worddoc.docx')
    # I.insertRow('testing', filename = 'textfile.txt')
    pass