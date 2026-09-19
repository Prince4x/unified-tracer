"""
UnifiedTrace - Streamlit Dashboard
Interactive frontend for fraud investigation and entity correlation
"""

import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO, BytesIO
import hashlib
from datetime import datetime
import json
import requests
from requests.exceptions import ConnectionError
import sys
import os

# Add backend to path
sys.path.insert(0, '/home/claude')
from backend import CorrelationEngine, app, init_db

st.set_page_config(
    page_title="UnifiedTrace - Cyber Fraud Investigation",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    h1 {
        color: #1a1a2e;
        border-bottom: 3px solid #e74c3c;
        padding-bottom: 1rem;
    }
    h2 {
        color: #16213e;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = CorrelationEngine()
    st.session_state.data_loaded = False
    st.session_state.analysis_done = False

# Main header
st.title("🔍 UnifiedTrace")
st.markdown("### AI-Powered Cyber Fraud Correlation & Digital Artifact Intelligence Platform")

# Sidebar
with st.sidebar:
    st.header("📁 Data Management")
    
    tab1, tab2, tab3 = st.tabs(["Upload Data", "Sample Data", "Settings"])
    
    with tab1:
        st.subheader("Upload Investigation Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cdr_file = st.file_uploader("📞 CDR Records (CSV)", type=['csv'], key='cdr')
        
        with col2:
            bank_file = st.file_uploader("🏦 Bank Transactions (CSV)", type=['csv'], key='bank')
        
        with col3:
            apk_file = st.file_uploader("📱 APK Metadata (CSV)", type=['csv'], key='apk')
        
        if st.button("🔄 Load Data", use_container_width=True):
            if cdr_file or bank_file or apk_file:
                try:
                    if cdr_file:
                        cdr_df = pd.read_csv(cdr_file)
                        st.session_state.engine.load_cdr(cdr_df)
                        st.success(f"✅ CDR: {len(cdr_df)} records loaded")
                    
                    if bank_file:
                        bank_df = pd.read_csv(bank_file)
                        st.session_state.engine.load_bank_data(bank_df)
                        st.success(f"✅ Bank: {len(bank_df)} records loaded")
                    
                    if apk_file:
                        apk_df = pd.read_csv(apk_file)
                        st.session_state.engine.load_apk_data(apk_df)
                        st.success(f"✅ APK: {len(apk_df)} records loaded")
                    
                    st.session_state.data_loaded = True
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please select at least one file")
    
    with tab2:
        st.subheader("Generate Sample Data")
        if st.button("📊 Create Demo Datasets", use_container_width=True):
            with st.spinner("Generating sample data..."):
                try:
                    # Import the generator
                    from test_data_generator import generate_test_datasets
                    cdr_df, bank_df, apk_df = generate_test_datasets()
                    
                    # Load into engine
                    st.session_state.engine.load_cdr(cdr_df)
                    st.session_state.engine.load_bank_data(bank_df)
                    st.session_state.engine.load_apk_data(apk_df)
                    st.session_state.data_loaded = True
                    
                    st.success("✅ Sample datasets generated and loaded!")
                    st.info(f"📈 Total entities: {len(st.session_state.engine.graph.nodes())}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with tab3:
        st.subheader("Settings")
        anomaly_threshold = st.slider("Anomaly Detection Threshold (%)", 0, 100, 70)
        show_low_risk = st.checkbox("Show low-risk entities", value=False)
        st.session_state.threshold = anomaly_threshold
        st.session_state.show_low = show_low_risk

# Main content
if not st.session_state.data_loaded:
    st.warning("📋 **No data loaded yet!**")
    st.markdown("""
    ## 🚀 Quick Start Guide:
    
    ### Step 1️⃣ - Load Data (Sidebar)
    - **Option A:** Click **Sample Data** → **"📊 Create Demo Datasets"** (FASTEST!)
    - **Option B:** Upload your own CDR, bank, or APK CSV files
    
    ### Step 2️⃣ - Run Analysis (Analysis Tab)
    - Click **"🔍 RUN ANALYSIS NOW"**
    - Wait 5-10 seconds for results
    
    ### Step 3️⃣ - View Results
    - **Analysis Tab** → See risk scores & distribution
    - **Entity Graph Tab** → See network visualization
    - **Entities Tab** → See all entities with risk levels
    - **Report Tab** → Generate forensic PDF report
    
    ---
    ### 📌 Current Status
    ✅ All features ready
    ⏳ Waiting for data...
    
    ### Features:
    - 🔗 Automated entity correlation across telecom, financial, and app data
    - 🤖 ML-based anomaly detection using Isolation Forest
    - 📊 Interactive network visualization
    - 📈 Risk scoring for entities
    - 📄 Court-admissible forensic reports with SHA-256 hash verification
    """)
else:
    # Tabs for different views
    tab_analysis, tab_graph, tab_entities, tab_report = st.tabs(
        ["📊 Analysis", "🕸️ Entity Graph", "📋 Entities", "📄 Report"]
    )
    
    with tab_analysis:
        st.subheader("Correlation Analysis")
        st.info("👇 **Step 1:** Click the button below to run the fraud detection analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Run analysis
        if st.button("🔍 RUN ANALYSIS NOW", use_container_width=True, key='analyze_btn'):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("⏳ Calculating risk scores...")
                progress_bar.progress(25)
                
                st.session_state.engine.calculate_risk_scores()
                progress_bar.progress(75)
                
                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)
                
                st.session_state.analysis_done = True
                st.success("✅ **Analysis Complete!**")
                st.info("""
                📊 **Next Steps:**
                1. 👈 Click **Entity Graph** tab to see network visualization
                2. 📋 Click **Entities** tab to see all entities with risk scores
                3. 📄 Click **Report** tab to generate forensic PDF report
                """)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        if st.session_state.analysis_done:
            # Calculate metrics
            total_entities = len(st.session_state.engine.graph.nodes())
            total_relationships = len(st.session_state.engine.graph.edges())
            high_risk = sum(1 for s in st.session_state.engine.risk_scores.values() 
                           if s > 70)
            medium_risk = sum(1 for s in st.session_state.engine.risk_scores.values() 
                             if 40 <= s <= 70)
            
            with col1:
                st.metric("Total Entities", total_entities, "🔗")
            with col2:
                st.metric("Relationships", total_relationships, "📊")
            with col3:
                st.metric("High Risk (>70)", high_risk, "🔴")
            with col4:
                st.metric("Medium Risk", medium_risk, "🟡")
            
            st.markdown("---")
            
            # Risk distribution chart
            st.subheader("Risk Score Distribution")
            risk_values = list(st.session_state.engine.risk_scores.values())
            
            fig = go.Figure(data=[
                go.Histogram(x=risk_values, nbinsx=30, marker_color='#e74c3c')
            ])
            fig.update_layout(
                title="Risk Score Distribution",
                xaxis_title="Risk Score",
                yaxis_title="Number of Entities",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Top risky entities
            st.subheader("Top 15 High-Risk Entities")
            top_risky = sorted(st.session_state.engine.risk_scores.items(), 
                              key=lambda x: x[1], reverse=True)[:15]
            
            risky_data = []
            for node, score in top_risky:
                node_str = str(node)
                if ':' in node_str:
                    entity_type, value = node_str.split(':', 1)
                else:
                    entity_type = "UNKNOWN"
                    value = node_str
                risky_data.append({
                    'Entity': value,
                    'Type': entity_type,
                    'Risk Score': f"{score:.1f}%"
                })
            risky_df = pd.DataFrame(risky_data)
            
            st.dataframe(risky_df, use_container_width=True, hide_index=True)
    
    with tab_graph:
        st.subheader("Entity Relationship Network")
        
        if not st.session_state.analysis_done:
            st.warning("⚠️ **Analysis not yet run!**")
            st.info("👈 Go to the **Analysis tab** and click **'RUN ANALYSIS NOW'** first")
            st.stop()
        
        if st.session_state.analysis_done:
            try:
                graph_data = st.session_state.engine.get_graph_data()
                
                # Create network visualization
                fig = go.Figure()
                
                # Extract positions using spring layout
                G = st.session_state.engine.graph
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
                
                # Add edges
                edge_x = []
                edge_y = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.append(x0)
                    edge_x.append(x1)
                    edge_x.append(None)
                    edge_y.append(y0)
                    edge_y.append(y1)
                    edge_y.append(None)
                
                fig.add_trace(go.Scatter(
                    x=edge_x, y=edge_y,
                    mode='lines',
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='none',
                    showlegend=False
                ))
                
                # Add nodes
                node_x = []
                node_y = []
                node_text = []
                node_color = []
                node_size = []
                
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    risk = st.session_state.engine.risk_scores.get(node, 0)
                    node_color.append(risk)
                    node_size.append(max(10, min(30, 10 + risk/5)))
                    # Safe node display
                    if ':' in str(node):
                        display_node = str(node).split(':', 1)[1]
                    else:
                        display_node = str(node)
                    node_text.append(f"{display_node}<br>Risk: {risk:.1f}%")
                
                fig.add_trace(go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers',
                    text=node_text,
                    hovertemplate='%{text}<extra></extra>',
                    marker=dict(
                        size=node_size,
                        color=node_color,
                        colorscale='Reds',
                        showscale=True,
                        colorbar=dict(title="Risk Score"),
                        line_width=2,
                        line_color='white'
                    ),
                    showlegend=False
                ))
                
                fig.update_layout(
                    title="Entity Correlation Network",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    height=600,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Network statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_degree = np.mean([G.degree(n) for n in G.nodes()])
                    st.metric("Avg Connections", f"{avg_degree:.1f}")
                with col2:
                    density = nx.density(G)
                    st.metric("Network Density", f"{density:.3f}")
                with col3:
                    if len(G) > 0:
                        diameter = nx.diameter(G.to_undirected()) if nx.is_connected(G.to_undirected()) else "N/A"
                        st.metric("Network Diameter", diameter)
                
            except Exception as e:
                st.error(f"❌ Error generating graph: {str(e)}")
        else:
            st.info("Run analysis first to see the network graph")
    
    with tab_entities:
        st.subheader("Entity Details")
        
        if not st.session_state.analysis_done:
            st.warning("⚠️ **Analysis not yet run!**")
            st.info("👈 Go to the **Analysis tab** and click **'RUN ANALYSIS NOW'** first")
            st.stop()
        
        if st.session_state.analysis_done:
            # Entity filter - safely extract types
            entity_types = set()
            for node in st.session_state.engine.graph.nodes():
                if ':' in str(node):
                    entity_type = str(node).split(':')[0]
                else:
                    entity_type = "UNKNOWN"
                entity_types.add(entity_type)
            selected_type = st.selectbox("Filter by entity type:", ["ALL"] + sorted(entity_types))
            
            # Build entity table
            entities_list = []
            for node, risk in st.session_state.engine.risk_scores.items():
                # Safely split node
                if ':' in node:
                    entity_type, value = node.split(':', 1)
                else:
                    entity_type = "UNKNOWN"
                    value = node
                
                if selected_type != "ALL" and entity_type != selected_type:
                    continue
                
                if risk < 40 and not st.session_state.show_low:
                    continue
                
                degree = st.session_state.engine.graph.degree(node)
                entities_list.append({
                    'Entity ID': node,
                    'Type': entity_type,
                    'Value': value,
                    'Risk Score': f"{risk:.1f}%",
                    'Connections': degree,
                    'Risk Level': '🔴 High' if risk > 70 else ('🟡 Medium' if risk >= 40 else '🟢 Low')
                })
            
            entities_df = pd.DataFrame(entities_list)
            st.dataframe(entities_df, use_container_width=True, hide_index=True)
            
            # Download option
            csv = entities_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="entities.csv",
                mime="text/csv"
            )
        else:
            st.info("Run analysis first to see entity details")
    
    with tab_report:
        st.subheader("Forensic Investigation Report")
        
        if not st.session_state.analysis_done:
            st.warning("⚠️ **Analysis not yet run!**")
            st.info("👈 Go to the **Analysis tab** and click **'RUN ANALYSIS NOW'** first")
            st.stop()
        
        if st.session_state.analysis_done:
            st.info("""
            ✅ **Court-Admissible Forensic Report**
            - SHA-256 hash verification per Bharatiya Sakshya Adhiniyam, 2023 (Section 63)
            - Digital evidence certification for admissibility
            - Complete chain-of-custody documentation
            """)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Generate PDF Report", use_container_width=True):
                    with st.spinner("Generating report..."):
                        try:
                            import tempfile
                            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                            report_path = st.session_state.engine.generate_report(temp_file.name)
                            
                            with open(report_path, "rb") as f:
                                st.download_button(
                                    label="💾 Download PDF",
                                    data=f,
                                    file_name="forensic_report.pdf",
                                    mime="application/pdf"
                                )
                            st.success("✅ Report generated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            with col2:
                if st.button("📊 Summary Statistics", use_container_width=True):
                    summary = {
                        'Total Entities': len(st.session_state.engine.graph.nodes()),
                        'Total Relationships': len(st.session_state.engine.graph.edges()),
                        'High Risk Entities (>70)': sum(1 for s in st.session_state.engine.risk_scores.values() if s > 70),
                        'Report Generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    st.json(summary)
            
            # Report preview
            st.subheader("Report Preview")
            
            st.markdown("### High-Risk Entities Summary")
            high_risk_entities = [(node, score) for node, score in 
                                 st.session_state.engine.risk_scores.items() if score > 70]
            
            if high_risk_entities:
                preview_data = []
                for node, score in sorted(high_risk_entities, key=lambda x: x[1], reverse=True)[:10]:
                    if ':' in str(node):
                        entity_type, value = str(node).split(':', 1)
                    else:
                        entity_type = "UNKNOWN"
                        value = str(node)
                    preview_data.append({
                        'Entity': value,
                        'Type': entity_type,
                        'Risk Score': f"{score:.1f}%"
                    })
                preview_df = pd.DataFrame(preview_data)
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
            else:
                st.info("No high-risk entities detected")
        
        else:
            st.info("Run analysis first to generate reports")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <p><strong>UnifiedTrace v1.0</strong> | AI-Powered Cyber Fraud Investigation Platform</p>
    <p>Built for Void Hacks 8.0 | Shri Vaishnav Vidyapeeth, Indore</p>
    <p>🔐 Forensic integrity verified per Bharatiya Sakshya Adhiniyam, 2023</p>
</div>
""", unsafe_allow_html=True)
