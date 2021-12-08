from pydantic import BaseModel, validator

# @todo change on real db
fake_db = {
    1: 'ru',
    2: 'UK-ua'
}


class Language(BaseModel):
    language: int

    @validator('language')
    def validate_language(cls, value: int) -> str:
        if (value in fake_db) and (fake_db[value] not in ('ru', 'UK-ua')):
            raise ValueError
        else:
            return fake_db[value]
