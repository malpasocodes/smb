import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_utils import merge_datasets, prepare_mobility_ladder

def show_mobility_ladder():
    """Display the mobility ladder analysis."""
    df = merge_datasets()
    
    if df is not None:
        st.markdown("### Mobility Ladder Analysis")
        st.markdown("""
        This analysis shows the probability distribution of economic outcomes for students 
        whose parents were in the bottom quintile (bottom 20%) of the income distribution.
        """)
        
        # Add group selector
        selected_group = st.selectbox(
            "Select Institution Group",
            ["All"] + sorted(df['tier_name'].unique().tolist()),
            help="Filter analysis by institution group"
        )
        
        # Get mobility ladder data
        ladder_df = prepare_mobility_ladder(df, selected_group)
        
        # Add view type selector
        view_type = st.radio(
            "Select View Type",
            ["Bar Chart", "Ladder Visualization"],
            horizontal=True
        )
        
        if view_type == "Bar Chart":
            show_bar_chart(ladder_df)
        else:
            show_ladder_viz(ladder_df)
        
        # Show the underlying data
        st.markdown("### Detailed Probabilities")
        st.dataframe(
            ladder_df.style.format({
                'probability': '{:.1%}'
            }),
            hide_index=True,
            use_container_width=True
        )

def show_bar_chart(ladder_df):
    """Display bar chart of mobility probabilities."""
    fig = px.bar(
        ladder_df,
        x='quintile',
        y='probability',
        text='probability',
        custom_data=['description', 'income_range'],
        title='Probability Distribution of Economic Outcomes',
        labels={
            'quintile': 'Child Income Quintile',
            'probability': 'Probability',
        },
        height=500
    )
    
    # Update layout
    fig.update_traces(
        texttemplate='%{text:.1%}',
        textposition='outside',
        hovertemplate=(
            '<b>%{customdata[0]}</b><br>' +
            'Income Range: %{customdata[1]}<br>' +
            'Probability: %{y:.1%}<br>' +
            '<extra></extra>'
        )
    )
    
    fig.update_layout(
        yaxis=dict(
            tickformat='.0%',
            title_font=dict(size=14),
            tickfont=dict(size=12),
            range=[0, max(ladder_df['probability']) * 1.2]  # Add space for text
        ),
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_ladder_viz(ladder_df):
    """Display ladder visualization of mobility."""
    # Create figure
    fig = go.Figure()
    
    # Calculate positions
    y_positions = [i * 20 for i in range(5)]  # Space out the rungs
    
    # Fixed width for probability bars (using full available space)
    bar_start = 10  # Left edge of bars
    bar_end = 70    # Right edge of bars (leaving space for labels)
    bar_width = bar_end - bar_start
    
    # Get baseline data for all institutions
    df = merge_datasets()
    baseline_df = prepare_mobility_ladder(df, "All")
    
    # Add ladder rungs (horizontal lines)
    for i, (row, baseline_row) in enumerate(zip(ladder_df.iterrows(), baseline_df.iterrows())):
        row = row[1]  # Get the row data from the tuple
        baseline_row = baseline_row[1]
        
        # Add rung
        fig.add_shape(
            type="line",
            x0=10,
            y0=y_positions[i],
            x1=90,
            y1=y_positions[i],
            line=dict(color="gray", width=2)
        )
        
        # Add quintile label
        fig.add_annotation(
            x=5,
            y=y_positions[i],
            text=row['quintile'],
            showarrow=False,
            font=dict(size=14)
        )
        
        # Add baseline probability bar
        baseline_length = bar_width * baseline_row['probability']
        fig.add_shape(
            type="rect",
            x0=bar_start,
            y0=y_positions[i] - 3,
            x1=bar_start + baseline_length,
            y1=y_positions[i] + 3,
            fillcolor="lightgray",
            line=dict(color="gray", width=1),
            opacity=0.5,
            layer="below"
        )
        
        # Add selected group probability bar
        bar_length = bar_width * row['probability']
        fig.add_shape(
            type="rect",
            x0=bar_start,
            y0=y_positions[i] - 3,
            x1=bar_start + bar_length,
            y1=y_positions[i] + 3,
            fillcolor="lightblue",
            line=dict(color="blue", width=1)
        )
        
        # Add probability labels
        fig.add_annotation(
            x=bar_start + bar_length + 2,
            y=y_positions[i] + 2,
            text=f"{row['probability']:.1%}",
            showarrow=False,
            font=dict(size=12, color="blue")
        )
        
        fig.add_annotation(
            x=bar_start + baseline_length + 2,
            y=y_positions[i] - 2,
            text=f"All: {baseline_row['probability']:.1%}",
            showarrow=False,
            font=dict(size=12, color="gray")
        )
        
        # Add description
        fig.add_annotation(
            x=95,
            y=y_positions[i],
            text=f"{row['description']}<br>{row['income_range']}",
            showarrow=False,
            font=dict(size=12),
            align="left",
            xanchor="left"
        )
    
    # Add vertical lines
    fig.add_shape(
        type="line",
        x0=10,
        y0=0,
        x1=10,
        y1=y_positions[-1],
        line=dict(color="gray", width=2)
    )
    
    fig.add_shape(
        type="line",
        x0=90,
        y0=0,
        x1=90,
        y1=y_positions[-1],
        line=dict(color="gray", width=2)
    )
    
    # Add legend
    fig.add_annotation(
        x=50,
        y=max(y_positions) + 10,
        text="Blue bars: Selected group | Gray bars: All institutions",
        showarrow=False,
        font=dict(size=12),
        align="center"
    )
    
    # Update layout
    fig.update_layout(
        title="Economic Mobility Ladder",
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[0, 100]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-5, max(y_positions) + 15]  # Increased to accommodate legend
        ),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)