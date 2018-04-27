import requests
import datetime
import timeit
import argparse


def get_trending_repositories(top_stars, days_ago):

    date_ago = datetime.date.today() - datetime.timedelta(days_ago)
    request_params = {
        'q': '{}{}'.format('created:>', date_ago.strftime('%Y-%m-%d')),
        'sort': 'stars',
        'order': 'desc',
        'per_page': top_stars
    }
    response = requests.get(
        'https://api.github.com/search/repositories',
        params=request_params
    )
    if response.ok:
        return response.json()['items']
    else:
        return response.status_code


def get_open_issues_amount(repo):

        repo_name = repo.get('full_name')
        repo_owner = repo.get('owner').get('login')
        repo_url = repo.get('url')
        response = requests.get(
            'https://api.github.com/repos/{}/issues'.format(repo_name)
            )
        if response.ok:
            issues_count = len(response.json())
        else:
            issues_count = 'Error: {}'.format(response.status_code)
        return 'User: {0} URL: {1} Repositories: {2} Issues: {3}\n'.format(
            repo_owner,
            repo_url,
            repo_name,
            issues_count)


def handler_trend_repos(trend_repos):
    url_and_issues_repos = []

    for repo in trend_repos:
        url_and_issues_repos.append(get_open_issues_amount(repo))
    return url_and_issues_repos


def pprint_repos_data(url_and_issues_repos):

    print('')
    for idx, data_repo in enumerate(url_and_issues_repos, start=1):
        print(idx, data_repo)


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

    trend_repos = get_trending_repositories(
        arguments.top_stars,
        arguments.days_ago
        )
    if list(trend_repos) and trend_repos is not None:
        url_and_issues_repos = handler_trend_repos(trend_repos)
        pprint_repos_data(url_and_issues_repos)
    else:
        error_status = trend_repos
        print(' Problem of the request to the server: {}'.format(error_status))
    print(' Script Time: {}'.format(timeit.default_timer() - start_time))
