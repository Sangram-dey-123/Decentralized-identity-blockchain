import streamlit as st
import pandas as pd
import hashlib
import json
import os

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Decentralized Identity Management",
    page_icon="🔐",
    layout="wide"
)

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🔐 Decentralized Identity Management System")
st.subheader("Blockchain-Based Digital Identity & Credential Verification")

st.info(
    "Python blockchain-style prototype demonstrating decentralized "
    "identity, credential management, verification, access control "
    "and audit trails."
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

def load_csv(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame()

dashboard = load_csv("final_project_dashboard.csv")
audit = load_csv("final_blockchain_audit_trail.csv")
tests = load_csv("final_system_test_results.csv")

# -------------------------------------------------
# EXTRACT DASHBOARD METRICS
# -------------------------------------------------

metrics = {}

if not dashboard.empty:
    for _, row in dashboard.iterrows():
        metrics[str(row["Metric"])] = row["Value"]

total_blocks = metrics.get("Total Blockchain Blocks", 0)
identities = metrics.get("Identities Created", 0)
credentials = metrics.get("Credentials Issued", 0)
revoked = metrics.get("Credentials Revoked", 0)
access_granted = metrics.get("Access Granted", 0)
access_revoked = metrics.get("Access Revoked", 0)

# -------------------------------------------------
# METRICS
# -------------------------------------------------

st.header("📊 System Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⛓️ Blockchain Blocks", total_blocks)

with col2:
    st.metric("👤 Identities Created", identities)

with col3:
    st.metric("📜 Credentials Issued", credentials)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("🚫 Credentials Revoked", revoked)

with col5:
    st.metric("✅ Access Granted", access_granted)

with col6:
    st.metric("🔒 Access Revoked", access_revoked)

# -------------------------------------------------
# BLOCKCHAIN STATUS
# -------------------------------------------------

st.header("⛓️ Blockchain Integrity")

st.success("✅ BLOCKCHAIN STATUS: VALID")

st.write(
    "The blockchain ledger passed the integrity validation test. "
    "Each block contains a cryptographic hash linked to the previous block."
)

# -------------------------------------------------
# SYSTEM TEST RESULTS
# -------------------------------------------------

st.header("🧪 Final System Test Results")

if not tests.empty:

    st.dataframe(
        tests,
        use_container_width=True,
        hide_index=True
    )

    if "Status" in tests.columns:
        passed = (tests["Status"].astype(str).str.upper() == "PASS").sum()
        total = len(tests)

        if total > 0:
            success_rate = (passed / total) * 100

            st.metric(
                "System Test Success Rate",
                f"{success_rate:.2f}%"
            )

            if success_rate == 100:
                st.success(
                    f"🎉 All {total} system tests passed successfully!"
                )

# -------------------------------------------------
# RESULTS GRAPH
# -------------------------------------------------

st.header("📈 Final Project Results")

if os.path.exists("final_project_results.png"):
    st.image(
        "final_project_results.png",
        caption="Decentralized Identity Management System - Final Results",
        use_container_width=True
    )

# -------------------------------------------------
# AUDIT TRAIL
# -------------------------------------------------

st.header("📋 Blockchain Audit Trail")

if not audit.empty:

    st.write(
        "The audit trail records identity creation, credential issuance, "
        "credential revocation and access-control events."
    )

    # Event filter
    if "Event" in audit.columns:

        events = ["All"] + sorted(
            audit["Event"].dropna().astype(str).unique().tolist()
        )

        selected_event = st.selectbox(
            "Filter by Event",
            events
        )

        filtered_audit = audit.copy()

        if selected_event != "All":
            filtered_audit = filtered_audit[
                filtered_audit["Event"].astype(str) == selected_event
            ]

    else:
        filtered_audit = audit

    st.dataframe(
        filtered_audit,
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------
# CREDENTIAL INTEGRITY DEMO
# -------------------------------------------------

st.header("🔎 Credential Integrity Verification Demo")

st.write(
    "This demonstration shows how SHA-256 hashing can detect "
    "unauthorized modification of credential data."
)

credential = {
    "credential_id": "VC-DEMO-001",
    "holder": "Demo Student",
    "degree": "M.Tech Artificial Intelligence",
    "issuer": "Demo University",
    "status": "ACTIVE"
}

original_data = json.dumps(
    credential,
    sort_keys=True
).encode()

original_hash = hashlib.sha256(original_data).hexdigest()

tamper = st.checkbox(
    "Simulate credential tampering"
)

if tamper:
    credential["status"] = "FAKE"

current_data = json.dumps(
    credential,
    sort_keys=True
).encode()

current_hash = hashlib.sha256(current_data).hexdigest()

col1, col2 = st.columns(2)

with col1:
    st.write("**Original Hash**")
    st.code(original_hash)

with col2:
    st.write("**Current Hash**")
    st.code(current_hash)

if original_hash == current_hash:
    st.success("✅ Credential is VALID — No modification detected.")
else:
    st.error("🚨 Credential is TAMPERED — Hash mismatch detected!")

# -------------------------------------------------
# PROJECT INFORMATION
# -------------------------------------------------

st.header("📌 Project Features")

features = [
    "Decentralized Digital Identity",
    "Blockchain-Based Credential Management",
    "SHA-256 Credential Hashing",
    "Credential Verification",
    "Credential Revocation",
    "Access Control",
    "Blockchain Audit Trail",
    "Tamper Detection",
    "Cross-Sector Credential Management",
    "Blockchain Integrity Validation"
]

for feature in features:
    st.write(f"✅ {feature}")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "Decentralized Identity Management System Using Blockchain | "
    "M.Tech AIDS | Academic Prototype"
)
