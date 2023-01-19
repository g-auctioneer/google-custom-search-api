from pprint import pprint
from googleapiclient.discovery import build
import config


def p(str) -> None:
    """整形してprint

    Args:
        mixed: 表示する内容
    """
    pprint(str)

def get_search_result() -> list:
    """検索を実行 (30件しか取れない、、)

    Returns:
        list: 検索結果
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
                    exactTerms = config.EXACT_TERMS,
                    dateRestrict = 'w10'  # 過去10週間
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

def get_urls(search_result: list) -> list:
    """クリックするところのURLだけ欲しい

    Args:
        list: 検索結果

    Returns:
        list: URL一覧
    """
    urls = []
    for sr in search_result:
        urls.extend([sr['link']])

    return urls


if __name__ == '__main__':
    search_result = get_search_result()
    urls = get_urls(search_result)

    for url in urls:
        for ignore_word in config.IGNORE_WORDS:
            if ignore_word in url:
                break
        else:
            p(url)
