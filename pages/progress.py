import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from utils.database import get_user_progress

def show():
    st.title("Monitoraggio Progressi")
    
    if not st.session_state.user['logged_in']:
        st.warning("Effettua il login per monitorare i tuoi progressi")
        return
    
    # Get progress data
    # In a real app, this would come from the database
    if 'measurements' not in st.session_state:
        # Sample data for demonstration
        st.session_state.measurements = [
            {
                'date': (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                'weight': 80.5,
                'body_fat': 18.0,
                'chest': 95.0,
                'waist': 85.0,
                'hips': 100.0,
                'arms': 35.0,
                'thighs': 55.0,
                'notes': "Starting measurements"
            },
            {
                'date': (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
                'weight': 79.0,
                'body_fat': 17.5,
                'chest': 96.0,
                'waist': 84.0,
                'hips': 99.5,
                'arms': 35.5,
                'thighs': 55.5,
                'notes': "Good progress"
            },
            {
                'date': (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                'weight': 78.0,
                'body_fat': 16.8,
                'chest': 97.0,
                'waist': 83.0,
                'hips': 99.0,
                'arms': 36.0,
                'thighs': 56.0,
                'notes': "Consistent training"
            },
            {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'weight': 77.5,
                'body_fat': 16.0,
                'chest': 98.0,
                'waist': 82.0,
                'hips': 98.5,
                'arms': 36.5,
                'thighs': 56.5,
                'notes': "Increased protein intake"
            }
        ]
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(st.session_state.measurements)
    
    # Progress summary cards
    st.subheader("Riepilogo")
    
    if not df.empty:
        # Calculate changes
        first_entry = df.iloc[0]
        last_entry = df.iloc[-1]
        
        # Create metrics showing progress
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            weight_change = last_entry['weight'] - first_entry['weight']
            st.metric("Peso", f"{last_entry['weight']} kg", f"{weight_change:.1f} kg")
        
        with col2:
            bf_change = last_entry['body_fat'] - first_entry['body_fat']
            st.metric("Grasso Corporeo", f"{last_entry['body_fat']}%", f"{bf_change:.1f}%")
        
        with col3:
            chest_change = last_entry['chest'] - first_entry['chest']
            st.metric("Petto", f"{last_entry['chest']} cm", f"{chest_change:.1f} cm")
        
        with col4:
            arm_change = last_entry['arms'] - first_entry['arms']
            st.metric("Braccia", f"{last_entry['arms']} cm", f"{arm_change:.1f} cm")
    
    # Main tabs for different progress views
    tab1, tab2, tab3 = st.tabs(["Grafici", "Misurazioni", "Storico Allenamenti"])
    
    with tab1:
        # Progress charts using Plotly
        st.subheader("Grafici Progressi")
        
        if df.empty:
            st.info("Nessun dato di progresso disponibile. Aggiungi misurazioni per vedere i tuoi progressi.")
        else:
            # Convert date column to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Mapping per tradurre i nomi delle metriche
            metrics_map = {
                "peso": "weight", 
                "grasso_corporeo": "body_fat", 
                "petto": "chest", 
                "vita": "waist", 
                "fianchi": "hips", 
                "braccia": "arms", 
                "cosce": "thighs"
            }
            
            # Traduciamo le opzioni del menu
            it_metrics = ["peso", "grasso_corporeo", "petto", "vita", "fianchi", "braccia", "cosce"]
            display_metrics = ["Peso", "Grasso Corporeo", "Petto", "Vita", "Fianchi", "Braccia", "Cosce"]
            
            # Crea un dizionario per la visualizzazione
            metrics_display = {metrics_map[m]: d for m, d in zip(it_metrics, display_metrics)}
            
            # Select which metrics to show
            selected_it_metrics = st.multiselect(
                "Seleziona metriche da visualizzare",
                display_metrics,
                default=["Peso", "Grasso Corporeo"]
            )
            
            # Converti le metriche selezionate in italiano nei corrispondenti valori inglesi
            display_to_original = {d: metrics_map[m] for m, d in zip(it_metrics, display_metrics)}
            metrics = [display_to_original[m] for m in selected_it_metrics]
            
            if metrics:
                # Line chart for selected metrics
                fig = go.Figure()
                
                for metric in metrics:
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df[metric],
                        mode='lines+markers',
                        name=metric.replace('_', ' ').title()
                    ))
                
                fig.update_layout(
                    title="Progress Over Time",
                    xaxis_title="Date",
                    yaxis_title="Measurement",
                    legend_title="Metrics",
                    height=500,
                    template="plotly_dark"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Before and after comparison
                st.subheader("Before vs. Current")
                
                # Get first and last entry for comparison
                first = df.iloc[0]
                last = df.iloc[-1]
                
                # Create comparison bar chart
                compare_df = pd.DataFrame({
                    'Metric': [m.replace('_', ' ').title() for m in metrics],
                    'Before': [first[m] for m in metrics],
                    'Current': [last[m] for m in metrics]
                })
                
                fig = px.bar(
                    compare_df,
                    x='Metric',
                    y=['Before', 'Current'],
                    barmode='group',
                    title="Before vs. Current Comparison",
                    height=400,
                    template="plotly_dark"
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Measurements data table
        st.subheader("Measurement History")
        
        if df.empty:
            st.info("No measurement history available. Add measurements to track your progress.")
        else:
            # Sort by date descending
            df_sorted = df.sort_values('date', ascending=False).reset_index(drop=True)
            
            # Display as a table
            st.dataframe(df_sorted)
            
            # Export option
            if st.button("Export Data (CSV)"):
                # In a real app, this would generate a CSV for download
                st.success("In a complete app, this would download your data as a CSV file.")
    
    with tab3:
        # Workout history
        st.subheader("Workout History")
        
        # In a real app, this would come from the database
        # Generate some sample workout history for demo
        if 'workout_history' not in st.session_state:
            # Sample workout history
            st.session_state.workout_history = []
            
            workout_names = ["Full Body Strength", "Cardio Blast", "Core Crusher", "Upper Body Focus", "Leg Day"]
            
            for i in range(12):
                date = datetime.now() - timedelta(days=i*5)
                st.session_state.workout_history.append({
                    'date': date.strftime("%Y-%m-%d"),
                    'workout': random.choice(workout_names),
                    'duration': random.randint(30, 60),
                    'calories': random.randint(200, 500),
                    'completed': True
                })
        
        # Display workout history
        if st.session_state.workout_history:
            # Convert to DataFrame
            workout_df = pd.DataFrame(st.session_state.workout_history)
            
            # Sort by date descending
            workout_df = workout_df.sort_values('date', ascending=False).reset_index(drop=True)
            
            # Display as a table
            st.dataframe(workout_df)
            
            # Create workout frequency chart
            st.subheader("Workout Frequency")
            
            # Convert date to datetime
            workout_df['date'] = pd.to_datetime(workout_df['date'])
            
            # Count workouts by week
            workout_df['week'] = workout_df['date'].dt.isocalendar().week
            weekly_counts = workout_df.groupby('week').size().reset_index(name='count')
            
            # Create bar chart
            fig = px.bar(
                weekly_counts,
                x='week',
                y='count',
                title="Workouts per Week",
                labels={'week': 'Week Number', 'count': 'Number of Workouts'},
                template="plotly_dark"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Workout type distribution
            st.subheader("Workout Type Distribution")
            
            # Count by workout type
            type_counts = workout_df['workout'].value_counts().reset_index()
            type_counts.columns = ['workout', 'count']
            
            # Create pie chart
            fig = px.pie(
                type_counts,
                values='count',
                names='workout',
                title="Workout Type Distribution",
                template="plotly_dark"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No workout history available. Complete workouts to track your activity.")
    
    # Add new progress entry
    st.divider()
    st.subheader("Add New Progress Entry")
    
    with st.form("add_progress"):
        # Form for entering new progress data
        st.write("Enter your current measurements")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=75.0)
            chest = st.number_input("Chest (cm)", min_value=50, max_value=150, value=95)
        
        with col2:
            body_fat = st.number_input("Body Fat (%)", min_value=3.0, max_value=50.0, value=15.0)
            waist = st.number_input("Waist (cm)", min_value=50, max_value=150, value=85)
        
        with col3:
            arms = st.number_input("Arms (cm)", min_value=20, max_value=60, value=35)
            thighs = st.number_input("Thighs (cm)", min_value=30, max_value=100, value=55)
        
        hips = st.number_input("Hips (cm)", min_value=50, max_value=150, value=100)
        notes = st.text_area("Notes", placeholder="Any additional notes about your progress")
        
        # Submit button
        submitted = st.form_submit_button("Save Progress")
        if submitted:
            # Add to measurements
            new_entry = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'weight': weight,
                'body_fat': body_fat,
                'chest': chest,
                'waist': waist,
                'hips': hips,
                'arms': arms,
                'thighs': thighs,
                'notes': notes
            }
            
            st.session_state.measurements.append(new_entry)
            st.success("Progress entry saved successfully!")
            st.rerun()
