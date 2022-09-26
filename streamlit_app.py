import streamlit as st
import requests
import json

# Title of the page
st.title("Ames House Price Prediction")

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

zoning = st.selectbox("Zoning: ", ('RL', 'RM', 'FV', 'C (all)', 'A (agr)', 'RH', 'I (all)'), help = '''A Agriculture
C Commercial
FV Floating Village Residential
I Industrial
RH Residential High Density
RL Residential Low Density
RP Residential Low Density Park
RM Residential Medium Density
''')

lotfrontage = st.number_input("Lot Frontage: ", min_value = 0, help="Linear feet of street connected to property")

lotarea = st.number_input("Lot Area: ", min_value = 0, help="Lot size in square feet")

street = st.selectbox("Street: ", ('Pave', 'Grvl'), help = '''Grvl Gravel
Pave Paved
''')

alley = st.selectbox("Alley: ", ('0', 'Pave', 'Grvl'), help = '''Grvl Gravel
Pave Paved
NA No alley access
''')

lotshape = st.selectbox("Lot Shape: ", ('Reg', 'IR1', 'IR2', 'IR3'), help = '''Reg Regular
IR1 Slightly irregular
IR2 Moderately Irregular
IR3 Irregular
''')

landcontour = st.selectbox("Land Contour: ", ('Lvl', 'HLS', 'Bnk', 'Low'), help = '''Lvl Near Flat/Level
Bnk Banked - Quick and significant rise from street grade to building
HLS Hillside - Significant slope from side to side
Low Depression
''')

utilities = st.selectbox("Utilities: ", ('AllPub', 'NoSeWa', 'NoSewr'), help = '''AllPub All public Utilities (E,G,W,& S)
NoSewr Electricity, Gas, and Water (Septic Tank)
NoSeWa Electricity and Gas Only
ELO Electricity only
''')

lotconfig = st.selectbox("Lot Config: ", ('Inside', 'CulDSac', 'Corner', 'FR2', 'FR3'), help = '''Inside Inside lot
Corner Corner lot
CulDSac Cul-de-sac
FR2 Frontage on 2 sides of property
FR3 Frontage on 3 sides of property
''')

landslope = st.selectbox("Land Slope: ", ('Gtl', 'Sev', 'Mod'), help = '''Gtl Gentle slope
Mod Moderate Slope
Sev Severe Slope
''')

neighborhood = st.selectbox("Neighborhood: ", ('NAmes', 'Sawyer', 'SawyerW', 'Timber', 'Edwards', 'OldTown','BrDale', 'CollgCr', 
                                               'Somerst', 'Mitchel', 'StoneBr', 'NridgHt','Gilbert', 'Crawfor', 'IDOTRR', 'NWAmes',
                                               'Veenker', 'MeadowV','SWISU', 'NoRidge', 'ClearCr', 'Blmngtn', 'BrkSide', 'NPkVill',
                                               'Blueste', 'GrnHill', 'Greens', 'Landmrk'), help = '''Blmngtn Bloomington Heights
Blueste Bluestem
BrDale Briardale
BrkSide Brookside
ClearCr Clear Creek
CollgCr College Creek
Crawfor Crawford
Edwards Edwards
Gilbert Gilbert
IDOTRR Iowa DOT and Rail Road
MeadowV Meadow Village
Mitchel Mitchell
Names North Ames
NoRidge Northridge
NPkVill Northpark Villa
NridgHt Northridge Heights
NWAmes Northwest Ames
OldTown Old Town
SWISU South & West of Iowa State University
Sawyer Sawyer
SawyerW Sawyer West
Somerst Somerset
StoneBr Stone Brook
Timber Timberland
Veenker Veenker
''')

condition1 = st.selectbox("Condition 1: ", ('Norm', 'RRAe', 'PosA', 'Artery', 'Feedr', 'PosN', 'RRAn', 'RRNe',
       'RRNn'), help = '''Artery Adjacent to arterial street
Feedr Adjacent to feeder street
Norm Normal
RRNn Within 200' of North-South Railroad
RRAn Adjacent to North-South Railroad
PosN Near positive off-site feature--park, greenbelt, etc.
PosA Adjacent to postive off-site feature
RRNe Within 200' of East-West Railroad
RRAe Adjacent to East-West Railroad
''')

condition2 = st.selectbox("Condition 2: ", ('Norm', 'RRNn', 'Feedr', 'Artery', 'PosA', 'PosN', 'RRAe', 'RRAn'), help = '''Artery Adjacent to arterial street
Feedr Adjacent to feeder street
Norm Normal
RRNn Within 200' of North-South Railroad
RRAn Adjacent to North-South Railroad
PosN Near positive off-site feature--park, greenbelt, etc.
PosA Adjacent to postive off-site feature
RRNe Within 200' of East-West Railroad
RRAe Adjacent to East-West Railroad
''')

bldgtype = st.selectbox("Bldg Type: ", ('1Fam', 'TwnhsE', 'Twnhs', '2fmCon', 'Duplex'), help = '''1Fam Single-family Detached
2FmCon Two-family Conversion; originally built as one-family dwelling
Duplx Duplex
TwnhsE Townhouse End Unit
TwnhsI Townhouse Inside Unit
''')

housetyle = st.selectbox("House Style: ", ('1Story', '2Story', '1.5Fin', 'SFoyer', 'SLvl', '2.5Unf', '2.5Fin',
       '1.5Unf'), help = '''1Story One story
1.5Fin One and one-half story: 2nd level finished
1.5Unf One and one-half story: 2nd level unfinished
2Story Two story
2.5Fin Two and one-half story: 2nd level finished
2.5Unf Two and one-half story: 2nd level unfinished
SFoyer Split Foyer
SLvl Split Level
''')

overallqual = st.selectbox("Overall Qual: ", (5.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 10.0), help = '''10 Very Excellent
9 Excellent
8 Very Good
7 Good
6 Above Average
5 Average
4 Below Average
3 Fair
2 Poor
1 Very Poor
''')

overallcond = st.selectbox("Overall Cond: ", (5.0, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 10.0), help = '''10 Very Excellent
9 Excellent
8 Very Good
7 Good
6 Above Average
5 Average
4 Below Average
3 Fair
2 Poor
1 Very Poor
''')

yearbuilt = st.number_input("Year Built: ", min_value = 0, max_value = 2022, help="Original construction date")

yearremodadd = st.number_input("Year Remod/Add: ", min_value = 0, max_value = 2022, help="Remodel date (same as construction date if no remodeling or additions)")

roofstyle = st.selectbox("Roof Style: ", ('Gable', 'Hip', 'Flat', 'Mansard', 'Shed', 'Gambrel'), help = '''Flat Flat
Gable Gable
Gambrel Gabrel (Barn)
Hip Hip
Mansard Mansard
Shed Shed
''')

roofmatl = st.selectbox("Roof Matl: ", ('CompShg', 'WdShngl', 'Tar&Grv', 'WdShake', 'Membran', 'ClyTile'), help = '''ClyTile Clay or Tile
CompShg Standard (Composite) Shingle
Membran Membrane
Metal Metal
Roll Roll
Tar&Grv Gravel & Tar
WdShake Wood Shakes
WdShngl Wood Shingles
''')

exterior1st = st.selectbox("Exterior 1st: ", ('VinylSd', 'HdBoard', 'Wd Sdng', 'BrkFace', 'Plywood', 'MetalSd',
                                              'AsbShng', 'CemntBd', 'WdShing', 'Stucco', 'BrkComm', 'Stone',
                                              'CBlock', 'ImStucc', 'AsphShn'), help = '''AsbShng Asbestos Shingles
AsphShn Asphalt Shingles
BrkComm Brick Common
BrkFace Brick Face
CBlock Cinder Block
CemntBd Cement Board
HdBoard Hard Board
ImStucc Imitation Stucco
MetalSd Metal Siding
Other Other
Plywood Plywood
PreCast PreCast
Stone Stone
Stucco Stucco
VinylSd Vinyl Siding
Wd Sdng Wood Siding
WdShing Wood Shingles
''')

masvnrtype = st.selectbox("Mas Vnr Type: ", ('None', 'BrkFace', 'Stone', 'BrkCmn', 'CBlock'), help = '''BrkCmn Brick Common
BrkFace Brick Face
CBlock Cinder Block
None None
Stone Stone
''')

masvnrarea= st.number_input("Mas Vnr Area: ", min_value = 0, help="Masonry veneer area in square feet")

exterqual = st.selectbox("Exter Qual: ", ('TA', 'Gd', 'Ex', 'Fa', 'Po'), help = '''Ex Excellent
Gd Good
TA Average/Typical
Fa Fair
Po Poor
''')

extercond = st.selectbox("Exter Cond: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent
Gd Good
TA Average/Typical
Fa Fair
Po Poor
''')

foundation = st.selectbox("Foundation: ", ('PConc', 'CBlock', 'BrkTil', 'Slab', 'Stone', 'Wood'), help = '''BrkTil Brick & Tile
CBlock Cinder Block
PConc Poured Contrete
Slab Slab
Stone Stone
Wood Wood
''')

bsmtqual = st.selectbox("Bsmt Qual: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent (100+ inches)
Gd Good (90-99 inches)
TA Typical (80-89 inches)
Fa Fair (70-79 inches)
Po Poor (<70 inches)
NA No Basement
''')


bsmtcond = st.selectbox("Bsmt Cond: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent
Gd Good
TA Typical - slight dampness allowed
Fa Fair - dampness or some cracking or settling
Po Poor - Severe cracking, settling, or wetness
NA No Basement
''')

bsmtexposure = st.selectbox("Bsmt Exposure: ", ('No', 'Gd', 'Av', 'Mn', 'NA') , help = '''Gd Good Exposure
Av Average Exposure (split levels or foyers typically score average or above)
Mn Mimimum Exposure
No No Exposure
NA No Basement
''')

bsmtfintype1 = st.selectbox("BsmtFin Type 1: ", ('GLQ', 'Unf', 'ALQ', 'Rec', 'BLQ', 'LwQ', 'NA'), help = '''GLQ Good Living Quarters
ALQ Average Living Quarters
BLQ Below Average Living Quarters
Rec Average Rec Room
LwQ Low Quality
Unf Unfinshed
NA No Basement
''')

bsmtfinsf1 = st.number_input("BsmtFin SF 1: ", min_value = 0, help="Type 1 finished square feet")

bsmtfintype2 = st.selectbox("BsmtFin Type 2: ", ('Unf', 'GLQ', 'ALQ', 'Rec', 'BLQ', 'LwQ', 'NA'), help = '''GLQ Good Living Quarters
ALQ Average Living Quarters
BLQ Below Average Living Quarters
Rec Average Rec Room
LwQ Low Quality
Unf Unfinshed
NA No Basement
''')

bsmtfinsf2 = st.number_input("BsmtFin SF 2: ", min_value = 0, help="Type 2 finished square feet")

bsmtunfsf = st.number_input("Bsmt Unf SF: ", min_value = 0, help="Type 2 finished square feet")

heating = st.selectbox("Heating: ", ('GasA', 'GasW', 'Grav', 'Wall', 'OthW'), help = '''Floor Floor Furnace
GasA Gas forced warm air furnace
GasW Gas hot water or steam heat
Grav Gravity furnace
OthW Hot water or steam heat other than gas
Wall Wall furnace
''')

heatingqc = st.selectbox("Heating QC: ", ('Ex', 'TA', 'Gd', 'Fa', 'Po'), help = '''Ex Excellent
Gd Good
TA Average/Typical
Fa Fair
Po Poor
''')

centralair = st.selectbox("Central Air: ", ('Y', 'N'), help = '''N No
Y Yes
''')

electrical = st.selectbox("Electrical: ", ('SBrkr', 'FuseF', 'FuseA', 'FuseP', 'Mix'), help = '''SBrkr Standard Circuit Breakers & Romex
FuseA Fuse Box over 60 AMP and all Romex wiring (Average)
FuseF 60 AMP Fuse Box and mostly Romex wiring (Fair)
FuseP 60 AMP Fuse Box and mostly knob & tube wiring (poor)
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

kitchenqual = st.selectbox("Kitchen Qual: ", ('TA', 'Gd', 'Fa', 'Ex'), help = '''Ex Excellent
Gd Good
TA Typical/Average
Fa Fair
Po Poor
''')

functional = st.selectbox("Functional: ", ('Typ', 'Mod', 'Min2', 'Maj1', 'Min1', 'Sev', 'Sal', 'Maj2'), help = '''Typ Typical Functionality
Min1 Minor Deductions 1
Min2 Minor Deductions 2
Mod Moderate Deductions
Maj1 Major Deductions 1
Maj2 Major Deductions 2
Sev Severely Damaged
Sal Salvage only
''')

fireplaces = st.number_input("Fireplaces: ", min_value = 0, help="Number of fireplaces")

garagetype = st.selectbox("Garage Type: ", ('Attchd', 'Detchd', 'BuiltIn', 'Basment', '2Types', 'CarPort', 'NA'), help = '''2Types More than one type of garage
Attchd Attached to home
Basment Basement Garage
BuiltIn Built-In (Garage part of house - typically has room above garage)
CarPort Car Port
Detchd Detached from home
NA No Garage
''')

garagefinish = st.selectbox("Garage Finish: ", ('Unf', 'RFn', 'Fin', 'MA'), help = '''Fin Finished
RFn Rough Finished
Unf Unfinished
NA No Garage
''')

garagearea = st.number_input("Garage Area: ", min_value = 0, help="Size of garage in square feet")

garagecond = st.selectbox("Garage Cond: ", ('TA', 'Fa', 'Po', 'Gd', 'Ex', 'NA'), help = '''Ex Excellent
Gd Good
TA Typical/Average
Fa Fair
Po Poor
NA No Garage
''')

paveddrive = st.selectbox("Paved Drive: ", ('Y', 'N', 'P'), help = '''Y Paved
P Partial Pavement
N Dirt/Gravel
''')

wooddecksf = st.number_input("Wood Deck SF: ", min_value = 0, help="Wood deck area in square feet")

openporchsf = st.number_input("Open Porch SF: ", min_value = 0, help="Open porch area in square feet")

enclosedporch = st.number_input("Enclosed Porch: ", min_value = 0, help="Enclosed porch area in square feet")

threessnporch = st.number_input("3Ssn Porch: ", min_value = 0, help="Three season porch area in square feet")

screenporch = st.number_input("Screen Porch: ", min_value = 0, help="Screen porch area in square feet")

poolarea = st.number_input("Pool Area: ", min_value = 0, help="Pool area in square feet")

fence = st.selectbox("Fence: ", ('NA', 'MnPrv', 'GdPrv', 'GdWo', 'MnWw'), help = '''GdPrv Good Privacy
MnPrv Minimum Privacy
GdWo Good Wood
MnWw Minimum Wood/Wire
NA No Fence
''')

miscfeature = st.selectbox("Misc Feature: ", ('NA', 'Shed', 'TenC', 'Gar2', 'Othr', 'Elev'), help = '''Elev Elevator
Gar2 2nd Garage (if not described in garage section)
Othr Other
Shed Shed (over 100 SF)
TenC Tennis Court
NA None
''')

miscval = st.number_input("Misc Val: ", min_value = 0, help="$Value of miscellaneous feature")

mosold = st.number_input("Mo Sold: ", min_value = 0, help="Month Sold")

yrsold = st.number_input("Yr Sold: ", min_value = 0, help="Year Sold")

saletype = st.selectbox("Sale Type: ", ('WD ', 'New', 'COD', 'ConLD', 'Con', 'CWD', 'Oth', 'ConLI','ConLw'), help = '''WD Warranty Deed - Conventional
CWD Warranty Deed - Cash
VWD Warranty Deed - VA Loan
New Home just constructed and sold
COD Court Officer Deed/Estate
Con Contract 15% Down payment regular terms
ConLw Contract Low Down payment and low interest
ConLI Contract Low Interest
ConLD Contract Low Down
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
