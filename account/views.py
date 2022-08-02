from decorator import common_ajax_response
from decorator import require_role
from utils import format_return, format_date_time
from account.interface import UserBase
from page import Page
from collections import Iterable


@common_ajax_response
def register_supper(request):
    """
    添加用户接口
    """
    nickname = request.POST.get('nickname')
    username = request.POST.get('username')
    password = request.POST.get('password')
    return UserBase().admin_register(nickname, username, password)


@common_ajax_response
def login(request):
    """
    登录接口
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    return UserBase().login(username, password)


@common_ajax_response
@require_role([1, ])
def register(request):
    """
    添加用户接口
    """
    nickname = request.POST.get('nickname')
    username = request.POST.get('username')
    password = request.POST.get('password')
    state = request.POST.get('state')
    return UserBase().register(nickname, username, password, state)


@common_ajax_response
@require_role([1, ])
def reset(request):
    """
    密码初始化接口
    """
    user_id = request.POST.get('user_id')
    return UserBase().reset_password_by_user_id(user_id)


@common_ajax_response
@require_role([1, 2, 3, ])
def change(request):
    """
    修改密码接口
    """
    user_id = request.user_id
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    return UserBase().change_password(user_id, old_password, new_password)


@common_ajax_response
@require_role([1, ])
def user_edit(request):
    """
    用户权限编辑接口
    """
    user_id = request.POST.get('user_id')
    nickname = request.POST.get('nickname')
    username = request.POST.get('username')
    password = request.POST.get('password')
    state = request.POST.get('state')
    return UserBase().edit_user_information(user_id=user_id, nickname=nickname, username=username, password=password, state=state)


@common_ajax_response
@require_role([1, ])
def user_delete(request):
    """
    用户删除接口
    """
    user_id = request.POST.get('user_id')
    return UserBase().del_user_information(user_id)


@common_ajax_response
@require_role([1, ])
def user_list(request):
    """
    用户列表接口
    """
    nickname = request.POST.get('nickname')
    state = request.POST.get('state')
    page_index = int(request.POST.get('page_index', 1))
    page_count = min(int(request.POST.get('page_count', 10)), 20)

    if not request.user_id:
        return format_return(0, data={'objs': [], 'total_page': 0, 'total_count': 0})

    objs = UserBase().get_user_information(nickname=nickname, state=state)
    data = Page(objs, page_count).page(page_index)
    return format_return(0, data={
        'objs': format_accounts(data['objects']), 'total_page': data['total_page'], 'total_count': data['total_count']
    })


def format_accounts(objs):
    def _format_obj(obj):
        if not obj:
            return None
        return {
            'id': obj.id, 'username': obj.username, 'nickname': obj.nickname, 'state': obj.state,
            'create_time': format_date_time(obj.create_time)
        }
    return [_format_obj(obj) for obj in objs] if isinstance(objs, Iterable) else _format_obj(objs)


