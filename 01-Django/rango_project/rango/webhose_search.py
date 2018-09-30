import json
import urllib.parse  # Py3
import urllib.request  # Py3

def read_webhose_key():

    webhose_api_key = None

    try:
        with open('search.key', 'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, size=10):
    """
    Given a string containing search terms (query), and a number of results to return (default of 10),
    returns a list of results from the Webhose API, with each result consisting of a title, link and summary.
    """
    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    # What's the base URL for the Webhose API?
    root_url = 'http://webhose.io/search'

    # Format the query string - escape special characters.
    query_string = urllib.parse.quote(search_terms)  # Py3

    # Use string formatting to construct the complete API URL.
    search_url = '{root_url}?token={key}&format=json&q={query}&sort=relevancy&size={size}'.format(
                    root_url=root_url,
                    key=webhose_api_key,
                    query=query_string,
                    size=size)

    results = []

    try:
        # Connect to the Webhose API, and convert the response to a Python dictionary.
        response = urllib.request.urlopen(search_url).read().decode('utf-8')  #Py3 (library, decode)
        json_response = json.loads(response)

        # Loop through the posts, appendng each to the results list as a dictionary.
        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link': post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    # Return the list of results to the calling function.
    return results