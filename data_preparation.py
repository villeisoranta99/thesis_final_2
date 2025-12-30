"""
Ville Isoranta Version: 17.11.2025. 
This script imports data from the CSV-file into the Biogeme model.
The CSV-file has been edited with Excel before importing the data.
"""

import pandas as pd 
import biogeme.database as db 
from biogeme.expressions import Variable #
import os

"""
Reads the data into  separate databases for different purposes.
"""
df = pd.read_csv ('file path removed', sep = ',') # read the csv
database = db.Database ('example', df ) # save the imported CSV into a database

df_pa = pd.read_csv ('file path removed', sep = ',') # read the csv
database_SP_PA = db.Database ('example_pa', df_pa) # save the imported CSV into a database

df_full = pd.read_csv ('file path removed', sep = ',') # read the csv
database_full = db.Database ('full', df_full ) # save the imported CSV into a database

dfMASA = pd.read_csv ('file path removed', sep = ',') # read the csv
database_MASA = db.Database ('MASA', dfMASA ) # save the imported CSV into a database

"""
Defines global variables.
"""

ID = Variable ('ID')
AGED = Variable('AGED')
COMM_FREQ_CAR = Variable('COMM_FREQ_CAR')
NUMB_VEHI = Variable('NUMB_VEHI')
DRIV_EXPE = Variable('DRIV_EXPE')
CAR_SHAR = Variable('CAR_SHAR')
MODE = Variable('MODE')
COMM_DURA_CAR = Variable('COMM_DURA_CAR')
COMM_DURA_TRAN = Variable('COMM_DURA_TRAN')
COMM_AVAI_TRAN = Variable('COMM_AVAI_TRAN')
DONT_KNOW = Variable('DONT_KNOW')
RP_TYPE = Variable('RP_TYPE')
RP_S = Variable('RP_S')
RP_E = Variable('RP_E')
PARK_FREE = Variable('PARK_FREE')
RP_P = Variable('RP_P')
RP_P_TOUR = Variable('RP_P_TOUR')
CHOI = Variable('CHOI')
PG = Variable('PG')
PG = Variable('PG')
PS = Variable('PS')
EG = Variable('EG')
ES = Variable('ES')
SG = Variable('SG')
SS = Variable('SS')
GEND = Variable('GEND')
EDUC = Variable('EDUC')
INCO = Variable('INCO')
TTRA = Variable('TTRA')

WEEKS = 4 # Sets the number of weeks in month as 4
"""
Transforms the price of the choice tasks 
from monthly into trip-based price using Equation 5. 
"""
PG_NORM_TRIP = database.define_variable ('PG_NORM_TRIP', (PG/((COMM_FREQ_CAR*2)*WEEKS)))
PS_NORM_TRIP = database.define_variable ('PS_NORM_TRIP', (PS/((COMM_FREQ_CAR*2)*WEEKS)))

PG_NORM_TRIP = database_SP_PA.define_variable ('PG_NORM_TRIP', (PG/((COMM_FREQ_CAR*2)*WEEKS)))
PS_NORM_TRIP = database_SP_PA.define_variable ('PS_NORM_TRIP', (PS/((COMM_FREQ_CAR*2)*WEEKS)))

PG_NORM_TRIP = database_full.define_variable ('PG_NORM_TRIP', (PG/((COMM_FREQ_CAR*2)*WEEKS)))
PS_NORM_TRIP = database_full.define_variable ('PS_NORM_TRIP', (PS/((COMM_FREQ_CAR*2)*WEEKS)))

"""
The RP-prices are either daily, weekly,
six month or annual prices. These all have been
transformed into tour based cost in a excel.
The tour-based price is transformed next into trip-
based cost. 
"""

P_NORM_RP = database_MASA.define_variable ('P_NORM_RP', (RP_P_TOUR/(2)))

"""
Definitions for dummy variables. 
"""
"""
Education. Base category is 2 (upper secondary/vocational). 
None had selected 1 (secondary/no education).
"""

EDUC_HIGH = database.define_variable ('EDUC_HIGH', (EDUC == 3))
EDUC_HIGH = database_SP_PA.define_variable ('EDUC_HIGH', (EDUC == 3))
EDUC_HIGH = database_MASA.define_variable ('EDUC_HIGH', (EDUC == 3))
EDUC_HIGH = database_full.define_variable ('EDUC_HIGH', (EDUC == 3))
"""
Gender.
Base category is 1 (men) 
"""
GEND_WOME = database.define_variable ('GEND_WOME', (GEND == 2))
GEND_WOME = database_SP_PA.define_variable ('GEND_WOME', (GEND == 2))
GEND_WOME = database_MASA.define_variable ('GEND_WOME', (GEND == 2))
GEND_WOME = database_full.define_variable ('GEND_WOME', (GEND == 2))

"""
Driving experimence.
Base category is 1 and 2 (under 2 years.
2-4 years) 
"""

DRIV_EXPE_TWOP = database_SP_PA.define_variable ('DRIV_EXPE_TWOP', ((DRIV_EXPE == 3)))
DRIV_EXPE_TWOP = database.define_variable ('DRIV_EXPE_TWOP', ((DRIV_EXPE == 3)))
DRIV_EXPE_TWOP = database_MASA.define_variable ('DRIV_EXPE_TWOP', ((DRIV_EXPE == 3)))
DRIV_EXPE_TWOP = database_full.define_variable ('DRIV_EXPE_TWOP', ((DRIV_EXPE == 3)))

"""
Income
Base category is 1 
(0-29 999€/year)
"""

INCO_MEDI = database.define_variable ('INCO_MEDI', (INCO == 2))
INCO_HIGH = database.define_variable ('INCO_HIGH', (INCO == 3))

INCO_MEDI = database_SP_PA.define_variable ('INCO_MEDI', (INCO == 2))
INCO_HIGH = database_SP_PA.define_variable ('INCO_HIGH', (INCO == 3))

INCO_MEDI = database_MASA.define_variable ('INCO_MEDI', (INCO == 2))
INCO_HIGH = database_MASA.define_variable ('INCO_HIGH', (INCO == 3))

INCO_MEDI = database_full.define_variable ('INCO_MEDI', (INCO == 2))
INCO_HIGH = database_full.define_variable ('INCO_HIGH', (INCO == 3))
"""
Age
Base category is 2 
(18-34years).
None had selected 1 (under 18) as it was part of the 
exclusion criteria.
"""

AGE_35 = database.define_variable ('AGE_35', (AGED == 3))
AGE_55 = database.define_variable ('AGE_55', (AGED == 4))

AGE_35 = database_SP_PA.define_variable ('AGE_35', (AGED == 3))
AGE_55 = database_SP_PA.define_variable ('AGE_55', (AGED == 4))

AGE_35 = database_MASA.define_variable ('AGE_35', (AGED == 3))
AGE_55 = database_MASA.define_variable ('AGE_55', (AGED == 4))

AGE_35 = database_full.define_variable ('AGE_35', (AGED == 3))
AGE_55 = database_full.define_variable ('AGE_55', (AGED == 4))

"""
Defines two of the databases as panel.
"""

database_SP_PA.panel('ID')
database_full.panel('ID')

