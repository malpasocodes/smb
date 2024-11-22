"""Affordability analysis view module."""
import streamlit as st
from utils.data_utils import merge_datasets
import plotly.express as px
import pandas as pd

def show_summary_statistics(df: pd.DataFrame, selected_group: str):
    """Display summary statistics for the selected institutions."""
    if selected_group != "All":
        df = df[df['group'] == selected_group]
    
    st.markdown("### Summary Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Number of Institutions", 
            value=f"{len(df):,}",
            help="Total number of colleges in the selected group"
        )
        
        avg_students = df['count'].mean()
        st.metric(
            label="Avg. Cohort Size", 
            value=f"{avg_students:,.0f}",
            help="Average number of students per cohort (1980-1982 birth cohorts)"
        )
    
    with col2:
        median_mobility = df['mobility_rate'].median()
        st.metric(
            label="Median Mobility Rate", 
            value=f"{median_mobility:.1%}",
            help="Median probability of moving from bottom quintile to top quintile (P(Child in Q5 | Parent in Q1))"
        )
        
        avg_q1_students = df['par_q1'].mean()
        st.metric(
            label="Avg. % Bottom Quintile", 
            value=f"{avg_q1_students:.1%}",
            help="Average percentage of students from bottom quintile of parent income distribution"
        )
    
    with col3:
        median_price = df['sticker_price_2013'].median()
        st.metric(
            label="Median Sticker Price", 
            value=f"${median_price:,.0f}",
            help="Median sticker price (before financial aid) in 2013"
        )
        
        avg_married = df['k_married'].mean()
        st.metric(
            label="% Married in 2014", 
            value=f"{avg_married:.1%}",
            help="Percentage of students who were married in 2014"
        )

def show_institution_list(df: pd.DataFrame, selected_group: str):
    """Display the list of institutions."""
    if selected_group != "All":
        df = df[df['group'] == selected_group]
    
    # Create display dataframe
    display_df = df[[
        'name', 'subgroup', 'sticker_price_2013', 
        'mobility_rate', 'par_q1', 'count'
    ]].copy()
    
    # Rename columns
    display_df = display_df.rename(columns={
        'name': 'Institution',
        'subgroup': 'Type',
        'sticker_price_2013': 'Sticker Price',
        'mobility_rate': 'Mobility Rate',
        'par_q1': 'Bottom Quintile %',
        'count': 'Cohort Size'
    })
    
    st.dataframe(
        display_df.sort_values('Mobility Rate', ascending=False)
        .reset_index(drop=True)
        .assign(Rank=lambda x: range(1, len(x) + 1))
        .set_index('Rank')
        .style.format({
            'Sticker Price': '${:,.0f}',
            'Mobility Rate': '{:.1%}',
            'Bottom Quintile %': '{:.1%}',
            'Cohort Size': '{:,.0f}'
        }),
        use_container_width=True,
        help="""
        Institution: Name of college or university
        Type: Institution subgroup (e.g., Public, Private, Ivy Plus)
        Sticker Price: Published tuition and fees (before financial aid) in 2013
        Mobility Rate: Probability of moving from bottom to top quintile
        Bottom Quintile %: Percentage of students from bottom 20% of parent income
        Cohort Size: Average number of students per cohort (1980-1982)
        """
    )

def show_affordability_plot(df: pd.DataFrame, selected_group: str):
    """Display the affordability analysis plot."""
    if selected_group != "All":
        plot_df = df[df['group'] == selected_group].copy()
    else:
        plot_df = df.copy()

    # Calculate global medians for reference lines
    global_median_price = df['sticker_price_2013'].median()
    global_median_mobility = df['mobility_rate'].median()

    # Calculate axis ranges
    x_min = df['sticker_price_2013'].min()
    x_max = df['sticker_price_2013'].max()
    y_min = 0
    y_max = df['mobility_rate'].max() * 1.1

    fig = px.scatter(
        plot_df,
        x='sticker_price_2013',
        y='mobility_rate',
        color='subgroup',
        size='par_q1',
        size_max=10,
        hover_name='name',
        labels={
            'sticker_price_2013': 'Sticker Price ($)',
            'mobility_rate': 'Mobility Rate (Q4 + Q5)',
            'subgroup': 'Institution Type',
            'par_q1': 'Q1 Students'
        },
        title=f"Mobility vs Affordability - {selected_group} (Global Medians)"
    )

    # Add reference lines for quadrants
    fig.add_hline(y=global_median_mobility, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=global_median_price, line_dash="dash", line_color="gray", opacity=0.5)

    # Add quadrant labels
    fig.add_annotation(
        text="<b>High Mobility<br>Low Cost</b>",
        x=global_median_price - (global_median_price - x_min) * 0.7,
        y=global_median_mobility + (y_max - global_median_mobility) * 0.7,
        showarrow=False,
        font=dict(size=14, color="black"),
        align='left'
    )
    fig.add_annotation(
        text="<b>High Mobility<br>High Cost</b>",
        x=global_median_price + (x_max - global_median_price) * 0.7,
        y=global_median_mobility + (y_max - global_median_mobility) * 0.7,
        showarrow=False,
        font=dict(size=14, color="black"),
        align='right'
    )
    fig.add_annotation(
        text="<b>Low Mobility<br>Low Cost</b>",
        x=global_median_price - (global_median_price - x_min) * 0.7,
        y=global_median_mobility * 0.3,
        showarrow=False,
        font=dict(size=14, color="black"),
        align='left'
    )
    fig.add_annotation(
        text="<b>Low Mobility<br>High Cost</b>",
        x=global_median_price + (x_max - global_median_price) * 0.7,
        y=global_median_mobility * 0.3,
        showarrow=False,
        font=dict(size=14, color="black"),
        align='right'
    )

    # Update layout for better visualization
    fig.update_layout(
        xaxis=dict(
            autorange='reversed',  # Reverse x-axis
            tickformat='$,.0f',
            range=[x_min * 0.95, x_max * 1.05],  # Full range with small padding
        ),
        yaxis=dict(
            tickformat='.0%',
            range=[y_min, y_max]  # Full range with padding for annotations
        ),
        height=800,
        width=1200,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        autosize=False
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{hovertext}</b>",
            "Sticker Price: $%{x:,.0f}",
            "Mobility Rate: %{y:.1%}",
            "Q1 Students: %{marker.size:.1%}",
            "<extra></extra>"
        ])
    )

    st.plotly_chart(fig, use_container_width=True)

def show_institution_list(df: pd.DataFrame, selected_group: str):
    """Display the list of institutions."""
    if selected_group != "All":
        df = df[df['group'] == selected_group]
    
    # Prepare display columns
    display_df = df[[
        'name', 'subgroup', 'sticker_price_2013', 
        'scorecard_netprice_2013', 'mobility_rate', 'par_q1'
    ]].copy()
    
    # Format columns
    display_df['sticker_price_2013'] = display_df['sticker_price_2013'].apply(lambda x: f"${x:,.0f}")
    display_df['scorecard_netprice_2013'] = display_df['scorecard_netprice_2013'].apply(lambda x: f"${x:,.0f}")
    display_df['mobility_rate'] = display_df['mobility_rate'].apply(lambda x: f"{x:.1%}")
    display_df['par_q1'] = display_df['par_q1'].apply(lambda x: f"{x:.1%}")
    
    # Rename columns for display
    display_df.columns = [
        'Institution', 'Type', 'Sticker Price', 
        'Net Price', 'Mobility Rate', 'Bottom Quintile Share'
    ]
    
    st.dataframe(
        display_df.sort_values('Mobility Rate', ascending=False)
        .reset_index(drop=True)
        .assign(Rank=lambda x: range(1, len(x) + 1))
        .set_index('Rank')
        .style.format({
            'Sticker Price': '${:,.0f}',
            'Mobility Rate': '{:.1%}',
            'Bottom Quintile Share': '{:.1%}'
        }),
        use_container_width=True,
        help="""
        Institution: Name of college or university
        Type: Institution subgroup (e.g., Public, Private, Ivy Plus)
        Sticker Price: Published tuition and fees (before financial aid) in 2013
        Net Price: Average net price (after financial aid) in 2013
        Mobility Rate: Probability of moving from bottom to top quintile
        Bottom Quintile Share: Percentage of students from bottom 20% of parent income
        """
    )

def show_affordability_analysis():
    """Display the affordability analysis view."""
    df = merge_datasets()
    
    if df is not None:
        def get_group_and_subgroup(row):
            if row['tier'] in [1, 2]:
                group = 'Elite'
                subgroup = 'Ivy Plus' if row['tier'] == 1 else 'Other Elite'
            elif row['tier'] in [3, 4]:
                group = 'Highly Selective'
                subgroup = 'Public' if row['tier'] == 3 else 'Private'
            elif row['tier'] in [5, 6]:
                group = 'Selective'
                subgroup = 'Public' if row['tier'] == 5 else 'Private'
            elif row['tier'] in [7, 8]:
                group = 'Nonselective'
                subgroup = 'Public' if row['tier'] == 7 else 'Private'
            elif row['tier'] == 10:
                group = 'Four-year for-profit'
                subgroup = 'For-profit'
            return pd.Series([group, subgroup])
        
        df[['group', 'subgroup']] = df.apply(get_group_and_subgroup, axis=1)
        df['mobility_rate'] = df['kq4_cond_parq1'] + df['kq5_cond_parq1']
        
        st.sidebar.header("Filters")
        
        min_q1_pct = st.sidebar.slider(
            "Minimum % of Q1 Students",
            min_value=0,
            max_value=50,
            value=5,
            step=1,
            help="Filter institutions by minimum percentage of students from bottom quintile"
        )
        
        df = df[df['par_q1'] * 100 >= min_q1_pct]
        
        selected_group = st.sidebar.selectbox(
            "Select Institution Group",
            ["All"] + sorted(df['group'].unique().tolist())
        )
        
        # Add view type selector
        view_type = st.sidebar.selectbox(
            "Select View Type",
            ["Plot", "List"]
        )
        
        if view_type == "Plot":
            show_affordability_plot(df, selected_group)
        else:  # List view
            show_summary_statistics(df, selected_group)
            st.divider()  # Add visual separator
            
            # Calculate global medians for quadrant analysis
            global_median_price = df['sticker_price_2013'].median()
            global_median_mobility = df['mobility_rate'].median()
            
            # Calculate quadrant counts
            q1 = len(df[(df['sticker_price_2013'] > global_median_price) & 
                       (df['mobility_rate'] > global_median_mobility)])
            q2 = len(df[(df['sticker_price_2013'] < global_median_price) & 
                       (df['mobility_rate'] > global_median_mobility)])
            q3 = len(df[(df['sticker_price_2013'] > global_median_price) & 
                       (df['mobility_rate'] < global_median_mobility)])
            q4 = len(df[(df['sticker_price_2013'] < global_median_price) & 
                       (df['mobility_rate'] < global_median_mobility)])
            
            st.markdown("### Quadrant Distribution")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **High Cost Region:**
                - High Mobility: {q1} institutions
                - Low Mobility: {q3} institutions
                """)
            with col2:
                st.markdown(f"""
                **Low Cost Region:**
                - High Mobility: {q2} institutions
                - Low Mobility: {q4} institutions
                """)
            
            st.divider()
            st.markdown("### Institution Lists by Quadrant")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "High Mobility, Low Cost", 
                "High Mobility, High Cost",
                "Low Mobility, Low Cost",
                "Low Mobility, High Cost"
            ])
            
            with tab1:
                high_mob_low_cost = df[
                    (df['sticker_price_2013'] < global_median_price) & 
                    (df['mobility_rate'] > global_median_mobility)
                ].copy()
                
                if not high_mob_low_cost.empty:
                    display_df = high_mob_low_cost[['name', 'subgroup', 'sticker_price_2013', 'mobility_rate', 'par_q1']].copy()
                    display_df = display_df.rename(columns={
                        'name': 'Institution',
                        'subgroup': 'Type',
                        'sticker_price_2013': 'Sticker Price',
                        'mobility_rate': 'Mobility Rate',
                        'par_q1': 'Q1 Students'
                    })
                    st.dataframe(
                        display_df.sort_values('Mobility Rate', ascending=False)
                        .reset_index(drop=True)
                        .assign(Rank=lambda x: range(1, len(x) + 1))
                        .set_index('Rank')
                        .style.format({
                            'Sticker Price': '${:,.0f}',
                            'Mobility Rate': '{:.1%}',
                            'Q1 Students': '{:.1%}'
                        }),
                        use_container_width=True
                    )
                else:
                    st.write("No institutions in this quadrant")
            
            with tab2:
                high_mob_high_cost = df[
                    (df['sticker_price_2013'] > global_median_price) & 
                    (df['mobility_rate'] > global_median_mobility)
                ].copy()
                
                if not high_mob_high_cost.empty:
                    display_df = high_mob_high_cost[['name', 'subgroup', 'sticker_price_2013', 'mobility_rate', 'par_q1']].copy()
                    display_df = display_df.rename(columns={
                        'name': 'Institution',
                        'subgroup': 'Type',
                        'sticker_price_2013': 'Sticker Price',
                        'mobility_rate': 'Mobility Rate',
                        'par_q1': 'Q1 Students'
                    })
                    st.dataframe(
                        display_df.sort_values('Mobility Rate', ascending=False)
                        .reset_index(drop=True)
                        .assign(Rank=lambda x: range(1, len(x) + 1))
                        .set_index('Rank')
                        .style.format({
                            'Sticker Price': '${:,.0f}',
                            'Mobility Rate': '{:.1%}',
                            'Q1 Students': '{:.1%}'
                        }),
                        use_container_width=True
                    )
                else:
                    st.write("No institutions in this quadrant")
            
            with tab3:
                low_mob_low_cost = df[
                    (df['sticker_price_2013'] < global_median_price) & 
                    (df['mobility_rate'] < global_median_mobility)
                ].copy()
                
                if not low_mob_low_cost.empty:
                    display_df = low_mob_low_cost[['name', 'subgroup', 'sticker_price_2013', 'mobility_rate', 'par_q1']].copy()
                    display_df = display_df.rename(columns={
                        'name': 'Institution',
                        'subgroup': 'Type',
                        'sticker_price_2013': 'Sticker Price',
                        'mobility_rate': 'Mobility Rate',
                        'par_q1': 'Q1 Students'
                    })
                    st.dataframe(
                        display_df.sort_values('Mobility Rate', ascending=False)
                        .reset_index(drop=True)
                        .assign(Rank=lambda x: range(1, len(x) + 1))
                        .set_index('Rank')
                        .style.format({
                            'Sticker Price': '${:,.0f}',
                            'Mobility Rate': '{:.1%}',
                            'Q1 Students': '{:.1%}'
                        }),
                        use_container_width=True
                    )
                else:
                    st.write("No institutions in this quadrant")
            
            with tab4:
                low_mob_high_cost = df[
                    (df['sticker_price_2013'] > global_median_price) & 
                    (df['mobility_rate'] < global_median_mobility)
                ].copy()
                
                if not low_mob_high_cost.empty:
                    display_df = low_mob_high_cost[['name', 'subgroup', 'sticker_price_2013', 'mobility_rate', 'par_q1']].copy()
                    display_df = display_df.rename(columns={
                        'name': 'Institution',
                        'subgroup': 'Type',
                        'sticker_price_2013': 'Sticker Price',
                        'mobility_rate': 'Mobility Rate',
                        'par_q1': 'Q1 Students'
                    })
                    st.dataframe(
                        display_df.sort_values('Mobility Rate', ascending=False)
                        .reset_index(drop=True)
                        .assign(Rank=lambda x: range(1, len(x) + 1))
                        .set_index('Rank')
                        .style.format({
                            'Sticker Price': '${:,.0f}',
                            'Mobility Rate': '{:.1%}',
                            'Q1 Students': '{:.1%}'
                        }),
                        use_container_width=True
                    )
                else:
                    st.write("No institutions in this quadrant")
            
            st.divider()
            st.markdown("### Complete Institution List")
            show_institution_list(df, selected_group)
