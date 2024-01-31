import yaml
import tiktoken
import streamlit as st

from utils import calculate_vision_token_cost


st.set_page_config(
    page_title="OpenAI API Pricing Calculator",
    page_icon="💡",
    initial_sidebar_state="expanded",
)

# Load model attributes from YAML file
with open("config.yaml", "r") as file:
    models_data = yaml.safe_load(file)

# Sidebar for selecting model type
model_type = st.sidebar.selectbox("Select Type", ["Language Models"])

# Get the selected models based on the type
model_classes = models_data.get(model_type, [])

# Sidebar for selecting specific model
selected_model_class = st.sidebar.selectbox(
    "Select Model Class", [model_class["name"] for model_class in model_classes]
)
select_model_class_idx = next(
    i
    for i, model_class in enumerate(model_classes)
    if model_class["name"] == selected_model_class
)

models = model_classes[select_model_class_idx]["models"]
selected_model = st.sidebar.selectbox(
    "Select Model", [model["name"] for model in models]
)


# finding relevant model from model class
idx = next(i for i, model in enumerate(models) if model["name"] == selected_model)

# for vision models different pricing exists
if selected_model == "gpt-4-1106-vision-preview":
    vision_dict = models[idx].get("vision", {})
    if vision_dict:
        resolution = st.sidebar.selectbox("Select Resolution", vision_dict.keys())

        width = st.sidebar.number_input("Width", min_value=0, value=512, step=1)
        height = st.sidebar.number_input("Height", min_value=0, value=512, step=1)

        number_of_images = st.sidebar.number_input(
            "Number of images", min_value=0, step=1
        )

        image_token_count = (
            calculate_vision_token_cost(width, height, detail=resolution)
            * number_of_images
        )
        st.sidebar.markdown(
            f"Number of tokens for {number_of_images} images: **{image_token_count}**"
        )

# Display input cost per {per_token} for the selected model in the sidebar
per_token = models[idx].get("per_token", 1)
input_cost_per_token = models[idx].get("input_cost", "NA")
st.sidebar.markdown(
    f"""
    Input Cost per {per_token} tokens:   
    **${input_cost_per_token}** for **{selected_model}**
    """
)

# Main content
st.title("Prompt To Price")

# Textbox for user input
text_container = st.container()
user_input = text_container.text_area("Enter your text:", key="input", height=200)

col1, col2, *cols = st.columns(8)

pricing_button = col1.button("Pricing")
if pricing_button or user_input:
    with st.spinner():
        if selected_model.startswith("text-embedding"):
            encoding = tiktoken.get_encoding("cl100k_base")
        else:
            encoding = tiktoken.encoding_for_model(selected_model)

        token_count = len(encoding.encode(user_input))

        # Calculate total cost
        if selected_model == "gpt-4-1106-vision-preview":
            total_cost = (
                (token_count + image_token_count) * input_cost_per_token / per_token
            )
            st.info(
                "Checkout https://platform.openai.com/docs/guides/vision/calculating-costs for more details"
            )
        else:
            total_cost = token_count * input_cost_per_token / per_token

        # Display total cost
        result_container = st.container(border=True)
        if user_input:
            if selected_model == "gpt-4-1106-vision-preview":
                result_container.markdown(
                    f"""
                    Number of characters: {len(user_input)}  
                    Number of Text Tokens: {token_count}  
                    Number of Images Tokens: {image_token_count}  
                    Total Cost: ${total_cost:.7f}
                """
                )
            else:
                result_container.markdown(
                    f"""
                    Number of characters: {len(user_input)}  
                    Number of Tokens: {token_count}  
                    Total Cost: ${total_cost:.7f}
                """
                )


# Clear button to reset the text area
def clear_text():
    st.session_state["input"] = ""


col2.button("Clear", on_click=clear_text)
