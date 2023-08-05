import os
import sys
from lingorm.orm import ORM
from lingorm.tools.mysql_entity_generator import MysqlEntityGenerator
from .entity.company_entity import CompanyEntity


class Test:
    def generate_entity(self):           
        file_dir = sys.path[0] + "/test/entity"
        MysqlEntityGenerator("47.112.123.236", "lirun", "Dbtest_lr").generate("company", "company", file_dir)

    def table_first(self):
        db=ORM.db("company")
        t = CompanyEntity
        where = db.create_where()
        where.add_and(t.companyName.like("%测试%"), t.id.gt(5))
        where.or_and(t.companyName.like("%立润%"), t.id.le(40))
        result = db.table(t).select(t.companyName).where(where).order_by(t.id.desc()).find()
        return result

