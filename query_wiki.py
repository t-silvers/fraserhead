from atlassian import Confluence
from bs4 import BeautifulSoup


confluence = Confluence(
    url='https://medwiki.stanford.edu/display/fraserlab/Fraser+Lab+Home',
    username='tsilvers',
    password=password)

page_id=117932093

soup = BeautifulSoup(confluence.get_page_by_id(page_id, expand=None))
print(soup.get_text())

# confluence.history(page_id)
