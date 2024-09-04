# masterarbeit-fuas
## **Project Overview**
This project investigates the trends in ESG (Environmental, Social, and Governance) disclosures across various industries. By leveraging machine learning models, data extraction, and fine-tuning techniques, we aim to uncover patterns and provide meaningful insights into how industries report ESG-related data.

## **Notebook Breakdown**

### **1. 00extract_pdf.ipynb**
**Task:** Extracts raw ESG disclosure data from PDF documents or structured text files.  
**Input Files:**  
- `input_pdfs/` directory containing PDF reports with ESG disclosures.
- `config.json` (optional) for specifying extraction parameters like page ranges or sections to extract.

**Output Files:**  
- `output_texts/` directory containing the extracted text files for each PDF.

**Key Steps:**
- Convert PDFs into a text format using tools like `pdfplumber`.
- Perform initial cleaning to remove unnecessary content like headers/footers.
  
---

### **2. 01replaceStrings.ipynb**
**Task:** Cleans and preprocesses the extracted data by replacing unwanted strings or correcting common text errors.  
**Input Files:**  
- `output_texts/` directory from the previous notebook, containing raw extracted text files.

**Output Files:**  
- `cleaned_texts/` directory, containing the cleaned and normalized text files.

**Key Steps:**
- Identify and replace common string patterns that may cause issues in later analysis (e.g., correcting encoding errors, removing special characters).
- Normalize company names or other entities for consistency.


---

### **3. 02FilterBERT.ipynb**
**Task:** Filters the cleaned data to extract only the relevant ESG disclosure content using a pre-trained BERT model.  
**Input Files:**  
- `cleaned_texts/` directory from the previous notebook.
- `bert_model/` directory containing the pre-trained BERT model.

**Output Files:**  
- `filtered_texts/` directory, containing only ESG-relevant content.

**Key Steps:**
- Load a pre-trained BERT model for text classification.
- Apply the model to filter out irrelevant content and retain only ESG-related text.

---

### **4. 03finetunellama3withunsloth.ipynb**
**Task:** Fine-tunes a LLaMA model using the filtered ESG data for unsupervised learning.  
**Input Files:**  
- `filtered_texts/` directory from the previous notebook.
- `llama_model/` directory containing the base LLaMA model.

**Output Files:**  
- `fine_tuned_model/` directory with the fine-tuned model ready for further analysis.

**Key Steps:**
- Fine-tune the LLaMA model on the ESG-specific text data.
- Use unsupervised learning techniques to adapt the model for specific ESG trend identification.

---

### **5. 04postprocessing.ipynb**
**Task:** Processes the outputs from the fine-tuned LLaMA model to structure the data for further calculations and insights.  
**Input Files:**  
- `fine_tuned_model/` directory from the previous notebook.

**Output Files:**  
- `postprocessed_results/` directory containing structured data ready for analysis.

**Key Steps:**
- Clean and organize the model’s output for further analysis.
- Format data into a structure suitable for visualizations and insights.

---

### **6. 05Calculate.ipynb**
**Task:** Performs calculations and generates industry-specific metrics from the post-processed data.  
**Input Files:**  
- `postprocessed_results/` directory from the previous notebook.

**Output Files:**  
- `calculated_metrics/` directory with calculated ESG metrics and trends.

**Key Steps:**
- Calculate industry-specific metrics such as the frequency of ESG mentions, sentiment scores, or topic distribution.

---

### **7. 06helper.ipynb**
**Task:** Contains helper functions that assist in data manipulation and other auxiliary tasks used across multiple notebooks.  
**Input Files:**  
- Supports various input files based on the operations needed in different notebooks.

**Output Files:**  
- Assists in generating intermediate outputs used by other notebooks.

**Key Steps:**
- Provides utility functions for data handling, formatting, and statistical analysis.

---

### **8. 07database.ipynb**
**Task:** Stores the processed and calculated ESG data into a database for future retrieval and reporting.  
**Input Files:**  
- `calculated_metrics/` directory containing the final processed data.

**Output Files:**  
- Data is stored in .csv file
  
**Key Steps:**
- Insert the final ESG data into appropriate tables or collections.
- Provide querying options for retrieving insights.


## Dash App Overview (Dashboard)

### 1. **compare_heatmap.py**

#### **Features:**
- **Heatmap Visualization for ESG Indicators:**
  This app provides a heatmap visualization that compares ESG (Environmental, Social, and Governance) indicators across different companies. It loads ESG data from a CSV file (`database.csv`) and allows users to visually compare companies on specific ESG indicators.

- **ESG Indicators:**
  The ESG indicators are divided into three categories:
  - **Environmental Indicators (E)** 
  - **Social Indicators (S)** 
  - **Governance Indicators (G)**

- **Dynamic Heatmap Generation:**
  Users can select different ESG indicators to visualize, and the app dynamically generates heatmaps that reflect the performance of companies across these metrics.

- **Matplotlib and Seaborn Integration:**
  The heatmaps are created using Seaborn, with Matplotlib serving as the rendering engine. 

#### **User Interaction:**
- Dropdown menus for selecting ESG categories (Environmental, Social, or Governance).
- Dynamic heatmap generation based on selected ESG metrics.

#### **Data Files:**
- **Input:** `database.csv` - This CSV file contains ESG data for various companies.
- **Libraries Used:** Dash, Pandas, Seaborn, Matplotlib.

---

### 2. **ESGIndicatorFrequecny.py**

#### **Features:**
- **ESG Indicator Frequency Dashboard:**
  This app visualizes the frequency of ESG disclosures across different companies. It analyzes how often each company reports on various ESG indicators by calculating the frequency of these indicators in `database.csv`.

- **Alias Mapping for Indicators:**
  The app uses an alias file (`esg_indicator_aliases.csv`) to map commonly used ESG terms or abbreviations to standardized ESG indicators. This ensures consistency when analyzing the frequency of disclosures.

- **Data Categorization:**
  The app divides ESG indicators into Environmental, Social, and Governance categories. This allows users to filter data and explore disclosure frequency based on the specific ESG dimension.

- **Company-Specific Insights:**
  Users can select a specific company from the dropdown menu to view how frequently it discloses certain ESG indicators.

#### **User Interaction:**
- Dropdown selection for specific companies.
- Interactive plots showing the frequency of ESG disclosures for the selected company.

#### **Data Files:**
- **Input:** 
  - `database.csv` - Contains ESG data for different companies.
  - `esg_indicator_aliases.csv` - Contains mappings of ESG indicator aliases to their standardized forms.
- **Libraries Used:** Dash, Pandas.

---

### 3. **IndustryLeaders.py**

#### **Features:**
- **Industry Leaders Comparison Dashboard:**
  This app allows users to compare how different industries perform in terms of ESG disclosures. It provides a dashboard where users can visualize which industries lead in specific ESG metrics, based on data loaded from `database.csv`.

- **Industry-Based ESG Performance:**
  The app presents data at the industry level, allowing users to compare industries on Environmental, Social, and Governance indicators. Users can explore which industries are leading in particular ESG areas and understand industry-wide trends.

- **Bootstrap Integration:**
  The app uses Dash Bootstrap Components for a polished and responsive UI, making the dashboard more visually appealing and user-friendly.

#### **User Interaction:**
- Dropdown menus for selecting industries or specific companies.
- Visual comparison of industries based on selected ESG metrics.

#### **Data Files:**
- **Input:** `database.csv` - Contains ESG data for various industries and companies.
- **Libraries Used:** Dash, Pandas, Matplotlib, Dash Bootstrap Components.

---

### **Summary of Features for All Three Dash Apps:**
1. **`compare_heatmap.py`:** 
   - Generates dynamic heatmaps to compare ESG indicators across companies.
   
2. **`ESGIndicatorFrequecny.py`:** 
   - Visualizes the frequency of ESG disclosures across selected companies.
   
3. **`IndustryLeaders.py`:** 
   - Compares industries and visualizes which industries are leaders in ESG performance.
