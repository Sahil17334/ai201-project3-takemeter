# TakeMeter: r/Cricket Discourse Classifier

## 1. Community & Labels
**Community:** `r/Cricket`
**Labels:**
1. `analysis`: Structured arguments backed by specific statistics (e.g., "Bumrah's economy rate in the death overs this IPL is 6.2...").
2. `hot_take`: Bold, confident opinions stated without evidence (e.g., "Virat Kohli is washed.").
3. `reaction`: Immediate emotional responses to specific events (e.g., "WHAT A CATCH!").

## 2. Dataset
* **Source:** Synthetically generated 268 realistic subreddit comments using Groq `llama-3.3-70b-versatile` to simulate scraping.
* **Label Distribution:** Evenly split across the three classes.
* **Hard Edge Case:** "Rohit is finished, his average is down by 2 runs." Labeled as `hot_take` because the stat is superficial and used purely for accusatory framing, not genuine analysis.

## 3. Fine-Tuning Pipeline
* **Base Model:** `distilbert-base-uncased`
* **Training Setup:** Fine-tuned on Google Colab (T4 GPU). 
* **Hyperparameters:** Used 3 epochs, learning rate 2e-5, and batch size of 16. I kept 3 epochs to prevent overfitting on my 268-row dataset.

## 4. Evaluation Report

### Baseline (Groq Zero-Shot) vs. Fine-Tuned (DistilBERT)
* **Baseline Accuracy:** 97.56%
* **Fine-Tuned Accuracy:** 90.24%

### Per-Class F1 Metrics (Fine-Tuned)
* **Analysis F1:** 86.7%
* **Hot_Take F1:** 88.0%
* **Reaction F1:** 96.3%

### Confusion Matrix (Fine-Tuned)
| True \ Predicted | analysis | hot_take | reaction |
|------------------|----------|----------|----------|
| **analysis** | 13       | 0        | 0        |
| **hot_take** | 3        | 11       | 0        |
| **reaction** | 1        | 0        | 13       |

### Failure Analysis (3 Wrong Predictions)
*(Looking at the confusion matrix, my model specifically struggled by over-predicting the `analysis` label, misclassifying 3 hot takes and 1 reaction as analysis).*

1.Wrong predictions: 4 / 41

--- #1 ---
Text:      Test cricket is boring because of the slow over rates. Teams take too long to bowl their overs.
True:      hot_take
Predicted: analysis  (confidence: 0.40)

--- #2 ---
Text:      The best wicket-keeper in the world is MS Dhoni. He's the most talented and athletic keeper.
True:      hot_take
Predicted: analysis  (confidence: 0.42)

--- #3 ---
Text:      UNBELIEVABLE BOWLING SPELL BY RABADA
True:      reaction
Predicted: analysis  (confidence: 0.37)

--- #4 ---
Text:      West Indies have the worst bowling attack in the world. They can't even get a team all out for under 300.
True:      hot_take
Predicted: analysis  (confidence: 0.55)


## 5. Sample Classifications
| Post Text | Predicted Label | Confidence Score |
|-----------|-----------------|------------------|
| "Bumrah finishes with 4-0-12-3, absolute genius spell!" | `analysis` | 98% |
| "Drop him immediately, worst performance ever!!" | `reaction` | 95% |

* **Reasoning:** For the first example, the prediction is highly reasonable because the specific bowling figures layout (`4-0-12-3`) serves as strong statistical input characteristic of deep cricket analysis.

## 6. Reflections
* **What the model learned vs intended:** I intended the model to evaluate the structural quality of reasoning. Instead, it learned basic lexical shortcuts. Because the DistilBERT model is small, it struggled to grasp internet sarcasm and nuance, heavily associating the mere presence of numbers with `analysis`. Interestingly, the massive 70-billion parameter Groq model scored 97.56% zero-shot, proving that sheer model size is sometimes required to genuinely understand human conversational nuance. 
* **Spec Reflection:** Writing out the planning edge-cases helped me construct tight boundary limits early. I diverged from manual data collection by designing an automated generation script, saving critical engineering hours while ensuring an even class distribution.
* **AI Usage:** 1. Used Groq to synthetically generate 268 rows of training data to skip manual copy-pasting.
  2. Used LLM patterns to inspect text classification discrepancies and identify linguistic dependencies across false predictions.