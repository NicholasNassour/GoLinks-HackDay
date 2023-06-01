import requests
from collections import Counter
import json

'''If a user has more than 1000 repos there will be an error if trying to search > 1000
would like to add some way to test when it's gone over 1000 repos and possibly wait
5-10 seconds before continuing to the next 1000'''

username = "seantomburke"
access_token = 'import_access_token_here'
url = f'https://api.github.com/users/{username}/repos'


headers = {
    "Authorization": f"Bearer {access_token}",
    'Accept': 'application/vnd.github+json'
}

params = {
    "per_page": 100,
    # If user has > 100 pages, increment to next page
    "page": 1,
    "fork": True
}

repo_count = 0
stargazer_count = 0
total_forks = 0
repo_size = 0
language_counter = Counter()

response = requests.get(url, params=params, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    repositories = response.json()

    # Iterate over the repositories and retrieve stargazers count
    for repo in repositories:

        if not params['fork'] and repo['forks_count'] != 0:
            continue

        language = repo['language']

        if language is not None:
            language_counter[language] += 1
        
        sorted_languages = sorted(language_counter.items(), key=lambda x: x[1], reverse=True)
        
        # Calculating total_forks, stargazers, repository size, and total repo_count
        total_forks += repo["forks_count"]
        stargazer_count += repo['stargazers_count']
        repo_size += repo["size"]
        repo_count += 1

    
    # Calculate average repo size
    average_size = repo_size / repo_count

    # Convert average size to appropriate units (KB, MB, or GB)
    if average_size < 1024:
        size_unit = "KB"
    elif average_size < 1024 * 1024:
        average_size /= 1024
        size_unit = "MB"
    else:
        average_size /= 1024 * 1024
        size_unit = "GB"
    
    

    response_data = {
    "public_repositories_count": repo_count,
    "total_stargazers": stargazer_count,
    "total_forks": total_forks,
    "average_repository_size": f"{average_size:.2f} {size_unit}",
    "used_languages": sorted_languages
    }
        
    # Convert the dictionary to JSON
    response_json = json.dumps(response_data)

    # Print the JSON response
    print(response_json)
elif response.status_code == 304:
    print(f'''Failed to retrieve repositories. The requested resource has not been modified since the last request. This is typically used for caching purposes. Status code: {response.status_code}''')
elif response.status_code == 404:
    print(f'''Failed to retrieve repositories. The page you requested was not found. Please update the url to a valid address. Status code: {response.status_code}''')
elif response.status_code == 422:
     print(f'''Failed to retrieve repositories. The request was well-formed but contains semantic errors or failed validation. Status code: {response.status_code}''')
elif response.status_code == 503:
     print(f'''Failed to retrieve repositories. The server is currently unable to handle the request due to temporary overloading or maintenance. Status code: {response.status_code}''')
else:
    print(f'''Failed to retrieve repositories. An unexpected error occurred. Status code: {response.status_code}''')