from src.genai.config.prompts import PromptTemplate


prompts: dict[str, PromptTemplate] = {
    "default": {
        "name": "default",
        "template": "You are a helpful assistant. Use the following context to answer the question at the end. Context: {context} Question: {query} Answer:",
        "context_fields": [
            "context",
            "question"
        ]
    },
    "general_qa": {
        "name": "general_qa",
        "template": "You are a helpful assistant. Use the following context to answer the question at the end. Context: {context} Question: {query} Answer:",
        "context_fields": [
            "context",
            "question"
        ]
    },
    "document_summary": {
        "name": "document_summary",
        "template": "Summarize this document while maintaining key technical details. Document: {document_content} Summary:",
        "context_fields": [
            "document_content"
        ]
    },
    "technical_support": {
        "name": "technical_support",
        "template": "Analyze the following error logs and provide troubleshooting steps. Error Details: {error_logs} System Info: {system_info} Troubleshooting Guide:",
        "context_fields": [
            "error_logs",
            "system_info"
        ]
    },
    "data_analysis": {
        "name": "data_analysis",
        "template": "Explain this dataset focusing on patterns and anomalies. Dataset: {dataset_sample} Context: {analysis_context} Explanation:",
        "context_fields": [
            "dataset_sample",
            "analysis_context"
        ]
    },
    "unknown_query_response": {
        "name": "unknown_query_response",
        "template": "I couldn't find relevant information for '{query}'. Could you please rephrase or provide more context?",
        "context_fields": [
            "original_query"
        ]
    }
}