"""
Clinical Variable Extraction from Stroke Reports using Ollama LLM

Author: Zhusi Zhong
Description:
    Extract structured clinical variables from stroke reports.
    Supports optional Chain-of-Thought prompting.
"""

import os
import re
import time
import argparse
import logging
from typing import List, Dict

import pandas as pd
from tqdm import tqdm
from ollama import Client


# ============================================================
# Logger
# ============================================================

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


# ============================================================
# Extract Final Answer
# ============================================================

def extract_final_answer(text: str) -> str:
    match = re.search(r"The final answer is:\s*(.*)", text, re.IGNORECASE)
    if not match:
        return "None"
    return match.group(1).strip()


# ============================================================
# Prompt Builder (NEW MODULAR DESIGN)
# ============================================================

def build_prompt(
    report_text: str,
    row_prompt: pd.Series,
    use_cot: bool,
) -> str:

    question = row_prompt["question"]
    answer_choices = row_prompt["answer_choices"]
    final_output = row_prompt["final_output"]

    base_prompt = (
        "**Context**: The following is a stroke clinical report.\n\n"
        f"{report_text}\n\n"
        f"**Question**: {question}\n\n"
        f"**Answer Choices**:\n{answer_choices}\n\n"
    )

    if use_cot:
        cot = row_prompt["cot"]
        reasoning_block = f"**Chain-of-Thought**:\n{cot}\n\n"
    else:
        reasoning_block = "\n"

    final_instruction = f"**Final Output**: {final_output}\n\n" 
    if use_cot:
        final_instruction += "Please output your complete thought process. "
    final_instruction += ("At the end of the output, using this as a conclusion format 'The final answer is: '+ the number answer."+ \
        "If you can't find any relevant content, using this as a conclusion format 'The final answer is: None'. "+\
        "Using plain text output. Please output in strict accordance with the required format: 'The final answer is: A NUMBER INDEX'."
    )

    return base_prompt + reasoning_block + final_instruction


# ============================================================
# Variable Extraction
# ============================================================

def variable_extraction(
    client: Client,
    model_name: str,
    report_text: str,
    row_prompt: pd.Series,
    use_cot: bool,
) -> str:

    prompt = build_prompt(report_text, row_prompt, use_cot)

    try:
        response = client.generate(model=model_name, prompt=prompt)
        return response["response"]
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return "The final answer is: None"


# ============================================================
# Main Loop
# ============================================================

def process_reports(
    clin_df: pd.DataFrame,
    prompt_df: pd.DataFrame,
    client: Client,
    model_name: str,
    output_file: str,
    use_cot: bool,
):

    results: List[Dict] = []

    for _, row in tqdm(clin_df.iterrows(), total=len(clin_df)):

        study_output: Dict[str, str] = {
            "Patient MRN": row.get("Patient MRN", ""),
            "Accession Number": row.get("Accession Number", ""),
        }

        report_text = row.get("Report Text", "")

        for key in prompt_df.index:

            row_prompt = prompt_df.loc[key]

            generated_text = variable_extraction(
                client,
                model_name,
                report_text,
                row_prompt,
                use_cot,
            )

            study_output[key] = extract_final_answer(generated_text)

            if use_cot:
                study_output[key + "_COT"] = generated_text[:1500]

        study_output["timestamp"] = time.time()
        results.append(study_output)

        pd.DataFrame(results).to_excel(output_file, index=False)

    logging.info("Processing complete.")


# ============================================================
# Entry Point
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--report_xlsx", type=str, required=True)
    parser.add_argument("--prompt_csv", type=str, required=True)

    parser.add_argument("--model", type=str, default="llama3.1")
    parser.add_argument("--host", type=str, default="http://localhost:11435")

    parser.add_argument("--output", type=str, default="predictions.xlsx")
    parser.add_argument("--use_cot", action="store_true")

    args = parser.parse_args()

    setup_logger()

    clin_df = pd.read_excel(
        os.path.join(args.data_path, args.report_xlsx)
    )

    prompt_df = pd.read_csv(args.prompt_csv)

    if "key" not in prompt_df.columns:
        raise ValueError("prompt_csv must contain a 'key' column.")

    prompt_df.set_index("key", inplace=True)

    client = Client(host=args.host)

    logging.info(f"Using model: {args.model}")
    logging.info(f"Chain-of-Thought enabled: {args.use_cot}")

    process_reports(
        clin_df,
        prompt_df,
        client,
        args.model,
        args.output,
        args.use_cot,
    )


if __name__ == "__main__":
    main()
