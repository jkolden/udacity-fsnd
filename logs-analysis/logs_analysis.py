import datetime
import psycopg2

# The view holds articles' paths and their PV
# in descending order of PV.
# Used to create another `view most_viewed_articles`.
query_initialize_view_most_viewed_paths = """
create or replace view most_viewed_paths as
    select path, count(*) as pv
        from log
        group by path
        order by pv desc
"""

# The view holds articles' title, author's ID and PV
# in descending order of PV.
# Used to generate the 1st and 2nd report.
query_initialize_view_most_viewed_articles = """
create or replace view most_viewed_articles as
    select title, author as author_id, pv
        from articles, most_viewed_paths
        where concat('/article/', articles.slug) = most_viewed_paths.path
        order by pv desc;
"""

# The view holds daily percentages of error (404) rate
# in the order of date.
# Used to generate the 3rd report.
query_initialize_view_daily_error_rates = """
create or replace view daily_error_rates as
    select date_trunc('day', time) as date,
    100.0 * count(case
                      when status = '404 NOT FOUND' then 1
                  end) / count(*) as error_rate
        from log
        group by date
        order by date;
"""

query_select_three_most_viewed_articles = """
select title, pv
    from most_viewed_articles
    limit 3;
"""

query_select_most_viewed_authors = """
select name, sum(pv) as authors_total_pv from authors, most_viewed_articles
    where authors.id = most_viewed_articles.author_id
    group by name
    order by authors_total_pv desc;
"""

query_select_daily_error_rate_more_than_one_percent = """
select *
    from daily_error_rates
    where error_rate > 1.0
    order by date;
"""


# Create views.
# If they already exist, replace them with the latest ones.
def initialize_views():
    conn = psycopg2.connect(database="news")
    cursor = conn.cursor()
    cursor.execute(query_initialize_view_most_viewed_paths)
    cursor.execute(query_initialize_view_most_viewed_articles)
    cursor.execute(query_initialize_view_daily_error_rates)
    conn.commit()
    conn.close()


def select_three_most_viewed_articles():
    conn = psycopg2.connect(database="news")
    cursor = conn.cursor()
    cursor.execute(query_select_three_most_viewed_articles)
    return cursor.fetchall()
    conn.close()


def select_most_viewed_authors():
    conn = psycopg2.connect(database="news")
    cursor = conn.cursor()
    cursor.execute(query_select_most_viewed_authors)
    return cursor.fetchall()
    conn.close()


def select_daily_error_rate_more_than_one_percent():
    conn = psycopg2.connect(database="news")
    cursor = conn.cursor()
    cursor.execute(query_select_daily_error_rate_more_than_one_percent)
    return cursor.fetchall()
    conn.close()


# Print the 1st report
def print_three_most_viewed_articles():
    print("1. The most popular three articles of all time:")
    articles = select_three_most_viewed_articles()
    for article in articles:
        print("\"" + article[0] + "\"" + " --- " + str(article[1]) + " views")
    print("")


# Print the 2nd report
def print_most_viewed_authors():
    print("2. The most popular article authors of all time:")
    authors = select_most_viewed_authors()
    for author in authors:
        print(author[0] + " --- " + str(author[1]) + " views")
    print("")


# Print the 3rd report
def print_daily_error_rate_more_than_one_percent():
    print("3. The dates when more than 1% of requests lead to errors:")
    rates = select_daily_error_rate_more_than_one_percent()
    for rate in rates:
        print(rate[0].strftime("%B %d, %Y") +
              " --- " +
              str(round(rate[1], 1)) +
              "% errors")
    print("")

# Create/Replace views, then print the reports
if __name__ == '__main__':
    initialize_views()
    print_three_most_viewed_articles()
    print_most_viewed_authors()
    print_daily_error_rate_more_than_one_percent()
