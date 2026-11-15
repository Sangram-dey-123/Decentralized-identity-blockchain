
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Decentralized Identity Dashboard",
    page_icon="🔐",
    layout="wide"
)

# =========================
# PROFESSIONAL DASHBOARD CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: #0b1120;
    color: #e5e7eb;
}
[data-testid="stSidebar"] {
    background: #111827;
}
h1, h2, h3 {
    color: #f8fafc;
}
.metric-card {
    background: linear-gradient(135deg,#172554,#1e293b);
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #334155;
}
.metric-title {
    color: #94a3b8;
    font-size: 14px;
}
.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #38bdf8;
}
.metric-sub {
    color: #94a3b8;
    font-size: 12px;
}
div[data-testid="stMetric"] {
    background: #111c32;
    border: 1px solid #26364f;
    padding: 16px;
    border-radius: 12px;
}
.stButton>button {
    border-radius: 8px;
    background-color: #2563eb;
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🔐 IDENTITY SYSTEM")
st.sidebar.caption("Hyperledger Fabric | Research Prototype")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "O1 Identity Management",
        "O2 Security & Integrity",
        "O3 Consent Access",
        "Audit & Network"
    ]
)

st.sidebar.divider()
st.sidebar.success("Research Prototype")
st.sidebar.caption("Org1 | Org2 | mychannel")

# =========================
# HEADER
# =========================
st.title("🔐 Decentralized Identity Management")
st.caption(
    "Blockchain-Based Identity, Credential Verification "
    "and Consent-Aware Access Control"
)

# =========================
# KPI FUNCTION
# =========================
def metric_card(title, value, subtitle):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# OVERVIEW
# =========================
if page == "Overview":

    st.subheader("System Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Blockchain Blocks", "56", "Project evaluation snapshot")

    with c2:
        metric_card("Identities", "25", "Project evaluation snapshot")

    with c3:
        metric_card("Credentials", "26", "Project evaluation snapshot")

    with c4:
        metric_card("Integrity", "VALID", "Reported evaluation result")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Research Objectives")

        objective_data = pd.DataFrame({
            "Objective": ["O1", "O2", "O3"],
            "Passed": [5, 4, 5],
            "Total": [5, 4, 5]
        })

        fig = px.bar(
            objective_data,
            x="Objective",
            y="Passed",
            text="Passed",
            color="Objective",
            title="Objective Evaluation Results"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120",
            showlegend=False
        )

        st.plotly_chart(fig, width="stretch")

    with right:
        st.subheader("System Architecture")

        st.markdown("""
        **Organization 1**
        - Identity Registration
        - Credential Issuance
        - Consent Management

        **Organization 2**
        - Credential Verification
        - Access Requests
        - Integrity Checking

        **Blockchain Layer**
        - Hyperledger Fabric
        - Chaincode
        - Immutable Audit Records
        """)

    st.info(
        "Dashboard evaluation values are project-reported snapshots. "
        "Live blockchain status will be connected in a later step."
    )

# =========================
# O1 IDENTITY
# =========================
elif page == "O1 Identity Management":

    st.subheader("O1 — Identity & Credential Lifecycle")

    st.markdown(
        "Identity registration, identity management, credential issuance "
        "and credential verification."
    )

    tab1, tab2 = st.tabs([
        "Identity Registration",
        "Credential Registration"
    ])

    with tab1:

        st.markdown("### Register Identity")

        identity_id = st.text_input("Identity ID")
        identity_name = st.text_input("Identity Name")
        identity_role = st.selectbox(
            "Identity Role",
            ["Healthcare", "Banking", "Government", "Student", "Other"]
        )

        if st.button("Preview Identity Registration"):

            if identity_id and identity_name:

                st.success("Identity registration preview generated.")

                st.json({
                    "identity_id": identity_id,
                    "name": identity_name,
                    "role": identity_role
                })

                st.warning(
                    "Preview only. This does not submit a Fabric transaction."
                )

            else:
                st.error("Enter Identity ID and Identity Name.")

    with tab2:

        st.markdown("### Register Credential")

        credential_id = st.text_input("Credential ID")
        owner_id = st.text_input("Owner Identity ID")
        credential_type = st.selectbox(
            "Credential Type",
            ["Healthcare Credential", "Banking KYC", "Government ID"]
        )

        if st.button("Preview Credential Registration"):

            if credential_id and owner_id:

                st.success("Credential preview generated.")

                st.json({
                    "credential_id": credential_id,
                    "owner_id": owner_id,
                    "credential_type": credential_type
                })

                st.warning(
                    "Preview only. Fabric integration will be added separately."
                )

            else:
                st.error("Enter Credential ID and Owner Identity ID.")

# =========================
# O2 SECURITY
# =========================
elif page == "O2 Security & Integrity":

    st.subheader("O2 — Blockchain Security & Integrity")

    st.markdown(
        "Cryptographic integrity checking using SHA-256 "
        "and digital signature verification using Ed25519."
    )

    tab1, tab2 = st.tabs([
        "SHA-256 Integrity",
        "Security Evaluation"
    ])

    with tab1:

        import hashlib

        original_data = st.text_area(
            "Original Credential Data",
            "Demo Healthcare Credential"
        )

        modified_data = st.text_area(
            "Verification Data",
            "Demo Healthcare Credential"
        )

        if st.button("Check SHA-256 Integrity"):

            original_hash = hashlib.sha256(
                original_data.encode()
            ).hexdigest()

            modified_hash = hashlib.sha256(
                modified_data.encode()
            ).hexdigest()

            st.code("Original Hash: " + original_hash)
            st.code("Verification Hash: " + modified_hash)

            if original_hash == modified_hash:
                st.success("Integrity Check: MATCH")
            else:
                st.error("Integrity Check: MISMATCH — Data Modified")

    with tab2:

        st.markdown("### Reported Security Evaluation")

        security_data = pd.DataFrame({
            "Scenario": [
                "Credential Modification",
                "Hash Tampering",
                "Signature Tampering",
                "Unauthorized Modification"
            ],
            "Detected": [1, 1, 1, 1]
        })

        fig = px.bar(
            security_data,
            x="Scenario",
            y="Detected",
            title="Reported Tampering Detection Scenarios",
            text="Detected"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120",
            yaxis_range=[0, 1.3]
        )

        st.plotly_chart(fig, width="stretch")

        st.success("Reported evaluation: 4/4 predefined scenarios detected")

        st.caption(
            "This visualization reflects reported prototype evaluation, "
            "not a new live security test."
        )

# =========================
# O3 CONSENT
# =========================
elif page == "O3 Consent Access":

    st.subheader("O3 — Consent-Based Credential Access")

    st.markdown(
        "Demonstration of consent-aware access control "
        "and post-revocation access rejection."
    )

    identity = st.text_input("Data Owner Identity")
    requester = st.text_input("Requesting Organization")

    if "consent_status" not in st.session_state:
        st.session_state.consent_status = "NOT GRANTED"

    st.markdown("### Consent Management")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Grant Consent"):
            st.session_state.consent_status = "GRANTED"

    with c2:
        if st.button("Revoke Consent"):
            st.session_state.consent_status = "REVOKED"

    with c3:
        if st.button("Reset Consent"):
            st.session_state.consent_status = "NOT GRANTED"

    st.info(
        "Current Consent Status: "
        + st.session_state.consent_status
    )

    st.divider()

    if st.button("Request Credential Access"):

        if st.session_state.consent_status == "GRANTED":
            st.success("ACCESS ACCEPTED — Consent is granted.")

        else:
            st.error(
                "ACCESS REJECTED — Consent not granted or revoked."
            )

    st.warning(
        "This is a local consent simulator. "
        "No actual chaincode request is executed."
    )

# =========================
# AUDIT & NETWORK
# =========================
elif page == "Audit & Network":

    st.subheader("Audit & Blockchain Information")

    st.markdown("### Network Configuration")

    st.code("""
Channel: mychannel
Organization 1: Org1
Organization 2: Org2
Consensus: Hyperledger Fabric Raft
Chaincode: identity-contract
""")

    st.markdown("### Reported Audit Snapshot")

    audit_data = pd.DataFrame({
        "Event": [
            "Identity Registration",
            "Credential Issuance",
            "Consent Granted",
            "Access Request",
            "Consent Revocation"
        ],
        "Status": [
            "Recorded",
            "Recorded",
            "Recorded",
            "Recorded",
            "Recorded"
        ]
    })

    st.dataframe(
        audit_data,
        width="stretch",
        hide_index=True
    )

    st.warning(
        "Audit rows shown here are illustrative. "
        "Live ledger history will be connected separately."
    )

# FOOTER
# =========================
st.divider()

st.caption(
    "Decentralized Identity Management System | "
    "Hyperledger Fabric | Academic Research Prototype"
)

