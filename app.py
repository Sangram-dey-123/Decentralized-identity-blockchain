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

    passed = 0
    total = len(tests)

    if "Status" in tests.columns:
        status_values = tests["Status"].astype(str).str.strip().str.upper()

        passed = status_values.isin(
            ["PASS", "PASSED", "TRUE", "SUCCESS", "SUCCESSFUL"]
        ).sum()

    elif "Result" in tests.columns:
        result_values = tests["Result"].astype(str).str.strip().str.upper()

        passed = result_values.isin(
            ["PASS", "PASSED", "TRUE", "SUCCESS", "SUCCESSFUL"]
        ).sum()

    if total > 0:
        success_rate = (passed / total) * 100

        st.metric(
            "System Test Success Rate",
            f"{success_rate:.2f}%"
        )

        st.write(
            f"**Tests Passed:** {passed}/{total}"
        )

        if success_rate == 100:
            st.success(
                f"🎉 All {total} system tests passed successfully!"
            )
        else:
            st.warning(
                f"{passed} out of {total} tests passed."
            )
