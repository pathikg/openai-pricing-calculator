# OpenAI API Pricing Calculator

## Overview

This tool is designed to help users estimate the pricing for OpenAI APIs based on the selected model and input parameters. It provides a convenient way to explore and understand the potential costs associated with different models and input scenarios.

## Getting Started

### Prerequisites

- Python 3.10
- Required Python packages: Install [requirements.txt](./requirements.txt)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/openai-api-pricing-calculator.git
    ```

2. Navigate to the project directory:

    ```bash
    cd openai-api-pricing-calculator
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run main.py
    ```

2. The app will open in your default web browser. Select the model type, specific model class, and individual model using the sidebar.

3. Customize input parameters, such as resolution and dimensions, if applicable.

4. Enter your text in the provided textbox.

5. Click the "Pricing" button to calculate and display the estimated cost based on the selected model and input.

6. Optionally, use the "Clear" button to reset the text area.

## Model Types

The tool currently supports language models. Depending on the selected model, additional options for vision models may be available.

## Additional Information

- The tool uses configuration data loaded from a YAML file (`config.yaml`) to determine model attributes and pricing details.

- For more information on vision models and calculating costs, refer to [OpenAI's documentation](https://platform.openai.com/docs/guides/vision/calculating-costs).

## Contributing

Feel free to contribute to the project by creating issues or submitting pull requests. Your feedback and improvements are welcome!

