import streamlit as st
import pandas as pd
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="My Tasks - Event Manager",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* White background */
    .stApp {
        background: #ffffff;
    }
    
    /* Glass morphism effect */
    .main-container {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header styling with gradient text */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .sub-header {
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease-in;
    }
    
    /* User card */
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
        margin-bottom: 2rem;
        animation: zoomIn 0.5s ease-out;
    }
    
    @keyframes zoomIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .user-avatar {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: bounce 1s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .user-name {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Stats boxes */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(56, 239, 125, 0.3);
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stat-box:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 40px rgba(56, 239, 125, 0.5);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Task cards */
    .task-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid;
        border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .task-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.2);
        background: linear-gradient(135deg, #ffffff 0%, #e8edff 100%);
    }
    
    .task-code {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 700;
        display: inline-block;
        margin-right: 0.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .task-team {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    .task-status {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.3);
        margin-left: 0.5rem;
    }
    
    /* Phase headers */
    .phase-header {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        border-left: 6px solid #667eea;
        padding-left: 1.5rem;
        animation: fadeInLeft 0.8s ease-out;
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.2) 0%, rgba(245, 87, 108, 0.2) 100%);
        padding: 2rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        border: 2px solid rgba(240, 147, 251, 0.3);
        text-align: center;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        padding: 1rem 2rem;
        border-radius: 1rem;
        border: none;
        font-size: 1.2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        transform: translateY(-3px);
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        font-weight: 600;
        border-radius: 0.75rem;
        border: none;
        box-shadow: 0 5px 20px rgba(56, 239, 125, 0.3);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
        box-shadow: 0 8px 25px rgba(56, 239, 125, 0.5);
        transform: translateY(-2px);
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #6b7280;
    }
    
    .empty-state-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    /* Checkbox styling */
    .task-checkbox {
        transform: scale(1.5);
        margin-right: 1rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None
if 'task_completion' not in st.session_state:
    st.session_state.task_completion = {}

# Header
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">✅ My Tasks Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">📋 View and manage your assigned tasks</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# File upload section
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<h2 style="color: #667eea; margin-bottom: 1rem;">📂 Upload Task Assignment File</h2>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose your CSV file from the Event Task Manager", type=['csv'], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_data = df
        st.success('✅ File uploaded successfully!')
    except Exception as e:
        st.error(f'❌ Error reading file: {str(e)}')

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main content
if st.session_state.uploaded_data is not None:
    df = st.session_state.uploaded_data
    
    # Get unique assigned members (excluding 'Unassigned')
    all_members = df['Assigned To'].unique()
    members = [m for m in all_members if m != 'Unassigned']
    members.sort()
    
    # User selection
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #667eea; text-align: center; margin-bottom: 2rem;">👤 Select Your Name</h2>', unsafe_allow_html=True)
    
    # Create columns for member selection
    cols = st.columns(min(4, len(members)))
    for idx, member in enumerate(members):
        with cols[idx % min(4, len(members))]:
            if st.button(f'👤 {member}', use_container_width=True, key=f'select_{member}'):
                st.session_state.selected_user = member
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display tasks for selected user
    if st.session_state.selected_user:
        user = st.session_state.selected_user
        user_tasks = df[df['Assigned To'] == user]
        
        # User card
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="user-card">
            <div class="user-avatar">👤</div>
            <div class="user-name">{user}</div>
            <div style="font-size: 1.1rem; opacity: 0.9;">Event Team Member</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Statistics
        total_tasks = len(user_tasks)
        completed_tasks = sum(1 for task_id in user_tasks['Code'] if st.session_state.task_completion.get(f"{user}_{task_id}", False))
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        st.markdown(f'''
        <div class="stats-container">
            <div class="stat-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div class="stat-label">📋 Total Tasks</div>
                <div class="stat-number">{total_tasks}</div>
            </div>
            <div class="stat-box" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                <div class="stat-label">✅ Completed</div>
                <div class="stat-number">{completed_tasks}</div>
            </div>
            <div class="stat-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="stat-label">⏳ Pending</div>
                <div class="stat-number">{pending_tasks}</div>
            </div>
            <div class="stat-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="stat-label">📊 Progress</div>
                <div class="stat-number">{completion_rate:.0f}%</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export personal tasks
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            # Create personal task export
            personal_csv = user_tasks.to_csv(index=False)
            st.download_button(
                label=f'📥 Download My Tasks (CSV)',
                data=personal_csv,
                file_name=f'{user}_tasks.csv',
                mime='text/csv',
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display tasks by phase
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        phases = {
            '🎬 1. PRE-EVENT': user_tasks[user_tasks['Code'].str.startswith('1')],
            '⏰ 2. 1 DAY BEFORE THE EVENT': user_tasks[user_tasks['Code'].str.startswith('2')],
            '🎪 3. DURING THE EVENT': user_tasks[user_tasks['Code'].str.startswith('3')],
            '🎉 4. POST-EVENT ACTIVITIES': user_tasks[user_tasks['Code'].str.startswith('4')]
        }
        
        for phase_name, phase_tasks in phases.items():
            if len(phase_tasks) > 0:
                st.markdown(f'<div class="phase-header">{phase_name}</div>', unsafe_allow_html=True)
                
                for _, task in phase_tasks.iterrows():
                    task_id = f"{user}_{task['Code']}"
                    is_completed = st.session_state.task_completion.get(task_id, False)
                    
                    col1, col2 = st.columns([0.5, 9.5])
                    
                    with col1:
                        if st.checkbox('', value=is_completed, key=f'check_{task_id}', label_visibility="collapsed"):
                            st.session_state.task_completion[task_id] = True
                        else:
                            st.session_state.task_completion[task_id] = False
                    
                    with col2:
                        status_style = 'opacity: 0.6; text-decoration: line-through;' if is_completed else ''
                        status_badge = '<span class="task-status">✅ Done</span>' if is_completed else '<span class="task-status" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">⏳ Pending</span>'
                        
                        st.markdown(f'''
                        <div class="task-card" style="{status_style}">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div style="flex: 1;">
                                    <div style="margin-bottom: 0.75rem;">
                                        <span class="task-code">{task['Code']}</span>
                                        <span class="task-team">{task['Team']}</span>
                                        {status_badge}
                                    </div>
                                    <p style="color: #1f2937; margin: 0; font-size: 1rem; line-height: 1.6;">{task['Task']}</p>
                                </div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Back button
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        if st.button('🔙 Change User', use_container_width=True):
            st.session_state.selected_user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty state
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('''
    <div class="empty-state">
        <div class="empty-state-icon">📂</div>
        <h2 style="color: #667eea; margin-bottom: 1rem;">No File Uploaded Yet</h2>
        <p style="font-size: 1.1rem;">Please upload the CSV file exported from the Event Task Manager app</p>
        <p style="color: #9ca3af; margin-top: 1rem;">The file should contain columns: Code, Task, Team, Assigned To</p>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<br><br>', unsafe_allow_html=True)
st.markdown('''
<div style="text-align: center; padding: 2rem; color: white; font-size: 0.875rem; opacity: 0.8;">
    <p>✨ Personal Task Dashboard</p>
    <p>📋 Track • Complete • Succeed</p>
</div>
''', unsafe_allow_html=True)
