很好 👍
下面给你一个**论文级 + 可公开 GitHub 项目级别的 README.md**。

包含：

* 项目标题（按论文风格）
* 项目简介
* 方法简介
* 文件说明
* 环境安装
* Docker 部署
* 运行示例
* Prompt 结构说明
* 可复现性说明
* Citation 模板
* License 建议

你可以直接复制保存为：

```
README.md
```

---

# 📄 README.md

```markdown
# LLM-Based Structured Clinical Variable Extraction for Endovascular Stroke Procedures

### A Modular Large Language Model Framework for Structured Stroke Chart Abstraction

---

## 📖 Overview

This repository provides a reproducible framework for structured clinical variable extraction from stroke procedure reports using locally deployed Large Language Models (LLMs) via Ollama.

The system is designed to extract predefined procedural and clinical variables from free-text stroke reports using a standardized prompt schema.

The framework supports:

- Modular prompt design
- Optional Chain-of-Thought reasoning
- Deterministic structured output
- Local GPU-based LLM inference
- Reproducible environment configuration

---

## 🧠 Research Context

This project supports the research study:

> **Large Language Model-Based Structured Abstraction of Endovascular Stroke Procedure Reports**

The goal is to evaluate whether LLMs can reliably extract structured clinical variables such as:

- Carotid stenting
- Intracranial angioplasty
- IV thrombolytics
- Occlusion site
- Final TICI score
- Admission NIHSS

from unstructured stroke procedure documentation.

---

## 📂 Repository Structure

```

environment.yml
prompt.csv
report_clin_extract_ollama.py
start_ollama_gpu.sh
README.md

```

### File Description

| File | Description |
|------|------------|
| `environment.yml` | Conda environment configuration |
| `prompt.csv` | Modular structured prompt definitions |
| `report_clin_extract_ollama.py` | Main extraction pipeline |
| `start_ollama_gpu.sh` | Docker-based Ollama GPU server launcher |

---

## ⚙️ Environment Setup

### 1️⃣ Create Conda Environment

```

conda env create -f environment.yml
conda activate ollama_py

```

---

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
- Expose API endpoint (default: http://localhost:11434)

---

## 📥 Pull Model

Example:

```

docker exec -it ollama_gpu0 ollama pull koesn/llama3-openbiollm-8b

```

---

## 🚀 Run Clinical Extraction

```

python report_clin_extract_ollama.py 
--data_path ./data 
--report_xlsx report.xlsx 
--prompt_csv prompt.csv 
--output results.xlsx

```

Optional Chain-of-Thought mode:

```

--use_cot

```

---

## 🧩 Prompt Structure

Each variable prompt is modularized into:

- **Question**
- **Answer Choices**
- **Optional Chain-of-Thought reasoning**
- **Final Output constraint**

The model is instructed to conclude strictly in the format:

```

The final answer is: X

```

This ensures structured and machine-readable outputs.

---

## 🔬 Extracted Variables

| Variable | Description |
|-----------|------------|
| Carotid Stent | Cervical ICA stenting |
| Carotid Angioplasty | Cervical ICA balloon angioplasty |
| Intracranial Stent | Intracranial stent placement |
| Intracranial Angioplasty | Intracranial angioplasty |
| IV Thrombolytics | IV alteplase / TNK |
| Site of Occlusion | ICA / M1 / M2 / Basilar / Other |
| TICI Post | Final modified TICI score |
| NIHSS | Admission NIHSS score |

---

## 🔁 Reproducibility

- Fully local inference
- Deterministic structured output
- Fixed environment specification
- Modular prompt design
- Compatible with multi-GPU inference

---

## 🏥 Intended Use

This framework is intended for:

- Clinical NLP research
- Structured chart abstraction studies
- LLM evaluation in medical text extraction
- Reproducible AI research

It is not intended for direct clinical decision-making.

---

## 📊 Example Output Format

```

## Accession Number | carotid_stent | iv_thrombolytics | site_of_occlusion | tici_post | nihss

12345678         | 1              | 1                 | 2                 | 5         | 14

```

---

## 📜 Citation

If you use this framework in academic work, please cite:

```

@article{stroke_llm_abstraction,
title={Large Language Model-Based Structured Abstraction of Endovascular Stroke Procedure Reports},
author={Zhong, Zhusi et al.},
journal={Under Review},
year={2025}
}

```

---

## 📄 License

MIT License

---

## 🤝 Acknowledgements

This project leverages:

- Ollama (local LLM deployment)
- Open-source large language models
- Python scientific ecosystem




