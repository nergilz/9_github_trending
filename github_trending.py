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
    request = requests.get(
        'https://api.github.com/search/repositories',
        params=request_params
    )
    if request.status_code == requests.codes.ok:
        return request.json()['items']
    else:
        return None


def get_open_issues_amount(repo_name):

        request = requests.get(
            'https://api.github.com/repos/{}/issues'.format(repo_name)
            )
        return len(request.json())


def pprint_data(request_json):

    for repo in request_json:
        repo_name = repo.get('full_name')
        repo_owner = repo.get('owner').get('login')
        repo_url = repo.get('url')
        issues_count = get_open_issues_amount(repo_name)
        print('User: {0} URL: {1} Repositories: {2} Issues: {3}\n'.format(
            repo_owner,
            repo_url,
            repo_name,
            issues_count
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

    request_json = get_trending_repositories(
        arguments.top_stars,
        arguments.days_ago
        )
    if request_json is not None:
        pprint_data(request_json)
    else:
        print(' Not data in request!')
    print(' Script Time: {}'.format(timeit.default_timer() - start_time))
