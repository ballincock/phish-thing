from app.models.user import db
from app.models.weather_log import ApiWeatherLog
from app.models.catch import Catch
from app.models.trip import Trip
from app.models.weather_log_summary import WeatherLog
import requests
from datetime import datetime
from urllib.parse import quote
from flask import Blueprint, render_template, request, jsonify
import math

fishing_bp = Blueprint('fishing_bp', __name__)

class FishingCalculators:
    @staticmethod
    def get_num(key):
        val = data.get(key)
        if val is None or val == "":
            return 0.0
        return float(val)
      
    def run_logic(cid, step, data):
        global db 
        if cid == 1:
            if step == 1.1: 
                simple_ipt = float(data.get('simple_ipt', 0) or 0)
                simple_line_diameter = float(data.get('simple_line_diameter', 0) or 0)
                simple_yards = float(data.get('simple_yards', 0) or 0)

                simple_desired_in = simple_yards * 36
                simple_diameter_in = simple_line_diameter * 0.0393701

                simple_radius = simple_ipt / (2 * math.pi)

                simple_inches_spooled = 0
                simple_turns = 0

                while simple_inches_spooled < simple_desired_in:
                    simple_circumference = 2 * math.pi * simple_radius

                    simple_inches_spooled += simple_circumference
                    simple_turns += 1

                return f"You need {simple_turns:.2f} handle turns to spool {simple_yards} of {simple_line_diameter} mm line."

            if step == 1.2:
                mid_ipt = float(data.get('mid_ipt', 0) or 0)
                mid_line_diameter = float(data.get('mid_line_diameter', 0) or 0)
                mid_yards = float(data.get('mid_yards', 0) or 0)
                mid_outer = float(data.get('mid_outer', 0) or 0)
                mid_inner = float(data.get('mid_inner', 0) or 0)

                mid_desired_in = mid_yards * 36
                mid_turns = mid_desired_in / mid_ipt if mid_ipt > 0 else 0

                mid_ldiameter_in = mid_line_diameter / 25.4

                if mid_ldiameter_in > 0 and mid_outer > mid_inner:
                    mid_spool_area = (math.pi / 4) * (mid_outer**2 - mid_inner**2)
                    mid_max = (mid_spool_area / (mid_ldiameter_in**2) * mid_ipt) / 36

                    if mid_yards > mid_max:
                         return f"Warning: {mid_yards} yards exceeds spool capacity. {mid_turns:.2f} handle turns necessary to spool {mid_yards:.0f} yards"

                return f"{mid_turns:.2f} handle turns necessary to spool {mid_yards:.0f} yards"

            if step == 1.3: 
                adv_ipt = float(data.get('adv_ipt', 0) or 0)
                adv_line_diameter = float(data.get('adv_line_diameter', 0) or 0)
                adv_desired = float(data.get('adv_yards', 0) or 0) 
                adv_outer = float(data.get('adv_outer', 0) or 0)
                adv_inner = float(data.get('adv_inner', 0) or 0)
                adv_packing = float(data.get('adv_packing', 0) or 0)
                adv_linetype = data.get('adv_linetype', 'Monofilament')

                adv_stretch_factors = {
                    'Braid': 1.01,     
                    'Stealth Braid': 1.01,
                    'Fluorocarbon': 1.10,   
                    'Monofilament': 1.08,  
                    'Fly Line': 1.03       
                }

                adv_turns = 1.0

                stretch_coeff = adv_stretch_factors.get(adv_linetype, 1.0)
                packing_efficiency = 1 + (adv_packing * 0.002)
                effective_ipt = adv_ipt * packing_efficiency

                if effective_ipt > 0 and adv_desired > 0:
                    total_inches = (adv_desired * 36) * stretch_coeff

                    adv_turns += (total_inches / effective_ipt)
                else:
                    adv_turns = 0

                return f"{adv_turns:.2f} handle turns necessary to spool {adv_desired:.0f} desired yards of line"

        if cid == 2:
            if step == 2.1: 
                simple_flength = float(data.get('simple_flength', 0) or 0)
                simple_fgirth = float(data.get('simple_fgirth', 0) or 0)
        
                sw_payload = 1.0

                if simple_flength > 0 and simple_fgirth > 0:
                    s_calculated_weight = (simple_flength * (simple_fgirth ** 2)) / 800
                    sw_payload += s_calculated_weight
                else:
                    sw_payload = 0.0 if simple_flength == 0 else 1.0

                return f"Estimated Weight: {sw_payload:.2f} lbs"

            if step == 2.2: 
                mid_flength = float(data.get('mid_flength', 0) or 0)
                mid_fgirth = float(data.get('mid_fgirth', 0) or 0)
                mid_is_spawning = data.get('mid_is_spawning') == True 
                mid_date_str = data.get('mid_datecaught', '')

                final_p = 0.0

                season_multiplier = 1.0
                season_name = "Unknown"
        
                if mid_date_str:
                    try:
                        catch_date = datetime.strptime(mid_date_str, '%Y-%m-%d')
                        month = catch_date.month
                
                        if month in [12, 1, 2]:
                            season_name, season_multiplier = "Winter", 0.95  
                        elif month in [3, 4, 5]:
                            season_name, season_multiplier = "Spring", 1.05  
                        elif month in [6, 7, 8]:
                            season_name, season_multiplier = "Summer", 1.00 
                        else:
                            season_name, season_multiplier = "Fall", 1.10    
                    except ValueError:
                        season_name = "Standard"

                spawn_multiplier = 1.15 if mid_is_spawning else 1.0

                if mid_flength > 0 and mid_fgirth > 0:
                    base_weight = (mid_flength * (mid_fgirth ** 2)) / 800
            
                    final_p = base_weight * season_multiplier * spawn_multiplier

                    final_p += 1.0

                return f"Estimated Weight: {final_p:.2f} lbs ({season_name} Season)"

            if step == 2.3: 
                adv_flength = float(data.get('adv_flength', 0) or 0)
                adv_fgirth = float(data.get('adv_fgirth', 0) or 0)
                adv_is_spawning = data.get('adv_is_spawning') == True
                adv_date_str = data.get('adv_datecaught', '')
                adv_armor = data.get('adv_armor', 'Normal (e.g. Bass)')

                armor_factors = {
                    'Normal (e.g. Bass)': 1.00,
                    'Slight (e.g. Channel Catfish)': 1.03,
                    'Mid (e.g. King Salmon)': 1.06,
                    'High (e.g. Bowfin/Gar)': 1.12,
                    'Extreme (e.g. Lake Sturgeon)': 1.18
                }
                armor_coeff = armor_factors.get(adv_armor, 1.00)

                season_multiplier = 1.0

                if adv_date_str:
                    try:
                        month = datetime.strptime(adv_date_str, '%Y-%m-%d').month

                        if month in [12, 1, 2]: season_multiplier = 0.95   
                        elif month in [3, 4, 5]: season_multiplier = 1.05 
                        elif month in [6, 7, 8]: season_multiplier = 1.00 
                        elif month in [9, 10, 11]: season_multiplier = 1.10 
                    except ValueError:
                        pass

                spawn_multiplier = 1.15 if adv_is_spawning else 1.0

                final_p = 1.0

                if adv_flength > 0 and adv_fgirth > 0:
                    base_calc = (adv_flength * (adv_fgirth ** 2)) / 800
            
                    final_p += (base_calc * armor_coeff * season_multiplier * spawn_multiplier)
                else:
                    final_p = 0.0

            return f"Estimated Weight: {final_p:.2f} lbs"
              
        if cid == 3:
            if step == 3.1: 
                regional_r = data.get('regional_r', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)')
                regional_season = data.get('regional_season', 'Summer')

                region_map = {
                    'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)': {
                        'Winter': ['Walleye', 'Yellow Perch', 'Northern Pike (Ice)'],
                        'Spring': ['Smallmouth Bass', 'Crappie', 'Steelhead'],
                        'Summer': ['Musky', 'Largemouth Bass', 'Channel Catfish'],
                        'Fall': ['Walleye', 'Chinook Salmon', 'Jumbo Perch']
                    },
                    'Lower Midwest (OH, IN, MS, KS, NB': {
                        'Winter': ['Sauger', 'Bluegill', 'Hybrid Striped Bass'],
                        'Spring': ['White Bass', 'Paddlefish', 'Crappie'],
                        'Summer': ['Flathead Catfish', 'Largemouth Bass', 'Carp'],
                        'Fall': ['Smallmouth Bass', 'Saugeye', 'Blue Catfish']
                    },
                    'PNW (OR, WA, ID, MONTANA, AK)': {
                        'Winter': ['Steelhead', 'Cutthroat Trout', 'Burbot'],
                        'Spring': ['Spring Chinook', 'Rainbow Trout', 'Walleye'],
                        'Summer': ['Sockeye Salmon', 'Smallmouth Bass', 'Halibut'],
                        'Fall': ['Coho Salmon', 'Chum Salmon', 'Brown Trout']
                    },
                    'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK': {
                        'Winter': ['Rainbow Trout', 'Striped Bass', 'Crappie'],
                        'Spring': ['Largemouth Bass', 'White Bass', 'Walleye'],
                        'Summer': ['Channel Catfish', 'Smallmouth Bass', 'Carp'],
                        'Fall': ['Brown Trout', 'Largemouth Bass', 'Striped Bass']
                    },
                    'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)': {
                        'Winter': ['Blue Catfish', 'Crappie', 'Redfish'],
                        'Spring': ['Largemouth Bass', 'Striped Bass', 'Tarpon'],
                        'Summer': ['Flathead Catfish', 'Snook', 'Alligator Gar'],
                        'Fall': ['Red Drum', 'Speckled Trout', 'Smallmouth Bass']
                    },
                    'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)': {
                        'Winter': ['Lake Trout (Ice)', 'Yellow Perch', 'Chain Pickerel'],
                        'Spring': ['Striped Bass (Run)', 'American Shad', 'Brook Trout'],
                        'Summer': ['Bluefish', 'Largemouth Bass', 'Fluke'],
                        'Fall': ['Tautog', 'Landlocked Salmon', 'Striped Bass']
                    }
                }

                regional_data = region_map.get(regional_r, {})
                species_list = regional_data.get(regional_season, ["Species not found"])

                formatted_list = ", ".join(species_list)
        
                return f"Top Species for {regional_season} in {regional_r}: {formatted_list}"

            if step == 3.2: 
                user_state = data.get('waterbody_state', 'Alabama')
                user_season = data.get('waterbody_season', 'Summer')

                waterbody_map = {
                    'Alabama': {
                        'Guntersville Lake': {
                            'Winter': ['Sauger', 'Bluegill', 'Crappie'],
                            'Spring': ['Largemouth Bass', 'Spotted Bass', 'Redear Sunfish'],
                            'Summer': ['Largemouth Bass', 'Channel Catfish', 'Bluegill'],
                            'Fall': ['Smallmouth Bass', 'Crappie', 'Largemouth Bass']
                        },
                        'Mobile-Tensaw Delta': {
                            'Winter': ['Redfish', 'Speckled Trout', 'Flounder'],
                            'Spring': ['Striped Bass', 'Largemouth Bass', 'Bluegill'],
                            'Summer': ['Alligator Gar', 'Redfish', 'Mangrove Snapper'],
                            'Fall': ['Red Drum', 'Speckled Trout', 'Striped Bass']
                        }
                    },
                    'Alaska': {
                        'Kenai River': {
                            'Winter': ['Dolly Varden', 'Rainbow Trout'],
                            'Spring': ['King Salmon (Chinook)', 'Steelhead'],
                            'Summer': ['Sockeye Salmon', 'Pink Salmon', 'King Salmon'],
                            'Fall': ['Silver Salmon (Coho)', 'Rainbow Trout', 'Chum Salmon']
                        },
                        'Kachemak Bay': {
                            'Winter': ['Feeder King Salmon', 'Pacific Cod'],
                            'Spring': ['Halibut', 'King Salmon'],
                            'Summer': ['Halibut', 'Lingcod', 'Rockfish'],
                            'Fall': ['Silver Salmon', 'Halibut']
                        }
                    },
                    'California': {
                        'Clear Lake': {
                            'Winter': ['Crappie', 'Largemouth Bass (Deep)', 'Channel Catfish'],
                            'Spring': ['Largemouth Bass (Spawn)', 'Bluegill'],
                            'Summer': ['Largemouth Bass', 'Catfish', 'Carp'],
                            'Fall': ['Largemouth Bass', 'Crappie']
                        },
                        'San Joaquin Delta': {
                            'Winter': ['Sturgeon', 'Striped Bass'],
                            'Spring': ['Striped Bass', 'Largemouth Bass', 'American Shad'],
                            'Summer': ['Largemouth Bass', 'Bluegill', 'Catfish'],
                            'Fall': ['Striped Bass', 'Salmon', 'Sturgeon']
                        }
                    },
                    'Florida': {
                        'Lake Okeechobee': {
                            'Winter': ['Speckled Perch (Crappie)', 'Largemouth Bass'],
                            'Spring': ['Largemouth Bass', 'Bluegill', 'Redear Sunfish'],
                            'Summer': ['Largemouth Bass', 'Channel Catfish'],
                            'Fall': ['Largemouth Bass', 'Bluegill']
                        },
                        'Florida Keys': {
                            'Winter': ['Sailfish', 'King Mackerel', 'Wahoo'],
                            'Spring': ['Tarpon', 'Permit', 'Bonefish'],
                            'Summer': ['Mahi Mahi', 'Mangrove Snapper', 'Grouper'],
                            'Fall': ['Sailfish', 'Blackfin Tuna', 'Snapper']
                        }
                    },
                    'Minnesota': {
                        'Lake of the Woods': {
                            'Winter': ['Walleye (Ice)', 'Sauger', 'Northern Pike'],
                            'Spring': ['Walleye', 'Sturgeon', 'Northern Pike'],
                            'Summer': ['Walleye', 'Smallmouth Bass', 'Musky'],
                            'Fall': ['Walleye', 'Crappie', 'Yellow Perch']
                        },
                        'Mille Lacs Lake': {
                            'Winter': ['Walleye', 'Yellow Perch', 'Northern Pike'],
                            'Spring': ['Smallmouth Bass', 'Walleye'],
                            'Summer': ['Smallmouth Bass', 'Musky', 'Walleye'],
                            'Fall': ['Walleye', 'Smallmouth Bass']
                        }
                    },
                    'Texas': {
                        'Lake Fork': {
                            'Winter': ['Largemouth Bass (Suspended)', 'Crappie'],
                            'Spring': ['Trophy Largemouth Bass', 'White Bass'],
                            'Summer': ['Largemouth Bass', 'Channel Catfish', 'Sunfish'],
                            'Fall': ['Largemouth Bass', 'Yellow Bass', 'Crappie']
                        },
                        'Galveston Bay': {
                            'Winter': ['Sheepshead', 'Black Drum', 'Flounder'],
                            'Spring': ['Redfish', 'Speckled Trout', 'Jack Crevalle'],
                            'Summer': ['Shark', 'Tarpon', 'Speckled Trout'],
                            'Fall': ['Redfish (Bull Reds)', 'Flounder', 'Speckled Trout']
                        }
                    },
                    'Michigan': {
                        'Lake St. Clair': {
                            'Winter': ['Yellow Perch (Ice)', 'Northern Pike'],
                            'Spring': ['Smallmouth Bass', 'Walleye (River Run)'],
                            'Summer': ['Musky', 'Smallmouth Bass', 'Largemouth Bass'],
                            'Fall': ['Smallmouth Bass', 'Musky', 'Walleye']
                        },
                        'Saginaw Bay': {
                            'Winter': ['Walleye (Ice)', 'Yellow Perch'],
                            'Spring': ['Walleye', 'Yellow Perch', 'Channel Catfish'],
                            'Summer': ['Walleye', 'Smallmouth Bass', 'Catfish'],
                            'Fall': ['Walleye', 'Perch']
                        }
                    },
                    'Wisconsin': {
                        'Lake Winnebago': {
                            'Winter': ['Lake Sturgeon (Spearing)', 'Walleye', 'Perch'],
                            'Spring': ['Walleye', 'White Bass', 'Crappie'],
                            'Summer': ['Largemouth Bass', 'Catfish', 'Bluegill'],
                            'Fall': ['Walleye', 'Yellow Perch']
                        },
                        'Green Bay': {
                            'Winter': ['Whitefish (Ice)', 'Walleye'],
                            'Spring': ['Walleye', 'Smallmouth Bass'],
                            'Summer': ['Musky', 'Smallmouth Bass', 'Walleye'],
                            'Fall': ['Musky', 'Smallmouth Bass']
                        }
                    },
                    'New York': {
                        'Lake Champlain': {
                            'Winter': ['Lake Trout', 'Landlocked Salmon', 'Yellow Perch'],
                            'Spring': ['Smallmouth Bass', 'Walleye', 'Atlantic Salmon'],
                            'Summer': ['Largemouth Bass', 'Lake Trout', 'Bowfin'],
                            'Fall': ['Smallmouth Bass', 'Northern Pike', 'Salmon']
                        },
                        'Salmon River': {
                            'Winter': ['Steelhead'],
                            'Spring': ['Steelhead', 'Brown Trout'],
                            'Summer': ['Smallmouth Bass', 'Brown Trout'],
                            'Fall': ['Chinook Salmon', 'Coho Salmon', 'Steelhead']
                        }
                    },
                    'Washington': {
                        'Columbia River': {
                            'Winter': ['Steelhead', 'Sturgeon'],
                            'Spring': ['Spring Chinook Salmon', 'Walleye'],
                            'Summer': ['Sockeye Salmon', 'Smallmouth Bass', 'Summer Chinook'],
                            'Fall': ['Fall Chinook', 'Coho Salmon', 'Steelhead']
                        },
                        'Puget Sound': {
                            'Winter': ['Blackmouth (Chinook)', 'Squid'],
                            'Spring': ['Lingcod', 'Halibut'],
                            'Summer': ['Pink Salmon', 'Chinook Salmon', 'Coho'],
                            'Fall': ['Coho Salmon', 'Chum Salmon']
                        }
                    },
                    'Colorado': {
                        'Eagle River': {
                            'Winter': ['Rainbow Trout', 'Brown Trout'],
                            'Spring': ['Rainbow Trout', 'Cutthroat Trout'],
                            'Summer': ['Brown Trout', 'Rainbow Trout'],
                            'Fall': ['Brown Trout (Spawn)', 'Rainbow Trout']
                        },
                        'Blue Mesa Reservoir': {
                            'Winter': ['Lake Trout (Ice)', 'Kokanee Salmon'],
                            'Spring': ['Rainbow Trout', 'Brown Trout'],
                            'Summer': ['Kokanee Salmon', 'Lake Trout', 'Perch'],
                            'Fall': ['Brown Trout', 'Rainbow Trout']
                        }
                    },
                    'Pennsylvania': {
                        'Lake Erie': {
                            'Winter': ['Steelhead (Tributaries)', 'Yellow Perch'],
                            'Spring': ['Walleye', 'Smallmouth Bass'],
                            'Summer': ['Walleye', 'Yellow Perch', 'Smallmouth Bass'],
                            'Fall': ['Steelhead (Run)', 'Walleye']
                        },
                        'Susquehanna River': {
                            'Winter': ['Walleye', 'Smallmouth Bass (Deep)'],
                            'Spring': ['Smallmouth Bass', 'Musky', 'Channel Catfish'],
                            'Summer': ['Smallmouth Bass', 'Flathead Catfish'],
                            'Fall': ['Smallmouth Bass', 'Walleye']
                        }
                    },
                    'North Carolina': {
                        'Jordan Lake': {
                            'Winter': ['Crappie (Deep)', 'Blue Catfish'],
                            'Spring': ['Largemouth Bass (Peak)', 'Crappie (Shallow)'],
                            'Summer': ['Largemouth Bass', 'Channel Catfish', 'Striped Bass'],
                            'Fall': ['Largemouth Bass', 'Crappie', 'White Bass']
                        },
                        'High Rock Lake': {
                            'Winter': ['Crappie (January Hotspot)', 'Catfish'],
                            'Spring': ['Largemouth Bass', 'Crappie (Brush Piles)', 'White Bass'],
                            'Summer': ['Largemouth Bass', 'Flathead Catfish', 'Sunfish'],
                            'Fall': ['Largemouth Bass', 'Crappie', 'Striped Bass']
                        }
                    },
                    'Tennessee': {
                        'Chickamauga Lake': {
                            'Winter': ['Striped Bass', 'Blue Catfish', 'Sauger'],
                            'Spring': ['Trophy Largemouth Bass', 'Crappie', 'White Bass'],
                            'Summer': ['Largemouth Bass (Night)', 'Catfish', 'Bluegill'],
                            'Fall': ['Largemouth Bass', 'Smallmouth Bass', 'Crappie']
                        },
                        'Douglas Lake': {
                            'Winter': ['Sauger', 'Crappie', 'Largemouth Bass'],
                            'Spring': ['Crappie (April Peak)', 'Largemouth Bass', 'Walleye'],
                            'Summer': ['Largemouth Bass', 'Channel Catfish', 'White Bass'],
                            'Fall': ['Largemouth Bass', 'Smallmouth Bass', 'Crappie']
                        }
                    },
                    'Missouri': {
                        'Lake of the Ozarks': {
                            'Winter': ['Crappie', 'Blue Catfish', 'Largemouth Bass (Deep)'],
                            'Spring': ['Largemouth Bass', 'Paddlefish', 'Walleye'],
                            'Summer': ['Largemouth Bass', 'White Bass', 'Channel Catfish'],
                            'Fall': ['Crappie', 'Largemouth Bass', 'White Bass']
                        },
                        'Truman Reservoir': {
                            'Winter': ['Blue Catfish', 'Crappie'],
                            'Spring': ['Crappie (Shallow)', 'Largemouth Bass', 'Paddlefish'],
                            'Summer': ['Flathead Catfish', 'Largemouth Bass', 'Hybrid Striped Bass'],
                            'Fall': ['Crappie', 'White Bass', 'Largemouth Bass']
                        }
                    },
                    'Oklahoma': {
                        'Lake Texoma': {
                            'Winter': ['Blue Catfish', 'Striped Bass'],
                            'Spring': ['Striped Bass', 'Smallmouth Bass', 'White Bass'],
                            'Summer': ['Striped Bass', 'Channel Catfish', 'Largemouth Bass'],
                            'Fall': ['Striped Bass', 'Smallmouth Bass', 'Crappie']
                        },
                     'Grand Lake Of the Cherokees': {
                            'Winter': ['Saugeye', 'Blue Catfish', 'Crappie'],
                            'Spring': ['Largemouth Bass (Pre-spawn)', 'Paddlefish', 'Crappie'],
                            'Summer': ['Largemouth Bass', 'White Bass', 'Channel Catfish'],
                            'Fall': ['Largemouth Bass', 'Crappie', 'Bluegill']
                        }
                    },
                    'Ohio': {
                        'Buckeye Lake': {
                            'Winter': ['Saugeye (Ice)', 'Crappie'],
                            'Spring': ['Saugeye', 'Hybrid Striped Bass', 'Crappie'],
                            'Summer': ['Largemouth Bass', 'Channel Catfish', 'Sunfish'],
                            'Fall': ['Saugeye', 'Hybrid Striped Bass', 'Yellow Perch']
                        },
                        'Indian Lake': {
                            'Winter': ['Saugeye (Ice)', 'Yellow Perch'],
                            'Spring': ['Saugeye', 'Crappie', 'Largemouth Bass'],
                            'Summer': ['Channel Catfish', 'Sunfish', 'Largemouth Bass'],
                            'Fall': ['Saugeye', 'Crappie', 'Yellow Perch']
                        }
                    },
                    'Arizona': {
                        'Roosevelt Lake': {
                            'Winter': ['Crappie', 'Rainbow Trout', 'Channel Catfish'],
                            'Spring': ['Largemouth Bass', 'Smallmouth Bass', 'Crappie'],
                            'Summer': ['Largemouth Bass (Night)', 'Flathead Catfish', 'Carp'],
                            'Fall': ['Largemouth Bass', 'Smallmouth Bass', 'White Bass']
                        },
                        'Lake Pleasant': {
                            'Winter': ['Striped Bass', 'White Bass', 'Trout'],
                            'Spring': ['Largemouth Bass', 'White Bass', 'Crappie'],
                            'Summer': ['Striped Bass', 'Tilapia', 'Channel Catfish'],
                            'Fall': ['Largemouth Bass', 'White Bass', 'Striped Bass']
                        }
                    }
                    #add more states and waterbodies
                }

                state_data = waterbody_map.get(user_state, {})
        
                if not state_data:
                    return f"Currently gathering data for {user_state}. Try Alabama, Alaska, California, Florida, Minnesota, or Texas."

                results = []
                for wb_name, seasons in state_data.items():
                    species = seasons.get(user_season, ["Species data pending"])
                    species_str = ", ".join(species)
                    results.append(f"{wb_name}: {species_str}")

                final_output = " | ".join(results)
                return f"Top Picks for {user_season} in {user_state} — {final_output}"

            if step == 3.3: 
                user_species = data.get('species_fadvice', 'Largemouth Bass')
                user_season = data.get('advice_season', 'Summer')

                advice_map = {
                    'Largemouth Bass': {
                        'Winter': "Target deep structure like rock piles or creek channels. Slow down your presentation—use jigs or drop-shots.",
                        'Spring': "Move to the shallows. Look for spawning beds in quiet bays. Spinnerbaits and chatterbaits work great in pre-spawn.",
                        'Summer': "Fish early morning or late evening. During the day, look for thick vegetation or deep docks. Topwater frogs are a must.",
                        'Fall': "Bass follow baitfish into creeks. Use moving baits like crankbaits and flukes to match the forage size."
                    },
                    'Walleye': {
                        'Winter': "Ice fishing is peak. Use bucktail jigs or jigging raps near the bottom on lake points or reef edges.",
                        'Spring': "Target river mouths and gravel shorelines for the spawn. Night fishing with shallow-diving jerkbaits is lethal.",
                        'Summer': "Troll deep flats with bottom bouncers or crawler harnesses. Look for 'the walleye chop' on the surface.",
                        'Fall': "Vertical jig over deep humps or rock piles as fish school up to follow shad or perch into deeper water."
                    },
                    'Crappie': {
                        'Winter': "Suspended over deep water. Use light fluorocarbon and tiny tungsten jigs or live minnows near submerged timber.",
                        'Spring': "The classic spawn run. Look for brush piles in 2-6 feet of water. Bobber and minnow is the go-to.",
                        'Summer': "Fish move to deeper, cooler structure or bridge pilings. Look for schools on electronics in 10-20 feet of water.",
                        'Fall': "Target secondary points and docks. Fish will start schooling heavily again as water temps drop."
                    },
                    'Steelhead': {
                        'Winter': "Slow and low. Target deep, slow pools in rivers. Use beads or spawn sacks under a float with a very light leader.",
                        'Spring': "Look for 'gravel' in the rivers. Fish are active and aggressive. Swinging streamers or drifting yarn balls works well.",
                        'Summer': "Mostly a deep-lake game unless in specific PNW runs. Target the thermocline in the Great Lakes.",
                        'Fall': "The 'Run' begins. Target river mouths and lower reaches. High energy fish—use bright colors and fresh spawn."
                    },
                    'Channel Catfish': {
                        'Winter': "Dormant but catchable in deep river holes. Use smelly cut-bait and keep it stationary on the bottom.",
                        'Spring': "Fish move to warm, shallow mudflats after rain. Use dip baits or chicken liver near moving water.",
                        'Summer': "Peak season. Fish deep holes by day and shallow flats by night. Punch baits and stink baits are most effective.",
                        'Fall': "Look for creek mouths where baitfish are congregating. Fresh cut-shad is the best big-fish producer."
                    }
                    #more species
                }

                species_data = advice_map.get(user_species, {})
                final_advice = species_data.get(user_season, "General Advice: Focus on structure, match the hatch, and watch water temperatures.")

                return f"Advice for {user_species} in the {user_season}: {final_advice}"

        if cid == 4:
            if step == 4.1: 
                hgear_info = data.get('hgear_info', 'Species Specific Inquiry')

                info_map = {
                    'Rod Weight Information': (
                        "Rod weight (Power) refers to how much force is needed to bend the rod. "
                        "Ratings range from Ultralight (very little force) to Heavy (significant force). "
                        "Choosing the right power ensures you can handle the weight of your target fish and the lures used."
                    ),
                    'Rod Speed Information': (
                        "Rod speed (Action) describes where the rod bends. "
                        "Fast Action bends only at the tip, offering high sensitivity and quick hooksets. "
                        "Moderate/Slow Action bends deeper into the blank, acting as a shock absorber for hard-pulling fish."
                    ),
                    'Reel Gearing Information': (
                        "Gear ratio (e.g., 6.2:1) indicates how many times the spool turns per handle rotation. "
                        "Low ratios (5.4:1) provide torque for deep-diving lures, while high ratios (7.1:1+) "
                        "are for fast retrieves and picking up slack line quickly."
                    ),
                    'Reel Capacity Information': (
                        "Line capacity determines how many yards of a specific pound-test line a reel can hold. "
                        "Larger reels (size 4000+) have deeper spools for long-running saltwater species, "
                        "while small reels (1000-2000) are optimized for thin, light lines."
                    ),
                    'Ultralight Info': (
                        "Gear: 4'6\" to 5'6\" rods, size 500-1000 reels, 2-6lb line. "
                        "Usage: Best for Panfish, Trout, and Microfishing. Extremely sensitive for tiny 1/64oz jigs."
                    ),
                    'Medium-Light Info': (
                        "Gear: 6'6\" to 7'0\" rods, size 2000-2500 reels, 6-10lb line. "
                        "Usage: Ideal for Finesse Bass (drop shots), Walleye jigging, and larger Trout."
                    ),
                    'Medium Info': (
                        "Gear: 7'0\" rods, size 2500-3000 reels, 8-12lb line. "
                        "Usage: The 'All-Rounder.' Perfect for Bass (crankbaits/worms), Channel Catfish, and Pier fishing."
                    ),
                    'Medium Heavy Info': (
                        "Gear: 7'0\" to 7'6\" rods, size 3000-4000 reels (or baitcasters), 12-20lb line. "
                        "Usage: Heavy cover Bass fishing (jigs/frogs), Pike, and Inshore saltwater (Redfish/Snook)."
                    ),
                    'Heavy Info': (
                        "Gear: 7'6\"+ rods, size 5000+ reels, 30lb+ braid. "
                        "Usage: Muskie, Flathead Catfish, Sturgeon, and Offshore saltwater. Built for maximum 'backbone'."
                    ),
                    'Species Specific Inquiry': (
                        "Targeting diverse species: "
                        "Panfish/Trout -> Ultralight; Bass -> Medium-Heavy Fast Action; "
                        "Walleye -> Medium-Light Moderate Action; Catfish/Pike/Salmon -> Heavy Power."
                    )
                }

                result_text = info_map.get(hgear_info, "Information for this selection is currently being updated.")

                return f"Gear Insight — {hgear_info}: {result_text}"

            if step == 4.2: 
                hlure_info = data.get('hlure_info', 'Crankbait Information')

                lure_db = {
                    'Crankbait Information': (
                        "Designed to dive when retrieved. Square-bills are for shallow cover (deflect off wood); "
                        "Deep-divers have long lips for targeting ledges. Use a moderate action rod to prevent pulling hooks."
                    ),
                    'Jig Information': (
                        "The ultimate 'big fish' lure. Flipping jigs are for heavy cover, swim jigs for moving through grass, "
                        "and football jigs for dragging across rocky bottoms. Always use a weed guard in timber."
                    ),
                    'Spoon/Spinner Information': (
                        "Old school but lethal. Spoons mimic wounded baitfish with flash and wobble. "
                        "In-line spinners (like Mepps) create vibration that triggers predatory instincts in Trout and Pike."
                    ),
                    'Microplastic Information': (
                        "Tiny 1-2 inch grubs or tubes. Essential for crappie, bluegill, and sunfish. "
                        "Best paired with a 1/32oz or 1/64oz jig head on ultralight tackle."
                    ),
                    'Catfish Rig Information': (
                        "Focus on the Carolina Rig or Santee Cooper Rig. Uses a heavy sinker and a leader to keep "
                        "cut bait or stink bait near the bottom where catfish scavenge."
                    ),
                    'Live Bait Rig Information': (
                        "Includes the slip-bobber rig for precision depth or the Lindy Rig for dragging minnows/leeches. "
                        "Keep bait lively by using circle hooks to ensure corner-of-the-mouth hooksets."
                    ),
                    'Spinnerbait/Chatterbait Information': (
                        "Reaction baits. Spinnerbaits use blades for flash in murky water; Chatterbaits (vibrating jigs) "
                        "create intense thumping felt through the rod. Great for searching large areas of grass."
                    ),
                    'Swimbait Information': (
                        "Paddle-tails provide a realistic swimming motion. Can be rigged on a weighted jig head or "
                        "weedless swimbait hook. Effective for everything from Bass to Saltwater Stripers."
                    ),
                    'Glidebait Information': (
                        "Hard-bodied lures that 'S-turn' on a slow retrieve. These are trophy hunters. "
                        "Twitch the reel handle to make the bait dart side-to-side, mimicking a dying gizzard shad."
                    ),
                    'Ned Rig/Tube Information': (
                        "Finesse at its finest. The Ned Rig uses a small plastic on a mushroom head to stand straight up. "
                        "Tubes mimic crawfish or gobies and are a staple for Smallmouth Bass."
                    ),
                    'Senko/Finneseplastic Information': (
                        "The stick-bait (Senko) is most famous when rigged 'Wacky' style (hooked in the middle). "
                        "It has a unique shimmy on the fall that fish cannot resist. Low-pressure, high-reward."
                    ),
                    'Topwater Information': (
                        "Walking baits (Spooks), Poppers, and Frogs. Used when fish are looking up. "
                        "Wait until you feel the weight of the fish before setting the hook to avoid 'pulling it away'."
                    ),
                    'Very Small Fly Information': (
                        "Sizes 18-24. Mimics midges and tiny nymphs. Requires 6x or 7x tippet and "
                        "extreme stealth. Essential for technical tailwater trout fishing."
                    ),
                    'Fly Information': (
                        "Standard dry flies (Adams, Elk Hair Caddis) and nymphs (Hare's Ear). "
                        "Focus on 'Matching the Hatch'—using the fly that represents the bugs currently hitting the water."
                    ),
                    'Large fly / Streamer Information': (
                        "Wooly Buggers, Galloup-style streamers, and articulated patterns. "
                        "These mimic sculpins, leeches, or baitfish. Stripped fast to trigger aggressive strikes."
                    ),
                    'Bait Information': (
                        "Natural forage like nightcrawlers, red worms, crickets, and waxworms. "
                        "Nothing beats the real thing when the bite is tough or when introducing beginners to the sport."
                    )
                }

                result_text = lure_db.get(hlure_info, "Information for this tackle category is coming soon.")

                return f"Lure Guide — {hlure_info}: {result_text}"


            if step == 4.3: 
                hjgwent_info = data.get('hjgwent_info', 'Lures')

                savings_db = {
                    'Lures': (
                        "Save by sticking to core colors (Green Pumpkin, Black/Blue) instead of buying every variety. "
                        "Reliable 'knock-off' alternatives like the Bass Pro Shops Stik-O or Yum Dinger offer similar "
                        "action to premium senkos for a fraction of the cost. Use a lighter to weld torn soft plastics back together."
                    ),
                    'Bait': (
                        "Catch or gather your own live bait whenever possible. Red worms can be found in moist soil, "
                        "and small baitfish can be caught with a simple cast net or minnow trap. If using store-bought, "
                        "salt down leftovers for future trips to preserve them without freezing."
                    ),
                    'Rods': (
                        "Look for 'Mid-Range' workhorses like the Ugly Stik Elite or Daiwa Crossfire. These offer "
                        "the best 'bang for your buck' durability without the premium markup of high-modulus graphite. "
                        "Check clearance sections in early spring for discontinued last-season models."
                    ),
                    'Reels': (
                        "Rod and reel combos are almost always cheaper than buying separately. For budget reliability, "
                        "stick with brands like Zebco for entry-level or Abu Garcia's Max series for affordable baitcasters. "
                        "Second-hand reels from reputable marketplaces often just need a quick cleaning to perform like new."
                    ),
                    'Tackle Accessories/Misc': (
                        "Buy bulk packs for high-loss items like hooks, sinkers, and bobber stops. For tools, look at "
                        "multi-tool combos like the Pursuit 14-in-1 which often include a headlamp. A basic paper clip "
                        "can double as a snag-releasing tool, saving you from losing expensive rigs."
                    ),
                    'Kayaks and Boats': (
                        "Focus on the used market. Freshwater kayaks depreciate quickly; you can often find 'fully rigged' "
                        "used vessels for 50 percent of their retail price. For new budget options, simple sit-on-top models "
                        "offer better stability and value for recreational fishing than specialized 'pro' pedal drives."
                    )
                }

                result_text = savings_db.get(hjgwent_info, "General Tip: Only buy what you need for your next three trips.")

                return f"Budget Insight — {hjgwent_info}: {result_text}"

        if cid == 5:
            if step == 5.1: 
                regional_pt = data.get('regional_pt', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)')
                pt_season = data.get('pt_season', 'Summer')

                travel_map = {
                    'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)': {
                        'Winter': "Target ice fishing on major lakes like Lake of the Woods (MN) or Lake Gogebic (MI) for jumbo perch and walleye. For open water, look for warm water discharges near Great Lakes power plants which stay ice-free and attract schools of baitfish and trout.",
                        'Spring': "Focus on river mouths and shallow gravel flats for the walleye run. Rainy Lake and Lake Michigan harbors offer world-class spring action as fish move into warmer, shallower bays.",
                        'Summer': "Head to the 'Up North' glacial lakes for musky and largemouth bass. For consistent action, deep-water trolling on the Great Lakes for lake trout and salmon is at its peak.",
                        'Fall': "The 'Fall Feed' is in full swing. Target deep rock humps and steep ledges for trophy walleye or hit river tributaries for migrating chinook and coho salmon."
                    },
                    'Lower Midwest (OH, IN, MS, KS, NB': {
                        'Winter': "Look for saugeye and hybrid striped bass below dams and spillways where current prevents ice. Lakes like Buckeye Lake (OH) offer solid ice fishing for saugeye when conditions permit.",
                        'Spring': "Prime crappie season. Target standing timber and brush piles in reservoirs like Rend Lake (IL) or Patoka Lake (IN). Spring spillway bites are also excellent for white bass.",
                        'Summer': "Night fishing is king for flathead and blue catfish in major river systems. For bass, target deep-water structure and ledges in large reservoirs like Lake of the Ozarks.",
                        'Fall': "Bass follow baitfish into secondary creek arms. This is also the best time for trophy smallmouth on the Susquehanna or Ohio Rivers as they feed heavily before winter."
                    },
                    'PNW (OR, WA, ID, MONTANA, AK)': {
                        'Winter': "Focus on coastal rivers for winter-run steelhead. The Skagit, Cowlitz, and Nestucca rivers provide consistent runs through March. Use float-fishing techniques with roe or beads.",
                        'Spring': "Target the 'Spring Chinook' (Springer) run on the Columbia and Willamette rivers. This is also the start of peak trout fishing in the high-desert lakes of Eastern Washington.",
                        'Summer': "Hit the main rivers like the Columbia and Cowlitz for summer-run steelhead and sockeye salmon. High-altitude mountain lakes in Montana and Idaho are also prime for cutthroat trout during this window.",
                        'Fall': "Peak salmon migration. Target the Puget Sound and major tributaries for coho and chum salmon. Late fall also sees 'desert steelhead' action in the Methow and Deschutes rivers."
                    },
                    'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK': {
                        'Winter': "Head to Lake Fork (TX) for trophy largemouth bass or target winter striped bass on Lake Mead (NV). High-altitude lakes in Colorado provide excellent ice fishing for kokanee salmon and lake trout.",
                        'Spring': "Peak spawning window for bass in the desert reservoirs. Roosevelt Lake (AZ) and Lake Texoma (OK/TX) offer explosive topwater and bed-fishing opportunities.",
                        'Summer': "Night fishing for bass and catfish to beat the heat. Higher elevations in New Mexico and Colorado provide a cooler escape for wild brown and rainbow trout in mountain streams.",
                        'Fall': "As water temps drop, striped bass and white bass blitz on the surface of Lake Pleasant (AZ) and Lake Lanier (GA/South region border). Brown trout begin their fall spawning runs in Utah and Colorado rivers."
                    },
                    'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)': {
                        'Winter': "The 'Blue Catfish' season is peaking in Tennessee's Chickamauga Lake. For saltwater, hit the Florida Keys for sailfish and king mackerel or the Outer Banks (NC) for winter striped bass and red drum.",
                        'Spring': "The South's bass fishing is world-class in March/April. Target Lake Okeechobee (FL) or Guntersville (AL) for giant pre-spawn females moving into the grass.",
                        'Summer': "Focus on the Gulf Coast for tarpon, snook, and offshore mahi-mahi. Inland, target river bends and deep holes for flathead catfish or search out cooler trout streams in the Smoky Mountains.",
                        'Fall': "Saltwater 'Fall Run' begins for redfish and speckled trout in the marshes. Inland, striped bass become highly active on the surface of deep reservoirs as they chase schooling shad."
                    },
                    'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)': {
                        'Winter': "Ice fishing on Lake Champlain (NY/VT) for yellow perch and pike is a staple. In the coastal rivers like the Salmon River (NY), target hardy winter steelhead.",
                        'Spring': "The Atlantic striped bass migration starts moving north. Target the Chesapeake Bay and Jersey Shore. For freshwater, brook trout fishing in small mountain streams is at its peak.",
                        'Summer': "Head offshore for bluefish and fluke. Freshwater anglers should target the Finger Lakes or Lake Erie for walleye and smallmouth bass in deeper, cooler waters.",
                        'Fall': "The 'Striper Blitz'—migratory bass move south along the coast. Target rocky points and harbors with topwater plugs. Inland, fall foliage provides a scenic backdrop for landlocked salmon runs in Maine and New York."
                    }
                }

                region_data = travel_map.get(regional_pt, {})
                final_advice = region_data.get(pt_season, "Focus on local seasonal migrations and consult area bait shops for current water conditions.")

                return f"Trip Advice — {regional_pt} ({pt_season}): {final_advice}"

            if step == 5.2: 
                regional_pt = data.get('regional_pt', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)')
                pt_season = data.get('pt_season', 'Summer')

                target_map = {
                    'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)': {
                        'Winter': "Yellow Perch & Walleye. Success comes from 'dead-sticking' a minnow on one line while aggressively jigging a tungsten spoon on the other to draw them in.",
                        'Spring': "Crappie & Bluegill. Fish shallow, dark-bottom bays that warm up first. Use a small 1/32oz jig under a slip bobber set only 2-3 feet deep.",
                        'Summer': "Smallmouth Bass. Target offshore rock piles and reefs. Drag a Ned Rig or a tube slowly across the bottom to mimic crayfish.",
                        'Fall': "Muskie. This is 'Fathead' season. Use large 10-12 inch suckers on a quick-strike rig or throw large 'pounder' soft plastics near steep breaklines."
                    },
                    'Lower Midwest (OH, IN, MS, KS, NB': {
                        'Winter': "Saugeye. Fish below dam tailwaters or spillways. Use a 1/8oz lead head with a bright plastic tail and a very slow retrieve through the current seams.",
                        'Spring': "White Bass. They run up tributaries in massive schools. Throw small inline spinners or silver spoons into the current to trigger reaction strikes.",
                        'Summer': "Flathead Catfish. Target deep timber or log jams during the day with live green sunfish or bullheads. At night, move to the shallow heads of the holes.",
                        'Fall': "Hybrid Striped Bass. Look for surface 'blitzes' where they push shad up. Cast topwater poppers or silver lipless crankbaits into the splashing."
                    },
                    'PNW (OR, WA, ID, MONTANA, AK)': {
                        'Winter': "Winter Steelhead. Target 'walking speed' water in rivers. Drift-fish a pink yarn ball or a 10mm bead 12-18 inches off the bottom.",
                        'Spring': "Rainbow & Cutthroat Trout. As insects hatch, switch to fly gear or small 1/16oz spinners. Focus on the edges of main current seams.",
                        'Summer': "Chinook (King) Salmon. In the big rivers, use 'back-bouncing' techniques with fresh cured salmon roe or troll large 'Super Bait' lures behind flashers.",
                        'Fall': "Coho (Silver) Salmon. They love 'twitching' jigs. Cast a 3/8oz feathered jig, let it sink, and sharply snap the rod tip up as you retrieve."
                    },
                    'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK': {
                        'Winter': "Rainbow Trout. Many desert lakes are stocked now. Use 'Powerbait' on a treble hook with a 12-inch leader off the bottom for easy success.",
                        'Spring': "Largemouth Bass. It's bed-fishing time. Use a white-colored soft plastic (easier for you to see) and drop it directly into the center of the nest.",
                        'Summer': "Striped Bass. Use your electronics to find schools in 40-60 feet of water. Use a 'heavy slab' spoon and vertically jig it rapidly through the school.",
                        'Fall': "Smallmouth Bass. As water cools, they move to points. Use a 'Drop Shot' rig with a 3-inch minnow imitation held just off the rocky floor."
                    },
                    'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)': {
                        'Winter': "Blue Catfish. The monsters are active in deep river channels. Use fresh-cut Skipjack or Gizzard Shad on a 7/0 circle hook with heavy weights.",
                        'Spring': "Largemouth Bass. Target lily pads and grass edges. Use a 'Texas-rigged' lizard or creature bait to punch through the vegetation.",
                        'Summer': "Redfish & Seatrout. In the marshes, fish the 'falling tide.' Use a gold spoon for Redfish or a live shrimp under a popping cork for Trout.",
                        'Fall': "Striped Bass (Rockfish). They move into the major river arms. Troll deep-diving crankbaits or use live threadfin shad on a 'down-line' rig."
                    },
                    'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)': {
                        'Winter': "Northern Pike. Use 'Tip-ups' on the ice with a large dead Cisco or Smelt. Set the bait about 2 feet off the bottom near weed edges.",
                        'Spring': "Atlantic Striped Bass. The migration starts in the bays. Use 'chunk' bunker (Menhaden) on the bottom or cast large white swimbaits near bridges.",
                        'Summer': "Fluke (Summer Flounder). Use a 'bucktail' tipped with a Gulp strip. Bounce it aggressively along the sandy bottom as the boat drifts.",
                        'Fall': "Landlocked Salmon. They move into the tributaries to spawn. Use small 'egg pattern' flies or orange/red spoons pulled behind a downrigger."
                    }
                }

                regional_data = target_map.get(regional_pt, {})
                final_advice = regional_data.get(pt_season, "General Target: Panfish and Bass. Method: Use live bait or small jigs near visible cover.")

                return f"Target Species — {regional_pt} ({pt_season}): {final_advice}"

            if step == 5.3: 
                regional_ptg = data.get('regional_ptg', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)')
                ptg_season = data.get('ptg_season', 'Summer')

                gear_map = {
                    'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)': {
                        'Winter': "Target: Walleye & Perch. Gear: 28\" Med-Light Ice Rod. Lure: 1/8oz Gold Jigging Rap or Tungsten Spoons tipped with minnow heads.",
                        'Spring': "Target: Crappie & Walleye. Gear: 6'6\" Light Spinning Rod, 4-6lb Mono. Lure: 1/16oz Chartreuse Marabou Jigs or curly tail grubs.",
                        'Summer': "Target: Smallmouth Bass. Gear: 7'0\" Medium Spinning Rod, 8lb Fluoro. Lure: Ned Rigs, Tubes, or 3\" Keitech swimbaits on ball heads.",
                        'Fall': "Target: Muskie & Jumbo Perch. Gear: 8'0\" Heavy Casting Rod, 80lb Braid. Lure: Large Double-Cowgirl bucktails or 10\" Suick jerkbaits."
                    },
                    'Lower Midwest (OH, IN, MS, KS, NB': {
                        'Winter': "Target: Saugeye & Bluegill. Gear: 6'0\" Med-Light Spinning Rod. Lure: 1/8oz Vibe blades or small blade baits worked slowly off the bottom.",
                        'Spring': "Target: White Bass & Crappie. Gear: 6'6\" Medium Spinning Rod. Lure: 1/4oz Rooster Tails or small white curly tail jigs in the current.",
                        'Summer': "Target: Catfish & Bass. Gear: 7'0\" Medium-Heavy Rod, 20lb Mono. Lure: Santee Cooper Rigs with cut shad or 1/2oz dark-colored Jigs.",
                        'Fall': "Target: Hybrid Striped Bass. Gear: 7'0\" Medium Fast-Action Rod. Lure: Silver Lipless Crankbaits (Rat-L-Traps) or Walking Topwaters."
                    },
                    'PNW (OR, WA, ID, MONTANA, AK)': {
                        'Winter': "Target: Winter Steelhead. Gear: 9'0\"-10'6\" Medium Casting Rod. Lure: 10mm soft beads, Pink Worms, or Nightmare-pattern jigs under a float.",
                        'Spring': "Target: Chinook Salmon & Trout. Gear: 9'0\" Heavy Rod. Lure: Mag Lip 4.5 plugs or 1/4oz Blue Fox spinners for trout in tributaries.",
                        'Summer': "Target: Sockeye & Summer Steelhead. Gear: 8'6\" Medium Spinning Rod. Lure: Small pink squids (Hoochies) behind flashers or size 4 hammered brass spinners.",
                        'Fall': "Target: Coho Salmon. Gear: 8'6\" Med-Heavy Spinning Rod. Lure: 3/8oz Twitching Jigs (Purple/Pink) or Vibrax size 5 spinners."
                    },
                    'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK': {
                        'Winter': "Target: Stocked Trout & Striped Bass. Gear: 6'0\" Ultra-Light Rod. Lure: PowerBait rigs or 2.5\" silver jerkbaits for winter stripers.",
                        'Spring': "Target: Largemouth Bass. Gear: 7'0\" Med-Heavy Baitcaster. Lure: White spinnerbaits or Texas-rigged lizards in shallow brush.",
                        'Summer': "Target: Striped Bass & Catfish. Gear: 7'0\" Medium Rod. Lure: 1oz Jigging Spoons or topwater 'Spooks' during early morning boils.",
                        'Fall': "Target: Smallmouth Bass. Gear: 7'0\" Med-Light Spinning Rod. Lure: Drop-shot rigs with 3\" Roboworms or small finesse swimbaits."
                    },
                    'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)': {
                        'Winter': "Target: Blue Catfish & Crappie. Gear: 7'6\" Heavy Catfish Rod. Lure: Carolina Rigs with fresh-cut skipjack or 2\" Bobby Garland jigs.",
                        'Spring': "Target: Largemouth Bass. Gear: 7'2\" Heavy Rod, 50lb Braid. Lure: Hollow-body Frogs or black/blue jigs pitched into heavy grass.",
                        'Summer': "Target: Redfish & Snook. Gear: 7'0\" Medium Saltwater Spinning Rod. Lure: 1/2oz Gold Spoons or Paddletails on weedless hooks.",
                        'Fall': "Target: Striped Bass & Redfish. Gear: 7'0\" Med-Heavy Rod. Lure: 5\" White Swimbaits or large 'Popping Cork' rigs with live shrimp imitations."
                    },
                    'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)': {
                        'Winter': "Target: Pike & Perch. Gear: Tip-ups & 24\" Ultra-Light Rods. Lure: Large dead Smelt on quick-strike rigs or small Swedish Pimples.",
                        'Spring': "Target: Striped Bass & Shad. Gear: 9'0\" Surf Rod or 7'0\" Med-Heavy Spinning. Lure: 7\" SP Minnows or white bucktail jigs with trailers.",
                        'Summer': "Target: Fluke & Bluefish. Gear: 7'0\" Medium Boat Rod. Lure: Bucktails tipped with Gulp! Grubs or metal 'Diamond Jigs'.",
                        'Fall': "Target: Tautog & Salmon. Gear: 7'0\" Heavy Conventional Rod. Lure: Crab-flavored jigs for Tog; Orange/Gold spoons for Salmon in rivers."
                    }
                }

                region_data = gear_map.get(regional_ptg, {})
                final_advice = region_data.get(ptg_season, "Bring a 7'0\" Medium spinning rod and a variety of soft plastics and inline spinners.")

                return f"Gear Recommendation — {regional_ptg} ({ptg_season}): {final_advice}"

        if cid == 6:
            if step == 6.1: 
                yest_p = float(data.get('yesterdays_pressure', 0) or 0)
                today_p = float(data.get('todays_pressure', 0) or 0)
                is_precip = data.get('is_precip') == True
                low_t = float(data.get('low_temp', 0) or 0)
                high_t = float(data.get('high_temp', 0) or 0)
                wind_dir = data.get('wind_dir', 'North')
                wind_low = float(data.get('wind_low', 0) or 0)
                wind_high = float(data.get('wind_high', 0) or 0)

                p_change = today_p - yest_p
                t_spread = high_t - low_t
                w_gust = wind_high - wind_low
        
                p_trend = "Rising" if p_change > 0.05 else "Falling" if p_change < -0.05 else "Steady"
                t_trend = "Warming" if t_spread > 15 else "Stable" if t_spread >= 5 else "Cold Snap"

                if is_precip and low_t <= 32:
                    condition = "Blizzard/Freeze Event"
                    advice = "Fish deep or near warm water discharges; ice safety is paramount."
                elif is_precip and p_trend == "Falling":
                    condition = "Low Pressure Storm System"
                    advice = "Aggressive feeding window before the front hits. Use fast-moving baits."
                elif p_trend == "Rising" and wind_dir in ['North', 'Northwest']:
                    condition = "Cold Frontal Passage"
                    advice = "Post-frontal blues. Fish slow, tight to cover, and downsize your lures."
                elif p_change == 0 and t_spread < 5:
                    condition = "Stationary Front"
                    advice = "Consistent but slow. Target suspension zones in the water column."
                elif p_trend == "Falling" and w_gust > 15:
                    condition = "Occluded Front (Impending Storm)"
                    advice = "High wind. Target wind-blown shorelines where baitfish are pushed."
                else:
                    condition = "Standard Transitional Weather"
                    advice = "Standard patterns apply. Match your depth to the temp high."

                return f"Trend: {condition}. {advice} (Pressure: {p_trend} | Air: {t_trend})"

            if step == 6.2: 
                category = data.get('stat_category', 'Line Statistics')
                budget = float(data.get('stat_budget', 0) or 0)
                env = data.get('stat_environment', 'Freshwater')
                priority = data.get('stat_priority', 'Versatility')

                if category == 'Line Statistics':
                    vol_efficiency = "320%" if priority == 'Price Efficiency' else "410%"
                    stretch_factor = "1-3%" if priority == 'Breaking Strength' else "25-30% (Mono)"
            
                    result = (
                        f"Statistical Analysis: In {env} environments, Braid yields a {vol_efficiency} increase in spool "
                        f"capacity over Mono. Priority ({priority}) indicates: "
                    )
                    if priority == 'Breaking Strength':
                        result += "Sufix 832 or Berkley Fireline (0% stretch, high knot integrity)."
                    elif priority == 'Price Efficiency':
                        result += "Bulk spool KastKing or Piscifun (high strength-to-dollar ratio)."
                    else:
                        result += "Fluorocarbon leader to Braid mainline (best of both worlds)."

                elif category == 'Rod Statistics':
                    efficiency_score = (budget / 60) * 1.5 if budget < 200 else (budget / 500) * 0.8
            
                    result = f"Analysis for ${budget:.0f} {env} Rod: "
                    if priority == 'Durability':
                        result += "Ugly Stik GX2 (Clear Tip Tech) remains the statistical outlier for lifespan."
                    elif priority == 'Versatility':
                        result += "7'0\" Medium-Fast Graphite Composite. Covers 92% of standard lures."
                    else: 
                        result += "Shimano Sellus or Daiwa Aird-X; high-modulus carbon feel at sub-$60 pricing."

                elif category == 'Reel Statistics':
                    seal_rating = "IPX5 or higher" if env == 'Saltwater' else "Shielded Bearings"
            
                    result = f"Reel Statistics ({env}): "
                    if priority == 'Durability':
                        result += f"Penn Spinfisher/Battle series (Full Metal Body) rated for 5+ years with {seal_rating}."
                    elif priority == 'Price Efficiency':
                        result += "Piscifun Viper/Carbon X. Performance matches $150 name-brands at 45% lower cost."
                    else: 
                        result += "Shimano Stradic (Hagane Gear). Statistical peak of weight-to-power ratio."

                elif category == 'Lure Statistics':
                    result = f"Lure Efficiency ({priority}): "
                    if env == 'Freshwater':
                        result += "Stick Baits (Senkos) have the highest 'Catch-Per-Hour' but highest cost-per-lure."
                    else:
                        result += "Paddle-tail swimbaits on jig heads represent the best ROI in Saltwater."
            
                    if priority == 'Price Efficiency':
                        result += " Recommendation: Z-Man ElaZtech (10x durability per plastic ensures 100+ catches/bait)."

                return result

            if step == 6.3: 
                strategy = data.get('strategy_type', 'Geology Advice')
                water = data.get('water_type', 'Rivers/Streams')
                intensity = int(data.get('strategy_intensity', 1))

                if strategy == 'Geology Advice':
                    if water == 'Rivers/Streams':
                        advice = ("Focus on 'Pool-Riffle' sequences. Fish sit in the deep pools to save energy "
                          "and move to the gravel riffles to feed. Look for 'Outside Bends' where "
                          "current carves deep undercut banks.")
                    elif water == 'Large Lakes/Reservoirs':
                        advice = ("Search for submerged 'Points' and 'Humps.' These act as underwater highways. "
                          "Gravel beds are ideal for spawning, while chunk rock (rip-rap) holds heat and crawfish.")
                    else:
                        advice = "Target transition lines where mud changes to sand or rock. Fish love 'edges'."

                elif strategy == 'Hydrology Advice':
                    if water == 'Rivers/Streams':
                        advice = ("Identify 'Eddies' (swirling reverse current) behind boulders. Fish sit in the slack "
                          "water facing upstream to grab food. 'Bottlenecks' increase current speed and oxygen.")
                    elif water == 'Large Lakes/Reservoirs':
                        advice = ("Look for 'Thermoclines'—the layer where warm surface water meets cold deep water. "
                          "In summer, fish often suspend exactly at this depth for optimal oxygen and temp.")
                    else:
                        advice = "Wind-driven current is key. Fish the windward shore where plankton and bait are pushed."

                elif strategy == 'Weather Advice':
                    advice = ("Low/Falling Pressure (Pre-Front): Fish are highly active. Use fast, vibrating baits. "
                      "High Pressure (Post-Front): Fish move deep into heavy cover. Use slow, finesse baits. "
                      "Overcast skies allow fish to roam; bright sun pushes them to shade/depth."
                    )

                else:
                    advice = ("Predators (Bass, Pike, Snook) stay near 'Structure' (wood/docks) or 'Cover' (weeds). "
                      "Pelagic fish (Tuna, Stripers, Walleye) follow 'Forage' (baitfish schools). "
                      "If you find the bait on your electronics, the predators are within 50 yards."
                    )

                if intensity == 3:
                    advice = f"[ADVANCED ANALYSIS] {advice} Note: Monitor Barometric Delta (>0.02 inHg/hr) for trigger events."
        
                return f"Strategic Rundown — {strategy}: {advice}"

        if cid == 7: #MORE SPECIES AND CLASSIFICATIONS NEEDED 
            if step == 7.1: 
                lure = data.get('lure_selection', 'Crankbait')
                species = data.get('species_selection', 'Largemouth')
                hours = int(data.get('catch_effort', 1))

                rarity_map = {
                    ('Carp', 'Crankbait'): [10, "Legendary. Carp are primarily suction feeders; hitting a crankbait suggests extreme aggression or a foul hook."],
                    ('Carp', 'Small Plastics'): [7, "Rare. Small nymphs or grubs can fool carp if presented perfectly on the bottom."],
                    #for structure and expansion ('Carp', 'Small Plastics'): [7, "Rare. Small nymphs or grubs can fool carp if presented perfectly on the bottom."],
                    #for structure and expansion ('Carp', 'Small Plastics'): [7, "Rare. Small nymphs or grubs can fool carp if presented perfectly on the bottom."],
                    #for structure and expansion ('Carp', 'Small Plastics'): [7, "Rare. Small nymphs or grubs can fool carp if presented perfectly on the bottom."],
                    ('Sucker Species', 'Jig'): [8, "Very Rare. Suckers rarely strike moving predatory lures unless bumped or 'flossed'."],
                    #for structure and expansion ('Sucker Species', 'Jig'): [8, "Very Rare. Suckers rarely strike moving predatory lures unless bumped or 'flossed'."],
                    #for structure and expansion ('Sucker Species', 'Jig'): [8, "Very Rare. Suckers rarely strike moving predatory lures unless bumped or 'flossed'."],
                    #for structure and expansion ('Sucker Species', 'Jig'): [8, "Very Rare. Suckers rarely strike moving predatory lures unless bumped or 'flossed'."],
                    ('Freshwater Drum', 'Crankbait'): [2, "Common. Drum are highly aggressive predators of crawfish and shad imitations."],
                    #for structure and expansion ('Freshwater Drum', 'Crankbait'): [2, "Common. Drum are highly aggressive predators of crawfish and shad imitations."],
                    #for structure and expansion ('Freshwater Drum', 'Crankbait'): [2, "Common. Drum are highly aggressive predators of crawfish and shad imitations."],
                    #for structure and expansion ('Freshwater Drum', 'Crankbait'): [2, "Common. Drum are highly aggressive predators of crawfish and shad imitations."],
                    #for structure and expansion ('Freshwater Drum', 'Crankbait'): [2, "Common. Drum are highly aggressive predators of crawfish and shad imitations."],
                    ('Walleye', 'Topwater'): [9, "Extremely Rare. Walleyes are light-sensitive bottom dwellers; catching one on the surface is a 'once-in-a-career' event."],
                    #for structure and expansion ('Walleye', 'Topwater'): [9, "Extremely Rare. Walleyes are light-sensitive bottom dwellers; catching one on the surface is a 'once-in-a-career' event."],
                    #for structure and expansion ('Walleye', 'Topwater'): [9, "Extremely Rare. Walleyes are light-sensitive bottom dwellers; catching one on the surface is a 'once-in-a-career' event."],
                    #for structure and expansion  ('Walleye', 'Topwater'): [9, "Extremely Rare. Walleyes are light-sensitive bottom dwellers; catching one on the surface is a 'once-in-a-career' event."],
                    ('Pike / Muskie', 'Ned Rig / Tube'): [6, "Uncommon. Known as 'bite-offs.' These fish usually snap light finesse line instantly."],
                    #for structure and expansion ('Pike / Muskie', 'Ned Rig / Tube'): [6, "Uncommon. Known as 'bite-offs.' These fish usually snap light finesse line instantly."],
                    #for structure and expansion ('Pike / Muskie', 'Ned Rig / Tube'): [6, "Uncommon. Known as 'bite-offs.' These fish usually snap light finesse line instantly."],
                    #for structure and expansion ('Pike / Muskie', 'Ned Rig / Tube'): [6, "Uncommon. Known as 'bite-offs.' These fish usually snap light finesse line instantly."],
                    #for structure and expansion ('Pike / Muskie', 'Ned Rig / Tube'): [6, "Uncommon. Known as 'bite-offs.' These fish usually snap light finesse line instantly."],
                    ('Trout', 'Topwater'): [3, "Common (Dry Fly context) / Rare (Lure context). On hard baits, this is a high-energy strike."],
                    #for structure and expansion ('Trout', 'Topwater'): [3, "Common (Dry Fly context) / Rare (Lure context). On hard baits, this is a high-energy strike."],
                    #for structure and expansion ('Trout', 'Topwater'): [3, "Common (Dry Fly context) / Rare (Lure context). On hard baits, this is a high-energy strike."],
                    #for structure and expansion ('Trout', 'Topwater'): [3, "Common (Dry Fly context) / Rare (Lure context). On hard baits, this is a high-energy strike."],
                    ('Panfish', 'Glidebait'): [10, "Mathematically Impossible (although swipes arent unheard of). A trophy-sized glidebait is usually larger than the panfish itself."],
                    #for structure and expansion ('Panfish', 'Glidebait'): [10, "Mathematically Impossible (although swipes arent unheard of). A trophy-sized glidebait is usually larger than the panfish itself."],
                    #for structure and expansion  ('Panfish', 'Glidebait'): [10, "Mathematically Impossible (although swipes arent unheard of). A trophy-sized glidebait is usually larger than the panfish itself."],
                    #for structure and expansion ('Panfish', 'Glidebait'): [10, "Mathematically Impossible (although swipes arent unheard of). A trophy-sized glidebait is usually larger than the panfish itself."],
                    ('Largemouth', 'Ned Rig / Tube'): [1, "Standard. This is a primary finesse technique for this species."],
                    #for structure and expansion ('Largemouth', 'Ned Rig / Tube'): [1, "Standard. This is a primary finesse technique for this species."],
                    #for structure and expansion ('Largemouth', 'Ned Rig / Tube'): [1, "Standard. This is a primary finesse technique for this species."],
                    #for structure and expansion ('Largemouth', 'Ned Rig / Tube'): [1, "Standard. This is a primary finesse technique for this species."],
                    ('Largemouth', 'Ned Rig / Tube'): [1, "Standard. This is a primary finesse technique for this species."],
                    ('Salmon', 'Spoon/Spinner'): [1, "Standard. These trigger the 'aggression response' in migratory salmon."],
                    #for structure and expansion ('Salmon', 'Spoon/Spinner'): [1, "Standard. These trigger the 'aggression response' in migratory salmon."],
                    #for structure and expansion ('Salmon', 'Spoon/Spinner'): [1, "Standard. These trigger the 'aggression response' in migratory salmon."],
                    #for structure and expansion ('Salmon', 'Spoon/Spinner'): [1, "Standard. These trigger the 'aggression response' in migratory salmon."]
                }

                catch_data = rarity_map.get((species, lure), [5, "A standard predatory interaction. Consistent with seasonal feeding patterns."])
                score = catch_data[0]
                insight = catch_data[1]

                if score >= 9: tier = "MYTHICAL"
                elif score >= 7: tier = "RARE"
                elif score >= 4: tier = "UNCOMMON"
                else: tier = "COMMON"

                effort_mod = " (High Effort Result)" if hours > 8 else ""

                return f"Result: [{tier}]{effort_mod} - {species} on a {lure}. {insight}"

            if step == 7.2: 
                region = data.get('reg_selection', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)')
                season = data.get('season_selection', 'Summer')
                species = data.get('spec_selection', 'Walleye')

                rarity_matrix = {
                    ('Peacock Bass', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Winter'): [10, "Impossible. Peacock Bass are intolerant to water below 60°F; this would be a captive escapee."],
                    ('Tarpon', 'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)', 'Summer'): [8, "Very Rare. Known as 'Vagrant' catches; Tarpon occasionally follow warm Gulf Stream eddies north in August."],
            
                    ('Bull Shark', 'Lower Midwest (OH, IN, MS, KS, NB)', 'Summer'): [9, "Legendary. While Bull Sharks can tolerate freshwater, reaching the Midwest via the Mississippi is a rare historical anomaly."],
            
                    ('Chinook Salmon', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Spring'): [7, "Rare. Most Great Lakes Chinook are offshore in deep water; finding them in accessible shallows is uncommon until Fall."],
                    ('Walleye', 'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)', 'Summer'): [6, "Uncommon. Southern Walleye exist but retreat to extreme depths or spring-fed thermal refuges in heat."],
            
                    ('Snakehead', 'Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Summer'): [9, "Alarming. This species is invasive and typically found in the Mid-Atlantic; a catch here indicates a new range expansion."],
                    ('Arctic Grayling', 'PNW (OR, WA, ID, MONTANA, AK)', 'Summer'): [3, "Common (AK/Montana) / Rare (OR/WA). Highly dependent on specific high-altitude cold-water pockets."],
            
                    ('Largemouth Bass', 'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)', 'Spring'): [1, "Standard. This is the heart of the species' range during their most active period."],
                    ('Smallmouth Bass', 'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)', 'Fall'): [1, "Standard. Peak feeding window as fish transition to wintering holes."]
                }

                result_data = rarity_matrix.get((species, region, season), [5, "Moderate. The species is present in this region, but seasonal conditions make the encounter unpredictable."])
                score = result_data[0]
                insight = result_data[1]

                if score >= 9: tier, color = "EXTREME ANOMALY", "🔴"
                elif score >= 7: tier, color = "REGIONAL RARITY", "🟡"
                elif score >= 4: tier, color = "SEASONAL CHALLENGE", "🔵"
                else: tier, color = "EXPECTED ENCOUNTER", "🟢"

                return f"{color} {tier} (Score: {score}/10): {species} in {region} during {season}. {insight}"

            if step == 7.3: 
                species = data.get('target_species', 'Walleye')
                companion = data.get('companion_species', 'None/Unknown')
                season = data.get('current_season', 'Summer')
                effort = float(data.get('fishing_effort_hours', 1.0))

                base_cpue = {
                    'Walleye': 0.5,       
                    'Largemouth Bass': 0.8,
                    'Smallmouth Bass': 0.7,
                    'Channel Catfish': 0.6,
                    'Crappie': 1.2,
                    'Northern Pike': 0.3,
                    'Yellow Perch': 2.5   
                }

                companion_mods = {
                    ('Walleye', 'Emerald Shiner'): 1.25,  
                    ('Walleye', 'Round Goby'): 0.85,     
                    ('Largemouth Bass', 'Bluegill'): 1.30, 
                    ('Smallmouth Bass', 'Round Goby'): 1.40, 
                    ('Yellow Perch', 'White Perch'): 0.70, 
                    ('Crappie', 'Gizzard Shad'): 1.20      
                }

                season_mods = {
                    'Spring': 1.4, 
                    'Summer': 1.0, 
                    'Fall': 1.25, 
                    'Winter': 0.6  
                }

                p_base = base_cpue.get(species, 0.5)
                assoc_mod = companion_mods.get((species, companion), 1.0)
                time_mod = season_mods.get(season, 1.0)

                expected_catch = (p_base * assoc_mod * time_mod) * effort
        
                # 1 - e^(-EC) -- simplified scaling 
                prob_percentage = min(99, (1 - (2.718 ** -expected_catch)) * 100)

                insight = f"In {season}, {species} populations often interact with {companion}. "
                if assoc_mod > 1.0:
                    insight += "This association is a positive forage link, increasing local abundance."
                elif assoc_mod < 1.0:
                    insight += "High competition for resources may decrease your strike frequency."

                return f"Overall Probability: {prob_percentage:.1f}% — Expected Catch: {expected_catch:.2f} fish in {effort} hrs. {insight}"

        if cid == 8:
            if step == 8.1:
                species = data.get('species', '').strip()
                time_c = data.get('time_caught')
                date_c = data.get('date_caught')
                weather = data.get('weather_conditions')
                lure = data.get('lure_used')
    
                if not species:
                    return "System Error: Missing required 'species' field parameter."
        
                try:
                    new_catch = Catch(
                        species=species,
                        time_caught=time_c,
                        date_caught=date_c,
                        weather_conditions=weather,
                        lure_used=lure
                    )
                    db.session.add(new_catch)
                    db.session.commit()

                    rows = Catch.query.order_by(Catch.id.desc()).limit(5).all()
        
                    history_list = ""
                    for r in rows:
                        history_list += f"\n- {r.species} | {r.date_caught or 'N/A'} | {r.lure_used or 'None'}"
            
                    return f"Success! Catch logged. Recent History:{history_list}"
        
                except Exception as err:
                    db.session.rollback()
                    return f"Database Error: {str(err)}"

            if step == 8.2:
                loc = data.get('location_name', 'Unknown').strip() or 'Unknown'
                success = data.get('trip_success', 0)
                species = data.get('primary_species', 'None').strip() or 'None'
                lures = data.get('lures_used', 'None').strip() or 'None'
                time_e = data.get('time_elapsed', '0').strip() or '0'
                season = data.get('season', 'Unknown').strip() or 'Unknown'
    
                try:
                    try:
                        success_rating = int(success)
                    except (ValueError, TypeError):
                        success_rating = 0

                    new_trip = Trip(
                        location_name=loc,
                        trip_success=success_rating,
                        primary_species=species,
                        lures_used=lures,
                        time_elapsed=time_e,
                        season=season
                    )
                    db.session.add(new_trip)
                    db.session.commit()
        
                    rows = Trip.query.order_by(Trip.id.desc()).limit(5).all()
        
                    history_list = ""
                    for r in rows:
                        history_list += f"\n- {r.location_name} | Rating: {r.trip_success}/10 | Targeted: {r.primary_species}"
            
                    return f"Success! Trip at {loc} saved. Recent History:{history_list}"
        
                except Exception as err:
                    db.session.rollback()
                    return f"Database Error: {str(err)}"

            if step == 8.3:
                date = data.get('log_date')

                try:
                    p_low = float(data.get('pressure_low', 1013) or 1013)
                    p_high = float(data.get('pressure_high', 1013) or 1013)
                    w_low = float(data.get('wind_speed_low', 0) or 0)
                    w_high = float(data.get('wind_high', 0) or 0)
                    t_min = int(data.get('temp_min', 0) or 0)
                    t_max = int(data.get('temp_max', 0) or 0)
                except (ValueError, TypeError):
                    p_low, p_high = 1013.0, 1013.0
                    w_low, w_high = 0.0, 0.0
                    t_min, t_max = 0, 0

                w_dir = data.get('wind_dir', 'N')
    
                p_delta = p_high - p_low
                t_delta = t_max - t_min
                trends = []
    
                if p_delta > 5:
                    trends.append("Developing Frontal Boundary")
                if w_high - w_low > 15:
                    trends.append("Gusty/Unstable Conditions")
                if p_low < 1000:
                    trends.append("Low Pressure Storm Risk")
                if w_dir in ['NW', 'N'] and t_delta < 10:
                    trends.append("Possible Cold Frontal Passage")
                elif w_dir in ['S', 'SW'] and t_delta > 15:
                    trends.append("Warm Frontal Incursion")
        
                trend_analysis = " | ".join(trends) if trends else "No notable trends recognized."
    
                try:
                    new_log = WeatherLog(
                        log_date=date,
                        pressure_low=p_low,
                        pressure_high=p_high,
                        wind_speed_low=w_low,
                        wind_high=w_high,
                        wind_dir=w_dir,
                        temp_min=t_min,
                        temp_max=t_max,
                        trend_analysis=trend_analysis
                    )
                    db.session.add(new_log)
                    db.session.commit()

                    rows = WeatherLog.query.order_by(WeatherLog.id.desc()).limit(3).all()
                    history = "".join([f"\n- {r.log_date}: {r.trend_analysis}" for r in rows])
        
                    return f"Success! Weather for {date} logged as {trend_analysis}. History:{history}"
        
                except Exception as err:
                    db.session.rollback()
                    return f"Database Error: {str(err)}"

        if cid == 9:
            if step == 9.1:
                city = data.get('city_input', 'Chicago').strip()
                api_key = "YU87AQZC9FSKBEL8GL97CD6K3"
                url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/today"
                params = {"unitGroup": "us", "key": api_key, "include": "current", "contentType": "json"}
    
                try:
                    response = requests.get(url, params=params, timeout=10)
                    response.raise_for_status()
        
                    current = response.json().get('currentConditions', {})
                    temp = current.get('temp', 0)
                    pressure = current.get('pressure', 1013)
                    precip = current.get('precip', 0)
                    w_speed = current.get('windspeed', 0)
                    w_dir_deg = current.get('winddir', 0)
        
                    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                    w_dir = dirs[int((w_dir_deg + 22.5) % 360 / 45)]
        
                    log_entry = ApiWeatherLog(
                        location=city,
                        temp=float(temp),
                        pressure=float(pressure),
                        precip=float(precip),
                        wind_speed=float(w_speed),
                        wind_dir=w_dir
                    )
                    db.session.add(log_entry)
                    db.session.commit()
        
                    rows = ApiWeatherLog.query.order_by(ApiWeatherLog.id.desc()).limit(5).all()
                    history = "".join([f"\n- {r.location}: {r.temp}°F at {r.logged_at.strftime('%H:%M:%S')}" for r in rows])
        
                    return f"Current in {city}: {temp}°F, {w_speed}mph {w_dir}, {pressure}mb. History:{history}"
        
                except Exception as e:
                    db.session.rollback()
                    return f"System Error: {str(e)}"

            if step == 9.2:
                raw_city = data.get('city_input', 'Chicago').strip()
                city = quote(raw_city)
                start = data.get('date_start')
                end = data.get('date_end')
                api_key = "YU87AQZC9FSKBEL8GL97CD6K3"
    
                if not start or not end:
                    return "System Error: Missing required Start Date or End Date parameters."
        
                try:
                    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
                    url = f"{base_url}{city}/{start}/{end}"
        
                    params = {
                        "unitGroup": "us",
                        "key": api_key,
                        "include": "days",
                        "contentType": "json"
                    }
        
                    response = requests.get(url, params=params, timeout=12, verify=True)
                    response.raise_for_status()
        
                    days = response.json().get('days', [])
                    trend = "Stable"
        
                    for i in range(len(days)):
                        day = days[i]
                        trend = "Stable"
            
                        if i > 0:
                            prev = days[i-1]
                            current_temp = day.get('temp', 0) or 0
                            prev_temp = prev.get('temp', 0) or 0
                            current_pressure = day.get('pressure', 1013.25) or 1013.25
                
                            if current_temp - prev_temp < -10:
                                trend = "Cold Front"
                            elif current_pressure < 1000:
                                trend = "Storm Alert"
 
                        try:
                            parsed_logged_at = datetime.strptime(day['datetime'], '%Y-%m-%d')
                        except (ValueError, KeyError):
                            parsed_logged_at = datetime.utcnow()
                
                        log_entry = ApiWeatherLog(
                            location=raw_city,
                            temp=float(day.get('temp', 0) or 0),
                            pressure=float(day.get('pressure', 1013.25) or 1013.25),
                            precip=float(day.get('precip', 0) or 0),
                            wind_speed=float(day.get('windspeed', 0) or 0),
                            wind_dir=None,  
                            trends=f"Trend: {trend}", 
                            logged_at=parsed_logged_at
                        )
                        db.session.add(log_entry)
            
                    db.session.commit()
                    return f"Success! {len(days)} days logged for {raw_city}. Recent Trends detected: {trend}."
        
                except Exception as err:
                    db.session.rollback()
                    return f"System Error: {str(err)}"
                    
            if step == 9.3:
                raw_city = data.get('city_input', 'Chicago').strip()
                api_key = "YU87AQZC9FSKBEL8GL97CD6K3"
    
                try:
                    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
                    url = f"{base_url}{raw_city}/today"
        
                    params = {
                        "unitGroup": "us",
                        "key": api_key,
                        "include": "current",
                        "contentType": "json"
                    }
        
                    response = requests.get(url, params=params, timeout=10)
                    response.raise_for_status()
        
                    current = response.json().get('currentConditions', {})
                    temp = current.get('temp', 0)
                    pressure = current.get('pressure', 1013)
                    w_speed = current.get('windspeed', 0)
        
                    prob = 50
                    reasons = []

                    parsed_pressure = float(pressure or 1013)
        
                    if 1005 <= parsed_pressure <= 1015:
                        prob += 20
                        reasons.append("Stable Pressure")
                    elif parsed_pressure < 1005:
                        prob += 10
                        reasons.append("Falling Barometer (Active Feed)")
            
                    final_score = max(5, min(95, prob))
                    verdict = "EXCELLENT" if final_score > 75 else "GOOD" if final_score > 50 else "TOUGH"
                    trends_payload = f"Prob: {final_score}% ({verdict})"
        
                    new_log = ApiWeatherLog(
                        location=raw_city,
                        temp=float(temp or 0),
                        pressure=parsed_pressure,
                        wind_speed=float(w_speed or 0),
                        wind_dir=None,
                        precip=0.0,
                        trends=trends_payload,
                        reasons=", ".join(reasons) if reasons else "No anomalous readings"  
                    )
                    db.session.add(new_log)
                    db.session.commit()
        
                    return f"Success! {raw_city} 'good day' Odds: {final_score}% ({verdict})."
        
                except Exception as e:
                    try:
                        db.session.rollback()
                    except Exception:
                        pass 
                    return f"System Error: {str(e)}"

@fishing_bp.route('/', methods=['GET']) 
def calculator_page():
    return render_template('dashboard.html')

@fishing_bp.route('/process_fishing', methods=['POST'])
def process_fishing():
    payload = request.get_json()
    cid = int(payload.get('cid'))
    step = float(payload.get('step'))
    data = payload.get('data')

    try:
        output = FishingCalculators.run_logic(cid, step, data)
        return jsonify({"success": True, "result": output})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
