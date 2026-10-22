import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import apply_custom_styles, render_hero, get_plotly_dark_template
from utils.db_connection import execute_query
from utils.query_catalog import (
    get_all_queries,
    get_query,
    get_categories
)

st.set_page_config(
    page_title="Analytics Hub | Cricbuzz LiveStats",
    page_icon="🔍",
    layout="wide"
)

apply_custom_styles()
dark_template = get_plotly_dark_template()

render_hero(
    title="Analytics Hub",
    subtitle="Interactive execution console for comprehensive cricket analytical queries.",
    badge="Analytics Hub"
)

# Filter: Category Domain
categories = ["All Categories"] + get_categories()
selected_category = st.selectbox("📂 Filter by Analytical Domain:", categories)

# Filter query list based on domain selection
filtered_queries = get_all_queries()

if selected_category != "All Categories":
    filtered_queries = [q for q in filtered_queries if q.get("category") == selected_category]

if not filtered_queries:
    st.warning("No queries match the selected filters.")
else:
    # Query Dropdown without [Beginner]/[Intermediate]/[Advanced] tags
    query_map = {q['title']: q['id'] for q in filtered_queries}
    selected_title = st.selectbox("🔍 Select Analytical Query to Execute:", list(query_map.keys()))
    selected_id = query_map[selected_title]
    q_data = get_query(selected_id)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Parameter Input Form
    param_schema = q_data.get("param_schema", {})
    query_params = dict(q_data.get("default_params", {}))
    
    if param_schema:
        st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #FCD34D; margin-bottom: 8px;'>Filters:</div>", unsafe_allow_html=True)
        param_cols = st.columns(len(param_schema))
        
        for idx, (p_name, p_spec) in enumerate(param_schema.items()):
            with param_cols[idx]:
                p_type = p_spec.get("type")
                p_label = p_spec.get("label", p_name)
                
                if p_type == "selectbox":
                    opts = p_spec.get("options", [])
                    def_idx = opts.index(p_spec.get("default")) if p_spec.get("default") in opts else 0
                    val = st.selectbox(p_label, opts, index=def_idx, key=f"param_{selected_id}_{p_name}")
                    if p_name == "year":
                        query_params["start_range"] = f"{val}-01-01"
                        query_params["end_range"] = f"{val}-12-31"
                    else:
                        query_params[p_name] = val
                        
                elif p_type == "slider":
                    min_v = p_spec.get("min", 1)
                    max_v = p_spec.get("max", 100)
                    step_v = p_spec.get("step", 1)
                    def_v = p_spec.get("default", min_v)
                    val = st.slider(p_label, min_value=min_v, max_value=max_v, value=def_v, step=step_v, key=f"param_{selected_id}_{p_name}")
                    query_params[p_name] = val
                    
                elif p_type == "number":
                    min_v = p_spec.get("min", 1)
                    max_v = p_spec.get("max", 100)
                    def_v = p_spec.get("default", 10)
                    val = st.number_input(p_label, min_value=min_v, max_value=max_v, value=def_v, key=f"param_{selected_id}_{p_name}")
                    query_params[p_name] = val

    # Execute Action Button
    exec_col1, exec_col2 = st.columns([1, 4])
    with exec_col1:
        run_query = st.button("Analysis", use_container_width=True)
        
    # Execute and Render Results
    try:
        df = execute_query(q_data["sql"], query_params)
        
        # Plotly Visualizations (if defined)
        chart_type = q_data.get("chart_type")
        cfg = q_data.get("chart_config", {})
        
        if chart_type and chart_type != "table" and not df.empty:
            st.subheader("📊 Analytical Visualization")
            
            if chart_type == "bar":
                y_col = cfg.get("y")
                fig = px.bar(
                    df,
                    x=cfg.get("x"),
                    y=y_col,
                    color=cfg.get("color"),
                    barmode="group" if isinstance(y_col, list) else "relative",
                    title=cfg.get("title", q_data["title"])
                )
                fig.update_layout(template=dark_template, height=400)
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type in ["pie", "donut"]:
                fig = px.pie(
                    df,
                    names=cfg.get("names"),
                    values=cfg.get("values"),
                    hole=0.45 if chart_type == "donut" else 0.0,
                    title=cfg.get("title", q_data["title"])
                )
                fig.update_layout(template=dark_template, height=400)
                st.plotly_chart(fig, use_container_width=True)
                
        # Table Output
        st.subheader("Output")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
