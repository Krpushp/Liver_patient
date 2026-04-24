import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Liver Data Dashboard", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>Liver Patient Data Visualization Dashboard</h1>",
    unsafe_allow_html=True
)

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv(
    r"C:\Users\Pushp\OneDrive\Office\Analysis\Cleaning\liver_patient_dataset.csv"
)

st.markdown(
"""
### 📊 Dataset Preview

This section provides a quick overview of the dataset used for liver disease analysis.  
It displays the first few records to help understand the structure, features, and type of data available.

The dataset contains important medical attributes such as age, gender, and various blood test parameters 
including bilirubin levels, liver enzymes, and protein measures.
"""
)
st.dataframe(df.head())

st.divider()
st.markdown(
"""
### Summary Statistics

This section presents a statistical overview of key numerical features in the dataset.  
It helps in understanding the distribution, central tendency, and variability of medical parameters.
"""
)

st.title(" Summary Tables")

cols = ["Age", "TB", "DB", "Alkphos", "Sgpt", "Sgot", "TP", "ALB"]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=cols)

# ==========================
# FUNCTION: SUMMARY TABLE
# ==========================
def summary_table(column):
    return pd.DataFrame({
        "Mean": [round(df[column].mean(), 2)],
        "Median": [round(df[column].median(), 2)],
        "Std": [round(df[column].std(), 2)],
        "Q1 (25%)": [round(df[column].quantile(0.25), 2)],
        "Q3 (75%)": [round(df[column].quantile(0.75), 2)],
        "Min": [round(df[column].min(), 2)],
        "Max": [round(df[column].max(), 2)]
    })

# ==========================
# DISPLAY USING COLUMNS
# ==========================
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Age")
    st.dataframe(summary_table("Age"))

with col2:
    st.subheader("Total Bilirubin")
    st.dataframe(summary_table("TB"))

with col3:
    st.subheader("Direct Bilirubin")
    st.dataframe(summary_table("DB"))

col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("Alkaline Phosphotase")
    st.dataframe(summary_table("Alkphos"))

with col5:
    st.subheader("SGPT(Alamine Aminotransferase)")
    st.dataframe(summary_table("Sgpt"))

with col6:
    st.subheader("SGOT(Aspartate Aminotransferase)")
    st.dataframe(summary_table("Sgot"))

col7, col8 = st.columns(2)

with col7:
    st.subheader("Total Proteins")
    st.dataframe(summary_table("TP"))

with col8:
    st.subheader("ALB(Albumin)")
    st.dataframe(summary_table("ALB"))

st.divider()
st.markdown(
"""
### 🧪 Data Distribution by Disease

This section analyzes how different features vary between patients with and without liver disease.The dataset is grouped based on the target variable (disease status), allowing direct comparison of medical parameters.
"""
)
st.title(" Data by Disease")

cols = ["Age", "TB", "Sgpt", "ALB"]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=cols)

# ==========================
# SMALL PLOT FUNCTION
# ==========================
def small_plot(x, y="Selector", kind="box"):
    fig, ax = plt.subplots(figsize=(4,3))  # 👈 small size

    if kind == "box":
        sns.boxplot(x=y, y=x, data=df, palette="Set2", ax=ax)
    elif kind == "violin":
        sns.violinplot(x=y, y=x, data=df, palette="Set2", ax=ax)
    elif kind == "count":
        sns.countplot(x=x, hue=y, data=df, palette="Set2", ax=ax)

    ax.set_title(f"{x} vs Disease", fontsize=10)
    ax.tick_params(labelsize=8)

    return fig

# ==========================
# ROW 1
# ==========================
col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(small_plot("Age"))

with col2:
    st.pyplot(small_plot("Gender", kind="count"))

with col3:
    st.pyplot(small_plot("ALB"))
st.divider()

st.markdown("<h3 style='text-align: center;'>Pairplot Analysis</h3>", unsafe_allow_html=True)
pair_fig = sns.pairplot(
    df[["TB", "DB", "Sgpt", "ALB", "Selector"]],
    hue="Selector",
    palette="Set2"
)

st.pyplot(pair_fig)

##### Inflyence

st.divider()
st.markdown(
    "<h3 style='text-align: center;'>🩸 TB + DB + SGPT Analysis</h3>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# ==========================
# LEFT PLOT (your original)
# ==========================
with col1:
    fig1, ax1 = plt.subplots(figsize=(4,3))  # 👈 smaller size

    sns.scatterplot(
        data=df,
        x="TB",
        y="DB",
        hue="Sgpt",
        size="Sgpt",
        sizes=(20, 200),
        palette="viridis",
        ax=ax1
    )

    ax1.set_title("TB vs DB (SGPT influence)", fontsize=9)
    ax1.tick_params(labelsize=8)

    st.pyplot(fig1)

# ==========================
# RIGHT PLOT (new)
# ==========================
with col2:
    fig2, ax2 = plt.subplots(figsize=(4,3))

    sns.scatterplot(
        data=df,
        x="TB",
        y="Sgpt",
        hue="Selector",   # disease grouping
        palette="Set2",
        ax=ax2
    )

    ax2.set_title("TB vs SGPT (by Disease)", fontsize=9)
    ax2.tick_params(labelsize=8)

    st.pyplot(fig2)



st.divider()

st.title(" Visualization of the dataset")
# ==============================
# STYLE
# ==============================
plt.style.use('ggplot')
sns.set_palette("Set2")

numeric_cols = ['Age', 'TB', 'DB', 'Alkphos', 'Sgpt', 'Sgot', 'TP', 'ALB', 'A/G Ratio']

# ==============================
# CREATE FIGURE
# ==============================
fig, axes = plt.subplots(3, 3, figsize=(18, 15))
#fig.suptitle("Complete Data Visualization Dashboard", fontsize=18)

# 1 Target Distribution
sns.countplot(x='Selector', data=df, palette=['#FF6B6B', '#4ECDC4'], ax=axes[0,0])
axes[0,0].set_title("Target Distribution")

# 2 Gender Distribution
sns.countplot(x='Gender', data=df, palette=['#FFD93D', '#6BCB77'], ax=axes[0,1])
axes[0,1].set_title("Gender Distribution")

# 3 Age Histogram
sns.histplot(df['Age'], bins=20, color='#5DADE2', ax=axes[0,2])
axes[0,2].set_title("Age Histogram")

# 4 TB vs DB
sns.scatterplot(x='TB', y='DB', hue='Selector', data=df,
                palette=['#FF6B6B', '#1A535C'], ax=axes[1,0])
axes[1,0].set_title("TB vs DB")

# 5 Boxplot
sns.boxplot(data=df[numeric_cols], palette='Set3', ax=axes[1,1])
axes[1,1].set_title("Boxplot")
axes[1,1].tick_params(axis='x', rotation=45)

# 6 Correlation Heatmap
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=axes[1,2])
axes[1,2].set_title("Correlation Heatmap")

# 7 KDE Plot
sns.kdeplot(df['Age'], fill=True, color='#FF6B6B', label='Age', ax=axes[2,0])
sns.kdeplot(df['TB'], fill=True, color='#4ECDC4', label='TB', ax=axes[2,0])
axes[2,0].legend()
axes[2,0].set_title("Density Plot")

# 8 Violin Plot
sns.violinplot(x='Selector', y='Age', data=df,
               palette=['#FFB6B9', '#6A0572'], ax=axes[2,1])
axes[2,1].set_title("Age vs Target")

# 9 Mean Feature Comparison
df.groupby('Selector')[numeric_cols].mean().T.plot(
    kind='bar',
    colormap='viridis',
    ax=axes[2,2]
)
axes[2,2].set_title("Mean Features")

# ==============================
# FINAL RENDER IN STREAMLIT
# ==============================
plt.tight_layout()

st.pyplot(fig)