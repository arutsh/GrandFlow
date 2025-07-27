from pydantic import BaseModel, field_validator
from enum import Enum
import pycountry


def create_country_enum():
    countries = {c.alpha_2: c.name for c in pycountry.countries}
    # Create dynamic Enum with code as value and name as description
    return Enum("CountryEnum", {f"{code}": code for code in countries.keys()})


CountryEnum = create_country_enum()
COUNTRY_NAMES = {c.alpha_2: c.name for c in pycountry.countries}

class CustomerType(str, Enum):
    donor = "donor"
    ngo = "ngo"


class Customer(BaseModel):
    id: str | None = None
    name: str
    country: str
    type: CustomerType
    currency: str

    @field_validator("country")
    def validate_country(cls, v):
        if not pycountry.countries.get(alpha_2=v.upper()):
            raise ValueError(f"{v} is not a valid ISO Alpha-2 country code.")
        return v.upper()

    model_config = {"from_attributes": True}
