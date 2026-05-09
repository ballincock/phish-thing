const cycleState = {
   1: 0,
   2: 0,
   3: 0,
   4: 0,
   5: 0,
   6: 0,
   7: 0,
   8: 0,
   9: 0
};

let currentCid = 1;
let currentStep = 1;
let amode = 0,
   cycles = Array(10).fill(1);
const calcConfig = {
   1: {
      name: "Spooling",
      1.1: {
         title: "Simple Spool",
         f: [{
            id: 'simple_ipt',
            t: 'number',
            l: 'Inches Per Turn',
            step: 1,
            min: 20,
            max: 45
         }, {
            id: 'simple_line_diameter',
            t: 'number',
            l: 'Line Diameter (mm)',
            step: 0.05,
            min: 0.10,
            max: 0.50
         }, {
            id: 'simple_yards',
            t: 'number',
            l: 'Desired Yards to Spool',
            step: 5,
            min: 5,
            max: 450
         }]
      },
      1.2: {
         title: "Mid Spool",
         f: [{
            id: 'mid_ipt',
            t: 'number',
            l: 'Inches Per Turn',
            step: 1,
            min: 20,
            max: 45
         }, {
            id: 'mid_line_diameter',
            t: 'number',
            l: 'Line Diameter (mm)',
            step: 0.05,
            min: 0.10,
            max: 0.50
         }, {
            id: 'mid_yards',
            t: 'number',
            l: 'Desired Yards to Spool',
            step: 5,
            min: 5,
            max: 450
         }, {
            id: 'mid_outer',
            t: 'number',
            l: 'Outer Spool Width (mm)',
            step: 1,
            min: 25,
            max: 60
         }, {
            id: 'mid_inner',
            t: 'number',
            l: 'Inner Spool Width (mm)',
            step: 1,
            min: 10,
            max: 40
         }]
      },
      1.3: {
         title: "Advanced Spool",
         f: [{
            id: 'adv_ipt',
            t: 'number',
            l: 'Inches Per Turn',
            step: 1,
            min: 20,
            max: 45
         }, {
            id: 'adv_line_diameter',
            t: 'number',
            l: 'Line Diameter (mm)',
            step: 0.05,
            min: 0.10,
            max: 0.50
         }, {
            id: 'adv_yards',
            t: 'number',
            l: 'Desired Yards to Spool',
            step: 5,
            min: 5,
            max: 450
         }, {
            id: 'adv_outer',
            t: 'number',
            l: 'Outer Spool Width (mm)',
            step: 1,
            min: 25,
            max: 60
         }, {
            id: 'adv_inner',
            t: 'number',
            l: 'Inner Spool Width (mm)',
            step: 1,
            min: 10,
            max: 40
         }, {
            id: 'adv_packing',
            t: 'range',
            l: 'Packing Tension',
            min: 0,
            max: 15
         }, {
            id: 'adv_linetype',
            t: 'select',
            o: ['Monofilament', 'Fluorocarbon', 'Braid', 'Stealth Braid', 'Fly Line'],
            l: 'Line Type'
         }]
      }
   },
   2: {
      name: "Weight",
      2.1: {
         title: "Simple Weight",
         f: [{
            id: 'simple_flength',
            t: 'number',
            l: 'Length (in)',
            step: 0.5,
            min: 3,
            max: 120
         }, {
            id: 'simple_fgirth',
            t: 'number',
            l: 'Girth (in)',
            step: 0.5,
            min: 3,
            max: 120
         }]
      },
      2.2: {
         title: "Mid Weight",
         f: [{
            id: 'mid_flength',
            t: 'number',
            l: 'Length (in)',
            step: 0.5,
            min: 3,
            max: 120
         }, {
            id: 'mid_fgirth',
            t: 'number',
            l: 'Girth (in)',
            step: 0.5,
            min: 3,
            max: 120
         }, {
            l: "Pre Spawn",
            t: "checkbox",
            id: "mid_is_spawning"
         }, {
            id: 'mid_datecaught',
            t: 'date',
            l: 'Date of Catch (Seasonality)'
         }]
      },
      2.3: {
         title: "Advanced Weight",
         f: [{
            id: 'adv_flength',
            t: 'number',
            l: 'Length (in)',
            step: 0.5,
            min: 3,
            max: 120
         }, {
            id: 'adv_fgirth',
            t: 'number',
            l: 'Length (in)',
            step: 0.5,
            min: 3,
            max: 120
         }, {
            l: "Pre Spawn",
            t: "checkbox",
            id: "adv_is_spawning"
         }, {
            id: 'adv_datecaught',
            t: 'date',
            l: 'Date of Catch (Seasonality)'
         }, {
            id: 'adv_armor',
            t: 'select',
            o: ['Normal (e.g. Bass)', 'Slight (e.g. Channel Catfish', 'Mid (e.g. King Salmon)', 'High (e.g. Bowfin/Gar)', 'Extreme (e.g. Lake Sturgeon)'],
            l: 'Armor Coefficient'
         }]
      }
   },
   3: {
      name: "Species",
      3.1: {
         title: "Regional Species",
         f: [{
            id: 'regional_r',
            t: 'select',
            o: ['Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Lower Midwest (OH, IN, MS, KS, NB', 'PNW (OR, WA, ID, MONTANA, AK)', 'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK', 'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)', 'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)'],
            l: 'Region'
         }, {
            id: 'regional_season',
            t: 'select',
            o: ['Winter', 'Spring', 'Summer', 'Fall'],
            l: 'Season'
         }]
      },
      3.2: {
         title: "Waterbody Specific",
         f: [{
            id: 'waterbody_state',
            t: 'select',
            o: ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'],
            l: 'State'
         }, {
            id: 'waterbody_season',
            t: 'select',
            o: ['Winter', 'Spring', 'Summer', 'Fall'],
            l: 'Season'
         }]
      },
      3.3: {
         title: "Species Advice",
         f: [{
            id: 'species_fadvice',
            t: 'select',
            o: ['Largemouth Bass', 'Smallmouth Bass', 'Freshwater Drum', 'Walleye', 'Sauger', 'Saugeye', 'White Bass', 'White Perch', 'Yellow Bass', 'Crappie', 'Yellow Perch', 'Coho Salmon', 'King salmon', 'Atlantic Salmon', , 'Pink Salmon', , 'Steelhead', 'Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Gila Trout', 'Golden Trout', 'Cutthroat Trout', 'Whitefish', 'Mountain Whitefish', 'Northern Pikeminnow', 'Peamouth', 'Suckers', 'Microfish', 'Commmon Panfish (BG, PS, GS, etc)', 'Pike', 'Muskie', 'Channel Catfish', 'Flathead Catfish', 'Bullheads'],
            l: 'Species'
         }, {
            id: 'advice_season',
            t: 'select',
            o: ['Winter', 'Spring', 'Summer', 'Fall'],
            l: 'Season'
         }]
      }
   },
   4: {
      name: "Gear Info.",
      4.1: {
         title: "Rod/Reel Information",
         f: [{
            id: 'hgear_info',
            t: 'select',
            o: ['Rod Weight Information', 'Rod Speed Information', 'Reel Gearing Information', 'Reel Capacity Information', 'Ultralight Info', 'Medium-Light Info', 'Medium Info', 'Medium Heavy Info', 'Heavy Info', 'Species Specific Inquiry'],
            l: 'Select an option from the dropdown:'
         }]
      },
      4.2: {
         title: "Lure Information",
         f: [{
            id: 'hlure_info',
            t: 'select',
            o: ['Crankbait Information', 'Jig Information', 'Spoon/Spinner Information', 'Microplastic Information', 'Catfish Rig Information', 'Live Bait Rig Information', 'Spinnerbait/Chatterbait Information', 'Swimbait Information', 'Glidebait Information', 'Ned Rig/Tube Information', 'Senko/Finneseplastic Information', 'Topwater Information', 'Very Small Fly Information', 'Fly Information', 'Large fly / Streamer Information', 'Bait Information'],
            l: 'Select an option from the dropdown:'
         }]
      },
      4.3: {
         title: "Money-Saving Tips",
         f: [{
            id: 'hjgwent_info',
            t: 'select',
            o: ['Lures', 'Bait', 'Rods', 'Reels', 'Tackle Accessories/Misc', 'Kayaks and Boats'],
            l: 'Select an option from the dropdown:'
         }]
      }
   },
   5: {
      name: "Plan a trip!",
      5.1: {
         title: "Where should I go?",
         f: [{
            id: 'regional_pt',
            t: 'select',
            o: ['Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Lower Midwest (OH, IN, MS, KS, NB', 'PNW (OR, WA, ID, MONTANA, AK)', 'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK', 'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)', 'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)'],
            l: 'Region'
         }, {
            id: 'pt_season',
            t: 'select',
            o: ['Winter', 'Spring', 'Summer', 'Fall'],
            l: 'Season'
         }]
      },
      5.2: {
         title: "What should I fish for?",
         f: [{
            id: 'regional_pt',
            t: 'select',
            o: ['Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Lower Midwest (OH, IN, MS, KS, NB', 'PNW (OR, WA, ID, MONTANA, AK)', 'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK', 'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)', 'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)'],
            l: 'Region'
         }, {
            id: 'pt_season',
            t: 'select',
            o: ['Winter', 'Spring', 'Summer', 'Fall'],
            l: 'Season'
         }]
      },
      5.3: {
         title: "What gear should I bring?",
         f: [{
            id: 'regional_ptg',
            t: 'select',
            o: ['Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Lower Midwest (OH, IN, MS, KS, NB', 'PNW (OR, WA, ID, MONTANA, AK)', 'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK', 'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)', 'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)'],
            l: 'Region'
         }, {
            id: 'ptg_season',
            t: 'select',
            o: ['Winter', 'Spring', 'Summer', 'Fall'],
            l: 'Season'
         }]
      }
   },
   6: {
      name: "References",
      6.1: {
         title: "Weather - Trend Parsing",
         f: [{
            id: 'yesterdays_pressure',
            t: 'number',
            l: 'Yesterdays Pressure (hPa - Sea level 1013.25 hPa) Step: 25',
            step: 25,
            min: 100,
            max: 1500
         }, {
            id: 'todays_pressure',
            t: 'number',
            l: 'Yesterdays Pressure (hPa - Sea level 1013.25 hPa) Step: 25',
            step: 25,
            min: 100,
            max: 1500
         }, {
            l: "Precipitating?",
            t: "checkbox",
            id: "is_precip"
         }, {
            id: 'low_temp',
            t: 'range',
            l: 'Temp. Low (Min -40 / Max 120 - Step: +/- 2.5)',
            min: -40,
            max: 120,
            step: 2.5
         }, {
            id: 'high_temp',
            t: 'range',
            l: 'Temp. High (Min -39 / Max 121 - Step: +/- 2.5)',
            min: -39,
            max: 121,
            step: 2.5
         }, {
            id: 'wind_dir',
            t: 'select',
            o: ['North', 'Northeast', 'Northwest', 'South', 'Southeast', 'Southwest', 'East', 'West'],
            l: 'Wind Direction'
         }, {
            id: 'wind_low',
            t: 'range',
            l: 'Wind Low (Min 0 / Max 30 - Step: +/- 1)',
            min: 0,
            max: 30,
            step: 1
         }, {
            id: 'wind_high',
            t: 'range',
            l: 'Wind High (Min 0 / Max 31 - Step: +/- 1)',
            min: 0,
            max: 31,
            step: 1
         }]
      },
      6.2: {
         title: "Gear - Statistical Analysis",
         f: [{
            id: 'stat_category',
            t: 'select',
            l: 'Analysis Category',
            o: ['Line Statistics', 'Rod Statistics', 'Reel Statistics', 'Lure Statistics']
         }, {
            id: 'stat_budget',
            t: 'range',
            l: 'Target Budget ($)',
            min: 20,
            max: 1000,
            step: 10
         }, {
            id: 'stat_environment',
            t: 'select',
            l: 'Water Type',
            o: ['Freshwater', 'Saltwater', 'Brackish']
         }, {
            id: 'stat_priority',
            t: 'select',
            l: 'Primary Goal',
            o: ['Versatility', 'Durability', 'Breaking Strength', 'Price Efficiency']
         }]
      },
      6.3: {
         title: "Strategic Rundown",
         f: [{
            id: 'strategy_type',
            t: 'select',
            l: 'Strategic Focus',
            o: ['Geology Advice', 'Hydrology Advice', 'Weather Advice', 'Species Localization']
         }, {
            id: 'water_type',
            t: 'select',
            l: 'Environment',
            o: ['Rivers/Streams', 'Large Lakes/Reservoirs', 'Small Ponds', 'Inshore/Saltwater']
         }, {
            id: 'strategy_intensity',
            t: 'range',
            l: 'Experience Level',
            min: 1,
            max: 3,
            step: 1
         }]
      }
   },
   7: {
      name: "Rarity",
      7.1: {
         title: "Species-Lure Rarity Analysis",
         f: [{
            id: 'lure_selection',
            t: 'select',
            l: 'Lure Type Used',
            o: ['Crankbait', 'Glidebait', 'Swimbait', 'Jig', 'Spoon/Spinner', 'Small Plastics', 'Topwater', 'Feather Jig', 'Straight Tail Jig', 'Ned Rig / Tube']
         }, {
            id: 'species_selection',
            t: 'select',
            l: 'Species Caught',
            o: ['Largemouth', 'Smallmouth', 'Freshwater Drum', 'Walleye', 'Carp', 'Sucker Species', 'Pike / Muskie', 'Panfish', 'Crappie', 'Trout', 'Salmon']
         }, {
            id: 'catch_effort',
            t: 'range',
            l: 'Hours Spent Fishing',
            min: 1,
            max: 24,
            step: 1
         }]
      },
      7.2: {
         title: "Species-Conditions Rarity",
         f: [{
            id: 'reg_selection',
            t: 'select',
            l: 'Region',
            o: ['Upper Midwest (MN, WI, MI, IL, N/S Dakota, IA)', 'Lower Midwest (OH, IN, MS, KS, NB)', 'PNW (OR, WA, ID, MONTANA, AK)', 'SW (AZ, NM, NV, TX, UTAH, CO, SCA, OK)', 'South (AR, AL, WV, TN, SC, NC, MS, LA, GE, FL, KY)', 'Northeast (ME, CT, MA, NH, DE, RI, VT, NJ, NY, PA, MD)']
         }, {
            id: 'season_selection',
            t: 'select',
            l: 'Season',
            o: ['Winter', 'Spring', 'Summer', 'Fall']
         }, {
            id: 'spec_selection',
            t: 'select',
            l: 'Species Encountered',
            o: ['Walleye', 'Largemouth Bass', 'Smallmouth Bass', 'Bull Shark', 'Alligator Gar', 'Arctic Grayling', 'Snakehead', 'Peacock Bass', 'Chinook Salmon', 'Tarpon']
         }]
      },
      7.3: {
         title: "Overall Probability of Catch",
         f: [{
            id: 'target_species',
            t: 'select',
            l: 'Target Species',
            o: ['Walleye', 'Largemouth Bass', 'Smallmouth Bass', 'Channel Catfish', 'Crappie', 'Northern Pike', 'Yellow Perch']
         }, {
            id: 'companion_species',
            t: 'select',
            l: 'Presence of Companion Species',
            o: ['None/Unknown', 'Gizzard Shad', 'Bluegill', 'Round Goby', 'White Perch', 'Emerald Shiner', 'Carp/Suckers']
         }, {
            id: 'current_season',
            t: 'select',
            l: 'Season',
            o: ['Winter', 'Spring', 'Summer', 'Fall']
         }, {
            id: 'fishing_effort_hours',
            t: 'range',
            l: 'Hours of Active Fishing',
            min: 1,
            max: 12,
            step: 0.5
         }]
      }
   },
   8: {
      name: "Databuilding",
      8.1: {
         title: "Log a Fishing Catch",
         f: [{
            id: 'species',
            t: 'select',
            l: 'Species',
            o: ['Largemouth Bass', 'Smallmouth Bass', 'Walleye', 'Pike', 'Trout']
         }, {
            id: 'time_caught',
            t: 'time',
            l: 'Time Caught'
         }, {
            id: 'date_caught',
            t: 'date',
            l: 'Date Caught'
         }, {
            id: 'weather_conditions',
            t: 'select',
            l: 'Weather',
            o: ['Sunny', 'Overcast', 'Rain']
         }, {
            id: 'lure_used',
            t: 'text',
            l: 'Lure/Bait Used'
         }]
      },
      8.2: {
         title: "Log a Trip (private)",
         f: [{
            id: 'step',
            t: 'hidden',
            v: 2
         }, {
            id: 'location_name',
            t: 'text',
            l: 'Location Name'
         }, {
            id: 'trip_success',
            t: 'range',
            l: 'Success (1-10)',
            min: 1,
            max: 10,
            step: 1
         }, {
            id: 'primary_species',
            t: 'select',
            l: 'Primary Species',
            o: ['Largemouth Bass', 'Smallmouth Bass', 'Walleye', 'Pike', 'Trout', 'Panfish']
         }, {
            id: 'lures_used',
            t: 'text',
            l: 'Lures Used'
         }, {
            id: 'time_elapsed',
            t: 'text',
            l: 'Time Elapsed'
         }, {
            id: 'season',
            t: 'select',
            l: 'Season',
            o: ['Winter', 'Spring', 'Summer', 'Fall']
         }]
      },
      8.3: {
         title: "Log the Weather",
         f: [{
            id: 'log_date',
            t: 'date',
            l: 'Today\'s Date'
         }, {
            id: 'pressure_low',
            t: 'range',
            l: 'Pressure Low (mb)',
            min: 950,
            max: 1050,
            step: 1
         }, {
            id: 'pressure_high',
            t: 'range',
            l: 'Pressure High (mb)',
            min: 950,
            max: 1050,
            step: 1
         }, {
            id: 'wind_speed_low',
            t: 'range',
            l: 'Wind Speed Low (mph)',
            min: 0,
            max: 100,
            step: 1
         }, {
            id: 'wind_high',
            t: 'range',
            l: 'Wind Speed High (mph)',
            min: 0,
            max: 100,
            step: 1
         }, {
            id: 'wind_dir',
            t: 'select',
            l: 'Wind Direction',
            o: ['N', 'E', 'S', 'W', 'NE', 'NW', 'SW', 'SE']
         }, {
            id: 'temp_min',
            t: 'range',
            l: 'Min Temperature (°F)',
            min: -40,
            max: 120,
            step: 1
         }, {
            id: 'temp_max',
            t: 'range',
            l: 'Max Temperature (°F)',
            min: -40,
            max: 120,
            step: 1
         }]
      }
   },
   9: {
      name: "Forecast",
      9.1: {
         title: "Current Weather Search",
         f: [{
            id: 'city_input',
            t: 'text',
            l: 'Enter City/Location',
            placeholder: 'e.g., Chicago, IL'
         }]
      },
      9.2: {
         title: "Historical Weather Range",
         f: [{
            id: 'city_input',
            t: 'text',
            l: 'Enter City/Location',
            placeholder: 'e.g., Miami, FL'
         }, {
            id: 'date_start',
            t: 'date',
            l: 'Start Date'
         }, {
            id: 'date_end',
            t: 'date',
            l: 'End Date'
         }]
      },
      9.3: {
         title: "Fishing Success Forecast",
         f: [{
            id: 'city_input',
            t: 'text',
            l: 'Enter City/Location',
            placeholder: 'e.g., Chicago, IL'
         }]
      }
   }
};

function renderGrid() {
   const grid = document.getElementById('button-grid');
   grid.innerHTML = '';

   for (let cid in calcConfig) {
      const btn = document.createElement('button');
      btn.className = 'grid-btn';
      btn.id = `btn-cat-${cid}`;

      const steps = Object.keys(calcConfig[cid]).filter(k => k !== 'name');
      const currentStepKey = steps[cycleState[cid]];
      const s = calcConfig[cid][currentStepKey];

      btn.innerHTML = `
                    <span style="font-size:0.7em; color:#8f94a8; text-transform:uppercase;">${calcConfig[cid].name}</span>
                    <span style="margin-top:5px;">${s.title}</span>
                    <div class="cycle-dots">
                        <div class="dot ${cycleState[cid] === 0 ? 'active' : ''}"></div>
                        <div class="dot ${cycleState[cid] === 1 ? 'active' : ''}"></div>
                        <div class="dot ${cycleState[cid] === 2 ? 'active' : ''}"></div>
                    </div>
                `;

      btn.onclick = () => {
         openModal(cid, currentStepKey);

         cycleState[cid] = (cycleState[cid] + 1) % 3;
         renderGrid();

      };
      grid.appendChild(btn);
   }
}

function openModal(cid, step) {
   const s = calcConfig[cid][step];
   let html = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <h3 style="color:#00a8ff; margin:0;">${s.title}</h3>
            <span style="color:#4e5467; font-size:0.7em; font-weight:bold;">${calcConfig[cid].name.toUpperCase()}</span>
        </div>
        <form id="activeForm">`;

   s.f.forEach(field => {
      html += `<div class="form-group"><label>${field.l}</label>`;

      if (field.t === 'select') {
         html += `<select id="${field.id}" class="calc-input">`;
         field.o.forEach(opt => html += `<option value="${opt}">${opt}</option>`);
         html += `</select>`;
      } else if (field.t === 'range') {
         html += `
                <div style="display:flex; align-items:center; gap:10px;">
                    <input type="range" id="${field.id}" min="${field.min}" max="${field.max}" step="${field.step}" 
                           class="calc-input" style="flex:1;" oninput="this.nextElementSibling.value = this.value">
                    <output style="color:#00a8ff; font-weight:bold; width:30px;">${field.min}</output>
                </div>`;
      } else {
         html += `<input type="${field.t}" id="${field.id}" placeholder="${field.placeholder || ''}" class="calc-input">`;
      }
      html += `</div>`;
   });

   html += `
        <div class="modal-footer">
            <button type="button" class="btn-cycle" onclick="cycleInModal('${cid}')">🔄 Next Mode</button>
            <button type="button" class="btn-run" onclick="runCalc('${cid}', '${step}')">Run Logic</button>
        </div>
        <button type="button" class="btn-close" onclick="closeModal()" style="width:100%; margin-top:15px; color:#fff; cursor:pointer; border:none; background:none;">Back to Grid</button>
    </form>`;

   document.getElementById('modal-body').innerHTML = html;
   document.getElementById('calcModal').classList.add('show');

   html += `
        <!--<button type="button" class="btn-run" onclick="runCalc('${cid}', '${step}')">Run Calculation</button>-->
        <button type="button" class="back-home" onclick="closeModal()">Back</button>
    </form>`;

   document.getElementById('modal-body').innerHTML = html;
   document.getElementById('calcModal').classList.add('show');
}

function cycleInModal(cid) {

   cycleState[cid] = (cycleState[cid] + 1) % 3;

   const steps = Object.keys(calcConfig[cid]).filter(k => k !== 'name');
   const nextStepKey = steps[cycleState[cid]];

   renderGrid();
   openModal(cid, nextStepKey);
}

async function runCalc(cid, step) {
   const s = calcConfig[cid][step];
   const data = {};
   s.f.forEach(f => data[f.id] = document.getElementById(f.id).value);

   const formElement = document.getElementById('activeForm');
   formElement.innerHTML = `<h3 style="color:#00a8ff">Processing...</h3>`;

   const res = await fetch('/process_fishing', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         cid,
         step,
         data
      })
   });
   const json = await res.json();

   formElement.innerHTML = `
        <h3 style="color:#00a8ff">Results</h3>
        <pre>${json.result}</pre>
        <div class="modal-footer">
            <button type="button" class="btn-run" onclick="closeModal()">Finish</button>
        </div>
    `;
}

function closeModal() {
   document.getElementById('calcModal').classList.remove('show');
}
renderGrid();
