const matrixCycleState = {
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

const matrixConfig = {
   1: {
      name: "Hydrology - Volume",
      "1.1": {
         title: "Pipe Capacity",
         fields: [{
            id: "pipe_dia_in",
            label: "Pipe Diameter (in)",
            type: "number",
            placeholder: "1"
         }, {
            id: "pipe_slope_ft_ft",
            label: "Pipe Slope (ft)",
            type: "number",
            placeholder: "1"
         }]
      },
      "1.2": {
         title: "Pond Volume",
         fields: [{
            id: "p_length",
            label: "Pipe Length",
            type: "number"
         }, {
            id: "p_width",
            label: "Pipe Width",
            type: "number"
         }, {
            id: "p_depth",
            label: "Pipe Depth",
            type: "number"
         }]
      },
      "1.3": {
         title: "V-Notch Weir",
         fields: [{
            id: "v_head_ft",
            label: "V-Head",
            type: "number"
         }]
      }
   },
   2: {
      name: "Hydrology - Flows",
      "2.1": {
         title: "Infiltration Rate",
         fields: [{
            id: "drop_inches",
            label: "Drop (in)",
            type: "number",
            placeholder: "10"
         }, {
            id: "time_minutes",
            label: "Time (min)",
            type: "number",
            placeholder: "10"
         }]
      },
      "2.2": {
         title: "Quick Runoff",
         fields: [{
            id: "r_area_acres",
            label: "R Area (acres)",
            type: "number"
         }, {
            id: "'r_intensity_in_hr",
            label: "R Intensity (hr)",
            type: "number"
         }]
      },
      "2.3": {
         title: "Orifice Flow",
         fields: [{
            id: "o_area_sqft",
            label: "O Area (sq. ft)",
            type: "number"
         }, {
            id: "o_head_ft",
            label: "O Head (ft)",
            type: "number"
         }]
      }
   },
   3: {
      name: "Hydrology - Runoff",
      "3.1": {
         title: "Time of Concentration",
         fields: [{
            id: "tc_length_ft",
            label: "TC Length (ft)",
            type: "number",
            placeholder: "10"
         }, {
            id: "tc_slope_ft_ft",
            label: "Time (min)",
            type: "number",
            placeholder: "10"
         }]
      },
      "3.2": {
         title: "NRCS Runoff Depth",
         fields: [{
            id: "precip_in",
            label: "Precipitation (in)",
            type: "number"
         }, {
            id: "cn_value",
            label: "CN Value",
            type: "number"
         }]
      },
      "3.3": {
         title: "Ditch Capacity",
         fields: [{
            id: "b_width_ft",
            label: "B Width (ft)",
            type: "number"
         }, {
            id: "flow_depth_ft",
            label: "Flow Depth (ft)",
            type: "number"
         },  {
            id: "side_slope_z",
            label: "Side Slope (z)",
            type: "number"
         },  {
            id: "ch_slope_ft_ft",
            label: "CH Slope (ft)",
            type: "number"
         }]
      }
   },
   4: {
      name: "Hydrology - Capacity",
      "4.1": {
         title: "RipRap Sizing",
         fields: [{
            id: "v_fps",
            label: "V (fps)",
            type: "number",
            placeholder: "10"
         }]
      },
      "4.2": {
         title: "Est. Detention Storage",
         fields: [{
            id: "q_peak_inflow",
            label: "Q Peak Inflow",
            type: "number"
         }, {
            id: "q_allowable_out",
            label: "Q Allowable (OUT)",
            type: "number"
         }, {
            id: "storm_duration_min",
            label: "Storm Duration (min)",
            type: "number"
         }]
      },
      "4.3": {
         title: "Curb Inlet Capacity",
         fields: [{
            id: "inlet_length_ft",
            label: "Inlet Length (ft)",
            type: "number"
         }, {
            id: "inlet_depth_ft",
            label: "Inlet Depth (ft)",
            type: "number"
         }]
      }
   },
   5: {
      name: "Hydrology - Flows",
      "5.1": {
         title: "Infiltration Rate",
         fields: [{
            id: "drop_inches",
            label: "Drop (in)",
            type: "number",
            placeholder: "10"
         }, {
            id: "time_minutes",
            label: "Time (min)",
            type: "number",
            placeholder: "10"
         }]
      },
      "5.2": {
         title: "Quick Runoff",
         fields: [{
            id: "r_area_acres",
            label: "R Area (acres)",
            type: "number"
         }, {
            id: "'r_intensity_in_hr",
            label: "R Intensity (hr)",
            type: "number"
         }]
      },
      "5.3": {
         title: "Orifice Flow",
         fields: [{
            id: "o_area_sqft",
            label: "O Area (sq. ft)",
            type: "number"
         }, {
            id: "o_head_ft",
            label: "O Head (ft)",
            type: "number"
         }]
      }
   },
   6: {
      name: "Hydrology - Flows",
      "6.1": {
         title: "Infiltration Rate",
         fields: [{
            id: "drop_inches",
            label: "Drop (in)",
            type: "number",
            placeholder: "10"
         }, {
            id: "time_minutes",
            label: "Time (min)",
            type: "number",
            placeholder: "10"
         }]
      },
      "6.2": {
         title: "Quick Runoff",
         fields: [{
            id: "r_area_acres",
            label: "R Area (acres)",
            type: "number"
         }, {
            id: "'r_intensity_in_hr",
            label: "R Intensity (hr)",
            type: "number"
         }]
      },
      "6.3": {
         title: "Orifice Flow",
         fields: [{
            id: "o_area_sqft",
            label: "O Area (sq. ft)",
            type: "number"
         }, {
            id: "o_head_ft",
            label: "O Head (ft)",
            type: "number"
         }]
      }
   },
   7: {
      name: "Hydrology - Flows",
      "7.1": {
         title: "Infiltration Rate",
         fields: [{
            id: "drop_inches",
            label: "Drop (in)",
            type: "number",
            placeholder: "10"
         }, {
            id: "time_minutes",
            label: "Time (min)",
            type: "number",
            placeholder: "10"
         }]
      },
      "7.2": {
         title: "Quick Runoff",
         fields: [{
            id: "r_area_acres",
            label: "R Area (acres)",
            type: "number"
         }, {
            id: "'r_intensity_in_hr",
            label: "R Intensity (hr)",
            type: "number"
         }]
      },
      "7.3": {
         title: "Orifice Flow",
         fields: [{
            id: "o_area_sqft",
            label: "O Area (sq. ft)",
            type: "number"
         }, {
            id: "o_head_ft",
            label: "O Head (ft)",
            type: "number"
         }]
      }
   },
   8: {
      name: "Hydrology - Flows",
      "8.1": {
         title: "Infiltration Rate",
         fields: [{
            id: "drop_inches",
            label: "Drop (in)",
            type: "number",
            placeholder: "10"
         }, {
            id: "time_minutes",
            label: "Time (min)",
            type: "number",
            placeholder: "10"
         }]
      },
      "8.2": {
         title: "Quick Runoff",
         fields: [{
            id: "r_area_acres",
            label: "R Area (acres)",
            type: "number"
         }, {
            id: "'r_intensity_in_hr",
            label: "R Intensity (hr)",
            type: "number"
         }]
      },
      "8.3": {
         title: "Orifice Flow",
         fields: [{
            id: "o_area_sqft",
            label: "O Area (sq. ft)",
            type: "number"
         }, {
            id: "o_head_ft",
            label: "O Head (ft)",
            type: "number"
         }]
      }
   },
   9: {
      name: "Hydrology - Flows",
      "9.1": {
         title: "Infiltration Rate",
         fields: [{
            id: "drop_inches",
            label: "Drop (in)",
            type: "number",
            placeholder: "10"
         }, {
            id: "time_minutes",
            label: "Time (min)",
            type: "number",
            placeholder: "10"
         }]
      },
      "9.2": {
         title: "Quick Runoff",
         fields: [{
            id: "r_area_acres",
            label: "R Area (acres)",
            type: "number"
         }, {
            id: "'r_intensity_in_hr",
            label: "R Intensity (hr)",
            type: "number"
         }]
      },
      "9.3": {
         title: "Orifice Flow",
         fields: [{
            id: "o_area_sqft",
            label: "O Area (sq. ft)",
            type: "number"
         }, {
            id: "o_head_ft",
            label: "O Head (ft)",
            type: "number"
         }]
      }
   }
};

function renderMatrixGridDeck() {
   const grid = document.getElementById('matrix-button-grid');
   if (!grid) return;
   grid.innerHTML = '';

   for (let cid in matrixConfig) {
      const btn = document.createElement('button');
      btn.className = 'grid-btn';
      btn.style = "display:flex; flex-direction:column; align-items:flex-start; text-align:left; width:100%; position:relative; min-height:110px; background:#1e1e1e; border:1px solid #2d2d2d; border-radius:8px; padding:15px; cursor:pointer;";

      const steps = Object.keys(matrixConfig[cid]).filter(k => k !== 'name');
      const activeStepKey = steps[matrixCycleState[cid]];
      const subFormSpec = matrixConfig[cid][activeStepKey];

      btn.innerHTML = `
            <span style="font-size:0.75rem; color:var(--primary); text-transform:uppercase; font-weight:bold; letter-spacing:0.5px;">${matrixConfig[cid].name}</span>
            <span style="margin-top:6px; font-size:1.05rem; color:#fff; font-weight:600;">${subFormSpec.title}</span>
            <span style="font-size:0.75rem; color:#666; margin-top:4px;">ID: ${cid} | Step: ${activeStepKey}</span>
            
            <div class="cycle-dots" style="position:absolute; bottom:15px; right:15px; display:flex; gap:6px;">
                <div style="width:6px; height:6px; border-radius:50%; background:${matrixCycleState[cid] === 0 ? 'var(--primary)' : '#333'}"></div>
                <div style="width:6px; height:6px; border-radius:50%; background:${matrixCycleState[cid] === 1 ? 'var(--primary)' : '#333'}"></div>
                <div style="width:6px; height:6px; border-radius:50%; background:${matrixCycleState[cid] === 2 ? 'var(--primary)' : '#333'}"></div>
            </div>
        `;

      btn.onclick = () => openMatrixModalFrame(cid, activeStepKey);
      grid.appendChild(btn);
   }
}

function openMatrixModalFrame(cid, step) {
   const subFormSpec = matrixConfig[cid][step];
   let html = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; border-bottom:1px solid #2d2d2d; padding-bottom:10px;">
            <h3 style="color:#fff; margin:0; font-size:1.2rem;">${subFormSpec.title}</h3>
            <span style="color:var(--primary); font-size:0.75rem; font-weight:bold; text-transform:uppercase;">${matrixConfig[cid].name}</span>
        </div>
        <form id="matrixActiveSubmissionForm" style="display:flex; flex-direction:column; gap:14px; margin:0;">
    `;

   subFormSpec.fields.forEach(f => {
      html += `<div style="display:flex; flex-direction:column; gap:5px;"><label style="color:#aaa; font-size:0.8rem;">${f.label}</label>`;
      if (f.type === 'select') {
         html += `<select id="${f.id}" style="background:#1e1e1e; color:#fff; border:1px solid #2d2d2d; border-radius:6px; padding:10px; font-size:0.85rem; width:100%;">`;
         f.options.forEach(opt => html += `<option value="${opt}">${opt}</option>`);
         html += `</select>`;
      } else if (f.type === 'range') {
         html += `
                <div style="display:flex; align-items:center; gap:12px;">
                    <input type="range" id="${f.id}" min="${f.min}" max="${f.max}" step="${f.step}" value="${f.min}" style="flex:1;" oninput="this.nextElementSibling.value = this.value">
                    <output style="color:var(--primary); font-weight:bold; font-size:0.9rem; width:30px; text-align:center;">${f.min}</output>
                </div>`;
      } else {
         html += `<input type="${f.type}" id="${f.id}" placeholder="${f.placeholder || ''}" style="background:#1e1e1e; color:#fff; border:1px solid #2d2d2d; border-radius:6px; padding:10px; font-size:0.85rem; box-sizing:border-box; width:100%;">`;
      }
      html += `</div>`;
   });

   html += `
            <div style="display:flex; gap:10px; margin-top:15px; justify-content:flex-end;">
                <button type="button" onclick="cycleModalSubMode('${cid}')" class="nav-back-btn" style="background:#1e1e1e; margin:0; border-color:#2d2d2d; color:#fff; border-radius:6px; padding:6px 12px; font-size:0.8rem; cursor:pointer;">🔄 Next Mode</button>
                <button type="button" onclick="dispatchMatrixExecution('${cid}', '${step}')" class="btn-primary" style="margin:0; width:auto; padding:6px 25px; font-weight:bold; border-radius:6px; background:var(--primary); border:none; color:#fff; font-size:0.8rem; cursor:pointer;">Run Logic</button>
            </div>
            <button type="button" onclick="closeMatrixModalFrame()" style="width:100%; margin-top:15px; color:#666; cursor:pointer; border:none; background:none; font-size:0.8rem; font-weight:bold;">Back to Grid Workspace</button>
        </form>
    `;

   document.getElementById('matrixModalBody').innerHTML = html;
   document.getElementById('matrixCalcModal').style.display = 'flex';
}

function cycleModalSubMode(cid) {
   matrixCycleState[cid] = (matrixCycleState[cid] + 1) % 3;
   const steps = Object.keys(matrixConfig[cid]).filter(k => k !== 'name');
   const nextStepKey = steps[matrixCycleState[cid]];
   renderMatrixGridDeck();
   openMatrixModalFrame(cid, nextStepKey);
}

async function dispatchMatrixExecution(cid, step) {
   const subFormSpec = matrixConfig[cid][step];
   const extractedFormData = {};
   subFormSpec.fields.forEach(f => {
      extractedFormData[f.id] = document.getElementById(f.id).value;
   });

   const formWrapper = document.getElementById('matrixActiveSubmissionForm');
   formWrapper.innerHTML = `<h3 style="color:var(--primary); text-align:center; padding:20px 0; margin:0;">⏳ Compiling matrix pipeline inputs...</h3>`;

   try {
      const res = await fetch('/api/hydrology/execute', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            cid: cid,
            step: step,
            data: extractedFormData
         })
      });

      const json = await res.json();
      const displayOutput = json.result || json.error || "Execution dropout";

      formWrapper.innerHTML = `
            <h3 style="color:#fff; margin-top:0; margin-bottom:12px;">Results Profile</h3>
            <pre style="background:#1e1e1e; color:#fff; padding:15px; border-radius:6px; white-space:pre-wrap; font-family:monospace; font-size:0.85rem; text-align:left; margin:0; border:1px solid #2d2d2d; line-height:1.4;">${displayOutput}</pre>
            <div style="display:flex; justify-content:flex-end; margin-top:20px;">
                <button type="button" class="btn-primary" onclick="closeMatrixModalFrame()" style="margin:0; width:auto; padding:8px 25px; font-weight:bold; background:var(--primary); border:none; color:#fff; border-radius:6px; cursor:pointer;">Finish Processing</button>
            </div>
        `;
   } catch (err) {
      formWrapper.innerHTML = `
            <h3 style="color:#f43f5e; margin-top:0;">Network Exception</h3>
            <pre style="background:#1e1e1e; color:#f43f5e; padding:15px; border-radius:6px; white-space:pre-wrap;">${err.message}</pre>
            <div style="display:flex; justify-content:flex-end; margin-top:20px;">
                <button type="button" class="nav-back-btn" onclick="closeMatrixModalFrame()" style="margin:0;">Close</button>
            </div>
        `;
   }
}

function closeMatrixModalFrame() {
   document.getElementById('matrixCalcModal').style.display = 'none';
   renderMatrixGridDeck();
}

document.addEventListener("DOMContentLoaded", () => {
   renderMatrixGridDeck();
});
