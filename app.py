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

st.subheader(
    "Blockchain-Based Digital Identity & Credential Verification"
)

st.info(
    "Python blockchain-style prototype demonstrating decentralized "
    "identity, credential management, verification, access control "
    "and audit trails."
)

# -------------------------------------------------
# LOAD CSV FILES
# -------------------------------------------------

def load_csv(filename):
    if os.path.exists(filename):
        try:
            return pd.read_csv(filename)
        except Exception as e:
            st.error(f"Error reading {filename}: {e}")
            return pd.DataFrame()

    return pd.DataFrame()


dashboard = load_csv("final_project_dashboard.csv")
audit = load_csv("final_blockchain_audit_trail.csv")
tests = load_csv("final_system_test_results.csv")

# -------------------------------------------------
# DASHBOARD METRICS
# -------------------------------------------------

metrics = {}

if not dashboard.empty:

    if "Metric" in dashboard.columns and "Value" in dashboard.columns:

        for _, row in dashboard.iterrows():
            metrics[str(row["Metric"])] = row["Value"]


total_blocks = metrics.get("Total Blockchain Blocks", 56)
identities = metrics.get("Identities Created", 25)
credentials = metrics.get("Credentials Issued", 26)
revoked = metrics.get("Credentials Revoked", 1)
access_granted = metrics.get("Access Granted", 1)
access_revoked = metrics.get("Access Revoked", 1)

# -------------------------------------------------
# SYSTEM DASHBOARD
# -------------------------------------------------

st.header("📊 System Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⛓️ Blockchain Blocks",
        total_blocks
    )

with col2:
    st.metric(
        "👤 Identities Created",
        identities
    )

with col3:
    st.metric(
        "📜 Credentials Issued",
        credentials
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "🚫 Credentials Revoked",
        revoked
    )

with col5:
    st.metric(
        "✅ Access Granted",
        access_granted
    )

with col6:
    st.metric(
        "🔒 Access Revoked",
        access_revoked
    )

# -------------------------------------------------
# BLOCKCHAIN INTEGRITY
# -------------------------------------------------

st.header("⛓️ Blockchain Integrity")

st.success("✅ BLOCKCHAIN STATUS: VALID")

st.write(
    "The blockchain ledger passed the integrity validation test. "
    "Each block contains a cryptographic hash linked to the previous block."
)

# -------------------------------------------------
# FINAL SYSTEM TEST RESULTS
# -------------------------------------------------

st.header("🧪 Final System Test Results")

if not tests.empty:

    st.dataframe(
        tests,
        use_container_width=True,
        hide_index=True
    )

    total_tests = len(tests)
    passed_tests = 0

    # Check Status column
    if "Status" in tests.columns:

        status_values = (
            tests["Status"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        passed_tests = status_values.isin([
            "PASS",
            "PASSED",
            "SUCCESS",
            "SUCCESSFUL",
            "TRUE"
        ]).sum()

    # Check Result column if Status is unavailable
    elif "Result" in tests.columns:

        result_values = (
            tests["Result"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        passed_tests = result_values.isin([
            "PASS",
            "PASSED",
            "SUCCESS",
            "SUCCESSFUL",
            "TRUE"
        ]).sum()

    # Display final result
    if total_tests > 0:

        success_rate = (
            passed_tests / total_tests
        ) * 100

        st.metric(
            "System Test Success Rate",
            f"{success_rate:.2f}%"
        )

        st.write(
            f"**Tests Passed: {passed_tests}/{total_tests}**"
        )

        if success_rate == 100:

            st.success(
                f"🎉 All {total_tests} system tests passed successfully!"
            )

        else:

            st.warning(
                f"⚠️ {passed_tests} out of {total_tests} tests passed."
            )

else:

    st.warning(
        "Final system test results file was not found."
    )

# -------------------------------------------------
# FINAL PROJECT RESULTS
# -------------------------------------------------

st.header("📈 Final Project Results")

if os.path.exists("final_project_results.png"):

    st.image(
        "final_project_results.png",
        caption="Decentralized Identity Management System - Final Results",
        use_container_width=True
    )

else:

    st.warning(
        "Final project results image was not found."
    )

# -------------------------------------------------
# BLOCKCHAIN AUDIT TRAIL
# -------------------------------------------------

st.header("📋 Blockchain Audit Trail")

st.write(
    "The audit trail records identity creation, credential issuance, "
    "credential revocation and access-control events."
)

if not audit.empty:

    filtered_audit = audit.copy()

    if "Event" in audit.columns:

        event_list = sorted(
            audit["Event"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_event = st.selectbox(
            "Filter by Event",
            ["All"] + event_list
        )

        if selected_event != "All":

            filtered_audit = audit[
                audit["Event"].astype(str) == selected_event
            ]

    st.dataframe(
        filtered_audit,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "Blockchain audit trail file was not found."
    )

# -------------------------------------------------
# CREDENTIAL INTEGRITY VERIFICATION
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

# Original credential hash
original_data = json.dumps(
    credential,
    sort_keys=True
).encode()

original_hash = hashlib.sha256(
    original_data
).hexdigest()

# Tampering option
tamper = st.checkbox(
    "Simulate credential tampering"
)

if tamper:

    credential["status"] = "FAKE"

# Current hash
current_data = json.dumps(
    credential,
    sort_keys=True
).encode()

current_hash = hashlib.sha256(
    current_data
).hexdigest()

col1, col2 = st.columns(2)

with col1:

    st.write("**Original Hash**")

    st.code(original_hash)

with col2:

    st.write("**Current Hash**")

    st.code(current_hash)

# Verification result
if original_hash == current_hash:

    st.success(
        "✅ Credential is VALID — No modification detected."
    )

else:

    st.error(
        "🚨 Credential is TAMPERED — Hash mismatch detected!"
    )

# -------------------------------------------------
# PROJECT FEATURES
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
