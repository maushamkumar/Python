#!/usr/bin/env python3
"""
Streamlit Web Interface for CEFR Vocabulary Level Estimator
=========================================================

This script creates an interactive web application using Streamlit to estimate the CEFR vocabulary level of a given text.
"""

import streamlit as st
from main import CEFRVocabularyEstimator
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# Global estimator instance
estimator = None

def initialize_estimator():
    """Initialize the CEFR estimator."""
    global estimator
    if estimator is None:
        estimator = CEFRVocabularyEstimator()
    return estimator

def create_visualization(result):
    """Create visualization charts for the analysis results."""
    plt.style.use('seaborn-v0_8')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    levels = list(result.level_percentages.keys())
    percentages = list(result.level_percentages.values())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    bars = ax1.bar(levels, percentages, color=colors[:len(levels)])
    ax1.set_title('CEFR Level Distribution (%)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('CEFR Levels')
    ax1.set_ylabel('Percentage of Words')
    ax1.set_ylim(0, max(percentages) * 1.1 if percentages else 10)
    
    for bar, pct in zip(bars, percentages):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(percentages)*0.01,
                f'{pct:.1f}%', ha='center', va='bottom')
    
    pie_labels = list(result.vocabulary_distribution.keys())
    word_counts = list(result.vocabulary_distribution.values())
    ax2.pie(word_counts, labels=pie_labels, colors=colors[:len(pie_labels)], autopct='%1.1f%%', startangle=90)
    ax2.set_title('Word Count Distribution by Level', fontsize=14, fontweight='bold')
    
    if result.complexity_metrics:
        metrics = list(result.complexity_metrics.keys())
        values = list(result.complexity_metrics.values())
        
        normalized_values = []
        for i, (metric, value) in enumerate(result.complexity_metrics.items()):
            if 'ratio' in metric or 'diversity' in metric:
                normalized_values.append(value * 100)
            else:
                normalized_values.append(value)
        
        bars = ax3.barh(range(len(metrics)), normalized_values, color='skyblue')
        ax3.set_yticks(range(len(metrics)))
        ax3.set_yticklabels([m.replace('_', ' ').title() for m in metrics])
        ax3.set_title('Text Complexity Metrics', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Value')
        
        for i, (bar, value) in enumerate(zip(bars, normalized_values)):
            ax3.text(bar.get_width() + max(normalized_values)*0.01, bar.get_y() + bar.get_height()/2,
                    f'{value:.2f}', ha='left', va='center')
    
    level_numeric = [estimator.level_to_numeric[level] for level in levels]
    ax4.scatter(level_numeric, percentages, s=100, c=colors[:len(levels)], alpha=0.7)
    ax4.plot(level_numeric, percentages, 'b--', alpha=0.5)
    ax4.set_xticks(range(len(estimator.cefr_levels)))
    ax4.set_xticklabels(estimator.cefr_levels)
    ax4.set_title('Vocabulary Level Progression', fontsize=14, fontweight='bold')
    ax4.set_xlabel('CEFR Levels')
    ax4.set_ylabel('Percentage of Words')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig

def main():
    st.set_page_config(page_title="CEFR Vocabulary Level Estimator", layout="wide")
    st.title("CEFR Vocabulary Level Estimator")

    text_input = st.text_area("Enter text to analyze:", height=200)

    if st.button("Analyze"):
        if text_input.strip():
            with st.spinner("Analyzing..."):
                est = initialize_estimator()
                result = est.analyze_text(text_input)
                
                st.header("Analysis Results")
                st.metric("Estimated CEFR Level", result.estimated_level)
                st.metric("Confidence Score", f"{result.confidence_score:.3f}")

                st.subheader("Text Statistics")
                st.text(f"Word Count: {result.word_count}")
                st.text(f"Sentence Count: {result.sentence_count}")
                st.text(f"Average Sentence Length: {result.avg_sentence_length:.1f}")

                st.subheader("CEFR Level Distribution")
                st.bar_chart({k: v for k, v in result.level_percentages.items()})

                st.subheader("Visualization")
                fig = create_visualization(result)
                st.pyplot(fig)

                st.subheader("Detailed Report")
                st.text(est.generate_report(result))
        else:
            st.warning("Please enter text to analyze.")

if __name__ == '__main__':
    main()