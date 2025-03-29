import streamlit as st

# Page Config
st.set_page_config(page_title=" Binary Search Visualizer", layout="centered")
st.title(" Binary Search Visualizer")

# Styled divider
st.markdown("---")

# 📥 User Input Section
st.subheader(" Enter your Data")
input_list = st.text_input(" Enter a sorted list (comma-separated numbers):", "1,3,5,7,9,11,13,15,17,19")
target = st.number_input(" Enter the target number to search:", step=1)

# Convert input list to integers
try:
    num_list = list(map(int, input_list.strip().split(",")))
    num_list.sort()
    st.success(f"✅ Sorted List: {num_list}")
except:
    st.error("❌ Please enter a valid list of numbers!")

# 🔍 Binary Search Function with Detailed Step Info
def binary_search(arr, target):
    steps = []
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        steps.append({
            "low_index": low,
            "low_value": arr[low],
            "high_index": high,
            "high_value": arr[high],
            "mid_index": mid,
            "mid_value": arr[mid]
        })
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps

# 🎯 Search Trigger
if st.button("🚀 Start Binary Search"):
    if len(num_list) == 0:
        st.warning("⚠ List is empty!")
    else:
        index, steps = binary_search(num_list, target)

        # 🧮 Show Steps
        st.subheader("📊 Step-by-Step Search Progress")
        for i, step in enumerate(steps):
            st.markdown(f"""
            🔸 **Step {i+1}:**
            - 🔽 **Low Index:** `{step['low_index']}` ➝ Value: `{step['low_value']}`
            - 🔼 **High Index:** `{step['high_index']}` ➝ Value: `{step['high_value']}`
            - 🎯 **Mid Index:** `{step['mid_index']}` ➝ Value: `{step['mid_value']}`
            """)

        # ✅ Final Result
        st.markdown("---")
        st.subheader("📍 Final Result")
        if index != -1:
            st.success(f"🎯 Target **{target}** found at **Index {index}**, Value: `{num_list[index]}`")
        else:
            st.error(f"❌ Target **{target}** not found in the list.")

