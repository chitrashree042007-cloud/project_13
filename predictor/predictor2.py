import streamlit as st
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
.stApp {
    background: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.header {
    background: linear-gradient(135deg, #172b4d, #1e88e5);
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
    color: white;
}

.header h1 {
    font-size: 38px;
    margin: 0;
    font-weight: 800;
}

.header p {
    font-size: 17px;
    margin-top: 8px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.card h3 {
    color: #172b4d;
    margin-top: 0;
}

.score-card {
    background: linear-gradient(135deg, #eaf4ff, #ffffff);
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #cfe5ff;
}

.score-title {
    font-size: 14px;
    font-weight: 700;
    color: #6b7280;
    letter-spacing: 1px;
}

.score {
    font-size: 60px;
    font-weight: 800;
    color: #1e88e5;
    margin: 5px 0;
}

.score-text {
    color: #6b7280;
}

.metric-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #e5e7eb;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}

.metric-title {
    font-size: 13px;
    color: #6b7280;
    font-weight: 700;
}

.metric-value {
    font-size: 27px;
    color: #172b4d;
    font-weight: 800;
    margin-top: 5px;
}

.footer {
    text-align: center;
    color: #9ca3af;
    padding: 25px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

train_hours = [1, 2, 3, 4]
train_scores = [52, 58, 62, 71]

test_hours = [5]
test_scores = [78]


# ============================================================
# LOSS FUNCTION
# ============================================================

def loss(m, c):
    total = 0

    for x, real in zip(train_hours, train_scores):
        guess = m * x + c
        total += (guess - real) ** 2

    return total / len(train_hours)


# ============================================================
# GRADIENT FUNCTION
# ============================================================

def gradients(m, c):
    grad_m = 0
    grad_c = 0

    n = len(train_hours)

    for x, real in zip(train_hours, train_scores):
        error = (m * x + c) - real

        grad_m += 2 * error * x
        grad_c += 2 * error

    return grad_m / n, grad_c / n


# ============================================================
# TRAINING FUNCTION
# ============================================================

def train_model(learning_rate, iterations):

    m = 0
    c = 0

    loss_history = []

    for step in range(iterations):

        gm, gc = gradients(m, c)

        m -= learning_rate * gm
        c -= learning_rate * gc

        loss_history.append(loss(m, c))

    return m, c, loss_history


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Model Settings")

st.sidebar.write(
    "Adjust the parameters used by the Gradient Descent algorithm."
)

learning_rate = st.sidebar.slider(
    "Learning Rate",
    0.001,
    0.05,
    0.01,
    0.001
)

iterations = st.sidebar.slider(
    "Training Iterations",
    100,
    5000,
    1000,
    100
)

st.sidebar.divider()

st.sidebar.subheader("📚 Dataset")

st.sidebar.write("Training samples:", len(train_hours))
st.sidebar.write("Testing samples:", len(test_hours))

st.sidebar.divider()

st.sidebar.info(
    "The model learns the relationship between study hours and exam scores."
)


# ============================================================
# TRAIN MODEL
# ============================================================

m, c, loss_history = train_model(
    learning_rate,
    iterations
)


# ============================================================
# TEST MODEL
# ============================================================

test_prediction = m * test_hours[0] + c

test_error = abs(
    test_prediction - test_scores[0]
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="header">
        <h1>📊 Student Score Predictor</h1>
        <p>Machine Learning Dashboard • Linear Regression • Gradient Descent</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">LEARNING RATE</div>
            <div class="metric-value">{learning_rate}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">ITERATIONS</div>
            <div class="metric-value">{iterations}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">MODEL LOSS</div>
            <div class="metric-value">{loss(m, c):.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">TEST ERROR</div>
            <div class="metric-value">{test_error:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# PREDICTION + MODEL
# ============================================================

left, right = st.columns(2)


# ---------------- PREDICTION ----------------

with left:

    st.markdown(
        """
        <div class="card">
            <h3>🎯 Predict Student Score</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    study_hours = st.number_input(
        "Enter study hours",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5
    )

    prediction = m * study_hours + c

    prediction = max(
        0,
        min(100, prediction)
    )

    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-title">PREDICTED SCORE</div>
            <div class="score">{prediction:.1f}</div>
            <div class="score-text">
                Estimated score for {study_hours:g} hour(s) of study
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- MODEL ----------------

with right:

    st.markdown(
        """
        <div class="card">
            <h3>🤖 Trained Model</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.latex(
        f"y = {m:.2f}x + {c:.2f}"
    )

    st.write(f"**Slope (m):** {m:.4f}")
    st.write(f"**Intercept (c):** {c:.4f}")
    st.write(f"**Training Loss:** {loss(m, c):.4f}")

    st.info(
        "The model uses Gradient Descent to learn the best-fitting line."
    )


# ============================================================
# REGRESSION GRAPH
# ============================================================

st.divider()

st.subheader("📈 Study Hours vs Score")

fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(
    train_hours,
    train_scores,
    s=100,
    label="Training Data"
)

line_x = [0, 6]

line_y = [
    m * x + c
    for x in line_x
]

ax.plot(
    line_x,
    line_y,
    linewidth=2,
    label="Regression Line"
)

ax.scatter(
    test_hours,
    test_scores,
    s=120,
    marker="X",
    label="Test Data"
)

ax.set_xlabel("Study Hours")
ax.set_ylabel("Score")
ax.set_title("Linear Regression Prediction")

ax.set_xlim(0, 6)
ax.set_ylim(0, 100)

ax.grid(alpha=0.25)
ax.legend()

st.pyplot(fig)


# ============================================================
# LOSS GRAPH
# ============================================================

st.divider()

st.subheader("📉 Training Progress")

fig2, ax2 = plt.subplots(figsize=(10, 4))

ax2.plot(
    loss_history,
    linewidth=2
)

ax2.set_xlabel("Training Iteration")
ax2.set_ylabel("Loss")

ax2.set_title(
    "Loss Reduction During Gradient Descent"
)

ax2.grid(alpha=0.25)

st.pyplot(fig2)


# ============================================================
# TEST DATA
# ============================================================

st.divider()

st.subheader("🧪 Model Evaluation")

test_col1, test_col2, test_col3 = st.columns(3)

with test_col1:
    st.metric(
        "Test Hours",
        test_hours[0]
    )

with test_col2:
    st.metric(
        "Actual Score",
        test_scores[0]
    )

with test_col3:
    st.metric(
        "Predicted Score",
        f"{test_prediction:.1f}"
    )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

with st.expander("🧠 How This Machine Learning Project Works"):

    st.markdown("""
    ### 1. Training Data

    The model is trained using:

    | Study Hours | Score |
    |------------:|------:|
    | 1 | 52 |
    | 2 | 58 |
    | 3 | 62 |
    | 4 | 71 |

    ### 2. Linear Regression

    The model learns the equation:

    **y = mx + c**

    where:

    - `x` = study hours
    - `y` = predicted score
    - `m` = slope
    - `c` = intercept

    ### 3. Loss Function

    Mean Squared Error is used to measure the difference
    between predicted and actual scores.

    ### 4. Gradient Descent

    The model repeatedly updates `m` and `c` to reduce the loss.

    ### 5. Testing

    The value of **5 hours** was kept outside the training data
    and is used to test the trained model.

    ### 6. Prediction

    You can enter new study hours above and the trained model
    will estimate the student's score.
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        📊 Student Score Predictor<br>
        Python • Streamlit • Linear Regression • Gradient Descent
    </div>
    """,
    unsafe_allow_html=True
)