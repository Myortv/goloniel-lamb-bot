from app.utils.toml_utils import FromTomlFile


class Descriptions(FromTomlFile):
    list: str
    show: str
    me: str
    # me_show: str
    # me_edit: str
    # group: str
    rate: str
    approve: str
    approve_request: str
    master_desc: str
    master_name: str


class Commands(FromTomlFile):
    list: str
    show: str
    me: str
    # me_show: str
    # me_edit: str
    # group: str
    rate: str
    approve: str
    approve_request: str


class PageText(FromTomlFile):
    placeholder_image: str
    approve_request_title: str
    you_are_not_master_yet: str
    approval: str

    rating_deleted: str
    approval_deleted: str

    empty: str
    no_description: str
    no_user: str
    no_groups: str
    no_approval_request_reason: str
    no_rating: str
    rating_out_of_bounds: str

    e_user_not_found: str
    e_mentioned_user_not_found: str

    f_rating: str
    f_user: str
    f_is_approved: str
    f_groups: str
    f_approvals_amount: str
    f_approval_request_state: str

    t_group_oneline: str

    btn_create_approval_request: str
    btn_edit_master: str
    btn_create_master: str
    btn_delete_rating: str
    btn_delete_approve: str
    btn_set_master_approval: str
    btn_set_master_rating: str


class Dialog(FromTomlFile):
    title_create: str
    title_update: str
    title_rating: str

    f_title: str
    f_description: str
    f_cover_picture: str
    f_rating: str

    placeholder_title: str
    placeholder_description: str
    placeholder_cover_picture: str
    placeholder_rating: str


D = Descriptions('resources/master.toml')
C = Commands('resources/master.toml')
P = PageText('resources/master.toml')
DIALOG = Dialog('resources/master.toml')
