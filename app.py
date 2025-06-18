import streamlit as st
import datetime
from db_institution import init_institution_db, add_institution, get_all_institutions, delete_institution
from db_accreditation import init_accreditation_db, add_accreditation, get_all_accreditations, delete_accreditation
import pandas as pd  # Make sure this is at the top of app.py
import sqlite3


# Initialize databases
init_institution_db()
init_accreditation_db()

st.title("🎓 Accreditation Management System")

st.markdown(
    "<span style='color: red; font-weight: bold;'>‼️ Click the <span style='font-family: monospace;'>&gt;&gt;</span> button on the left sidebar to expand it and see the options.</span>",
    unsafe_allow_html=True
)

# st.markdown("""
# **Project Members:**  
# - ARJIT PRAVEEN KUMAR *(1BY23CS030)*  
# - FIRDOUS UMME HANI *(1BY23CS063)*
# """)

st.markdown("""
**Project Members**
<table style='width: 100%; border-collapse: collapse;'>
  <thead>
    <tr style='background-color: #f2f2f2;'>
      <th style='text-align: left; padding: 8px;'>Name</th>
      <th style='text-align: left; padding: 8px;'>USN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style='padding: 8px;'>ARJIT PRAVEEN KUMAR</td>
      <td style='padding: 8px;'>1BY23CS030</td>
    </tr>
    <tr>
      <td style='padding: 8px;'>FIRDOUS UMME HANI</td>
      <td style='padding: 8px;'>1BY23CS063</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)


st.sidebar.header("Choose Action")
action = st.sidebar.radio("Go to", [
    "Add Institution", "Add Accreditation", "View Data", "Delete Data", "Query Results"
])


# Add Institution
if action == "Add Institution":
    st.subheader("➕ Add New Institution")
    name = st.text_input("Institution Name")
    type_ = st.selectbox("Type", ["College", "University", "Autonomous", "Other"])
    location = st.text_input("Location")
    email = st.text_input("Contact Email")

    if st.button("Add Institution"):
        if name and email:
            add_institution(name, type_, location, email)
            st.success(f"Institution '{name}' added.")
        else:
            st.warning("Please fill in all required fields.")

# Add Accreditation
elif action == "Add Accreditation":
    st.subheader("📝 Add Accreditation Record")

    institutions = get_all_institutions()
    if not institutions:
        st.warning("No institutions found. Please add an institution first.")
    else:
        inst_display = [f"{inst[0]} - {inst[1]}" for inst in institutions]
        selected = st.selectbox("Select Institution", inst_display)
        institution_id = int(selected.split(" - ")[0])

        body = st.selectbox("Accreditation Body", ["NAAC", "NBA", "AICTE", "UGC", "ISO", "Other"])
        level = st.text_input("Accreditation Level (e.g., A+, Tier-1)")
        valid_from = st.date_input("Valid From", value=datetime.date.today())
        valid_until = st.date_input("Valid Until", value=datetime.date.today())
        status = st.selectbox("Status", ["Active", "Expired", "Revoked"])

        if st.button("Add Accreditation"):
            add_accreditation(institution_id, body, level, str(valid_from), str(valid_until), status)
            st.success("Accreditation added successfully.")

# View Data
elif action == "View Data":
    st.subheader("🏫 Institutions")
    institutions = get_all_institutions()
    institution_columns = ["ID", "Name", "Type", "Location", "Email"]
    institution_df = pd.DataFrame(institutions, columns=institution_columns)
    st.dataframe(institution_df, use_container_width=True)

    st.subheader("📄 Accreditation Records")
    accs = get_all_accreditations()
    accreditation_columns = [
        "ID", "Institution ID", "Body Name", "Level",
        "Valid From", "Valid Until", "Status"
    ]
    acc_df = pd.DataFrame(accs, columns=accreditation_columns)
    st.dataframe(acc_df, use_container_width=True)

elif action == "Delete Data":
    st.subheader("❌ Delete Records")

    delete_choice = st.radio("Select what to delete", ["Institution", "Accreditation"])

    if delete_choice == "Institution":
        institutions = get_all_institutions()
        if not institutions:
            st.info("No institutions available to delete.")
        else:
            options = [f"{i[0]} - {i[1]}" for i in institutions]
            selected = st.selectbox("Select Institution to Delete", options)
            inst_id = int(selected.split(" - ")[0])
            if st.button("Delete Institution"):
                delete_institution(inst_id)
                st.success(f"Institution ID {inst_id} deleted.")

    elif delete_choice == "Accreditation":
        accs = get_all_accreditations()
        if not accs:
            st.info("No accreditation records to delete.")
        else:
            options = [f"{a[0]} - {a[2]} ({a[3]})" for a in accs]  # ID - Body (Level)
            selected = st.selectbox("Select Accreditation to Delete", options)
            acc_id = int(selected.split(" - ")[0])
            if st.button("Delete Accreditation"):
                delete_accreditation(acc_id)
                st.success(f"Accreditation ID {acc_id} deleted.")

# ---------------------------------------------------------------------

elif action == "Query Results":
    st.subheader("🔍 Query Accreditation Records")

    # Connect and read both databases
    conn_in = sqlite3.connect('institution.db')
    conn_acc = sqlite3.connect('accreditation.db')

    inst_df = pd.read_sql_query("SELECT * FROM institutions", conn_in)
    acc_df = pd.read_sql_query("SELECT * FROM accreditations", conn_acc)

    # Merge datasets
    merged = pd.merge(acc_df, inst_df, on="institution_id", how="left")

    # Rename columns for clarity
    merged = merged.rename(columns={
        "name": "Institution Name",
        "type": "Institution Type",
        "location": "Location",
        "contact_email": "Email",
        "body_name": "Accreditation Body",
        "level": "Level",
        "valid_from": "Valid From",
        "valid_until": "Valid Until",
        "status": "Status"
    })

    # ---- FILTERS ----
    st.markdown("### 🧮 Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.selectbox("Filter by Status", ["All"] + sorted(merged["Status"].dropna().unique()))

    with col2:
        level_filter = st.selectbox("Filter by Level", ["All"] + sorted(merged["Level"].dropna().unique()))

    with col3:
        body_filter = st.selectbox("Filter by Accreditation Body", ["All"] + sorted(merged["Accreditation Body"].dropna().unique()))

    # Apply filters
    if status_filter != "All":
        merged = merged[merged["Status"] == status_filter]
    if level_filter != "All":
        merged = merged[merged["Level"] == level_filter]
    if body_filter != "All":
        merged = merged[merged["Accreditation Body"] == body_filter]

    # Sort control
    sort_order = st.radio("Sort by Institution Name", ["Ascending", "Descending"])
    merged = merged.sort_values(by="Institution Name", ascending=(sort_order == "Ascending"))

    # Show final table
    st.dataframe(merged.reset_index(drop=True), use_container_width=True)

    conn_in.close()
    conn_acc.close()
