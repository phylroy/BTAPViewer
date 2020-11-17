import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("C:\\BTAPViewer\\primary_school.csv")
df = df[df['btap_results.energy_eui_total_gj_per_m_sq'].notnull()]
df = df.dropna(axis='columns', how='all')
df = df.loc[:, df.apply(pd.Series.nunique) != 1]
print(df.columns)

# this will convert the string values to ordered ints so it can be used in PC view.
string_cols = [col for col, dt in df.dtypes.items() if dt == object]
string_maps = {}
for col_name in string_cols:
    counter = 0
    data = []
    for item in df[col_name].unique():
        data.append([counter, item])
        counter += 1
    string_maps[col_name] = pd.DataFrame(data, columns=['counter', 'string'])
    df2 = string_maps[col_name]
    df[col_name + '_enum'] = df[col_name].map(df2.set_index('string')['counter'])

fig = go.Figure(

    layout=go.Layout(
        title=go.layout.Title(
            text="Scenario Pathways",
            font=dict(
                size=25,
                color='white'
            )
        ),
        plot_bgcolor='green',
        paper_bgcolor='rgb(0, 51, 102)',

    ),
    data=go.Parcoords(
        labelfont=dict(color='white'),
        tickfont=dict(color='blue'),

        line=dict(
            color=df['btap_results.energy_eui_total_gj_per_m_sq'],
            colorscale=[[0, 'green'], [0.5, 'yellow'], [1.0, 'red']]
        ),
        dimensions=list(
            [

                ## Roof
                dict(
                    label='Roof Cond.',
                    values=df['btap_standard_envelope.ext_roof_cond'],
                ),

                ## Wall
                dict(
                    label='Wall Cond.',
                    values=df['btap_standard_envelope.ext_wall_cond']
                ),

                ## Windows
                dict(
                    label='Windows',
                    values=df['btap_standard_envelope.fixed_window_cond'],

                ),

                ### Strings
                ## System
                dict(
                    tickvals=df['btap_standard_systems.ecm_system_type_enum'].unique(),
                    ticktext=df['btap_standard_systems.ecm_system_type'].unique(),
                    label='SystemType',
                    values=df['btap_standard_systems.ecm_system_type_enum']
                ),

                ## Daylighting Controls
                dict(
                    tickvals=df['btap_standard_systems.daylighting_type_enum'].unique(),
                    ticktext=df['btap_standard_systems.daylighting_type'].unique(),
                    label='DayLightControls',
                    values=df['btap_standard_systems.daylighting_type_enum']
                ),

                ## DCV
                dict(
                    tickvals=df['btap_standard_systems.dcv_type_enum'].unique(),
                    ticktext=df['btap_standard_systems.dcv_type'].unique(),
                    label='DCV',
                    values=df['btap_standard_systems.dcv_type_enum']
                ),

                ## Lights
                dict(
                    tickvals=df['btap_standard_systems.lights_type_enum'].unique(),
                    ticktext=df['btap_standard_systems.lights_type'].unique(),
                    label='LightType',
                    values=df['btap_standard_systems.lights_type_enum']
                ),

                ## Material Costs
                dict(
                    range=[df.min()['btap_results.cost_equipment_total_cost_per_m_sq'],
                           df.max()['btap_results.cost_equipment_total_cost_per_m_sq']],
                    label='Material Cost ($/m2)', values=df['btap_results.cost_equipment_total_cost_per_m_sq']
                ),

                ## Utility Costs
                dict(
                    range=[df.min()['btap_results.cost_utility_neb_total_cost_per_m_sq'],
                           df.max()['btap_results.cost_utility_neb_total_cost_per_m_sq']],
                    label='Util Cost ($/m2)', values=df['btap_results.cost_utility_neb_total_cost_per_m_sq']
                ),

                ## EUI
                dict(
                    range=[df.min()['btap_results.energy_eui_total_gj_per_m_sq'],
                           df.max()['btap_results.energy_eui_total_gj_per_m_sq']],
                    label='EUI GJ/m2',
                    values=df['btap_results.energy_eui_total_gj_per_m_sq']
                ),
            ]
        ),

    )
)

fig.show()


fig = px.scatter(df,
                 x="btap_results.energy_eui_total_gj_per_m_sq",
                 y="btap_results.cost_equipment_total_cost_per_m_sq",
                 color="btap_standard_systems.dcv_type",
                 labels={
                     "btap_results.energy_eui_total_gj_per_m_sq": "EUI (GJ/m2)",
                     "btap_results.cost_equipment_total_cost_per_m_sq": "MaterialCost ($/m2)",
                     "btap_standard_systems.dcv_type": "DemandControlVentilation"
                 },
                 title="Energy vs Material Costs")

fig.show()
