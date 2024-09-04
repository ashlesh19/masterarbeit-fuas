# masterarbeit-fuas
# **Analysis of ESG Disclosure Trends: A Comparative Study Across Industries**

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
- 
**Key Steps:**
- Insert the final ESG data into appropriate tables or collections.
- Provide querying options for retrieving insights.


