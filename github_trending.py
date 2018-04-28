import requests
import datetime
import timeit
import argparse
from collections import namedtuple


def get_response_trends_repos(top_stars, days_ago):

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


def get_response_issues_repos(repo_name):

    return requests.get(
        'https://api.github.com/repos/{}/issues'.format(repo_name))


def get_data_on_trend_repos(trend_repos):
    Data_repo = namedtuple('Data_repo', 'owner url name count')
    urls_issues_names_repos = []

    for repo in trend_repos:
        repo_owner = repo['owner']['login']
        repo_name = repo['full_name']
        repo_url = repo['url']
        response_issues = get_response_issues_repos(repo_name)
        issues_count = len(response_issues.json())
        urls_issues_names_repos.append(
            Data_repo(
                repo_owner,
                repo_url,
                repo_name,
                issues_count)
            )
    return urls_issues_names_repos


def pprint_repos_data(url_issues_names_repos):

    print()
    for index, data_repo in enumerate(url_issues_names_repos, start=1):
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
        description='This top_count and days_ago arguments for scripts'
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

    try:
        response_trends = get_response_trends_repos(
            arguments.top_stars,
            arguments.days_ago
            )
        trend_repos = response_trends.json()['items']
        urls_issues_names_repos = get_data_on_trend_repos(trend_repos)
        pprint_repos_data(urls_issues_names_repos)

    except requests.exceptions.HTTPError as error:
        print(' Requests ERROR:', error)

    print(' Script Time: {}'.format(timeit.default_timer() - start_time))
