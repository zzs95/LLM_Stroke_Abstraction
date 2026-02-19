# Large Language Models for Accurate Medical Chart Abstraction: Enabling Scalable and Secure AI Deployment in Stroke

## 📖 Overview

This repository provides a reproducible framework for structured clinical variable extraction from stroke procedure reports using locally deployed Large Language Models (LLMs) via Ollama.

The system is designed to extract predefined procedural and clinical variables from free-text stroke reports using a standardized prompt schema.


### File Description

| File | Description |
|-|-|
| `environment.yml` | Conda environment configuration |
| `prompt.csv` | Modular structured prompt definitions |
| `report_clin_extract_ollama.py` | Main extraction pipeline |
| `start_ollama_gpu.sh` | Docker-based Ollama GPU server launcher |


## ⚙️ Environment Setup

### 1️⃣ Create Conda Environment

```

conda env create -f environment.yml
conda activate ollama_py

```



## 🐳 Ollama Docker Deployment

Ensure Docker and NVIDIA runtime are installed.

### Start Ollama on GPU

```

bash start_ollama_gpu.sh

```

This will:

- Pull the official `ollama/ollama` image
- Bind a GPU device
- Launch a local inference server
- Expose API endpoint 



## 📥 Pull Model

Example:

```

docker exec -it ollama_gpu0 ollama pull qwen3:4b-q4_K_M

```



## 🚀 Run Clinical Extraction

```

python report_clin_extract_ollama.py 
--data_path ./data
--model qwen3:4b-q4_K_M
--report_xlsx report.xlsx 
--prompt_csv prompt.csv 
--output results.xlsx

```

Optional Chain-of-Thought mode:

```

--use_cot

```



## 🧩 Prompt Structure

Each variable prompt is modularized into:

- **Question**
- **Answer Choices**
- **Chain-of-Thought reasoning (Optional)**
- **Final Output constraint**

The model is instructed to conclude strictly in the format:

```
(Step-by-step reasoning for CoT)
The final answer is: X
```



## 🔬 Extracted Variables

| Variable | Description |
|--|--|
| Carotid Stent | Cervical ICA stenting |
| Carotid Angioplasty | Cervical ICA balloon angioplasty |
| Intracranial Stent | Intracranial stent placement |
| Intracranial Angioplasty | Intracranial angioplasty |
| IV Thrombolytics | IV alteplase / TNK |
| Site of Occlusion | ICA / M1 / M2 / Basilar / Other |
| TICI Post | Final modified TICI score |
| NIHSS | Admission NIHSS score |



## 📜 Citation

If you use this framework in academic work, please cite:

```

@article{stroke_llm_abstraction,
title={Large Language Models for Accurate Medical Chart Abstraction: Enabling Scalable and Secure AI Deployment in Stroke},
author={Zhong, Zhusi et al.},
journal={Under Review},
year={2026}
}

```



## 🤝 Acknowledgements

This project leverages:

- Ollama (local LLM deployment)
- Open-source large language models
- Python scientific ecosystem




