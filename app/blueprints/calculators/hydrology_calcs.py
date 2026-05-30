import requests
import math
from datetime import datetime
from flask import Blueprint, render_template, request, session, jsonify
from app.models.user import User, db

Hydrology = Blueprint('hydrology_bp', __name__, template_folder='../templates')

@hydrology_bp.route('/hydrology-calc', methods=['GET'])
def hydro_page():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(session['user_id'])
    return render_template('calculators/hydrology_calcs.html', user=user)

@hydrology_bp.route('/api/hydrology/execute', methods=['POST'])
def execute_hydro_calc():
    if 'user_id' not in session: 
        return jsonify({"error": "Unauthorized"}), 401
        
    payload = request.get_json() or {}
    cid = str(payload.get('cid', '1'))       
    step = str(payload.get('step', '1.1'))     
    data = payload.get('data', {})      
    
    try:
        if cid == "1" and step == "1.1":
            pipe_dia = float(data.get('pipe_dia_in') or 0)
            pipe_slope = float(data.get('pipe_slope_ft_ft') or 0)
            n_roughness = 0.013 

            if pipe_dia > 0 and pipe_slope > 0:
                radius_ft = (pipe_dia / 12) / 4
                area = 3.1415 * ((pipe_dia / 12 / 2) ** 2)
                velocity = (1.486 / n_roughness) * (radius_ft ** (2/3)) * (pipe_slope ** 0.5)
                capacity_cfs = area * velocity

            return jsonify({"success": True, "result": f"{capacity_cfs:.2f} cfs"})
            
        elif cid == "1" and step == "1.2":
            p_length = float(data.get('p_length') or 0)
            p_width = float(data.get('p_width') or 0)
            p_depth = float(data.get('p_depth') or 0)

            if p_length > 0 and p_width > 0 and p_depth > 0:
                total_cf = p_length * p_width * p_depth
                total_gallons = total_cf * 7.48

            return jsonify({"success": True, "result": f"{total_cf:.0f} ft³ ({total_gallons:,.0f}) gal"})
            
        elif cid == "1" and step == "1.3":
            v_head = float(data.get('v_head_ft') or 0)
        
            if v_head > 0:
                v_discharge = 2.5 * (v_head ** 2.5)

            return jsonify({"success": True, "result": f"{v_discharge:.2f} cfs"})

        elif cid == "2" and step == "2.1":
            drop_inches = float(data.get('drop_inches') or 0)
            time_minutes = float(data.get('time_minutes') or 0)
            
            if time_minutes > 0:
                inf_rate = (drop_inches / time_minutes) * 60

            return jsonify({"success": True, "result": f"{inf_rate:.2f} in/hr"})
            
        elif cid == "2" and step == "2.2":
            r_area = float(data.get('r_area_acres') or 0)
            r_intensity = float(data.get('r_intensity_in_hr') or 0)
            r_coeff = 0.9

            r_peak_q = r_coeff * r_intensity * r_area

            return jsonify({"success": True, "result": f"{r_peak_q:.2f} cfs"})
            
        elif cid == "2" and step == "2.3":
            o_area = float(data.get('o_area_sqft', 0) or 0)
            o_head = float(data.get('o_head_ft', 0) or 0)
            if o_area > 0 and o_head > 0:
                o_discharge = 0.62 * o_area * ((2 * 32.2 * o_head) ** 0.5)
                
            return jsonify({"success": True, "result": f"{o_discharge:.2f} cfs"})

        elif cid == "3" and step == "3.1":
            tc_length = float(data.get('tc_length_ft', 0) or 0)
            tc_slope = float(data.get('tc_slope_ft_ft', 0) or 0)
            if tc_length > 0 and tc_slope > 0:
                tc_minutes = 0.0078 * (tc_length**0.77) * (tc_slope**-0.385)
              
            return jsonify({"success": True, "result": f"{tc_minutes:.2f} minutes"})
            
        elif cid == "3" and step == "3.2":
            precip = float(data.get('precip_in', 0) or 0)
            cn_value = float(data.get('cn_value', 0) or 0)
            if precip > 0 and cn_value > 0:
                s_retention = (1000 / cn_value) - 10
                if precip > (0.2 * s_retention):
                    q_runoff = ((precip - 0.2 * s_retention)**2) / (precip + 0.8 * s_retention)
                else:
                    q_runoff = 0
                  
            return jsonify({"success": True, "result": f"{q_runoff:.2f} inches"})
            
        elif cid == "3" and step == "3.3":
            b_width = float(data.get('b_width_ft', 0) or 0)
            flow_depth = float(data.get('flow_depth_ft', 0) or 0)
            side_slope = float(data.get('side_slope_z', 0) or 0) 
            ch_slope = float(data.get('ch_slope_ft_ft', 0) or 0)
            if flow_depth > 0 and ch_slope > 0:
                area = (b_width + side_slope * flow_depth) * flow_depth
                wetted_p = b_width + 2 * flow_depth * ((1 + side_slope**2)**0.5)
                radius = area / wetted_p
                velocity = (1.486 / 0.030) * (radius**(2/3)) * (ch_slope**0.5)
                q_ditch = area * velocity
              
            return jsonify({"success": True, "result": f"{q_ditch:.2f} cfs"})
          
        elif cid == "4" and step == "4.1":
            v_fps = float(data.get('v_fps', 0) or 0)
            if v_fps > 0:
                d50_in = ((v_fps**2) / (2 * 32.2 * (2.65 - 1) * (0.86**2))) * 12
              
            return jsonify({"success": True, "result": f"{d50_in:.1f} inch D50 stone"})
            
        elif cid == "4" and step == "4.2":
            q_in = float(data.get('q_peak_inflow', 0) or 0)
            q_out = float(data.get('q_allowable_out', 0) or 0)
            duration_min = float(data.get('storm_duration_min', 0) or 0)
            if q_in > q_out:
                storage_cf = (q_in - q_out) * (duration_min * 60) * 0.5 
              
            return jsonify({"success": True, "result": f"{storage_cf:.0f} ft³"})
            
        elif cid == "4" and step == "4.3":
            inlet_length = float(data.get('inlet_length_ft', 0) or 0)
            inlet_depth = float(data.get('inlet_depth_ft', 0) or 0)
            if inlet_length > 0 and inlet_depth > 0:
                q_inlet = 3.0 * inlet_length * (inlet_depth ** 1.5)
              
            return jsonify({"success": True, "result": f"{q_inlet:.2f} cfs"})

        elif cid == "5" and step == "5.1":
            flow_cfs = float(data.get('flow_cfs', 0) or 0)
            p_dia_in = float(data.get('p_dia_in', 0) or 0)
            if flow_cfs > 0 and p_dia_in > 0:
                p_area = 3.1415 * (((p_dia_in / 12) / 2) ** 2)
                exit_v = flow_cfs / p_area
                status = "SCOUR RISK" if exit_v > 5.0 else "SAFE"
              
            return jsonify({"success": True, "result": f"{exit_v:.2f} fps ({status})"})
            
        elif cid == "5" and step == "5.2":
            peak_q = float(data.get('peak_q_cfs', 0) or 0)
            settle_vel = float(data.get('settle_vel_fps', 0.0004) or 0.0004) 
            if peak_q > 0:
                min_area_sqft = peak_q / settle_vel
              
            return jsonify({"success": True, "result": f"{min_area_sqft:,.0f} sq. ft."})
            
        elif cid == "5" and step == "5.3":
            n1_val = float(data.get('n_main', 0.013) or 0.013)
            p1_len = float(data.get('p_main_ft', 0) or 0)
            n2_val = float(data.get('n_side', 0.035) or 0.035)
            p2_len = float(data.get('p_side_ft', 0) or 0)
            if p1_len > 0 or p2_len > 0:
                weighted_n = (((p1_len * (n1_val**1.5)) + (p2_len * (n2_val**1.5))) / (p1_len + p2_len))**(2/3)
              
            return jsonify({"success": True, "result": f"{weighted_n:.4f} n"})

        elif cid == "6" and step == "6.1":
            r_coeff = float(data.get('r_coeff', 0) or 0)
            r_precip = float(data.get('r_precip_in', 0) or 0)
            r_acres = float(data.get('r_acres', 0) or 0)
            if r_coeff > 0 and r_precip > 0:
                vol_cf = r_coeff * (r_precip / 12) * (r_acres * 43560)
              
            return jsonify({"success": True, "result": f"{vol_cf:,.0f} ft³"})
            
        elif cid == "6" and step == "6.2":
            w_width = float(data.get('w_width_ft', 0) or 0)
            w_head = float(data.get('w_head_ft', 0) or 0)
            if w_width > 0 and w_head > 0:
                q_weir = 3.33 * (w_width - (0.2 * w_head)) * (w_head ** 1.5)
              
            return jsonify({"success": True, "result": f"{q_weir:.2f} cfs"})
            
        elif cid == "6" and step == "6.3":
            g_area = float(data.get('g_area_sqft', 0) or 0)
            g_head = float(data.get('g_head_ft', 0) or 0)
            g_clog = float(data.get('g_clog_factor', 0.5) or 0.5)
            if g_area > 0 and g_head > 0:
                effective_area = g_area * (1 - g_clog)
                q_grate = 0.67 * effective_area * ((2 * 32.2 * g_head) ** 0.5)
              
            return jsonify({"success": True, "result": f"{q_grate:.2f} cfs"})
        
        elif cid == "7" and step == "7.1":
            p_dia = float(data.get('p_dia_in', 0) or 0)
            p_depth = float(data.get('p_depth_in', 0) or 0)
            p_slope = float(data.get('p_slope_ft_ft', 0) or 0)
            p_n = float(data.get('p_n_val', 0.013) or 0.013)
            if p_dia > 0 and p_depth > 0 and p_slope > 0:
                r = (p_dia / 12) / 2
                h = p_depth / 12
                theta = 2 * (3.14159 / 180) * (57.2958 * (1 - (h/r))) 
                area = (r**2) * (3.14159 - (theta - (0.5 * (theta * 2).sin() if hasattr(theta, 'sin') else 0))) 
                rh_approx = (p_dia / 12) / 4 
                vel = (1.486 / p_n) * (rh_approx ** (2/3)) * (p_slope ** 0.5)
                q_partial = area * vel 
              
            return jsonify({"success": True, "result": f"{q_partial:.2f} cfs"})
            
        elif cid == "7" and step == "7.2":
            wq_area = float(data.get('wq_area_acres', 0) or 0)
            wq_imp = float(data.get('wq_imperv_pct', 0) or 0)
            wq_rain = float(data.get('wq_rainfall_in', 1.0) or 1.0)
            if wq_area > 0:
                rv = 0.05 + (0.009 * wq_imp)
                wqv_cf = (wq_rain / 12) * rv * (wq_area * 43560)
              
            return jsonify({"success": True, "result": f"{wqv_cf:,.0f} ft³"})
            
        elif cid == "7" and step == "7.3":
            g_cross = float(data.get('gut_cross_slope', 0) or 0)
            g_long = float(data.get('gut_long_slope', 0) or 0)
            g_flow = float(data.get('gut_flow_cfs', 0) or 0)
            g_n = float(data.get('gut_n_val', 0.016) or 0.016)
            if g_cross > 0 and g_long > 0 and g_flow > 0:
                spread = ((g_flow * g_n) / (0.56 * (g_cross**1.67) * (g_long**0.5))) ** 0.375
              
            return jsonify({"success": True, "result": f"{spread:.2f} ft width"})
        
        elif cid == "8" and step == "8.1":
            r = float(data.get('r_factor', 0) or 0)
            k = float(data.get('k_factor', 0) or 0)
            ls = float(data.get('ls_factor', 0) or 0)
            c = float(data.get('c_factor', 1.0) or 1.0)
            if r > 0 and k > 0 and ls > 0:
                tons_per_acre = r * k * ls * c
              
            return jsonify({"success": True, "result": f"{tons_per_acre:.2f} tons/acre/yr"})
            
        elif cid == "8" and step == "8.2":
            c_flow = float(data.get('c_flow_cfs', 0) or 0)
            c_dia_ft = float(data.get('c_dia_in', 0) or 0) / 12
            c_c = float(data.get('c_form_factor', 0.02) or 0.02)
            if c_flow > 0 and c_dia_ft > 0:
                hw_depth = c_dia_ft * (c_c * (c_flow / (c_dia_ft**2.5))**2)
              
            return jsonify({"success": True, "result": f"{hw_depth:.2f} ft depth"})
            
        elif cid == "8" and step == "8.3":
            s_l = float(data.get('s_length_ft', 0) or 0)
            s_n = float(data.get('s_n_val', 0) or 0)
            s_p = float(data.get('s_precip_in', 0) or 0)
            s_s = float(data.get('s_slope', 0) or 0)
            if s_l > 0 and s_s > 0:
                tc_sheet = (0.007 * (s_n * s_l)**0.8) / ((s_p**0.5) * (s_s**0.4))
              
            return jsonify({"success": True, "result": f"{tc_sheet * 60:.2f} minutes"})
        
        elif cid == "9" and step == "9.1":
            f_l = float(data.get('f_length_ft', 0) or 0)
            f_d = float(data.get('f_dia_in', 0) or 0) / 12
            f_v = float(data.get('f_vel_fps', 0) or 0)
            f_f = float(data.get('f_friction', 0.02) or 0.02)
            if f_l > 0 and f_d > 0:
                h_loss = f_f * (f_l / f_d) * ((f_v**2) / (2 * 32.2))
              
            return jsonify({"success": True, "result": f"{h_loss:.2f} ft of head"})
            
        elif cid == "9" and step == "9.2":
            sw_d = float(data.get('sw_depth_ft', 0) or 0)
            sw_s = float(data.get('sw_slope_ft_ft', 0) or 0)
            if sw_d > 0 and sw_s > 0:
                stress = 62.4 * sw_d * sw_s
                risk = "HIGH (Lining Req)" if stress > 1.0 else "LOW (Grass OK)"
              
            return jsonify({"success": True, "result": f"{stress:.2f} lb/sq.ft ({risk})"})
            
        elif cid == "9" and step == "9.3":
            hp_q = float(data.get('hp_flow_gpm', 0) or 0)
            hp_h = float(data.get('hp_head_ft', 0) or 0)
            hp_e = float(data.get('hp_eff', 0.75) or 0.75)
            if hp_q > 0 and hp_h > 0:
                horsepower = (hp_q * hp_h) / (3960 * hp_e)
              
            return jsonify({"success": True, "result": f"{horsepower:.2f} HP"})
        
        else:
            return jsonify({
                "success": True, 
                "result": f"Lock.\nModule Channel: {cid} | Operational Step: {step}\nExtracted structural data tokens:\n{str(data)}"
            })
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Calculations structural routing breakdown: {str(e)}"}), 500
