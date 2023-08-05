 
import click
from insightful.main import insightful
from insightful.accessConfluence import accessConfluence

@click.group()
def cli():
    """Read and write insights with the sandbox.insights table."""
 
@cli.command()
@click.option('-p', '--project',
    help = 'Name of the project')
@click.option('-c', '--copy', default = None,
    help = 'Contents of the copy')
@click.option('-f', '--filename', default = None,
    help = 'Filepath containing contents of the copy')
def upload(project, copy, filename):
    """
    Insert a new piece of copy into sandbox.insights. Also send
    a slack notification.
    """
    I = insightful()
    I.upload(project, copy, filename)
    I.slackNotification()


@cli.command()
@click.option('-p', '--project',
    help = 'Name of the project')
@click.option('-n', default = -1,
    help = 'Number of the most recent insights to return. Defaults to -1, which returns all insights')
@click.option('-f', '--filename', default = None,
    help = 'Print results to this file (markdown recommended). Defaults to None, which prints to terminal')
def download(project, n, filename):
    """
    Get pieces of copy from sandbox.insights.
    """
    I = insightful()
    out = I.download(project, n)
    if filename is None:
        print(out)
    else:
        with open(filename, 'w') as f:
            for k,v in out.items():
                line = f"### {k}\n{v}\n\n"
                f.write(line)
        
        print('Printed to', filename)


@cli.command()
def listprojects():
    """
    Print all current projects in sandbox.insights.
    """
    I = insightful()
    I.listProjects()

@cli.group()
def confluence():
    """Access Confluence Cloud."""

@confluence.command()
@click.option('--limit', default = 25,
    help = 'Number of results to return')
def listpages(limit):
    """
    List pages in Confluence Cloud.
    """
    API = accessConfluence()
    out = API.listPages(limit)
    print(API.format_output(out))

@confluence.command()
@click.option('--title', default = None, type = str,
    help = 'Title of the document to download')
@click.option('--space', default = None, type = str,
    help = 'Space of the document to download')
@click.option('--id', default = None, type = str,
    help = 'id no of the document to download')
@click.option('--save/--no-save', default = False,
    help = "print to console (default) or save to local file.")
def download(title, space, id, save):
    """
    Download a page from Confluence Cloud.
    """
    API = accessConfluence()
    out = API.download(title = title, space = space, id = id)
    if save:
        API.saveAs()
    else:
        print(out)

@confluence.command()
def savetoken():
    """
    Ask for email and password and save to hidden pickle file.
    """
    API = accessConfluence()
    API.saveToken()

if __name__ == '__main__':
    cli()
