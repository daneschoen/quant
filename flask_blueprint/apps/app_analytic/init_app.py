
from apps import app

from .instr_models import Instr_Singleton 

# ----------

#const = app.config['CONST']
#INSTRS_NAME = const.INSTRS_NAME
from apps.settings.constants import INSTRS_NAME

# ================================================================================


def go():
    Instr = {}
    for instr_name in INSTRS_NAME:
        Instr[instr_name] = Instr_Singleton(instr_name)
