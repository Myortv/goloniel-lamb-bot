from pydantic import BaseModel, validator, ValidationError

# from fastapiplugins.exceptions import HandlableException


class RatingCreate(BaseModel):
    master_id: int
    rating: int

    @validator('rating')
    def rating_in_bounds(cls, v):
        if v < 0 or v > 5:
            raise ValidationError()
            # raise HandlableException(
            #     'SOCIAL-ratingoutofbounds',
            #     422,
            #     title='Rating should be in bounds of 0-5'
            # )
        return v


class Rating(BaseModel):
    user_id: int
    master_id: int
    rating: int

    @validator('rating')
    def rating_in_bounds(cls, v):
        if v < 0 or v > 5:
            raise ValidationError()
            # raise HandlableException(
            #     'SOCIAL-ratingoutofbounds',
            #     422,
            #     title='Rating should be in bounds of 0-5'
            # )
        return v

