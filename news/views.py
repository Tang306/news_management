from decorator import common_ajax_response
from utils import format_return
from news.interface import NewsInformation
from decorator import require_role
from page import Page
from collections import Iterable


@common_ajax_response
@require_role([1, 2, 3, ])
def news_list(request):
    """
    新闻列表接口
    """
    category = request.POST.get('category')
    news_id = request.POST.get('news_id')
    title = request.POST.get('title')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    news_state = request.POST.get('news_state')
    release_location = request.POST.get('release_location')
    page_index = int(request.POST.get('page_index', 1))
    page_count = min(int(request.POST.get('page_count', 10)), 20)

    if not request.user_id:
        return format_return(0, data={'objs': [], 'total_page': 0, 'total_count': 0})

    objs = NewsInformation().get_news_information(
        news_id=news_id, category=category, title=title, start_time=start_time, end_time=end_time, news_state=news_state,
        release_location=release_location
    )
    if not objs:
        return format_return(22201, "查询不到信息")
    data = Page(objs, page_count).page(page_index)
    return format_return(0, data={
        'objs': format_news(data['objects']), 'total_page': data['total_page'], 'total_count': data['total_count']
    })


@common_ajax_response
@require_role([1, 2, 3, ])
def web_list(request):
    """
    官网列表接口
    """
    category = request.POST.get('category')
    release_location = request.POST.get('release_location')
    news_id = request.POST.get('news_id')
    news = NewsInformation().get_web_information(category=category, release_location=release_location, news_id=news_id)
    if not news:
        return format_return(22201, "查询不到信息")
    data = format_news(news)
    return format_return(0, data=data)


@common_ajax_response
@require_role([1, 2, 3, ])
def get_news_info(request):
    """
    新闻详情接口
    """
    news_id = request.POST.get('news_id')
    news = NewsInformation().news_details(news_id)
    data = format_news(news)
    return format_return(0, data=data)


@common_ajax_response
@require_role([1, 2, ])
def add_news(request):
    """
    添加新闻接口
    """
    user_id = request.user_id
    release_location = request.POST.get('release_location')
    title = request.POST.get('title')
    topping = request.POST.get('topping')
    figure = request.POST.get('figure')
    explain = request.POST.get('explain')
    news_time = request.POST.get('news_time')
    news_text = request.POST.get('news_text')
    examine = request.POST.get('examine')
    release_time = request.POST.get('release_time')
    news_file = request.POST.get('news_file')
    category = request.POST.get('category')
    jump_link = request.POST.get('jump_link')
    banner_format = request.POST.get('banner_format')
    banner_order = request.POST.get('banner_order')
    news = NewsInformation().add_news_information(user_id=user_id, category=category, title=title, release_time=release_time,
                                                  release_location=release_location, topping=topping, figure=figure,
                                                  explain=explain, news_time=news_time, news_text=news_text, examine=examine,
                                                  jump_link=jump_link, banner_format=banner_format, banner_order=banner_order,
                                                  news_file=news_file)
    data = format_news(news)
    return format_return(0, data=data)


@common_ajax_response
@require_role([1, 2, ])
def post_news(request):
    """
    修改新闻接口
    """
    release_location = request.POST.get('release_location')
    news_id = request.POST.get('news_id')
    title = request.POST.get('title')
    topping = request.POST.get('topping')
    figure = request.POST.get('figure')
    explain = request.POST.get('explain')
    news_time = request.POST.get('news_time')
    news_text = request.POST.get('news_text')
    examine = request.POST.get('examine')
    release_time = request.POST.get('release_time')
    news_file = request.POST.get('news_file')
    jump_link = request.POST.get('jump_link')
    banner_format = request.POST.get('banner_format')
    banner_order = request.POST.get('banner_order')
    news = NewsInformation().modify_news_information(news_id=news_id, title=title, release_time=release_time,
                                                     release_location=release_location, topping=topping, figure=figure,
                                                     explain=explain, news_time=news_time, news_text=news_text, examine=examine,
                                                     jump_link=jump_link, banner_format=banner_format, banner_order=banner_order,
                                                     news_file=news_file)
    data = format_news(news)
    return format_return(0, data=data)


@common_ajax_response
@require_role([1, 2, ])
def del_news(request):
    """
    删除新闻接口
    """
    news_id = request.POST.get('news_id')
    news = NewsInformation().get_news_by_id(news_id)
    news.news_state = -1
    news.save()
    data = format_news(news)
    return format_return(0, data=data)


@common_ajax_response
@require_role([1, 2, ])
def submit_news(request):
    """
    提交新闻接口
    """
    news_id = request.POST.get('news_id')
    category = request.POST.get('category')
    news = NewsInformation().submit_news_information(category=category, news_id=news_id)
    data = format_news(news)
    return format_return(0, data=data)


@common_ajax_response
@require_role([1, 3, ])
def examine_news(request):
    """
    审核新闻接口
    """
    category = request.POST.get('category')
    examine_result = request.POST.get('examine_result')
    news_id = request.POST.get('news_id')
    news = NewsInformation().examine_news_information(category=category, examine_result=examine_result, news_id=news_id)
    data = format_news(news)
    return format_return(0, data=data)


def format_news(objs):
    def _format_obj(news):
        if not news:
            return None
        return {
            'id': news.id, 'title': news.title, 'category': news.category,
            'news_time': news.news_time, 'user': news.user.nickname,
            'topping': news.topping, 'release_time': news.release_time, 'news_state': news.news_state,
            'release_location': news.release_location, 'create_time': news.create_time,
            'figure': news.figure, 'news_text': news.news_text, 'views_number': news.views_number,
            'explain': news.explain, 'examine': news.examine, 'news_file': [news.news_file for news in news.attachments.all()],
            'jump_link': news.jump_link, 'banner_format': news.banner_format, 'banner_order': news.banner_order
        }
    return [_format_obj(news) for news in objs] if isinstance(objs, Iterable) else _format_obj(objs)