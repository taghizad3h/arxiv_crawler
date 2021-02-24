from requests_html import HTMLSession
from datetime import date, timedelta
import click

main_url = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={}&date-to_date={}&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start={}'

@click.command()
@click.option('--start_date', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()-timedelta(days=1)))
@click.option('--end_date', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()))
@click.option('--days_before', type=int, default=-1, help='If set specifies how many days should go back from end date')
def main(start_date, end_date, days_before):
    if days_before != -1:
        start_date = start_date-timedelta(days=days_before)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    print(f'crawling topics from date {start_date} to {end_date}')

    offset = 0
    all_titles = []
    all_links = []
    all_github_links = []
    while True:
        url = main_url.format(start_date, end_date, offset)
        sess = HTMLSession()
        result = sess.get(url)
        titles = result.html.find('.title.is-5.mathjax')
        titles = [t.text for t in titles]
        all_titles.extend(titles)
        links = result.html.find('p.list-title.is-inline-block > a')
        links = [l.attrs['href'] for l in links]
        all_links.extend(links)
        if len(titles) == 0:
            break
        print(f'found {len(titles)} articles in offset {offset}')
        offset += 200

    print(f'found {len(all_titles)} articles in total')
    with open(f'articles_from_{start_date}_to_{end_date}.csv', 'w', encoding='utf-8') as f:
        for t, l in zip(all_titles, all_links):
            f.write(t)
            f.write('\t')
            f.write(l)
            f.write('\n')


if __name__ == '__main__':
    main()