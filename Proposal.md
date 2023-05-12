Furkan Akkurt, 15 May

## 1. Question

Can we determine the number of senses of a word?

## 2. Introduction

Each word has at least one sense. Many words have multiple of them. Through time, these senses change in content and also count. Some senses go out of favor while some morph into others. Dictionary providers should keep track of a language's current usage to detect if a sense has appeared or changed for a word. Then, fittingly, they will update their dictionary so.

As can be seen, this is **quite** a task. What if we could automate this process by leveraging the contextualizing power of transformer models? In this project, I will try to figure out if a given dictionary has a different number of senses for a word than necessary. Hopefully, I'll also be able to provide the sentences responsible for the sense changes.

## 3. Method

When a given sentence is passed through BERT, each token has a contextual representation, as demonstrated by *Pasini et al. (2020)* [1]. *Zhou & Li (2020)* [2] "use the sum of the last 4 layers \[of BERT\] to encode both word meaning and context information". They mention that it has been suggested by BERT's authors. If we cluster these embeddings for each *distinct* word, we will hopefully end up with all the senses of each word, represented by the clusters.

All 3 of my selected presentation papers use BERT to produce contextualized outputs ot tokens from raw sentences [1, 2, 3]. After collecting all the embeddings for all the words in a dictionary using the sentences in the corpus, the second step is to create clusters. K-means has been used for this purpose by *Pasini et al. (2020)* [1], but this assumes the parameter *k* is known. I assume almost all the words in the dictionary will have the needed number of senses entered in the dictionary. For a word, the number of senses in the dictionary can be used as the *k* in clustering. 

We can consider the smallest amount of distance between any 2 clusters of any word as the smallest semantic difference that made the dictionary writers (lexicographers) want to represent the usages with different senses. For example, the word *main* has the following 2 senses (one being a subsense) in New Oxford American Dictionary [4] :
1. a principal pipe carrying water or gas to buildings, or taking sewage from them.
	- a principal cable carrying electricity.

These are very close meanings but the lexicographers deemed it important to separate them into 2 senses. In the clusters, I would expect to distinguish between these 2 senses. For this, I want to calculate the smallest distance in the entire semantic space of the dictionary that compelled the lexicographers to provide 2 senses, instead of merging them into 1.

After determining this distance, the steps are:
1. Cluster all the embeddings again based on this distance, instead of *k-means*
2. Compare the number of clusters with the sense count from the dictionary for each word
3. If there is a mismatch for a word, investigate it further. Hopefully, this word has been identified as having lost or gained a sense.

This approach won't be able to detect if a sense has been gained and lost at the same time because the cluster count will not change. The clusters are not aligned with the senses from the dictionary based on semantic information in the clusters. I am only comparing the counts. 

## 4. Corpora

I plan to find a raw English corpus of only sentences from recent years. [COCA](https://www.english-corpora.org/coca) is a contemporary corpus of English, and it seems to be useful for my application.

I plan to use [Merriam Webster](https://www.merriam-webster.com) as my dictionary of choice. It's a very respected and current dictionary of American English. I will use the entries, that I had gathered from their website a few years ago, as my vocabulary.

**A challenge**:
As alluded to above, words can have multiple entries, multiple senses and also subsenses. We may count all of them as just senses and find the *k* that way. For example, the word *main* has 2 entries in Merriam Webster:

![[main-n.png|center|400]]
<p align="center">First entry (noun)</p>

![[main-adj.png|center|400]]
<p align="center">Second entry (adjective)</p>

The first one (noun) has 5 senses, 2 of which have 2 subsenses each; the second one (adjective) has 5 senses (one (3rd) being *obsolete*, not to be counted). The number of senses may be considered as 11 from 5 + 2 + 4. We would like to differentiate between all of them and have 11 clusters.

## 5. Model

BERT large model (cased, English) from the `transformers` library of *Hugging Face*. I use the *cased* version to differentiate words in casing. Although words have the same meaning regardless of whether they are capitalized or not, proper words are capitalized and have different meanings. That's why in my approach I will not be using the capitalized words, such as the word at the start of a sentence. Proper words tend not to be represented in dictionaries comprehensively. For example, continuing with the example of the word *main*:
- *Main* is an adjective in the example below:
	> *Main* force should come from up above.
- It's a proper word here:
	> *Main* is a river of southwestern Germany. [4]

In these examples, we cannot automatically determine the *k* without the supervision of an encyclopedia.

## 6. Conclusion

If this can be done for a given dictionary, I'll try to do the same task in different dictionaries. I love dictionaries and enjoy learning whatever I can from them. This task can be done for Turkish if a dictionary sense counts of words and a current corpora is given.

This model can also be used on a historical corpus and a dictionary of the same era. It would be very interesting to see.

## References

1. [CluBERT: A Cluster-Based Approach for Learning Sense Distributions in Multiple Languages](https://aclanthology.org/2020.acl-main.369) (Pasini et al., ACL 2020)
2. [TemporalTeller at SemEval-2020 Task 1: Unsupervised Lexical Semantic Change Detection with Temporal Referencing](https://aclanthology.org/2020.semeval-1.27) (Zhou & Li, SemEval 2020)
3. [Sense representations for Portuguese: experiments with sense embeddings and deep neural language models](https://link.springer.com/article/10.1007/s10579-020-09525-1) (Rodrigues da Silva & Caseli, Language Resources & Evaluation 2021)
4. New Oxford American Dictionary, served by an [Apple](https://www.apple.com) product, 12 May 2023.