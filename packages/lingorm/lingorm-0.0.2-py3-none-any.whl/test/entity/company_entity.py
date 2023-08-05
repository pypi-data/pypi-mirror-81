from ...mapping import *


class CompanyEntity(ORMEntity):
    __table__ = "company"
    __database__ = "company"
    companyName = Field(field_name="company_name", field_type="string", length="45")
    createdAt = Field(field_name="created_at", field_type="datetime")
    deletedAt = Field(field_name="deleted_at", field_type="datetime")
    employeeNumber = Field(field_name="employee_number", field_type="int")
    englishAbbreviation = Field(field_name="english_abbreviation", field_type="string", length="255")
    id = Field(field_name="id", field_type="int", primary_key=True, is_generated=True)
    isDeleted = Field(field_name="is_deleted", field_type="int")
    isOpen = Field(field_name="is_open", field_type="int")
    logo = Field(field_name="logo", field_type="string", length="100")
    shortName = Field(field_name="short_name", field_type="string", length="20")
    updatedAt = Field(field_name="updated_at", field_type="datetime")

    def __init__(self, **kwargs):
        self.companyName = kwargs.get("companyName")
        self.createdAt = kwargs.get("createdAt")
        self.deletedAt = kwargs.get("deletedAt")
        self.employeeNumber = kwargs.get("employeeNumber")
        self.englishAbbreviation = kwargs.get("englishAbbreviation")
        self.id = kwargs.get("id")
        self.isDeleted = kwargs.get("isDeleted")
        self.isOpen = kwargs.get("isOpen")
        self.logo = kwargs.get("logo")
        self.shortName = kwargs.get("shortName")
        self.updatedAt = kwargs.get("updatedAt")