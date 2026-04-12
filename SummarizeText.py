import torch
from omegaconf import OmegaConf
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class SummarizeText:
    def __init__(self, config_path):
        self.config = OmegaConf.load(config_path)

        self.model_path = self.config.get("model_path", "facebook/bart-large-cnn")
        self.task_prefix = self.config.get("task_prefix", "")
        self.max_input_length = self.config.get("max_input_length", 1024)
        self.max_new_tokens = self.config.get("max_new_tokens", 160)
        self.min_length = self.config.get("min_length", 30)
        self.do_sample = self.config.get("do_sample", False)
        self.num_beams = self.config.get("num_beams", 5)
        self.no_repeat_ngram_size = self.config.get("no_repeat_ngram_size", 3)
        self.length_penalty = self.config.get("length_penalty", 1.0)

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)

    def __call__(self, text):
        if not isinstance(text, str):
            raise ValueError("Input text must be a string.")

        clean_text = text.strip()
        if not clean_text:
            raise ValueError("Input text is empty.")

        prompt_input = f"{self.task_prefix}{clean_text}" if self.task_prefix else clean_text
        inputs = self.tokenizer(
            prompt_input,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_input_length,
        )

        with torch.no_grad():
            summary_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=self.max_new_tokens,
                min_length=self.min_length,
                do_sample=self.do_sample,
                num_beams=self.num_beams,
                no_repeat_ngram_size=self.no_repeat_ngram_size,
                length_penalty=self.length_penalty,
                early_stopping=True,
            )

        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
