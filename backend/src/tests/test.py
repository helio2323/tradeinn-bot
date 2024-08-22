import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.models.Sqclass import Sqclass

sq = Sqclass()

response = sq.get_prod_xlsx(5)

for r in response:
    print(f'r: {r[0]}, q: {r[1]}, p: {r[3]}')