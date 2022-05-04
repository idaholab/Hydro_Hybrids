# %matplotlib inline
from tasks.app import app
from .model import model_tools as tools
import importlib
from pickle import load
from tensorflow.keras.models import load_model
import os
from helpers.encode import encode_plot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.switch_backend('agg')


def model(dict1, energy_profile, price_profile):
    # dict1 = {'storage': None, 'profiles': {'energy': {}, 'price': {}}, 'site': {'name': 'Nimbus', 'capacity': '13.4'}, 'financial': {'analysis': 10, 'discount': {'rate10': 1.79, 'rate20': 2.06}, 'capital': 7.6, 'oandm': 2.5, 'insurance': 0.5, 'property': 0.6, 'income': 24.9, 'cycles': 3500, 'lifespan': 10}, 'battery': {'range_power': [3.22,7.91], 'range_energy': [0.25, 8], 'plotting_interval': 10, 'range_charge': [20, 100], 'efficiency': 0.86}}

    # this captures all the x and y features that the ML model needs, will be used to check the format of final input files
    X_features = ['Energy (MWh)', 'Energy (MWh)_norm', 'Capacity-Power (MW)', 'Normalized battery capacity',
                  'Minimum Charge (%)', 'Total Efficiency (%)', 'Price: Energy ($/MWh)',
                  'Price: RegUp ($/MWh)', 'Price: RegDn ($/MWh)',
                  'Price: Spin ($/MWh)', 'Price: NonSpin ($/MWh)', 'Total Hydro Generation (MWh)_left', 'Total Hydro Generation (MWh)_left_norm']

    y_features = ['Revenue: Storage Energy to Grid ($)', 'Revenue: Storage RegUp ($)',
                  'Revenue: Storage RegDn ($)', 'Revenue: Storage Spin ($)', 'Revenue: Hydro Energy to Grid ($)_left']

    # step-1: extract information from user's input

    case_name = dict1['site']['project_name'].replace(" ", "")  # case name
    plant_capacity = float(dict1['site']['capacity'])  # maximum plant capacity
    battery_lifespan = dict1['battery']['lifespan']  # lifespan of battery
    # range of capacities that users want to test
    capacity_range = dict1['battery']['range_power']
    # energy_range = dict1['battery']['range_energy'] #range of energy ratings that users want to test
    # storag_range = dict1['battery']['range_storage'] #range of storage hours that users want to test
    min_charge = dict1['battery']['range_charge'][0]  # minimum state of charge
    # round-trip efficiency for battery
    efficiency = dict1['battery']['efficiency']

    datetime = pd.date_range(
        start='1/1/2019', end='1/1/2020', freq='5Min', closed='left')
    energy_profile_data = pd.read_csv(energy_profile)
    price_profile_data = pd.read_csv(price_profile)
    price_profile_data['Datetime'] = datetime

    # step-3: generate a range of power and energy ratings
    # define how many battery capacities will be tested, total number of capacities will be n
    capacity_interval = 15
    capacity_interval_range = [round(elem, 2) for elem in list(
        np.linspace(capacity_range[0], capacity_range[1], num=capacity_interval))]

    storage_hour_range = [0.5, 1, 2, 3, 4]
    storage_hour_interval = len(storage_hour_range)
    energy_df = pd.DataFrame()
    for capacity in range(0, capacity_interval):
        for interval in range(0, storage_hour_interval):
            energy_df = energy_df.append(
                [capacity_interval_range[capacity]*storage_hour_range[interval]])
        energy_df = energy_df.reset_index(drop=True)

    # combine capacity and energy ratings into one dataframe: configuration range
    c_l = pd.DataFrame()
    for i in range(0, capacity_interval):
        c_l = c_l.append([capacity_interval_range[i]]*storage_hour_interval)
    c_l = c_l.reset_index(drop=True)

    Con_range = pd.DataFrame()
    Con_range['E'] = energy_df.iloc[:, 0]
    Con_range['Cap'] = c_l.iloc[:, 0]
    Con_range['group'] = Con_range.index+1

    print("Capacity ratings that will be tested are: ", capacity_interval_range)
    print("Energy ratings that will be tested are: ", energy_df)

    # step-4: create input files for the ml model: df_combine
    def file_create(energy_profile_data, PC, PP, Cap, E, min_charge, efficiency, gp):
        Co_name = ['Total Hydro Generation (MWh)', 'Datetime', 'Price: Energy ($/MWh)', 'Price: RegUp ($/MWh)',
                   'Price: RegDn ($/MWh)', 'Price: Spin ($/MWh)', 'Price: NonSpin ($/MWh)']
        file = pd.DataFrame()
        file['Total Hydro Generation (MWh)'] = energy_profile_data['Total Hydro Generation (MWh)'].copy(
        )
        price_profile = PP
        file = pd.concat([file, price_profile], axis=1)
        file.columns = Co_name
        file['Energy (MWh)'] = E
        file['Energy (MWh)_norm'] = E/PC
        file['Capacity-Power (MW)'] = Cap
        file['Normalized battery capacity'] = Cap/PC
        file['Minimum Charge (%)'] = min_charge
        file['Total Efficiency (%)'] = efficiency
        file['group'] = gp
        return file

    df_combine = pd.DataFrame()
    con_n = len(Con_range)
    con_n

    for i in range(0, con_n):
        df = file_create(energy_profile_data, plant_capacity, price_profile_data,
                         Con_range.iloc[i, 1], Con_range.iloc[i, 0], min_charge, efficiency, Con_range.iloc[i, 2])
        df_combine = df_combine.append(df)

    # estimate what are the hydro_left portion
    df_combine['thld'] = df_combine['Capacity-Power (MW)']
    thld = df_combine['thld']
    hydro_gen = df_combine['Total Hydro Generation (MWh)']
    E_excs = hydro_gen - thld
    E_excs[E_excs < 0] = 0
    df_combine['Total Hydro Generation (MWh)_excs'] = E_excs
    df_combine['Total Hydro Generation (MWh)_left'] = hydro_gen - E_excs
    df_combine['Revenue: Hydro Energy to Grid ($)_cal'] = df_combine['Total Hydro Generation (MWh)_excs'] * \
        df_combine['Price: Energy ($/MWh)']/12
    df_combine['Revenue: Hydro Energy to Grid ($)_left_max'] = df_combine['Total Hydro Generation (MWh)'] * \
        df_combine['Price: Energy ($/MWh)']/12 - \
        df_combine['Revenue: Hydro Energy to Grid ($)_cal']
    df_combine['Total Hydro Generation (MWh)_left_norm'] = df_combine['Total Hydro Generation (MWh)_left']/plant_capacity

    df_combine.shape

    # step-5: import the ml model
    importlib.reload(tools)
    plt.style.use(['default'])

    model_num = 5
    # use the model with the optimal prediction time window
    hours = 8

    current_file = os.path.abspath(os.path.dirname(__file__))

    model_name = 'ann{0}_group_{1}_hour_adam_production_add_2_A_1.h5'.format(
        model_num, hours)
    model = load_model(os.path.join(current_file+"/model/"+model_name))

    X_sc = load(
        open(f'{current_file}/model/X_{hours}_scaler_add_2_A_1.pkl', 'rb'))
    y_sc = load(
        open(f'{current_file}/model/y_{hours}_scaler_add_2_A_1.pkl', 'rb'))

    # step-6: organize data for prediction
    data = df_combine
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    data.set_index('Datetime', inplace=True)
    data['month'] = data.index.month
    data['day'] = data.index.day
    data['year'] = data.index.year
    data['month'] = data['month'].astype(str)
    data['day'] = data['day'].astype(str)
    data['year'] = data['year'].astype(str)
    data['month_day'] = data['month']+'/'+data['day']+'/'+data['year']
    all_data = data

    # preparing training data for prediction model with normalized features

    X_features = ['Energy (MWh)', 'Energy (MWh)_norm', 'Capacity-Power (MW)', 'Normalized battery capacity',
                  'Minimum Charge (%)', 'Total Efficiency (%)', 'Price: Energy ($/MWh)',
                  'Price: RegUp ($/MWh)', 'Price: RegDn ($/MWh)',
                  'Price: Spin ($/MWh)', 'Price: NonSpin ($/MWh)', 'Total Hydro Generation (MWh)_left', 'Total Hydro Generation (MWh)_left_norm']

    y_features = ['Revenue: Storage Energy to Grid ($)', 'Revenue: Storage RegUp ($)',
                  'Revenue: Storage RegDn ($)', 'Revenue: Storage Spin ($)', 'Revenue: Hydro Energy to Grid ($)_left']

    segs = hours*12

    X = all_data[X_features].values

    groups = all_data['group'].values

    X = X_sc.transform(X)

    print('Building Data')
    X_df = pd.DataFrame(X, columns=X_features, index=all_data.index)
    X_df['group'] = groups
    X_df = tools.addDays(X_df)

    X, X_index, groups = tools.buildTestWindows_groups_inference(
        X_df, X_features, segs)

    print('Model data is prepared with {0} features.'.format(X.shape[1]))
    print()

    print('Training data contain {0} instances.'.format(len(X)))

    # Step-7: make the prediction, and replace negative daily revenue with 0
    print('Making the prediction...')
    preds = model.predict(X)
    preds_orig = y_sc.inverse_transform(preds)

    preds_df = pd.DataFrame(preds_orig, columns=y_features, index=X_index)
    preds_df['group'] = groups

    preds_df = tools.addDays(preds_df)

    preds_days = pd.DataFrame(columns=y_features)
    preds_days['day'] = None
    preds_days['group'] = None

    # replace daily total with zero if it is negative
    num = preds_df._get_numeric_data()
    num[num < 0] = 0
    num['month_day'] = preds_df['month_day']
    print('Aggregating results..')

    preds_days = num.groupby(by=["group", "month_day"]).sum()
    preds_days.loc[:, ["Group"]] = list(zip(*preds_days.index.values))[0]
    preds_days.loc[:, ["Day"]] = list(zip(*preds_days.index.values))[1]
    preds_days = preds_days.reset_index(drop=True)

    # step-8: calculate hydro-only revenue and maximum revenue from each stream
    all_data['Revenue only'] = all_data['Total Hydro Generation (MWh)'] * \
        all_data['Price: Energy ($/MWh)']/12

    rev_cal = all_data.copy()
    rev_cal['group'] = all_data['group']
    rev_cal['hydro_rev_noES'] = rev_cal['Total Hydro Generation (MWh)'] * \
        rev_cal['Price: Energy ($/MWh)']/12
    rev_cal['Revenue: Storage Energy to Grid ($)_max'] = rev_cal['Total Hydro Generation (MWh)_left'] * \
        rev_cal['Price: Energy ($/MWh)']/12
    rev_cal['Revenue: Storage RegUp ($)_max'] = rev_cal['Capacity-Power (MW)'] * \
        2*rev_cal['Price: RegUp ($/MWh)']/12
    rev_cal['Revenue: Storage RegDn ($)_max'] = rev_cal['Capacity-Power (MW)'] * \
        2*rev_cal['Price: RegDn ($/MWh)']/12
    rev_cal['Revenue: Storage Spin ($)_max'] = rev_cal['Capacity-Power (MW)'] * \
        2*rev_cal['Price: Spin ($/MWh)']/12
    rev_cal['Revenue: Hydro Energy to Grid ($)_left_max'] = rev_cal['Total Hydro Generation (MWh)'] * \
        rev_cal['Price: Energy ($/MWh)']/12 - \
        rev_cal['Revenue: Hydro Energy to Grid ($)_cal']

    rev = ['Revenue: Hydro Energy to Grid ($)_cal', 'Revenue only']
    rev_hydro = pd.DataFrame(columns=rev)
    rev_hydro['Revenue: Hydro Energy to Grid ($)_cal'] = rev_cal.groupby(
        by=["group", "month_day"])['Revenue: Hydro Energy to Grid ($)_cal'].sum()
    rev_hydro['Revenue only'] = rev_cal.groupby(by=["group", "month_day"])[
        'Revenue only'].sum()
    rev_hydro["Group"] = list(zip(*rev_hydro.index.values))[0]
    rev_hydro["Day"] = list(zip(*rev_hydro.index.values))[1]
    rev_hydro = rev_hydro.reset_index(drop=True)

    # step-9: aggregate the maximum daily revenue as the upper bound for the predicted revenue

    rev_1 = ['Revenue: Storage Energy to Grid ($)_max', 'Revenue: Storage RegUp ($)_max', 'Revenue: Storage RegDn ($)_max', 'Revenue: Storage Spin ($)_max', 'Revenue: Hydro Energy to Grid ($)_left_max',
             'Revenue: Hydro Energy to Grid ($)_cal', 'hydro_rev_noES']
    rev_days = pd.DataFrame(columns=rev)

    rev_days = rev_cal.groupby(by=["group", "month_day"]).sum()
    rev_days.loc[:, ["group"]] = list(zip(*rev_days.index.values))[0]
    rev_days.loc[:, ["Day"]] = list(zip(*rev_days.index.values))[1]
    rev_days = rev_days.reset_index(drop=True)

    # step 10:combine the pred and act and apply post processing steps
    combine = pd.concat([preds_days, rev_days], axis=1)
    print(combine)

    # rev from energy market
    tot_d = len(combine)
    max_c1 = combine.columns.get_loc("Revenue: Storage Energy to Grid ($)_max")

    for i in range(0, tot_d):
        for r in range(0, 5):
            if combine.iloc[i, r] > combine.iloc[i, r+max_c1]:
                combine.iloc[i, r] = combine.iloc[i, r+max_c1]

    print(combine)

    max_c2 = combine.columns.get_loc("Revenue: Storage RegUp ($)_max")
    combine['max_reserve_rev'] = combine.iloc[:, max_c2:max_c2+4].max(axis=1)
    max_c3 = combine.columns.get_loc('max_reserve_rev')

    for i in range(0, tot_d):
        if combine.iloc[i, 1] >= combine.iloc[i, max_c3]:
            combine.iloc[i, 1] = combine.iloc[i, max_c3]
            combine.iloc[i, 2] = 0
            combine.iloc[i, 3] = 0
        elif combine.iloc[i, 1] < combine.iloc[i, max_c3]:
            if combine.iloc[i, 1]+combine.iloc[i, 2] >= combine.iloc[i, max_c3]:
                combine.iloc[i, 2] = combine.iloc[i, max_c3]-combine.iloc[i, 1]
                combine.iloc[i, 3] = 0

    print(combine)
    print(combine.columns)

    # step-11: sum up all the revenues to revenue total and save it as csv files
    # daily revenue
    combine['Revenue: Hydro Energy to Grid ($)_left'] = combine['Revenue: Hydro Energy to Grid ($)_left'].astype(
        float).round(2)
    combine['Revenue: Hydro Energy to Grid ($)_cal'] = combine['Revenue: Hydro Energy to Grid ($)_cal'].astype(
        float).round(2)
    combine['Revenue: Storage Energy to Grid ($)'] = combine['Revenue: Storage Energy to Grid ($)'].astype(
        float).round(2)
    combine['Revenue: Storage RegUp ($)'] = combine['Revenue: Storage RegUp ($)'].astype(
        float).round(2)
    combine['Revenue: Storage RegDn ($)'] = combine['Revenue: Storage RegDn ($)'].astype(
        float).round(2)
    combine['Revenue: Storage Spin ($)'] = combine['Revenue: Storage Spin ($)'].astype(
        float).round(2)

    combine['Rev_total'] = combine['Revenue: Hydro Energy to Grid ($)_left']+combine['Revenue: Hydro Energy to Grid ($)_cal']+combine['Revenue: Storage Energy to Grid ($)'] + \
        combine['Revenue: Storage RegUp ($)']+combine['Revenue: Storage RegDn ($)'] + \
        combine['Revenue: Storage Spin ($)']

    # Predicted Daily Revenue Data
    Financial_Perfomance_Daily = combine.to_csv()
    #combine.to_csv('Predicted daily revenue data_{0}.csv'.format(case_name))

    # annual revenue
    preds_year = pd.DataFrame()
    preds_year['Total_Rev_Predicted'] = combine.groupby(['group'])[
        'Rev_total'].sum()
    preds_year['Revenue: Hydro Only'] = combine.groupby(['group'])[
        'hydro_rev_noES'].sum()
    preds_year['group'] = preds_year.index
    preds_year = preds_year.reset_index(drop=True)
    con_range = Con_range.iloc[:, 0:2]
    cb_plot = pd.concat([preds_year, con_range], axis=1)
    cb_plot
    #cb_plot.to_csv('Predicted annual revenue data_{0}.csv'.format(case_name))

    # step-12 a. predict the degradation cost
    model_num = 5
    # use the model with the optimal prediction time window
    hours = 24

    model_name = 'ann{0}_group_{1}_hour_adam_production_degd.h5'.format(
        model_num, hours)
    model = load_model(os.path.join(current_file+"/model/"+model_name))

    X_sc = load(open(f'{current_file}/model/X_{hours}_scaler_degd.pkl', 'rb'))
    y_sc = load(open(f'{current_file}/model/y_{hours}_scaler_degd.pkl', 'rb'))

    # preparing training data for prediction model with normalized features

    X_features = ['Energy (MWh)', 'Capacity-Power (MW)', 'Price: Energy ($/MWh)',
                  'Price: RegUp ($/MWh)', 'Price: RegDn ($/MWh)',
                  'Price: Spin ($/MWh)', 'Price: NonSpin ($/MWh)', 'Total Hydro Generation (MWh)_left']

    y_features = ['Storage Discharge Energy to Grid (MWh)',
                  'Storage RegUp (MWh)', 'Storage RegDn (MWh)', 'Storage Spin (MWh)', 'LOSS (%)']

    segs = hours*12

    X = all_data[X_features].values

    groups = all_data['group'].values

    X = X_sc.transform(X)

    print('Building Data')
    X_df = pd.DataFrame(X, columns=X_features, index=all_data.index)
    X_df['group'] = groups
    X_df = tools.addDays(X_df)

    X, X_index, groups = tools.buildTestWindows_groups_inference(
        X_df, X_features, segs)

    print('Model data is prepared with {0} features.'.format(X.shape[1]))
    print()

    print('Training data contain {0} instances.'.format(len(X)))

    # step-12 b. making the prediction
    preds_degd = model.predict(X)
    preds_degd_orig = y_sc.inverse_transform(preds_degd)

    preds_degd_df = pd.DataFrame(
        preds_degd_orig, columns=y_features, index=X_index)
    preds_degd_df['group'] = groups

    preds_degd_df = tools.addDays(preds_degd_df)

    preds_degd_days = pd.DataFrame(columns=y_features)
    preds_degd_days['day'] = None
    preds_degd_days['group'] = None

    print('Aggregating results')

    num = preds_degd_df._get_numeric_data()
    num[num < 0] = 0
    num['month_day'] = preds_degd_df['month_day']
    print('Aggregating results')

    preds_degd_days = num.groupby(by=["group", "month_day"]).sum()
    preds_degd_days.loc[:, ["group"]] = list(
        zip(*preds_degd_days.index.values))[0]
    preds_degd_days.loc[:, ["Day"]] = list(
        zip(*preds_degd_days.index.values))[1]
    preds_degd_days = preds_degd_days.reset_index(drop=True)

    # Predicted Daily Battery Degredation
    Battery_Degredation_Daily = preds_degd_days.to_csv()
    # preds_degd_days.to_csv('Predicted daily battery degradation_{0}.csv'.format(case_name))

    preds_degd_year = pd.DataFrame()
    preds_degd_year['LOSS (%)'] = preds_degd_days.groupby(
        ['group'])['LOSS (%)'].sum()
    preds_degd_year['group'] = preds_degd_year.index
    preds_degd_year = preds_degd_year.reset_index(drop=True)
    con_range = Con_range
    cb_degd_plot = pd.concat([preds_degd_year, con_range], axis=1)
    cb_degd_plot

    # Predicted Annual Battery Degredation
    Battery_Degredation_Annual = cb_degd_plot.to_csv()
    # cb_degd_plot.to_csv('Predicted annual battery degradation_{0}.csv'.format(case_name))

    # plot the revenue 3d surface

    # Creating dataset
    y = cb_plot['Cap']
    x = cb_plot['E']
    z_pred = cb_plot['Total_Rev_Predicted']
    z_act = cb_plot['Revenue: Hydro Only']

    cb_plot['Net_rev_ES'] = cb_plot['Total_Rev_Predicted'] - \
        cb_plot['Revenue: Hydro Only']

    max_REV = cb_plot['Net_rev_ES'].max()
    max_REV_index = cb_plot[cb_plot['Net_rev_ES'] == max_REV].index
    max_REV_E = cb_plot.loc[max_REV_index, 'E'].values[0]
    max_REV_Cap = cb_plot.loc[max_REV_index, 'Cap'].values[0]

    # Creating figure
    fig = plt.figure(figsize=(15, 15))
    ax = plt.axes(projection="3d")

    # Plot the surface for hydro only revenue
    x_surf, y_surf = np.meshgrid(x, y)
    # ex. function, which depends on x and y
    z_surf = np.array([z_act]*75)
    ax.plot_surface(x_surf, y_surf, z_surf, alpha=0.5, rstride=100,
                    cstride=100, color='g')    # plot a 3d surface plot

    # Creating plot
    ax.scatter3D(x, y, z_pred, c='b', marker='o', s=100)
    plt.title("Revenue vs Energy and Capacity ratings", fontweight='bold')
    # SET x, y, z label
    ax.set_xlabel('Energy (MWh)', labelpad=10)
    ax.set_ylabel('Capacity-Power (MW)', labelpad=10)
    ax.set_zlabel('Total reveune from ES ($)', labelpad=40)
    #ax.set_zlim(6e6, 1.8e7)
    plt.rc('font', size=20)
    plt.rc('axes', titlesize=23)

    E_mark_REV = max_REV_E + 2
    Cap_mark_REV = max_REV_Cap + 2

    ax.text(E_mark_REV, Cap_mark_REV, max_REV*1.35,
            "Optimal annual net revenue: ${0}".format(max_REV.round(2)), color='blue')
    ax.text(E_mark_REV, Cap_mark_REV, max_REV*1.25, "E = {0} MWh, Cap = {1} MW".format(
        max_REV_E.round(2), max_REV_Cap.round(2)), color='blue')
    ax.text(E_mark_REV, Cap_mark_REV,
            z_act[2]*1.4, "Hydro-only revenue: ${0}".format(z_act[2].round(2)), color='green')

    ax.view_init(azim=160, elev=5)
    # Revenue Plot
    Revenue_Plot = encode_plot(plt)
    # plt.savefig('Revenue plot_0_{0}.png'.format(case_name))

    # ROI calculation-calibrated on Sep 2021
    # X is the energy rating, Y is the Cap power rating, define the total cost of the energy storage device
    Min_C = 0.20
    Tot_E = 0.86
    # All cost information is cited from the low-cost scenario
    cap_c_kw = 223  # Capital Cost – Energy Capacity ($/kWh)
    cc_c = 92  # Construction and Commission Cost ($/kWh)
    P_C_c = 230  # Power Conversion System ($/kW)
    B_P_c = 80  # Balance of Plant ($/kW)
    unit = 1
    fix_c = 40000  # Annual O&M Fixed ($) - entire cascade (4 units)
    dep_rate = 0.05
    battery_lifespan = 10
    life_other = 25
    tax = 0.24873
    OM_vc = 0.03  # O&M Variable (Cents/kWh)
    OM_fix_c = 10  # O&M Fixed ($/kW-yr)=10

    def ROI_cal_5(x, y, Ann_rev, degd, gp_n):
        year = 5
        ROI_df = pd.DataFrame(
            {'group_number': gp_n+1, 'E': x, 'Cap': y}, index=[gp_n])
        Ann_Rev = Ann_rev
        # Total Project Costs: Capital Investment Cost ($) - entire cascade (4 units)
        Cap_c = (x)*(cap_c_kw*(1+degd/100)*year + cc_c) * \
            1000*unit + y*(P_C_c + B_P_c)*1000*unit
        OM_fix = y*OM_fix_c*1000*unit
        # OM_c = Ann_ES_G*OM_vc*1000/100 #annual operating cost = annual energy from ES to grid * O&M variable cost
        # annual depreciation cost of battery
        Ann_depre_b = (x)*cap_c_kw*1000*unit/battery_lifespan
        Annual_deprec_other = (Cap_c - x*cc_c*1000*unit - cap_c_kw*x*1000*unit)*(
            1-dep_rate)/life_other  # annual depreciation cost for other equipment
        # Total cost= Annual O&M fixed cost + Annual O&M Variable + annual depreciation cost for battery and other equip.
        T_Cost = OM_fix + Ann_depre_b + Annual_deprec_other
        E_without_tax = Ann_Rev*unit - (T_Cost)
        ROI = year*100*E_without_tax*(1-tax)/Cap_c
        ROI_df['5-yr ROI%'] = ROI
        # return T_Cost,E_without_tax, ROI, Cap_c, Ann_depre_b, Annual_deprec_other, OM_fix
        return ROI_df

    cb_plot['Net_rev_ES'] = cb_plot['Total_Rev_Predicted'] - \
        cb_plot['Revenue: Hydro Only']
    degd_c = cb_degd_plot['LOSS (%)']

    group_n = len(cb_plot)
    ROI_data = pd.DataFrame()

    for g_n in range(0, group_n):
        ROI_gp = ROI_cal_5(cb_plot.loc[g_n, 'E'], cb_plot.loc[g_n, 'Cap'],
                           cb_plot.loc[g_n, 'Net_rev_ES'], cb_degd_plot.loc[g_n, 'LOSS (%)'], g_n)
        ROI_data = ROI_data.append(ROI_gp)

    #ROI_data['group'] = ROI_data.index+1
    ROI_data
    cb_plot['5-yr ROI%'] = ROI_data['5-yr ROI%'].copy()
    #cb_plot.to_csv('Predicted annual financial performance_{0}.csv'.format(case_name))
    # ROI_list.to_csv(pge+'ROI_0.csv')

    # Creating dataset
    y = cb_plot['Cap']
    x = cb_plot['E']
    z_ROI = cb_plot['5-yr ROI%']

    max_ROI = cb_plot['5-yr ROI%'].max()
    max_ROI_index = cb_plot[cb_plot['5-yr ROI%'] == max_ROI].index
    max_ROI_E = cb_plot.loc[max_ROI_index, 'E'].values[0]
    max_ROI_Cap = cb_plot.loc[max_ROI_index, 'Cap'].values[0]

    # Creating figure
    fig = plt.figure(figsize=(15, 15))
    ax = plt.axes(projection="3d")

    # Creating plot
    ax.scatter3D(x, y, z_ROI, c='red', marker='o', s=100)
    #ax.scatter3D(x_train, y_train, z_train, c='r', marker='*', s=200)
    plt.title("ROI(%) vs Energy and Capacity ratings", fontweight='bold')
    # SET x, y, z label
    ax.set_xlabel('Energy (MWh)', labelpad=10)
    ax.set_ylabel('Capacity-Power (MW)', labelpad=10)
    ax.set_zlabel('ROI (%)', labelpad=40)
    plt.rc('font', size=20)
    plt.rc('axes', titlesize=23)

    E_mark = max_ROI_E*1.05
    Cap_mark = max_ROI_Cap*1.05

    ax.text(E_mark, Cap_mark, max_ROI*1.1,
            "Optimal 5-year ROI%: {0}".format(max_ROI.round(2)), color='green')
    ax.text(E_mark, Cap_mark, max_ROI*1, "E = {0} MWh, Cap = {1} MW".format(
        max_ROI_E.round(2), max_ROI_Cap.round(2)), color='green')

    ax.view_init(azim=40, elev=15)
    # plt.show()
    # ROI Plot
    ROI_Plot = encode_plot(plt)

    PBP_data = pd.DataFrame()

    def pay_back_p(x, y, Ann_rev, degd, gp_n):
        PBP_df = pd.DataFrame(
            {'group_number': gp_n+1, 'E': x, 'Cap': y}, index=[gp_n])
        Ann_Rev = Ann_rev
        # Total Project Costs: Capital Investment Cost ($) - entire cascade (4 units)
        Cap_c = (x)*(cap_c_kw*(1+degd/100) + cc_c) * \
            1000*unit + y*(P_C_c + B_P_c)*1000*unit
        #Cap_c = (x)*(cap_c_kw + cc_c)*1000*unit + y*(P_C_c+ B_P_c)*1000*unit
        OM_fix = y*OM_fix_c*1000*unit
        # OM_c = Ann_ES_G*OM_vc*1000/100 #annual operating cost = annual energy from ES to grid * O&M variable cost
        # annual depreciation cost of battery
        Ann_depre_b = (x)*cap_c_kw*1000*unit/battery_lifespan
        Annual_deprec_other = (Cap_c - x*cc_c*1000*unit - cap_c_kw*x*1000*unit)*(
            1-dep_rate)/life_other  # annual depreciation cost for other equipment
        # Total cost= Annual O&M fixed cost + Annual O&M Variable + annual depreciation cost for battery and other equip.
        T_Cost = OM_fix + Ann_depre_b + Annual_deprec_other
        E_wo_tax = (Ann_Rev*unit - (T_Cost))
        E_with_tax = E_wo_tax*(1-tax)
        Ann_cash_flow = E_with_tax + Annual_deprec_other + \
            Ann_depre_b  # Cash from Operating Activities
        PBP = Cap_c/Ann_cash_flow
        PBP_df['pay_back_period'] = PBP
        # return x,y,PBP, Cap_c, Ann_Rev, E_wo_tax, E_with_tax, Ann_cash_flow, T_Cost, Annual_deprec_other, Ann_depre_b, Annual_deprec_other, OM_fix
        return PBP_df

    for g_n in range(0, group_n):
        PBP_gp = pay_back_p(cb_plot.loc[g_n, 'E'], cb_plot.loc[g_n, 'Cap'],
                            cb_plot.loc[g_n, 'Net_rev_ES'], cb_degd_plot.loc[g_n, 'LOSS (%)'], g_n)
        PBP_data = PBP_data.append(PBP_gp)

    #PBP_data['group'] = PBP_data.index+1
    PBP_data
    cb_plot['Pay back period'] = PBP_data['pay_back_period'].copy()

    # Predicted Annual Financial Performance
    Financial_Perfomance_Annual = cb_plot.to_csv()

    # Creating dataset
    y = cb_plot['Cap']
    x = cb_plot['E']
    z_PBP = cb_plot['Pay back period']

    max_PBP = cb_plot['Pay back period'].min()
    max_PBP_index = cb_plot[cb_plot['Pay back period'] == max_PBP].index
    max_PBP_E = cb_plot.loc[max_PBP_index, 'E'].values[0]
    max_PBP_Cap = cb_plot.loc[max_PBP_index, 'Cap'].values[0]

    # Creating figure
    fig = plt.figure(figsize=(15, 15))
    ax = plt.axes(projection="3d")

    # Creating plot
    ax.scatter3D(x, y, z_PBP, c='red', marker='o', s=100)
    #ax.scatter3D(x_train, y_train, z_train, c='r', marker='*', s=200)
    plt.title("Pay back period (yrs) vs Energy and Capacity ratings",
              fontweight='bold')
    # SET x, y, z label
    ax.set_xlabel('Energy (MWh)', labelpad=10)
    ax.set_ylabel('Capacity-Power (MW)', labelpad=10)
    ax.set_zlabel('Pay back period (yrs)', labelpad=40)
    plt.rc('font', size=20)
    plt.rc('axes', titlesize=23)

    E_mark_PBP = max_PBP_E*1.05
    Cap_mark_PBP = max_PBP_Cap*1.05

    ax.text(E_mark_PBP*0.5, Cap_mark_PBP*0.5, max_PBP*4,
            "Shortest pay back period (yrs): {0}".format(max_PBP.round(2)), color='green')
    ax.text(E_mark_PBP*0.5, Cap_mark_PBP*0.5, max_PBP*3,
            "E = {0} MWh, Cap = {1} MW".format(max_PBP_E.round(2), max_PBP_Cap.round(2)), color='green')

    ax.view_init(azim=40, elev=15)
    # plt.show()

    # plt.savefig('Pay back period plot_0_{0}.png'.format(case_name))
    PaybackPeriod_Plot = encode_plot(plt)

    return Revenue_Plot, ROI_Plot, PaybackPeriod_Plot, Battery_Degredation_Daily, Battery_Degredation_Annual, Financial_Perfomance_Daily, Financial_Perfomance_Annual
