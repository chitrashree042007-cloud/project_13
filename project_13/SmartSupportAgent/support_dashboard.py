import streamlit as st
from datetime import datetime

from ticket_brain import (
    analyze_ticket,
    calculate_risk,
    get_risk_label
)

from reply_writer import generate_response


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Support Command Center",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "ticket" not in st.session_state:
    st.session_state.ticket = None

if "draft" not in st.session_state:
    st.session_state.draft = ""

if "approved" not in st.session_state:
    st.session_state.approved = False

if "ticket_count" not in st.session_state:
    st.session_state.ticket_count = 0

if "current_email" not in st.session_state:
    st.session_state.current_email = ""


# ============================================================
# TEST TICKETS
# ============================================================

TEST_TICKETS = {

    "💳 Unauthorized Charge":
        """I noticed an unauthorized charge of $499 on my
credit card this morning from your platform. Cancel this
immediately and refund my money before I contact my bank!""",

    "🔐 Account Security Alert":
        """I received an email stating my two-factor
authentication device was reset, but I did not request this.
I think someone accessed my account.""",

    "🔧 Production API Failure":
        """Our production REST API webhook returns HTTP 500
errors on every POST request since 8 AM. Our mobile app
checkout is completely broken.""",

    "🌙 Dark Mode Question":
        """Hi team, do you have a dark mode option available
on the iOS app? Thanks!"""
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Control Center")

    st.subheader("🔄 Support Workflow")

    st.write("📥 **Receive Ticket**")
    st.write("↓")
    st.write("🧠 **Analyze**")
    st.write("↓")
    st.write("🧭 **Route**")
    st.write("↓")
    st.write("🚦 **Set Priority**")
    st.write("↓")
    st.write("⏱️ **Calculate SLA**")
    st.write("↓")
    st.write("✉️ **Draft Response**")
    st.write("↓")
    st.write("👤 **Human Approval**")
    st.write("↓")
    st.write("✅ **Simulated Send**")

    st.divider()

    st.metric(
        "🎫 Tickets Processed",
        st.session_state.ticket_count
    )

    if st.session_state.ticket:

        st.metric(
            "⏱️ Current SLA",
            f"{st.session_state.ticket['sla_response_hours']} hrs"
        )

    st.divider()

    if st.button(
        "🧹 Reset Workspace",
        use_container_width=True
    ):

        st.session_state.ticket = None
        st.session_state.draft = ""
        st.session_state.approved = False
        st.session_state.current_email = ""

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🎧 Smart Support Command Center")

st.caption(
    "Autonomous Customer Support • "
    "Intelligent Triage • "
    "Smart Routing • "
    "Response Automation"
)

st.divider()


# ============================================================
# CUSTOMER TICKET SECTION
# ============================================================

st.header("📥 Customer Ticket")

input_col, smart_col = st.columns(
    [2.2, 1],
    gap="large"
)


# ============================================================
# TICKET INPUT
# ============================================================

with input_col:

    selected_ticket = st.selectbox(
        "Choose a test ticket",
        ["Custom Ticket"] + list(TEST_TICKETS.keys())
    )

    if selected_ticket == "Custom Ticket":
        starting_text = ""
    else:
        starting_text = TEST_TICKETS[selected_ticket]

    customer_email = st.text_area(
        "Customer Email / Inquiry",
        value=starting_text,
        height=200,
        placeholder=(
            "Paste a customer email or support request here..."
        )
    )


# ============================================================
# SMART TRIAGE CARD
# ============================================================

with smart_col:

    with st.container(border=True):

        st.subheader("🧠 Smart Triage Engine")

        st.write(
            "The intelligent engine automatically analyzes "
            "the customer request and detects:"
        )

        st.write("🏢 Department")
        st.write("🚦 Priority")
        st.write("😊 Customer Sentiment")
        st.write("⏱️ SLA Target")
        st.write("📊 Risk Score")
        st.write("🧭 Routing Reason")

        st.write("")

        analyze_button = st.button(
            "🚀 Analyze & Route",
            type="primary",
            use_container_width=True
        )


# ============================================================
# ANALYZE BUTTON
# ============================================================

if analyze_button:

    if not customer_email.strip():

        st.error(
            "⚠️ Please enter a customer inquiry first."
        )

    else:

        with st.spinner(
            "🧠 Analyzing ticket..."
        ):

            try:

                st.session_state.current_email = customer_email

                # --------------------------------------------
                # ANALYZE
                # --------------------------------------------

                ticket = analyze_ticket(
                    customer_email
                )

                # --------------------------------------------
                # CALCULATE RISK
                # --------------------------------------------

                risk = calculate_risk(
                    ticket
                )

                # --------------------------------------------
                # GENERATE RESPONSE
                # --------------------------------------------

                draft = generate_response(
                    customer_email,
                    ticket
                )

                # --------------------------------------------
                # ADD EXTRA INFORMATION
                # --------------------------------------------

                ticket["risk_score"] = risk

                ticket["urgency_label"] = get_risk_label(
                    risk
                )

                ticket["created_at"] = (
                    datetime.now().strftime(
                        "%d %b %Y • %I:%M %p"
                    )
                )

                # --------------------------------------------
                # SAVE
                # --------------------------------------------

                st.session_state.ticket = ticket

                st.session_state.draft = draft

                st.session_state.approved = False

                st.session_state.ticket_count += 1

                st.success(
                    "🎯 Ticket analyzed and routed successfully!"
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while analyzing "
                    "the ticket."
                )

                st.exception(e)


# ============================================================
# RESULTS
# ============================================================

if st.session_state.ticket:

    ticket = st.session_state.ticket

    st.divider()

    st.header("🧭 Intelligent Triage Result")


    # ========================================================
    # MAIN METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏢 Department",
            ticket.get(
                "department",
                "Unknown"
            )
        )

    with col2:

        st.metric(
            "🚦 Priority",
            ticket.get(
                "priority",
                "Unknown"
            )
        )

    with col3:

        st.metric(
            "😊 Sentiment",
            ticket.get(
                "sentiment",
                "Unknown"
            )
        )

    with col4:

        st.metric(
            "⏱️ SLA",
            f"{ticket.get('sla_response_hours', 'N/A')} hrs"
        )


    # ========================================================
    # STATUS
    # ========================================================

    st.subheader("📌 Ticket Status")

    priority = str(
        ticket.get(
            "priority",
            "Unknown"
        )
    ).upper()

    if priority == "CRITICAL":

        st.error(
            "🔴 CRITICAL PRIORITY"
        )

    elif priority == "HIGH":

        st.warning(
            "🟠 HIGH PRIORITY"
        )

    elif priority == "MEDIUM":

        st.info(
            "🟡 MEDIUM PRIORITY"
        )

    else:

        st.success(
            "🟢 LOW PRIORITY"
        )


    # ========================================================
    # RISK ANALYSIS
    # ========================================================

    st.divider()

    risk_col, reason_col = st.columns(
        [1, 2],
        gap="large"
    )

    with risk_col:

        st.subheader("📊 Risk Analysis")

        risk_score = ticket.get(
            "risk_score",
            0
        )

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

        st.progress(
            min(
                max(
                    int(risk_score),
                    0
                ),
                100
            )
        )

        urgency = ticket.get(
            "urgency_label",
            "Unknown"
        )

        if risk_score >= 80:

            st.error(
                f"🔴 {urgency}"
            )

        elif risk_score >= 60:

            st.warning(
                f"🟠 {urgency}"
            )

        elif risk_score >= 35:

            st.info(
                f"🟡 {urgency}"
            )

        else:

            st.success(
                f"🟢 {urgency}"
            )


    # ========================================================
    # ROUTING REASON
    # ========================================================

    with reason_col:

        st.subheader(
            "🧠 Why Was This Ticket Routed?"
        )

        reasoning = ticket.get(
            "reasoning",
            "No routing explanation available."
        )

        st.info(reasoning)


    # ========================================================
    # WORKFLOW STATUS
    # ========================================================

    st.divider()

    st.header("🔄 Workflow Status")

    step1, step2, step3, step4, step5 = st.columns(5)

    with step1:
        st.success("📥 Received")

    with step2:
        st.success("🧠 Classified")

    with step3:
        st.success("🧭 Routed")

    with step4:
        st.success("✉️ Drafted")

    with step5:

        if st.session_state.approved:
            st.success("✅ Approved")
        else:
            st.warning("⏳ Waiting")


    # ========================================================
    # RESPONSE DRAFT
    # ========================================================

    st.divider()

    st.header("✉️ Customer Response Draft")

    st.caption(
        "Review and edit the response before approval."
    )

    edited_response = st.text_area(
        "Editable Response",
        value=st.session_state.draft,
        height=320,
        key="editable_response"
    )

    st.session_state.draft = edited_response


    # ========================================================
    # ACTION BUTTONS
    # ========================================================

    approve_col, regenerate_col = st.columns(2)


    # ========================================================
    # APPROVE
    # ========================================================

    with approve_col:

        if st.button(
            "✅ Approve & Send",
            type="primary",
            use_container_width=True
        ):

            st.session_state.approved = True

            st.success(
                "✅ Response approved and sent successfully "
                "(simulation)."
            )

            st.balloons()


    # ========================================================
    # REGENERATE
    # ========================================================

    with regenerate_col:

        if st.button(
            "🔄 Regenerate Response",
            use_container_width=True
        ):

            with st.spinner(
                "✍️ Generating a new response..."
            ):

                try:

                    st.session_state.draft = (
                        generate_response(
                            st.session_state.current_email,
                            ticket
                        )
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "❌ Could not regenerate the response."
                    )

                    st.exception(e)


    # ========================================================
    # COMPLETE INTELLIGENCE
    # ========================================================

    st.divider()

    with st.expander(
        "🔍 View Complete Ticket Intelligence"
    ):

        st.json(
            {
                "department":
                    ticket.get("department"),

                "priority":
                    ticket.get("priority"),

                "sentiment":
                    ticket.get("sentiment"),

                "sla_response_hours":
                    ticket.get("sla_response_hours"),

                "risk_score":
                    ticket.get("risk_score"),

                "urgency_label":
                    ticket.get("urgency_label"),

                "reasoning":
                    ticket.get("reasoning"),

                "created_at":
                    ticket.get("created_at")
            }
        )


# ============================================================
# WELCOME SCREEN
# ============================================================

else:

    st.info(
        "👋 Welcome! Choose a test ticket or enter your "
        "own customer inquiry above, then click "
        "**🚀 Analyze & Route**."
    )

    st.subheader("✨ What this system does")

    welcome1, welcome2, welcome3 = st.columns(3)

    with welcome1:

        st.write("🧠 **Intelligent Analysis**")

        st.caption(
            "Understands the customer's request and "
            "identifies the appropriate support category."
        )

    with welcome2:

        st.write("🚦 **Smart Routing**")

        st.caption(
            "Determines priority, department, SLA and "
            "risk level."
        )

    with welcome3:

        st.write("✉️ **Response Automation**")

        st.caption(
            "Creates a professional customer response "
            "that can be reviewed before sending."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎧 Smart Support Command Center • "
    "Autonomous Customer Support & Ticket Routing"
)