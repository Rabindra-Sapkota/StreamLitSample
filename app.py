import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
tips = sns.load_dataset("tips")

st.title("💰 Interactive Tips Dashboard")
st.markdown("Filtered by Gender and Smoker; visualizations use numeric columns only.")

# Sidebar filters
st.sidebar.header("Filter Options")
gender_filter = st.sidebar.multiselect(
    "Select Gender", options=tips["sex"].unique(), default=tips["sex"].unique()
)
smoker_filter = st.sidebar.multiselect(
    "Select Smoker?", options=tips["smoker"].unique(), default=tips["smoker"].unique()
)

# Filter dataset
filtered_data = tips[
    (tips["sex"].isin(gender_filter)) & (tips["smoker"].isin(smoker_filter))
]

# Show filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Scatter Plot: total_bill vs tip
st.subheader("Scatter Plot: Total Bill vs Tip")
fig1, ax1 = plt.subplots()
for gender in filtered_data["sex"].unique():
    subset = filtered_data[filtered_data["sex"] == gender]
    ax1.scatter(subset["total_bill"], subset["tip"], label=gender, alpha=0.7)
ax1.set_xlabel("Total Bill")
ax1.set_ylabel("Tip")
ax1.set_title("Total Bill vs Tip by Gender")
ax1.legend()
st.pyplot(fig1)

# Histogram: tip
st.subheader("Histogram: Tip")
fig2, ax2 = plt.subplots()
for gender in filtered_data["sex"].unique():
    subset = filtered_data[filtered_data["sex"] == gender]
    ax2.hist(subset["tip"], alpha=0.5, label=gender, bins=10)
ax2.set_xlabel("Tip")
ax2.set_ylabel("Count")
ax2.set_title("Tip Distribution by Gender")
ax2.legend()
st.pyplot(fig2)

# Boxplot: total_bill by smoker
st.subheader("Boxplot: Total Bill by Smoker")
fig3, ax3 = plt.subplots()
data_to_plot = [
    filtered_data[filtered_data["smoker"] == s]["total_bill"]
    for s in filtered_data["smoker"].unique()
]
ax3.boxplot(data_to_plot, tick_labels=filtered_data["smoker"].unique())
ax3.set_ylabel("Total Bill")
ax3.set_title("Total Bill by Smoker")
st.pyplot(fig3)

# Correlation Heatmap (numeric only)
st.subheader("Correlation Heatmap")
numeric_cols = filtered_data.select_dtypes(include="number").columns
fig4, ax4 = plt.subplots()
cax = ax4.matshow(filtered_data[numeric_cols].corr(), cmap=plt.get_cmap("coolwarm"))
fig4.colorbar(cax)
ax4.set_xticks(range(len(numeric_cols)))
ax4.set_yticks(range(len(numeric_cols)))
ax4.set_xticklabels(numeric_cols, rotation=90)
ax4.set_yticklabels(numeric_cols)
ax4.set_title("Correlation Matrix", pad=20)
st.pyplot(fig4)
