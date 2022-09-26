import streamlit as st
import requests
import json

# Title of the page
st.title("Ames House Price Prediction")

#split into 3 columns
col1, col2 , col3 = st.columns(3)

st.header("General")
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

    lotarea = st.number_input("Lot Area: ", min_value = 0, help="Lot size in square feet")

    lotshape = st.selectbox("Lot Shape: ", ('Reg', 'IR1', 'IR2', 'IR3'), help = '''Reg Regular\n
    IR1 Slightly irregular\n
    IR2 Moderately Irregular\n
    IR3 Irregular
    ''')

    lotconfig = st.selectbox("Lot Config: ", ('Inside', 'CulDSac', 'Corner', 'FR2', 'FR3'), help = '''Inside Inside lot\n
    Corner Corner lot\n
    CulDSac Cul-de-sac\n
    FR2 Frontage on 2 sides of property\n
    FR3 Frontage on 3 sides of property
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

    yearbuilt = st.number_input("Year Built: ", min_value = 0, max_value = 2022, help="Original construction date")

    roofmatl = st.selectbox("Roof Matl: ", ('CompShg', 'WdShngl', 'Tar&Grv', 'WdShake', 'Membran', 'ClyTile'), help = '''ClyTile Clay or Tile\n
    CompShg Standard (Composite) Shingle\n
    Membran Membrane\n
    Metal Metal\n
    Roll Roll\n
    Tar&Grv Gravel & Tar\n
    WdShake Wood Shakes\n
    WdShngl Wood Shingles
    ''')

    masvnrarea= st.number_input("Mas Vnr Area: ", min_value = 0, help="Masonry veneer area in square feet")
    
    foundation = st.selectbox("Foundation: ", ('PConc', 'CBlock', 'BrkTil', 'Slab', 'Stone', 'Wood'), help = '''BrkTil Brick & Tile\n
    CBlock Cinder Block\n
    PConc Poured Contrete\n
    Slab Slab\n
    Stone Stone\n
    Wood Wood
    ''')
    
    bsmtexposure = st.selectbox("Bsmt Exposure: ", ('No', 'Gd', 'Av', 'Mn', 'NA') , help = '''Gd Good Exposure\n
    Av Average Exposure (split levels or foyers typically score average or above)\n
    Mn Mimimum Exposure\n
    No No Exposure\n
    NA No Basement
    ''')
with col2:
    
    zoning = st.selectbox("Zoning: ", ('RL', 'RM', 'FV', 'C (all)', 'A (agr)', 'RH', 'I (all)'), help = '''A Agriculture\n
    C Commercial\n
    FV Floating Village Residential\n
    I Industrial\n
    RH Residential High Density\n
    RL Residential Low Density\n
    RP Residential Low Density Park\n
    RM Residential Medium Density
    ''')

    street = st.selectbox("Street: ", ('Pave', 'Grvl'), help = '''Grvl Gravel\n
    Pave Paved
    ''')

    landcontour = st.selectbox("Land Contour: ", ('Lvl', 'HLS', 'Bnk', 'Low'), help = '''Lvl Near Flat/Level\n
    Bnk Banked - Quick and significant rise from street grade to building\n
    HLS Hillside - Significant slope from side to side\n
    Low Depression
    ''')

    landslope = st.selectbox("Land Slope: ", ('Gtl', 'Sev', 'Mod'), help = '''Gtl Gentle slope\n
    Mod Moderate Slope\n
    Sev Severe Slope
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

    yearremodadd = st.number_input("Year Remod/Add: ", min_value = 0, max_value = 2022, help="Remodel date (same as construction date if no remodeling or additions)")

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
    
    exterqual = st.selectbox("Exter Qual: ", ('TA', 'Gd', 'Ex', 'Fa', 'Po'), help = '''Ex Excellent\n
    Gd Good\n
    TA Average/Typical\n
    Fa Fair\n
    Po Poor
    ''')

    
    bsmtqual = st.selectbox("Bsmt Qual: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent (100+ inches)\n
    Gd Good (90-99 inches)\n
    TA Typical (80-89 inches)\n
    Fa Fair (70-79 inches)\n
    Po Poor (<70 inches)\n
    NA No Basement
    ''')
    
with col3: 
    lotfrontage = st.number_input("Lot Frontage: ", min_value = 0, help="Linear feet of street connected to property")

    alley = st.selectbox("Alley: ", ('0', 'Pave', 'Grvl'), help = '''Grvl Gravel\n
    Pave Paved\n
    NA No alley access
    ''')
    

    utilities = st.selectbox("Utilities: ", ('AllPub', 'NoSeWa', 'NoSewr'), help = '''AllPub All public Utilities (E,G,W,& S)\n
    NoSewr Electricity, Gas, and Water (Septic Tank)\n
    NoSeWa Electricity and Gas Only\n
    ELO Electricity only
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

    bldgtype = st.selectbox("Bldg Type: ", ('1Fam', 'TwnhsE', 'Twnhs', '2fmCon', 'Duplex'), help = '''1Fam Single-family Detached\n
    2FmCon Two-family Conversion; originally built as one-family dwelling\n
    Duplx Duplex\n
    TwnhsE Townhouse End Unit\n
    TwnhsI Townhouse Inside Unit
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

    roofstyle = st.selectbox("Roof Style: ", ('Gable', 'Hip', 'Flat', 'Mansard', 'Shed', 'Gambrel'), help = '''Flat Flat\n
    Gable Gable\n
    Gambrel Gabrel (Barn)\n
    Hip Hip\n
    Mansard Mansard\n
    Shed Shed
    ''')
    
    masvnrtype = st.selectbox("Mas Vnr Type: ", ('None', 'BrkFace', 'Stone', 'BrkCmn', 'CBlock'), help = '''BrkCmn Brick Common\n
    BrkFace Brick Face\n
    CBlock Cinder Block\n
    None None\n
    Stone Stone
    ''')
    
    extercond = st.selectbox("Exter Cond: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent\n
    Gd Good\n
    TA Average/Typical\n
    Fa Fair\n
    Po Poor
    ''')
    
    bsmtcond = st.selectbox("Bsmt Cond: ", ('TA', 'Gd', 'Fa', 'Ex', 'Po'), help = '''Ex Excellent\n
    Gd Good\n
    TA Typical - slight dampness allowed\n
    Fa Fair - dampness or some cracking or settling\n
    Po Poor - Severe cracking, settling, or wetness\n
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
    
st.header("Basement")
#split into 3 columns
col1, col2 , col3 = st.columns(3)

with col1:
    bsmtfinsf1 = st.number_input("BsmtFin SF 1: ", min_value = 0, help="Type 1 finished square feet")


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
