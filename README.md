# RC File Analyzer

This application is designed to extract data from a ZIP file and process specific files within the ZIP using a language model (LLM) for advanced text analysis. The extracted information can then be used to analyze and structure project-related details automatically.

## Features

- **Zip File Handling**: Automatically extracts and processes specific files from a given ZIP archive.
- **LLM-Based Analysis**: Uses a Language Model (e.g., Cohere's API) to extract structured information from text, such as project details, submission deadlines, contacts, etc.
- **Customizable Prompts**: Prompts can be customized to extract different types of information from the text.
  
## Requirements

- Python 3.x
- Required libraries specified in `setup.py` or `requirements.txt`

The key dependencies include:
- `cohere`: For leveraging Cohere's LLM API.
- `streamlit`: For building the user interface (if applicable).
- `python-dotenv`: For managing environment variables like API keys.
- `PyPDF2`: For handling PDF files within the ZIP archive (if applicable).

## Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/rc_file_analyzer.git
    ```

2. Navigate to the project directory:
    ```bash
    cd rc_file_analyzer
    ```

3. Install the dependencies:
    - If you are using `setup.py`, run:
      ```bash
      pip install .
      ```
    - Alternatively, you can install dependencies from `requirements.txt`:
      ```bash
      pip install -r requirements.txt
      ```

4. Set up environment variables:
    - Create a `.env` file and add your API keys and other necessary environment variables.
    - Example `.env` file:
      ```bash
      COHERE_API_KEY=your-cohere-api-key
      ```

## Usage

1. Ensure that your ZIP file is placed in the correct input directory, or provide the correct path in the UI (if using Streamlit).
   
2. Run the main application:
    ```bash
    python main.py
    ```

3. The program will:
   - Extract files from the ZIP archive.
   - Analyze specific files using an LLM (Language Model) to extract detailed project information.
   - Provide structured outputs such as:
     - Project name
     - Submission deadline
     - Contact information
     - And other relevant details as specified in the prompts.

## Example

Here’s an example of what the application does:
- **Input**: A ZIP file containing project documents (PDF, text, etc.).
- **Output**: A structured report containing:
  - Project name
  - RC number
  - Description
  - Submission deadline
  - Contact details, etc.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues or pull requests if you'd like to contribute to the project.

---

**Author**: Faycal Djilali  
**Email**: djilalifaycal97@gmail.com