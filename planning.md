# TakeMeter Planning: r/Cricket Discourse

## 1. Community
I am evaluating `r/Cricket`. This community is perfect for a classification task because the discourse varies wildly between rigorous statistical analysis (like calculating pitch conditions or bowler economy rates) and purely emotional, reactionary posts after a dropped catch or a bad over. 

## 2. Labels
1. **`analysis`**: The post makes a structured argument backed by specific statistics, historical comparisons, or tactical observations. Evidence is specific and verifiable.
   * *Example 1:* "Bumrah's economy rate in the death overs this IPL is 6.2. If you look at his pitch maps, he's landing the yorker 15% more often than last season."
   * *Example 2:* "The WPL pitch in Vadodara is slowing down considerably in the second innings; chasing anything over 150 here is mathematically highly improbable."
2. **`hot_take`**: A bold, confident opinion stated without supporting evidence. The claim might be true or false, but the post asserts rather than argues.
   * *Example 1:* "Virat Kohli is officially washed and shouldn't even be in the T20 squad anymore."
   * *Example 2:* "This is the worst captaincy I have ever seen in the history of the World Cup."
3. **`reaction`**: An immediate emotional response to a specific event. Little to no argument—just expressing a feeling in the moment.
   * *Example 1:* "LETS GOOOOOOOOO WHAT A CATCH!"
   * *Example 2:* "I am in physical pain watching this batting collapse."

## 3. Hard Edge Cases
**The Disguised Hot Take:** * *Example:* "Rohit is finished, his average is down by 2 runs this year." 
* *Decision Rule:* Even though it includes a number, the stat is superficial and cherry-picked simply to frame an accusatory claim. If the evidence is decorative rather than forming a genuine argument, it gets labeled `hot_take`.

## 4. Data Collection Plan
Manual collection of 200 posts takes hours. Instead, I will write a Python script using the Groq API to synthetically generate 220 realistic Reddit comments tailored exactly to these three labels, saving them directly to a CSV. 

## 5. Evaluation Metrics
Overall accuracy is not enough because class distribution might not be perfectly equal. I will rely on the **F1-Score** per class, which balances Precision (how many predicted `analysis` posts were actually `analysis`) and Recall (how many of the true `analysis` posts the model successfully caught).

## 6. Definition of Success
A zero-shot LLM baseline will likely score around 60-70% because community slang is tricky. Success for my fine-tuned DistilBERT model will be achieving an overall accuracy of >85%, proving that the weights successfully adjusted to the specific vocabulary of the subreddit.

## 7. AI Tool Plan
* **Annotation Assistance:** I will use the `llama-3.3-70b-versatile` model via the Groq API to synthetically generate my 200-row `dataset.csv`.
* **Failure Analysis:** After fine-tuning, I will feed the confusion matrix and wrong predictions to an LLM to help identify if the model systematically confuses `hot_take` and `reaction` due to exclamation point frequency.