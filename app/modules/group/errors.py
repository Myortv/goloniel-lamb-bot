from app.utils.toml_utils import FromTomlFile
from app.utils.exception_handling import HandlableException


class ErrorTitle(FromTomlFile):
    # no_master: str
    no_group: str
    no_join_request: str
    # rating_out_of_bounds: str


class ErrorDescription(FromTomlFile):
    # no_master: str
    no_group: str
    no_join_request: str
    # rating_out_of_bounds: str


ERR_TITLE = ErrorTitle('resources/group.toml')
ERR_DESCRIPTION = ErrorDescription('resources/group.toml')


# class NoMaster(HandlableException):
#     def __init__(self):
#         super().__init__(
#             title=ERR_TITLE.no_master,
#             description=ERR_DESCRIPTION.no_master
#         )


class NoGroup(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLE.no_group,
            description=ERR_DESCRIPTION.no_group
        )


class NoJoinRequest(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLE.no_join_request,
            description=ERR_DESCRIPTION.no_join_request
        )


# class RatingOutOfBounds(HandlableException):
#     def __init__(self):
#         super().__init__(
#             title=ERR_TITLE.rating_out_of_bounds,
#             description=ERR_DESCRIPTION.rating_out_of_bounds
#         )
