from app.utils.toml_utils import FromTomlFile
from app.utils.exception_handling import HandlableException


class ErrorTitle(FromTomlFile):
    no_master: str
    no_rating: str
    rating_out_of_bounds: str
    approve_already_exsists: str


class ErrorDescription(FromTomlFile):
    no_master: str
    no_rating: str
    rating_out_of_bounds: str
    approve_already_exsists: str


ERR_TITLE = ErrorTitle('resources/master.toml')
ERR_DESCRIPTION = ErrorDescription('resources/master.toml')


class NoMaster(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLE.no_master,
            description=ERR_DESCRIPTION.no_master
        )


class NoRating(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLE.no_rating,
            description=ERR_DESCRIPTION.no_rating
        )


class RatingOutOfBounds(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLE.rating_out_of_bounds,
            description=ERR_DESCRIPTION.rating_out_of_bounds
        )


class ApproveAlreadyExsists(HandlableException):
    def __init__(self):
        super().__init__(
            title=ERR_TITLE.approve_already_exsists,
            description=ERR_DESCRIPTION.approve_already_exsists,
        )
