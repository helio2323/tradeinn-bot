import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models.Sqclass import Sqclass
from src.services.bot import login, update_all_products

bd = Sqclass()

bd.set_all_list_false()
