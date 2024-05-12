from app.utils.toml_utils import FromTomlFile


class Descriptions(FromTomlFile):
    group_name: str
    group_desc: str
    join_request_name: str
    join_request_desc: str
    group_manage_name: str
    group_manage_desc: str
    group_admin_name: str
    group_admin_desc: str

    list: str
    show: str
    my_groups: str

    join: str
    list_requests: str
    leave: str

    show_join_request: str
    list_join_requests: str
    approve_join_request: str
    kick_member: str
    set_full: str


class Commands(FromTomlFile):
    list: str
    show: str
    my_groups: str

    join: str
    list_requests: str
    leave: str

    show_join_request: str
    list_join_requests: str
    approve_join_request: str
    kick_member: str
    set_full: str


class Options(FromTomlFile):
    show_join_request: str
    group_title: str


class PageText(FromTomlFile):

    placeholder_image: str
    join_request_title: str
    join_request_deleted: str

#     approve_request_title: str
#     you_are_not_master_yet: str

#     rating_deleted: str

    empty: str
    no_description: str
    no_master: str
    no_discord_id: str
    no_member: str
#     no_user: str
#     no_groups: str
#     no_approval_request_reason: str
#     no_rating: str
#     rating_out_of_bounds: str

#     e_user_not_found: str
#     e_mentioned_user_not_found: str

#     f_rating: str
    f_master: str
    f_members: str
    f_group_title: str
    f_is_full: str
    f_join_request_state: str
    f_join_request_is_accepted: str
#     f_user: str
#     f_is_approved: str
#     f_groups: str
#     f_approvals_amount: str
#     f_approval_request_state: str

#     t_group_oneline: str

    btn_join_request: str
    btn_leave_group: str
    btn_leave_message: str
    btn_list_requests: str
    btn_delete_group: str
    btn_set_full: str
    btn_join_request_delete: str
    btn_edit_group: str
#     btn_create_approval_request: str
#     btn_edit_master: str
#     btn_create_master: str
#     btn_delete_rating: str
#     btn_delete_approve: str


class Dialog(FromTomlFile):
    test: str


D = Descriptions('resources/group.toml')
C = Commands('resources/group.toml')
P = PageText('resources/group.toml')
O = Options('resources/group.toml')

DIALOG = Dialog('resources/group.toml')
