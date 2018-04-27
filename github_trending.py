import requests
import datetime
import timeit
import argparse
from collections import namedtuple


def get_trending_repositories(top_stars, days_ago):

    date_ago = datetime.date.today() - datetime.timedelta(days_ago)
    request_params = {
        'q': '{}{}'.format('created:>', date_ago.strftime('%Y-%m-%d')),
        'sort': 'stars',
        'order': 'desc',
        'per_page': top_stars
    }
    return requests.get(
        'https://api.github.com/search/repositories',
        params=request_params
        )


def get_open_issues_amount(repo):

    repo_name = repo['full_name']
    repo_owner = repo['owner']['login']
    repo_url = repo['url']
    response = requests.get(
        'https://api.github.com/repos/{}/issues'.format(repo_name)
        )
    if response.ok:
        issues_count = len(response.json())
    else:
        issues_count = 'Error: {}'.format(response.status_code)
    return Data_repo(repo_owner, repo_url, repo_name, issues_count)


def get_owner_url_issues_repo(trend_repos):
    url_issues_repos = []

    for repo in trend_repos:
        url_issues_repos.append(get_open_issues_amount(repo))
    return url_issues_repos


def pprint_repos_data(url_issues_repos):

    print()
    for index, data_repo in enumerate(url_issues_repos, start=1):
        print(
            index,
            'User: {} URL: {} Repo: {} Issues: {}\n'.format(
                data_repo.owner,
                data_repo.url,
                data_repo.name,
                data_repo.count
                )
            )


def get_parser_args():

    parser = argparse.ArgumentParser(
        description='This url to repositories, top_count and days_ago arguments for scripts'
    )
    parser.add_argument(
        'top_stars',
        type=int,
        nargs='?',
        default=20,
        help='Count of top repositories'
    )
    parser.add_argument(
        'days_ago',
        type=int,
        nargs='?',
        default=7,
        help='How many days ago created repositories'
    )
    return parser.parse_args()


if __name__ == '__main__':
    arguments = get_parser_args()
    start_time = timeit.default_timer()
    Data_repo = namedtuple('Data_repo', 'owner url name count')

    response_trends = get_trending_repositories(
        arguments.top_stars,
        arguments.days_ago
        )
    if response_trends.ok and response_trends.json()['items'] is not None:
        url_and_issues_repos = get_owner_url_issues_repo(response_trends.json()['items'])
        pprint_repos_data(url_and_issues_repos)
    else:
        print(' Problem of the request to the server: {}'.format(response_trends.status_code))
    print(' Script Time: {}'.format(timeit.default_timer() - start_time))
