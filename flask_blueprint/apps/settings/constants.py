import os
import datetime

#from .constants_coin import *
#from .constants_geo import *


# ==============================================================================
#
# ==============================================================================
VER = "Ver 0.1.0";
BUILD_VER = VER + ": " +  str(datetime.datetime.utcnow())
#TITLE = (BUILD_VER == 0) ? "Rivercast Capital - " + VER_DT : "DEV";
#TITLE = "Rivercast Capital Analytics Platform - " + VER_DT if (BUILD_VER == 0) else "DEV"


# ==============================================================================
# DATABASE COL/TABLES - Mongodb
# ==============================================================================
# MONGO_DBNAME_FINTECH = 'fintech'

COL_COIN_SPEC = 'coin_spec'
COL_COIN_TOP = 'coin_top'

COL_COIN_TOP_NOW = 'coin_top_now'

COL_COIN_HIST_DAILY = 'coin_hist_daily'
COL_COIN_HIST_DAILY2 = 'coin_hist_daily2'
COL_COIN_HIST_HOUR = 'coin_hist_hour'
COL_COIN_HIST_MIN = 'coin_hist_min'

COL_USER = 'user'
COL_CONTACT = 'contact'

# instantiation occurs in app_util/__init__.py:
# mongodb = MongoClient()[MONGO_DBNAME_FINTECH]
# col_coin_top = mongodb[COL_COIN_TOP]
# col_coin_hist_daily = mongodb[COL_COIN_HIST_DAILY]


COL_GEO_CITY = 'geo_city'
COL_GEO_CNTY = 'geo_cnty'
COL_FX = 'fx'

COL_BLOG_TRIBAL = 'blog_tribal'
COL_CONTACT = 'contact'


# ==============================================================================
# PLOTLY
# ==============================================================================

PLOT_COLORSCALES = ['Blackbody', 'Bluered', 'Blues', 'Earth', 'Electric', 'Greens',
  'Greys', 'Hot', 'Jet', 'Picnic', 'Portland', 'Rainbow', 'RdBu', 'Reds', 'Viridis',
  'YlGnBu', 'YlOrRd']

PLOT_COLORSCALES_SOLID = ['Bluered', 'Blues', 'Earth', 'Electric', 'Greens',
  'Hot', 'Jet', 'Portland', 'Reds', 'Viridis', 'YlGnBu', 'YlOrRd']

# ==============================================================================
# JAVA API
# ==============================================================================
API_SERVER_URL = 'http://localhost:8007'
API_SERVER_URL_ADMIN = 'http://localhost:8008'

INSTRS_SEP = '---'  # used in api url

def get_api_server_url(username):
    if username == 'admin':
        return API_SERVER_URL_ADMIN
    else:
        return API_SERVER_URL

# ==============================================================================
# DATABASE COL/TABLES - Mongodb
# ==============================================================================
# DB names are in settings_server.py

COL_EQUITYCURVE = 'col_equitycurve'
COL_USER = 'user'

COL_GEO_CITY = 'geo_city'
COL_GEO_CNTY = 'geo_cnty'
COL_FX = 'fx'


# ==============================================================================
# Data files:
# - esdata1min24hr.asc
# - econXYZ.txt, ...
# - holes.txt
# - excludees.txt
# ==============================================================================

COIN_TOP_100 = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'EOS', 'ADA', 'XLM', 'TRX', 'NEO', 'IOT', 'XMR', 'VEN', 'DASH', 'BNB', 'XEM', 'ETC', 'QTUM', 'XVG', 'LSK', 'HT', 'ICX', 'BTM*', 'BTG', 'ZEC', 'XRB', 'IOST', 'SNT', 'ZRX', 'ZIL', 'NAS', 'DGD', 'WAVES', 'ORME', 'LINK', 'STORJ', 'POWR', 'BAT', 'NCASH', 'STORM', 'GNX', 'SALT', 'HSR', 'SUB', 'MTL', 'KNC', 'CVC', 'GNT', 'MANA', 'GTO',
'MTX', 'ELF', 'SRN', 'REQ', 'SYS', 'MDS', 'BLZ', 'EDO', 'RDN*', 'NEBL', 'ABT', 'THETA', 'DTA', 'RCN', 'ENJ', 'ITC', 'RUFF', 'OCN', 'GTC', 'POA', 'CMT*', 'SWFTC', 'PRO', 'GVT', 'NULS', 'TNT', 'WPR', 'INS', 'MTN*', 'ADX', 'SOC', 'RPX', 'QUN', 'TRIG', 'MEE', 'SNC', 'OC', 'WAN', 'ACT*', 'ETHOS', 'OMG', 'ELA', 'AION', 'ONT', 'STRAT', 'PAY', 'WAX', 'GAS', 'MCO', 'QSP']
COIN_TOP_1_50 = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'EOS', 'ADA', 'XLM', 'TRX', 'NEO', 'IOT', 'XMR', 'VEN', 'DASH', 'BNB', 'XEM', 'ETC', 'QTUM', 'XVG', 'LSK', 'HT', 'ICX', 'BTM*', 'BTG', 'ZEC', 'XRB', 'IOST', 'SNT', 'ZRX', 'ZIL', 'NAS', 'DGD', 'WAVES', 'ORME', 'LINK', 'STORJ', 'POWR', 'BAT', 'NCASH', 'STORM', 'GNX', 'SALT', 'HSR', 'SUB', 'MTL', 'KNC', 'CVC', 'GNT', 'MANA', 'GTO']
COIN_TOP_51_100 = ['MTX', 'ELF', 'SRN', 'REQ', 'SYS', 'MDS', 'BLZ', 'EDO', 'RDN*', 'NEBL', 'ABT', 'THETA', 'DTA', 'RCN', 'ENJ', 'ITC', 'RUFF', 'OCN', 'GTC', 'POA', 'CMT*', 'SWFTC', 'PRO', 'GVT', 'NULS', 'TNT', 'WPR', 'INS', 'MTN*', 'ADX', 'SOC', 'RPX', 'QUN', 'TRIG', 'MEE', 'SNC', 'OC', 'WAN', 'ACT*', 'ETHOS', 'OMG', 'ELA', 'AION', 'ONT', 'STRAT', 'PAY', 'WAX', 'GAS', 'MCO', 'QSP']
COIN_TOP_10_POP = ['BTC', 'ETH', 'XRP', 'BCH', 'EOS', 'LTC', 'ADA', 'DASH', 'ZEC', 'XMR']
COIN_TOP_10_MKT = ['BTC', 'ETH', 'XRP', 'BCH', 'EOS', 'LTC', 'ADA', 'XLM', 'IOT', 'NEO']

# In this order will appear in select option's
INSTRS_NAME = ['es','da','us','ty','ec','cl','nk']

#Instrs = {}
#for instr in INSTRS_NAME:

INSTR_FILENAME_1MIN24HR_SUFFIX = 'data1min24hr'
INSTR_FILENAME_OUT_10MIN_SUFFIX = 'data10col'
INSTR_FILENAME_OUT_5MIN_SUFFIX = 'data5col'
INSTR_FILENAME_OUT_1MIN_SUFFIX = 'data1col'

INSTR_FILE_EXT = 'asc'
OUT_FILE_EXT = 'csv'
ECON_HOL_FILE_EXT = 'txt'

ECON = [
    "econemp",
    "econfomc",
    "econexp",
    "econnonq",
    "econquar",
    "econppi",
    "econcpi",
    "econlead",
    "econgdp"
]


HOL = []
EXCLUDE = []
for name in INSTRS_NAME:
    HOL.append('hol' + name.lower())
    EXCLUDE.append('exclude' + name.lower())


DATA_IN_DIR  = '/home/duncan/data_in/'
DATA_OUT_DIR = '/home/duncan/data_out/'


EXTRA_OUT_DIR = '/opt/www/rivercast/data/'
REGRESSION_FEATURES_OUT_FILESUFFIX = 'regression_feature'
OBS_FILESUFFIX = 'obs'
RES_MATRIX_FILESUFFIX = 'res'


#MATPLOTLIB_OUT_DIR = os.path.join(PROJECT_PATH, 'static/images/')
MATPLOTLIB_OUT_DIR = '/static/images/'
MATPLOTLIB_OUT_FILESUFFIX =  'regression_scatter'
MATPLOTLIB_OUT_FILEFORMAT = 'png'


MIN_INCR = 1


# ==============================================================================


DATE_FORMAT_MMddyyyy = "MM/dd/yyyy";
DATE_FORMAT_MMddyy = "MM/dd/yy";
TIME_FORMAT_HHmmss = "HH:mm:ss";
TIME_FORMAT_HHmm = "HH:mm";

DATE_FORMAT_TICK = DATE_FORMAT_MMddyyyy;
TIME_FORMAT_TICK = TIME_FORMAT_HHmmss;
DELIM_TICK = ",";

DATE_FORMAT_CSV = DATE_FORMAT_MMddyyyy;
TIME_FORMAT_CSV = TIME_FORMAT_HHmmss;
DELIM_CSV = ",";

DATE_FORMAT_HOL = "MM/dd/yyyy";

DATE_FORMAT = "M/dd/yyyy";



# ------------------------------------------------------------------------------

#from django.utils.translation import ugettext_lazy as _
#from app.utils_flask import ugettext_lazy as _

CATEGORY = ('accelerator', 'bootcamp', 'online course', 'hackathon')

#'pre-accelerator', 'coworking', 'coliving', 'conference'  )

SKILL_TECHNOLOGY = ('game development', 'devops', 'marketing', 'project management')


# ==============================================================================
#
# ==============================================================================

# --------------------
# CONSTANTS FOR SEARCH
# --------------------
PER_PAGE = 20

ZIPCODE_RADIUS_MILES = 20





# -------------------------------------
# CONSTANTS FOR SCHEDULING-CALENDAR APP, INBOX-MESSAGES
# -------------------------------------

# from enum import Enum
# class ScheduleStatus:
#     PENDING = "pending"
#     DECLINED = "declined"
#     CANCELED = "canceled"
#     CANCELED_PENDING = "canceled_pending"
#     FINISHED = "finished"

# this is better - can be used in jinja2 and python
SCHEDULE_STATUS = {
    'PENDING': 'pending',
    'DECLINED': 'declined',
    'ACCEPTED': 'accepted',
    'CANCELED': 'canceled',
    'CANCELED_PENDING': 'canceled_pending',
    'FINISHED': 'finished'
}


INTERVIEW_DURATION_MIN = 30   # just default
MAX_MESSAGE_COUNT = 50
FMT_DTIME = '%m-%d-%Y   %I:%M %p'
FMT_DTIME_SHORT = '%m-%d-%y %I:%M %p'
FMT_DT_ABBR = '%b %d %Y'
FMT_DT_LONG = '%m-%d-%Y'
FMT_DT_SHORT = '%m-%d-%y'
FMT_TIME = '%I:%M %p'



SCHEDULE_DURATION = [
    ('15','15 minutes'),
    ('30','30 minutes'),
    ('45','45 minutes'),
    ('60','1 hour'),
    ('90','1 hour 30 minutes'),
    ('120','2 hours'),
    ('150','2 hours 30 minutes'),
    ('180','3 hours'),
    ('210','3 hours 30 minutes'),
    ('240','4 hours'),
    ('270','4 hours 30 minutes'),
    ('300','5 hours'),
    ('330','5 hours 30 minutes'),
    ('360','6 hours'),
    ('390','6 hours 30 minutes'),
    ('420','7 hours'),
    ('450','7 hours 30 minutes'),
    ('480','8 hours'),
    ('510','8 hours 30 minutes'),
    ('540','9 hours'),
    ('570','9 hours 30 minutes'),
    ('600','10 hours'),
    ('630','10 hours 30 minutes'),
    ('660','11 hours'),
    ('690','11 hours 30 minutes'),
    ('720','12 hours')
]


SCHEDULE_DURATION_ = [
    ('15','15 minutes'),
    ('30','30 minutes'),
    ('45','45 minutes'),
    ('60','1 hour'),
    ('75','1 hour 15 minutes'),
    ('90','1 hour 30 minutes'),
    ('105','1 hour 45 minutes'),
    ('120','2 hours'),
    ('135','2 hours 15 minutes'),
    ('150','2 hours 30 minutes'),
    ('165','2 hours 45 minutes'),
    ('180','3 hours'),
    ('195','3 hours 15 minutes'),
    ('210','3 hours 30 minutes'),
    ('225','3 hours 30 minutes'),
    ('240','4 hours'),
    ('255','4 hours 15 minutes'),
    ('270','4 hours 30 minutes'),
    ('285','4 hours 45 minutes'),
    ('300','5 hours'),
    ('315','5 hours 15 minutes'),
    ('330','5 hours 30 minutes'),
    ('345','5 hours 45 minutes'),
    ('360','6 hours'),
    ('375','6 hours 15 minutes'),
    ('390','6 hours 30 minutes'),
    ('405','6 hours 45 minutes'),
    ('420','7 hours'),
    ('435','7 hours 15 minutes'),
    ('450','7 hours 30 minutes'),
    ('465','7 hours 45 minutes'),
    ('480','8 hours')
]


FREQUENCIES = {
    'YEARLY': 'YEARLY',
    'MONTHLY': 'MONTHLY',
    'WEEKLY': 'WEEKLY',
    'DAILY': 'DAILY',
}

FREQUENCY_CHOICES = (
    (FREQUENCIES['YEARLY'], 'Yearly'),
    (FREQUENCIES['MONTHLY'], 'Monthly'),
    (FREQUENCIES['WEEKLY'], 'Weekly'),
    (FREQUENCIES['DAILY'], 'Daily'),
)
"""
FREQUENCY_CHOICES = (
    (FREQUENCIES['YEARLY'], _('Yearly')),
    (FREQUENCIES['MONTHLY'], _('Monthly')),
    (FREQUENCIES['WEEKLY'], _('Weekly')),
    (FREQUENCIES['DAILY'], _('Daily')),
)
"""

OCCURRENCE_DECISIONS = {
    'all': 'all',
    'following': 'following',
    'this one': 'this one',
}

OCCURRENCE_DECISION_CHOICESS = (
    (OCCURRENCE_DECISIONS['all'], 'all'),
    (OCCURRENCE_DECISIONS['following'], 'following'),
    (OCCURRENCE_DECISIONS['this one'], 'this one'),
)


SERVICE_UNIT = {
    'HOUR': 'hour',
    'HOUR_SCALED': 'hour_scaled',
    'MENU': 'menu',   # service_menu_item
    'DAY': 'day',
    'NIGHT': 'night',
    'APPOINTMENT': 'appointment'
}


# -----------------------------------
# FORM - ERROR MESSAGES AND CONSTANTS
# -----------------------------------

# Catch-all error messages for forms
EMAIL_REQUIRED = u"Email required"

EMAIL_FORMAT_INVALID = "Email doesn't look correct"

EMAIL_NOT_FOUND = \
    u"""We can\'t find that e-mail in our system.  Please try another e-mail.
    """
PASSWORD_REQUIRED = u"Password required"

EMAIL_PASSWORD_MISMATCH = \
	u"""This email address or password does not match."""

FIRST_NAME_REQUIRED = u"First name required"

LAST_NAME_REQUIRED = u"Last name required"

PHONE_NUMBER_REQUIRED = u"Phone number required"

ZIPCODE_REQUIRED = u"Zipcode required"

NICKNAME_REQUIRED = \
    u"""Your Short Business Name is required
    """

BUSINESS_NAME_REQUIRED = \
    u"""Business Name is required
    """

DESCRIPTION_REQUIRED = \
    u"""Please enter a description
    """

# join pages
PASSWORD_CREATE_ACCOUNT_REQUIRED = u"Password required"

PASSWORD_CREATE_ACCOUNT_INVALID = \
    u"""Let\'s try creating your password again.  Be sure to make it 6+
    characters in length and that it only contain letters and numbers
    (NO fancy characters like !, @, or &).
    """
EMAIL_ALREADY_IN_USE = "Email already in use"  # add link to forgot password

USERNAME_ALREADY_IN_USE = u"Username already in use - please try another"

TERMS_REQUIRED = \
    u"""Oops! You have to agree to the terms in order to continue.
    """

# Contact page
CONTACT_US_MESSAGE_REQUIRED = \
    u"""We can keep moving ahead after you enter a message.
    """
CONTACT_US_NAME_REQUIRED = \
	u"""You must enter a name
	"""
CONTACT_US_PHONE_NUMBER_REQUIRED = \
    u"""Please enter your phone number
    """


RESET_PASSWORD_MUST_MATCH = \
    u"""New passwords don't match. Please try again
    """

RESET_PASSWORD_REQUIRED = \
    u"""The password field is required
    """

RESET_VERIFY_PASSWORD_REQUIRED = \
    u"""The verify password field is required
    """

DOW = [
    ('6','Sunday'),
    ('0','Monday'),
    ('1','Tuesday'),
    ('2','Wednesday'),
    ('3','Thursday'),
    ('4','Friday'),
    ('5','Saturday')
]


TIMES = [
    ('00:00','12:00 AM'),
    ('00:30','12:30 AM'),
    ('01:00','1:00 AM'),
    ('01:30','1:30 AM'),
    ('02:00','2:00 AM'),
    ('02:30','2:30 AM'),
    ('03:00','3:00 AM'),
    ('03:30','3:30 AM'),
    ('04:00','4:00 AM'),
    ('04:30','4:30 AM'),
    ('05:00','5:00 AM'),
    ('05:30','5:30 AM'),
    ('06:00','6:00 AM'),
    ('06:30','6:30 AM'),
    ('07:00','7:00 AM'),
    ('07:30','7:30 AM'),
    ('08:00','8:00 AM'),
    ('08:30','8:30 AM'),
    ('09:00','9:00 AM'),
    ('09:30','9:30 AM'),
    ('10:00','10:00 AM'),
    ('10:30','10:30 AM'),
    ('11:00','11:00 AM'),
    ('11:30','11:30 AM'),
    ('12:00','12:00 PM'),
    ('12:30','12:30 PM'),
    ('13:00','1:00 PM'),
    ('13:30','1:30 PM'),
    ('14:00','2:00 PM'),
    ('14:30','2:30 PM'),
    ('15:00','3:00 PM'),
    ('15:30','3:30 PM'),
    ('16:00','4:00 PM'),
    ('16:30','4:30 PM'),
    ('17:00','5:00 PM'),
    ('17:30','5:30 PM'),
    ('18:00','6:00 PM'),
    ('18:30','6:30 PM'),
    ('19:00','7:00 PM'),
    ('19:30','7:30 PM'),
    ('20:00','8:00 PM'),
    ('20:30','8:30 PM'),
    ('21:00','9:00 PM'),
    ('21:30','9:30 PM'),
    ('22:00','10:00 PM'),
    ('22:30','10:30 PM'),
    ('23:00','11:00 PM'),
    ('23:30','11:30 PM')
]

TIMES_I = [
    ('12:00 AM','12:00 AM'),
    ('12:30 AM','12:30 AM'),
    ('01:00 AM','1:00 AM'),
    ('01:30 AM','1:30 AM'),
    ('02:00 AM','2:00 AM'),
    ('02:30 AM','2:30 AM'),
    ('03:00 AM','3:00 AM'),
    ('03:30 AM','3:30 AM'),
    ('04:00 AM','4:00 AM'),
    ('04:30 AM','4:30 AM'),
    ('05:00 AM','5:00 AM'),
    ('05:30 AM','5:30 AM'),
    ('06:00 AM','6:00 AM'),
    ('06:30 AM','6:30 AM'),
    ('07:00 AM','7:00 AM'),
    ('07:30 AM','7:30 AM'),
    ('08:00 AM','8:00 AM'),
    ('08:30 AM','8:30 AM'),
    ('09:00 AM','9:00 AM'),
    ('09:30 AM','9:30 AM'),
    ('10:00 AM','10:00 AM'),
    ('10:30 AM','10:30 AM'),
    ('11:00 AM','11:00 AM'),
    ('11:30 AM','11:30 AM'),
    ('12:00 PM','12:00 PM'),
    ('12:30 PM','12:30 PM'),
    ('01:00 PM','1:00 PM'),
    ('01:30 PM','1:30 PM'),
    ('02:00 PM','2:00 PM'),
    ('02:30 PM','2:30 PM'),
    ('03:00 PM','3:00 PM'),
    ('03:30 PM','3:30 PM'),
    ('04:00 PM','4:00 PM'),
    ('04:30 PM','4:30 PM'),
    ('05:00 PM','5:00 PM'),
    ('05:30 PM','5:30 PM'),
    ('06:00 PM','6:00 PM'),
    ('06:30 PM','6:30 PM'),
    ('07:00 PM','7:00 PM'),
    ('07:30 PM','7:30 PM'),
    ('08:00 PM','8:00 PM'),
    ('08:30 PM','8:30 PM'),
    ('09:00 PM','9:00 PM'),
    ('09:30 PM','9:30 PM'),
    ('10:00 PM','10:00 PM'),
    ('10:30 PM','10:30 PM'),
    ('11:00 PM','11:00 PM'),
    ('11:30 PM','11:30 PM')
]

US_STATES = [
    ('', '-- Select --'),
    ('AK','Alaska'),
    ('AL','Alabama'),
    ('AR','Arkansas'),
    ('AZ','Arizona'),
    ('CA','California'),
    ('CO','Colorado'),
    ('CT','Connecticut'),
    ('DC','District of Columbia'),
    ('DE','Delaware'),
    ('FL','Florida'),
    ('GA','Georgia'),
    ('GU','Guam'),
    ('HI','Hawaii'),
    ('IA','Iowa'),
    ('ID','Idaho'),
    ('IL','Illinois'),
    ('IN','Indiana'),
    ('KS','Kansas'),
    ('KY','Kentucky'),
    ('LA','Louisiana'),
    ('MA','Massachusetts'),
    ('MD','Maryland'),
    ('ME','Maine'),
    ('MI','Michigan'),
    ('MN','Minnesota'),
    ('MO','Missouri'),
    ('MS','Mississippi'),
    ('MT','Montana'),
    ('NC','North Carolina'),
    ('ND','North Dakota'),
    ('NE','Nebraska'),
    ('NH','New Hampshire'),
    ('NJ','New Jersey'),
    ('NM','New Mexico'),
    ('NV','Nevada'),
    ('NY','New York'),
    ('OH','Ohio'),
    ('OK','Oklahoma'),
    ('OR','Oregon'),
    ('PA','Pennsylvania'),
    ('PR','Puerto Rico'),
    ('RI','Rhode Island'),
    ('SC','South Carolina'),
    ('SD','South Dakota'),
    ('TN','Tennessee'),
    ('TX','Texas'),
    ('UT','Utah'),
    ('VA','Virginia'),
    ('VT','Vermont'),
    ('WA','Washington'),
    ('WI','Wisconsin'),
    ('WV','West Virginia'),
    ('WY','Wyoming')
]


COUNTRY = [
    ()
]
"""
option value="ALB">Albania</option><option value="DZA">Algeria</option><option value="ASM">American Samoa</option><option value="AND">Andorra</option><option value="AGO">Angola</option><option value="AIA">Anguilla</option><option value="ATA">Antarctica</option><option value="ATG">Antigua and Barbuda</option><option value="ARG">Argentina</option><option value="ARM">Armenia</option><option value="ABW">Aruba</option><option value="AUS">Australia</option><option value="AUT">Austria</option><option value="AZE">Azerbaijan</option><option value="BHS">Bahamas</option><option value="BHR">Bahrain</option><option value="BGD">Bangladesh</option><option value="BRB">Barbados</option><option value="BLR">Belarus</option><option value="BEL">Belgium</option><option value="BLZ">Belize</option><option value="BEN">Benin</option><option value="BMU">Bermuda</option><option value="BTN">Bhutan</option><option value="BOL">Bolivia</option><option value="BES">Bonaire, Sint Eustatius and Saba</option><option value="BIH">Bosnia and Herzegovina</option><option value="BWA">Botswana</option><option value="BVT">Bouvet Island</option><option value="BRA">Brazil</option><option value="IOT">British Indian Ocean Territory</option><option value="VGB">British Virgin Islands</option><option value="BRN">Brunei</option><option value="BGR">Bulgaria</option><option value="BFA">Burkina Faso</option><option value="BDI">Burundi</option><option value="KHM">Cambodia</option><option value="CMR">Cameroon</option><option value="CAN">Canada</option><option value="CPV">Cape Verde</option><option value="CYM">Cayman Islands</option><option value="CAF">Central African Republic</option><option value="TCD">Chad</option><option value="CHL">Chile</option><option value="CHN">China</option><option value="CXR">Christmas Island</option><option value="CCK">Cocos Islands</option><option value="COL">Colombia</option><option value="COM">Comoros</option><option value="COK">Cook Islands</option><option value="CRI">Costa Rica</option><option value="HRV">Croatia</option><option value="CUW">Curacao</option><option value="CYP">Cyprus</option><option value="CZE">Czech Republic</option><option value="DNK">Denmark</option><option value="DJI">Djibouti</option><option value="DMA">Dominica</option><option value="DOM">Dominican Republic</option><option value="ECU">Ecuador</option><option value="EGY">Egypt</option><option value="SLV">El Salvador</option><option value="GNQ">Equatorial Guinea</option><option value="ERI">Eritrea</option><option value="EST">Estonia</option><option value="ETH">Ethiopia</option><option value="FLK">Falkland Islands</option><option value="FRO">Faroe Islands</option><option value="SOM">Federal Republic of Somalia</option><option value="FSM">Federated States of Micronesia</option><option value="FJI">Fiji</option><option value="FIN">Finland</option><option value="FRA">France</option><option value="GUF">French Guiana</option><option value="PYF">French Polynesia</option><option value="ATF">French Southern and Antarctic Territories</option><option value="GAB">Gabon</option><option value="GMB">Gambia</option><option value="GEO">Georgia</option><option value="DEU">Germany</option><option value="GHA">Ghana</option><option value="GIB">Gibraltar</option><option value="GRC">Greece</option><option value="GRL">Greenland</option><option value="GRD">Grenada</option><option value="GLP">Guadeloupe</option><option value="GUM">Guam</option><option value="GTM">Guatemala</option><option value="GIN">Guinea</option><option value="GNB">Guinea-Bissau</option><option value="GUY">Guyana</option><option value="HTI">Haiti</option><option value="HMD">Heard and McDonald Islands</option><option value="HND">Honduras</option><option value="HKG">Hong Kong</option><option value="HUN">Hungary</option><option value="ISL">Iceland</option><option value="IND">India</option><option value="IDN">Indonesia</option><option value="IRL">Ireland</option><option value="ISR">Israel</option><option value="ITA">Italy</option><option value="JAM">Jamaica</option><option value="JPN">Japan</option><option value="JOR">Jordan</option><option value="KAZ">Kazakhstan</option><option value="KEN">Kenya</option><option value="KIR">Kiribati</option><option value="KWT">Kuwait</option><option value="KGZ">Kyrgyzstan</option><option value="LAO">Laos</option><option value="LVA">Latvia</option><option value="LBN">Lebanon</option><option value="LSO">Lesotho</option><option value="LBY">Libya</option><option value="LIE">Liechtenstein</option><option value="LTU">Lithuania</option><option value="LUX">Luxembourg</option><option value="MAC">Macau</option><option value="MKD">Macedonia</option><option value="MDG">Madagascar</option><option value="MWI">Malawi</option><option value="MYS">Malaysia</option><option value="MDV">Maldives</option><option value="MLT">Malta</option><option value="MHL">Marshall Islands</option><option value="MTQ">Martinique</option><option value="MRT">Mauritania</option><option value="MUS">Mauritius</option><option value="MYT">Mayotte</option><option value="MEX">Mexico</option><option value="MDA">Moldova</option><option value="MCO">Monaco</option><option value="MNG">Mongolia</option><option value="MNE">Montenegro</option><option value="MSR">Montserrat</option><option value="MAR">Morocco</option><option value="MOZ">Mozambique</option><option value="MMR">Myanmar</option><option value="NAM">Namibia</option><option value="NRU">Nauru</option><option value="NPL">Nepal</option><option value="NLD">Netherlands</option><option value="NCL">New Caledonia</option><option value="NZL">New Zealand</option><option value="NIC">Nicaragua</option><option value="NER">Niger</option><option value="NGA">Nigeria</option><option value="NIU">Niue</option><option value="NFK">Norfolk Island</option><option value="MNP">Northern Mariana Islands</option><option value="NOR">Norway</option><option value="OMN">Oman</option><option value="PAK">Pakistan</option><option value="PLW">Palau</option><option value="PAN">Panama</option><option value="PNG">Papua New Guinea</option><option value="PRY">Paraguay</option><option value="PER">Peru</option><option value="PHL">Philippines</option><option value="PCN">Pitcairn Island</option><option value="POL">Poland</option><option value="PRT">Portugal</option><option value="PRI">Puerto Rico</option><option value="QAT">Qatar</option><option value="COG">Republic of the Congo</option><option value="REU">Reunion</option><option value="ROU">Romania</option><option value="RUS">Russia</option><option value="RWA">Rwanda</option><option value="WSM">Samoa</option><option value="SMR">San Marino</option><option value="STP">Sao Tome and Principe</option><option value="SAU">Saudi Arabia</option><option value="SEN">Senegal</option><option value="SRB">Serbia</option><option value="SYC">Seychelles</option><option value="SLE">Sierra Leone</option><option value="SGP">Singapore</option><option value="SXM">Sint Maarten</option><option value="SVK">Slovakia</option><option value="SVN">Slovenia</option><option value="SLB">Solomon Islands</option><option value="ZAF">South Africa</option><option value="SGS">South Georgia and the South Islands</option><option value="KOR">South Korea</option><option value="ESP">Spain</option><option value="LKA">Sri Lanka</option><option value="BLM">St. Barthelemy</option><option value="SHN">St. Helena</option><option value="KNA">St. Kitts and Nevis</option><option value="LCA">St. Lucia</option><option value="MAF">St. Martin</option><option value="SPM">St. Pierre and Miquelon</option><option value="VCT">St. Vincent and the Grenadines</option><option value="PSE">State of Palestine</option><option value="SUR">Suriname</option><option value="SJM">Svalbard</option><option value="SWZ">Swaziland</option><option value="SWE">Sweden</option><option value="CHE">Switzerland</option><option value="TWN">Taiwan</option><option value="TJK">Tajikistan</option><option value="TZA">Tanzania</option><option value="THA">Thailand</option><option value="TLS">Timor Leste</option><option value="TGO">Togo</option><option value="TKL">Tokelau</option><option value="TON">Tonga</option><option value="TTO">Trinidad and Tobago</option><option value="TUN">Tunisia</option><option value="TUR">Turkey</option><option value="TKM">Turkmenistan</option><option value="TCA">Turks and Caicos</option><option value="TUV">Tuvalu</option><option value="VIR">U.S. Virgin Islands</option><option value="UGA">Uganda</option><option value="UKR">Ukraine</option><option value="ARE">United Arab Emirates</option><option value="GBR">United Kingdom</option><option value="USA" selected="selected">United States of America</option><option value="URY">Uruguay</option><option value="UMI">US Minor Outlying Islands</option><option value="UZB">Uzbekistan</option><option value="VUT">Vanuatu</option><option value="VAT">Vatican City</option><option value="VEN">Venezuela</option><option value="VNM">Vietnam</option><option value="WLF">Wallis and Futuna</option><option value="ESH">Western Sahara</option><option value="ZMB">Zambia</option><option value="ZWE">Zimbabwe</option></select>        </div>
    </div>
"""
CC_BALANCED_ACCEPTED = [
    ('visa', 'Visa'),
    ('mastercard', 'MasterCard'),
    ('amex', 'AmericanExpress'),
    ('discover', 'Discover')
]



LANGUAGES = [
    ('Arabic','Arabic'),
    ('Chinese','Chinese'),('English','English'),('French','French'),
    ('German','German'),('Hebrew','Hebrew'),('Hindi','Hindi'),('Italian','Italian'),
    ('Japanese','Japanese'),('Korean','Korean'),('Portuguese','Portugese'),
    ('Russian','Russian'),('Spanish','Spanish'),('Other','Other')
]

GENDER = [
    ('','-- Select Gender --',),
    ('Female', 'Female'),
    ('Male', 'Male')
]

FAMILY_RELATION = [
    ('', '-- Select Relationship --'),
    ('Child','Child')
]
"""
[
    ('', '-- Select Relationship --'),
    ('Child','Child'),
    ('Parent','Parent'),
    ('Grandparent','Grandparent')
    ('Extended Family','Extended Family'),
    ('Friend','Friend'),
    ('Other','Other')
]
"""

PET_SPECIE = [
    ('', '-- Select Animal --'),
    ('Dog','Dog'),
    ('Cat','Cat'),
    ('Other','Other'),
]


PROVIDER_AGE = [
    ('None','-- Select Age --'),('less-than-20', 'Under 20'), ('20s', '20s'), ('30s', '30s'), ('40s', '40s'),
    ('50s', '50s'), ('60-and-over', '60s and over')
]

PROVIDER_DISTANCE_TO_TRAVEL = [
    ('None','-- Select Miles --'),('5','5 miles'),('10', '10 miles'), ('15', '15 miles'), ('20','20 miles'),
    ('25','25 miles'),('30','30 miles'),('40','40 miles'),('50','50 miles'),('60','60 miles'),('60+','60+ miles')
]

PROVIDER_TRANSPORTATION = [
    ('None','-- Select Transportation --'),('myown', 'I have my own'),
    ('pickedup','I need to be picked up')
]

PROVIDER_INTERVIEW_LOCATIONS = [
    ('Phone', 'Phone'),
    ('Skype','Skype'),
    ('provider_home', "My Home"),
    ('provider_facility', "My Facility"),
    ('receiver_home',"Client's Home"),
    ('Other','Other (Provided by Client')
]

PROVIDER_EDUCATION_LIST = [
    ('None','-- Select Education --'),('highschool','High School'),
    ('bachelors',"Bachelor's Degree"),('masters','Masters Degree'),
    ('phd','PhD'),('postdoc','Post-Doctorate')
]

PROVIDER_YEARS_EXPERIENCE = [
    ('None','-- Select Experience --'),('1','1 year'),('1_2','1 to 2 years'),
    ('2_4','2 to 4 years'),('4_6','4 to 6 years'),('6_10', '6 to 10 years'),
    ('10_14','10 to 14 years'),('14_20','14 to 20 years'),('20_26','20 to 26 years'),
    ('26_plus','26+ years')
]


MSG_MAX = 1000
ABOUT_MAX = 1000
SERVICE_MENU_ITEM_MAX = 20
SERVICE_DETAIL_MAX = 1000


EMAIL_NOREPLY = 'KikLearn <donotreply@kiklearn.com>'
