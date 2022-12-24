from pprint import pprint
from googleapiclient.discovery import build
import config


def p(str):
    """
    for debug
    """
    pprint(str)

def get_search_result():
    """
    検索を実行 (30件しか取れない、、)
    """
    service = build(
        'customsearch', 'v1', developerKey = config.API_KEY
    )

    start_index = 1
    get_num = 10
    search_result = []

    for i in range(10):
        try:
            res = (
                service.cse()
                .list(
                    q = config.SEARCH_WORD,
                    cx = config.SEARCH_ENGINE_ID,
                    lr = 'lang_ja',
                    start = start_index,
                    num = get_num,
                    exactTerms = config.EXACT_TERMS
                )
                .execute()
            )
            search_result.extend(res['items'])
            start_index += 10

        except Exception as e:
            p(e)
            break

    service.close()
    return search_result

def get_urls(search_result):
    """
    URLだけ欲しい
    """
    urls = []
    for sr in search_result:
        urls.extend([sr['link']])

    return urls


if __name__ == '__main__':
    search_result = get_search_result()
    urls = get_urls(search_result)
    p(urls)

