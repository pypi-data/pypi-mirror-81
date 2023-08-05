import os
import sys
from .test import Test

if __name__ == '__main__':
    os.environ['LINGORM_CONFIG'] = 'lingorm/test/database.json'
    result = Test().table_first()
    print(result[0].companyName)

