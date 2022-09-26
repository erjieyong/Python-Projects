import streamlit as st
import requests
import json

# Title of the page
st.title("Ames House Price Prediction")

#split into 3 columns
col1, col2 , col3 = st.columns(3)

with col1:
# Get user inputs
subclass = st.selectbox("Building Class: ", (20,30,40,45,50,60,70,75,80,85,90,120,150,160,180,190), help = '''20 1-STORY 1946 & NEWER ALL STYLES\n
30 1-STORY 1945 & OLDER\n
40 1-STORY W/FINISHED ATTIC ALL AGES\n
45 1-1/2 STORY - UNFINISHED ALL AGES\n
50 1-1/2 STORY FINISHED ALL AGES\n
60 2-STORY 1946 & NEWER\n
70 2-STORY 1945 & OLDER\n
75 2-1/2 STORY ALL AGES\n
80 SPLIT OR MULTI-LEVEL\n
85 SPLIT FOYER\n
90 DUPLEX - ALL STYLES AND AGES\n
120 1-STORY PUD (Planned Unit Development) - 1946 & NEWER\n
150 1-1/2 STORY PUD - ALL AGES\n
160 2-STORY PUD - 1946 & NEWER\n
180 PUD - MULTILEVEL - INCL SPLIT LEV/FOYER\n
190 2 FAMILY CONVERSION - ALL STYLES AND AGES''')

zoning = st.selectbox("Zoning: ", ('RL', 'RM', 'FV', 'C (all)', 'A (agr)', 'RH', 'I (all)'), help = '''A Agriculture\n
C Commercial\n
FV Floating Village Residential\n
I Industrial\n
RH Residential High Density\n
RL Residential Low Density\n
RP Residential Low Density Park\n
RM Residential Medium Density
''')


with col2:
lotfrontage = st.number_input("Lot Frontage: ", min_value = 0, help="Linear feet of street connected to property")

lotarea = st.number_input("Lot Area: ", min_value = 0, help="Lot size in square feet")

street = st.selectbox("Street: ", ('Pave', 'Grvl'), help = '''Grvl Gravel\n
Pave Paved
''')

alley = st.selectbox("Alley: ", ('0', 'Pave', 'Grvl'), help = '''Grvl Gravel\n
Pave Paved\n
NA No alley access
''')
with col3:
lotshape = st.selectbox("Lot Shape: ", ('Reg', 'IR1', 'IR2', 'IR3'), help = '''Reg Regular\n
IR1 Slightly irregular\n
IR2 Moderately Irregular\n
IR3 Irregular
''')

landcontour = st.selectbox("Land Contour: ", ('Lvl', 'HLS', 'Bnk', 'Low'), help = '''Lvl Near Flat/Level\n
Bnk Banked - Quick and significant rise from street grade to building\n
HLS Hillside - Significant slope from side to side\n
Low Depression
''')

utilities = st.selectbox("Utilities: ", ('AllPub', 'NoSeWa', 'NoSewr'), help = '''AllPub All public Utilities (E,G,W,& S)\n
NoSewr Electricity, Gas, and Water (Septic Tank)\n
NoSeWa Electricity and Gas Only\n
ELO Electricity only
''')

lotconfig = st.selectbox("Lot Config: ", ('Inside', 'CulDSac', 'Corner', 'FR2', 'FR3'), help = '''Inside Inside lot\n
Corner Corner lot\n
CulDSac Cul-de-sac\n
FR2 Frontage on 2 sides of property\n
FR3 Frontage on 3 sides of property
''')

landslope = st.selectbox("Land Slope: ", ('Gtl', 'Sev', 'Mod'), help = '''Gtl Gentle slope\n
Mod Moderate Slope\n
Sev Severe Slope
''')

neighborhood = st.selectbox("Neighborhood: ", ('NAmes', 'Sawyer', 'SawyerW', 'Timber', 'Edwards', 'OldTown','BrDale', 'CollgCr', 
                                               'Somerst', 'Mitchel', 'StoneBr', 'NridgHt','Gilbert', 'Crawfor', 'IDOTRR', 'NWAmes',
                                               'Veenker', 'MeadowV','SWISU', 'NoRidge', 'ClearCr', 'Blmngtn', 'BrkSide', 'NPkVill',
                                               'Blueste', 'GrnHill', 'Greens', 'Landmrk'), help = '''Blmngtn Bloomington Heights\n
Blueste Bluestem\n
BrDale Briardale\n
BrkSide Brookside\n
ClearCr Clear Creek\n
CollgCr College Creek\n
Crawfor Crawford\n
Edwards Edwards\n
Gilbert Gilbert\n
IDOTRR Iowa DOT and Rail Road\n
MeadowV Meadow Village\n
Mitchel Mitchell\n
Names North Ames\n
NoRidge Northridge\n
NPkVill Northpark Villa\n
NridgHt Northridge Heights\n
NWAmes Northwest Ames\n
OldTown Old Town\n
SWISU South & West of Iowa State University\n
Sawyer Sawyer\n
SawyerW Sawyer West\n
Somerst Somerset\n
StoneBr Stone Brook\n
Timber Timberland\n
Veenker Veenker
''')

condition1 = st.selectbox("Condition 1: ", ('Norm', 'RRAe', 'PosA', 'Artery', 'Feedr', 'PosN', 'RRAn', 'RRNe',
       'RRNn'), help = '''Artery Adjacent to arterial street\n
Feedr Adjacent to feeder street\n
Norm Normal\n
RRNn Within 200' of North-South Railroad\n
RRAn Adjacent to North-South Railroad\n
PosN Near positive off-site feature--park, greenbelt, etc.\n
PosA Adjacent to postive off-site feature\n
RRNe Within 200' of East-West Railroad\n
RRAe Adjacent to East-West Railroad
''')

condition2 = st.selectbox("Condition 2: ", ('Norm', 'RRNn', 'Feedr', 'Artery', 'PosA', 'PosN', 'RRAe', 'RRAn'), help = '''Artery Adjacent to arterial street\n
Feedr Adjacent to feeder street\n
Norm Normal\n
RRNn Within 200' of North-South Railroad\n
RRAn Adjacent to North-South Railroad\n
PosN Near positive off-site feature--park, greenbelt, etc.\n
PosA Adjacent to postive off-site feature\n
RRNe Within 200' of East-West Railroad\n
RRAe Adjacent to East-West Railroad
''')

bldgtype = st.selectbox("Bldg Type: ", ('1Fam', 'TwnhsE', 'Twnhs', '2fmCon', 'Duplex'), help = '''1Fam Single-family Detached\n
2FmCon Two-family Conversion; originally built as one-family dwelling\n
Duplx Duplex\n
TwnhsE Townhouse End Unit\n
TwnhsI Townhouse Inside Unit
''')

housetyle = st.selectbox("House Style: ", ('1Story', '2Story', '1.5Fin', 'SFoyer', 'SLvl', '2.5Unf', '2.5Fin',
       '1.5Unf'), help = '''1Story One story\n
1.5Fin One and one-half story: 2nd level finished\n
1.5Unf One and one-half story: 2nd level unfinished\n
2Story Two story\n
2.5Fin Two and one-half story: 2nd level finished\n
2.5Unf Two and one-half story: 2nd level unfinished\n
SFoyer Split Foyer\n
SLvl Split Level
''')

overallqual = st.selectbox("Overall Qual: ", (5.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 10.0), help = '''10 Very Excellent\n
9 Excellent\n
8 Very Good\n
7 Good\n
6 Above Average\n
5 Average\n
4 Below Average\n
3 Fair\n
2 Poor\n
1 Very Poor
''')

overallcond = st.selectbox("Overall Cond: ", (5.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 10.0), help = '''10 Very Excellent\n
9 Excellent\n
8 Very Good\n
7 Good\n
6 Above Average\n
5 Average\n
4 Below Average\n
3 Fair\n
2 Poor\n
1 Very Poor
''')

yearbuilt = st.number_input("Year Built: ", min_value = 0, max_value = 2022, help="Original construction date")

yearremodadd = st.number_input("Year Remod/Add: ", min_value = 0, max_value = 2022, help="Remodel date (same as construction date if no remodeling or additions)")

roofstyle = st.selectbox("Roof Style: ", ('Gable', 'Hip', 'Flat', 'Mansard', 'Shed', 'Gambrel'), help = '''Flat Flat\n
Gable Gable\n
Gambrel Gabrel (Barn)\n
Hip Hip\n
Mansard Mansard\n
Shed Shed
''')

roofmatl = st.selectbox("Roof Matl: ", ('CompShg', 'WdShngl', 'Tar&Grv', 'WdShake', 'Membran', 'ClyTile'), help = '''ClyTile Clay or Tile\n
CompShg Standard (Composite) Shingle\n
Membran Membrane\n
Metal Metal\n
Roll Roll\n
Tar&Grv Gravel & Tar\n
WdShake Wood Shakes\n
WdShngl Wood Shingles
''')

exterior1st = st.selectbox("Exterior 1st: ", ('VinylSd', 'HdBoard', 'Wd Sdng', 'BrkFace', 'Plywood', 'MetalSd',
                                              'AsbShng', 'CemntBd', 'WdShing', 'Stucco', 'BrkComm', 'Stone',
                                              'CBlock', 'ImStucc', 'AsphShn'), help = '''AsbShng Asbestos Shingles\n
AsphShn Asphalt Shingles\n
BrkComm Brick Common\n
BrkFace Brick Face\n
CBlock Cinder Block\n
CemntBd Cement Board\n
HdBoard Hard Board\n
ImStucc Imitation Stucco\n
MetalSd Metal Siding\n
Other Other\n
Plywood Plywood\n
PreCast PreCast\n
Stone Stone\n
Stucco Stucco\n
VinylSd Vinyl Siding\n
Wd Sdng Wood Siding\n
WdShing Wood Shingles
''')

masvnrtype = st.selectbox("Mas Vnr Type: ", ('None', 'BrkFace', 'Stone', 'BrkCmn', 'CBlock'), help = '''BrkCmn Brick Common\n
BrkFace Brick Face\n
CBlock Cinder Block\n
None None\n
Stone Stone
''')

masvnrarea= st.number_input("Mas Vnr Area: ", min_value = 0, help="Masonry veneer area in square feet")

exterqual = st.selectbox("Exter Qual: ", ('TA', 'Gd', 'Ex', 'Fa', 'Po'), help = '''Ex Excellent\n
Gd Good\n
TA Average/Typical\n
Fa Fair\n
Po Poor
''')

extercond = st.selectbox("Exter Cond: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent\n
Gd Good\n
TA Average/Typical\n
Fa Fair\n
Po Poor
''')

foundation = st.selectbox("Foundation: ", ('PConc', 'CBlock', 'BrkTil', 'Slab', 'Stone', 'Wood'), help = '''BrkTil Brick & Tile\n
CBlock Cinder Block\n
PConc Poured Contrete\n
Slab Slab\n
Stone Stone\n
Wood Wood
''')

bsmtqual = st.selectbox("Bsmt Qual: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent (100+ inches)\n
Gd Good (90-99 inches)\n
TA Typical (80-89 inches)\n
Fa Fair (70-79 inches)\n
Po Poor (<70 inches)\n
NA No Basement
''')


bsmtcond = st.selectbox("Bsmt Cond: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent\n
Gd Good\n
TA Typical - slight dampness allowed\n
Fa Fair - dampness or some cracking or settling\n
Po Poor - Severe cracking, settling, or wetness\n
NA No Basement
''')

bsmtexposure = st.selectbox("Bsmt Exposure: ", ('No', 'Gd', 'Av', 'Mn', 'NA') , help = '''Gd Good Exposure\n
Av Average Exposure (split levels or foyers typically score average or above)\n
Mn Mimimum Exposure\n
No No Exposure\n
NA No Basement
''')

bsmtfintype1 = st.selectbox("BsmtFin Type 1: ", ('GLQ', 'Unf', 'ALQ', 'Rec', 'BLQ', 'LwQ', 'NA'), help = '''GLQ Good Living Quarters\n
ALQ Average Living Quarters\n
BLQ Below Average Living Quarters\n
Rec Average Rec Room\n
LwQ Low Quality\n
Unf Unfinshed\n
NA No Basement
''')

bsmtfinsf1 = st.number_input("BsmtFin SF 1: ", min_value = 0, help="Type 1 finished square feet")

bsmtfintype2 = st.selectbox("BsmtFin Type 2: ", ('Unf', 'GLQ', 'ALQ', 'Rec', 'BLQ', 'LwQ', 'NA'), help = '''GLQ Good Living Quarters\n
ALQ Average Living Quarters\n
BLQ Below Average Living Quarters\n
Rec Average Rec Room\n
LwQ Low Quality\n
Unf Unfinshed\n
NA No Basement
''')

bsmtfinsf2 = st.number_input("BsmtFin SF 2: ", min_value = 0, help="Type 2 finished square feet")

bsmtunfsf = st.number_input("Bsmt Unf SF: ", min_value = 0, help="Type 2 finished square feet")

heating = st.selectbox("Heating: ", ('GasA', 'GasW', 'Grav', 'Wall', 'OthW'), help = '''Floor Floor Furnace\n
GasA Gas forced warm air furnace\n
GasW Gas hot water or steam heat\n
Grav Gravity furnace\n
OthW Hot water or steam heat other than gas\n
Wall Wall furnace
''')

heatingqc = st.selectbox("Heating QC: ", ('Ex', 'TA', 'Gd', 'Fa', 'Po'), help = '''Ex Excellent\n
Gd Good\n
TA Average/Typical\n
Fa Fair\n
Po Poor
''')

centralair = st.selectbox("Central Air: ", ('Y', 'N'), help = '''N No\n
Y Yes
''')

electrical = st.selectbox("Electrical: ", ('SBrkr', 'FuseF', 'FuseA', 'FuseP', 'Mix'), help = '''SBrkr Standard Circuit Breakers & Romex\n
FuseA Fuse Box over 60 AMP and all Romex wiring (Average)\n
FuseF 60 AMP Fuse Box and mostly Romex wiring (Fair)\n
FuseP 60 AMP Fuse Box and mostly knob & tube wiring (poor)\n
Mix Mixed
''')

firstflrsf = st.number_input("1st Flr SF: ", min_value = 0, help="First Floor square feet")

secondflrsf = st.number_input("2nd Flr SF: ", min_value = 0, help="Second floor square feet")

lowqualfinsf = st.number_input("Low Qual Fin SF: ", min_value = 0, help="Low quality finished square feet (all floors)")

grlivarea = st.number_input("Gr Liv Area: ", min_value = 0, help="Above grade (ground) living area square feet")

bsmtfullbath = st.number_input("Bsmt Full Bath: ", min_value = 0, help="Basement full bathrooms")

bsmthalfbath = st.number_input("Bsmt Half Bath: ", min_value = 0, help="Basement half bathrooms")

fullbath = st.number_input("Full Bath: ", min_value = 0, help="Full bathrooms above grade")

halfbath = st.number_input("Half Bath: ", min_value = 0, help="Half baths above grade")

bedroomabvgr = st.number_input("Bedroom AbvGr: ", min_value = 0, help="Number of bedrooms above basement level")

kitchenabvgr = st.number_input("Kitchen AbvGr: ", min_value = 0, help="Number of kitchens")

kitchenqual = st.selectbox("Kitchen Qual: ", ('TA', 'Gd', 'Fa', 'Ex'), help = '''Ex Excellent\n
Gd Good\n
TA Typical/Average\n
Fa Fair\n
Po Poor
''')

functional = st.selectbox("Functional: ", ('Typ', 'Mod', 'Min2', 'Maj1', 'Min1', 'Sev', 'Sal', 'Maj2'), help = '''Typ Typical Functionality\n
Min1 Minor Deductions 1\n
Min2 Minor Deductions 2\n
Mod Moderate Deductions\n
Maj1 Major Deductions 1\n
Maj2 Major Deductions 2\n
Sev Severely Damaged\n
Sal Salvage only
''')

fireplaces = st.number_input("Fireplaces: ", min_value = 0, help="Number of fireplaces")

garagetype = st.selectbox("Garage Type: ", ('Attchd', 'Detchd', 'BuiltIn', 'Basment', '2Types', 'CarPort', 'NA'), help = '''2Types More than one type of garage\n
Attchd Attached to home\n
Basment Basement Garage\n
BuiltIn Built-In (Garage part of house - typically has room above garage)\n
CarPort Car Port\n
Detchd Detached from home\n
NA No Garage
''')

garagefinish = st.selectbox("Garage Finish: ", ('Unf', 'RFn', 'Fin', 'MA'), help = '''Fin Finished\n
RFn Rough Finished\n
Unf Unfinished\n
NA No Garage
''')

garagearea = st.number_input("Garage Area: ", min_value = 0, help="Size of garage in square feet")

garagecond = st.selectbox("Garage Cond: ", ('TA', 'Fa', 'Po', 'Gd', 'Ex', 'NA'), help = '''Ex Excellent\n
Gd Good\n
TA Typical/Average\n
Fa Fair\n
Po Poor\n
NA No Garage
''')

paveddrive = st.selectbox("Paved Drive: ", ('Y', 'N', 'P'), help = '''Y Paved\n
P Partial Pavement\n
N Dirt/Gravel
''')

wooddecksf = st.number_input("Wood Deck SF: ", min_value = 0, help="Wood deck area in square feet")

openporchsf = st.number_input("Open Porch SF: ", min_value = 0, help="Open porch area in square feet")

enclosedporch = st.number_input("Enclosed Porch: ", min_value = 0, help="Enclosed porch area in square feet")

threessnporch = st.number_input("3Ssn Porch: ", min_value = 0, help="Three season porch area in square feet")

screenporch = st.number_input("Screen Porch: ", min_value = 0, help="Screen porch area in square feet")

poolarea = st.number_input("Pool Area: ", min_value = 0, help="Pool area in square feet")

fence = st.selectbox("Fence: ", ('NA', 'MnPrv', 'GdPrv', 'GdWo', 'MnWw'), help = '''GdPrv Good Privacy\n
MnPrv Minimum Privacy\n
GdWo Good Wood\n
MnWw Minimum Wood/Wire\n
NA No Fence
''')

miscfeature = st.selectbox("Misc Feature: ", ('NA', 'Shed', 'TenC', 'Gar2', 'Othr', 'Elev'), help = '''Elev Elevator\n
Gar2 2nd Garage (if not described in garage section)\n
Othr Other\n
Shed Shed (over 100 SF)\n
TenC Tennis Court\n
NA None
''')

miscval = st.number_input("Misc Val: ", min_value = 0, help="$Value of miscellaneous feature")

mosold = st.number_input("Mo Sold: ", min_value = 0, help="Month Sold")

yrsold = st.number_input("Yr Sold: ", min_value = 0, help="Year Sold")

saletype = st.selectbox("Sale Type: ", ('WD ', 'New', 'COD', 'ConLD', 'Con', 'CWD', 'Oth', 'ConLI','ConLw'), help = '''WD Warranty Deed - Conventional\n
CWD Warranty Deed - Cash\n
VWD Warranty Deed - VA Loan\n
New Home just constructed and sold\n
COD Court Officer Deed/Estate\n
Con Contract 15% Down payment regular terms\n
ConLw Contract Low Down payment and low interest\n
ConLI Contract Low Interest\n
ConLD Contract Low Down\n
Oth Other
''')


# Display the inputs
user_input = {'MS SubClass' : subclass, 
              'MS Zoning' : zoning, 
              'Lot Frontage' : lotfrontage, 
              'Lot Area' : lotarea, 
              'Street' : street,
              'Alley' : alley, 
              'Lot Shape' : lotshape, 
              'Land Contour' : landcontour,
              'Utilities' : utilities, 
              'Lot Config' : lotconfig,
              'Land Slope' : landslope, 
              'Neighborhood' : neighborhood, 
              'Condition 1' : condition1, 
              'Condition 2' : condition2, 
              'Bldg Type' : bldgtype,
              'House Style' : housetyle, 
              'Overall Qual' : overallqual, 
              'Overall Cond' : overallcond, 
              'Year Built' : yearbuilt,
              'Year Remod/Add' : yearremodadd, 
              'Roof Style' : roofstyle, 
              'Roof Matl' : roofmatl, 
              'Exterior 1st' : exterior1st,
              'Mas Vnr Type' : masvnrtype, 
              'Mas Vnr Area' : masvnrarea, 
              'Exter Qual' : exterqual, 
              'Exter Cond' : extercond,
              'Foundation' : foundation, 
              'Bsmt Qual' : bsmtqual, 
              'Bsmt Cond' : bsmtcond, 
              'Bsmt Exposure' : bsmtexposure,
              'BsmtFin Type 1' : bsmtfintype1, 
              'BsmtFin SF 1' : bsmtfinsf1, 
              'BsmtFin Type 2' : bsmtfintype2, 
              'BsmtFin SF 2' : bsmtfinsf2,
              'Bsmt Unf SF' : bsmtunfsf, 
              'Heating' : heating, 
              'Heating QC' : heatingqc, 
              'Central Air' : centralair, 
              'Electrical' : electrical,
              '1st Flr SF' : firstflrsf, 
              '2nd Flr SF' : secondflrsf, 
              'Low Qual Fin SF' : lowqualfinsf, 
              'Gr Liv Area' : grlivarea,
              'Bsmt Full Bath' : bsmtfullbath,
              'Bsmt Half Bath' : bsmthalfbath, 
              'Full Bath' : fullbath, 
              'Half Bath' : halfbath,
              'Bedroom AbvGr' : bedroomabvgr, 
              'Kitchen AbvGr' : kitchenabvgr, 
              'Kitchen Qual' : kitchenqual, 
              'Functional' : functional,
              'Fireplaces' : fireplaces, 
              'Garage Type' : garagetype, 
              'Garage Finish' : garagefinish, 
              'Garage Area' : garagearea,
              'Garage Cond' : garagecond, 
              'Paved Drive' : paveddrive, 
              'Wood Deck SF' : wooddecksf,
              'Open Porch SF' : openporchsf,
              'Enclosed Porch' : enclosedporch,
              '3Ssn Porch' : threessnporch, 
              'Screen Porch' : screenporch, 
              'Pool Area' : poolarea, 
              'Fence' : fence,
              'Misc Feature' : miscfeature,
              'Misc Val' : miscval, 
              'Mo Sold' : mosold, 
              'Yr Sold' : yrsold, 
              'Sale Type' : saletype}
st.write(user_input)

# Code to post the user inputs to the API and get the predictions
# Paste the URL to your GCP Cloud Run API here!
api_url = 'https://ames-house-price-predict-3azjia52jq-as.a.run.app'
api_route = '/predict'

response = requests.post(f'{api_url}{api_route}', json=json.dumps(user_input)) # json.dumps() converts dict to JSON
predictions = response.json()

# Add a submit button
if st.button("Submit"): 
    st.write(f"Prediction: {predictions['predictions'][0]}")
