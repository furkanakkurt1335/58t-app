Furkan Akkurt, 20 May

## Implementation

- Python<sup>1</sup>
	- Programming language used in the implementation.
- Libraries
	- `transformers`<sup>2</sup>
		- `BertTokenizer` and `BertModel` modules
			- I average the last 4 layers in calculation of token representations (embeddings), as suggested by the authors of the BERT paper.<sup>5</sup>
		- `AutoConfig` module to get access to all the hidden states
	- `torch`<sup>3</sup>
		- Used in converting lists to tensors (`tensor` function) and creating a tensor of ones (`ones_like` function).
	- `scipy`<sup>4</sup>
		- `cosine` function in the `spatial.distance` module, used to calculate embedding distances.
			- Since generally cosine similarity is used to compare word embeddings, I'm also using cosine similarity to calculate distances between individual embeddings.
	- `pandas`<sup>6</sup>
		- Reading *xlsx* files gotten from `wordfrequency.info`.

## Datasets

- Words to detect changes of: Since the entire language is quite infeasible to tackle at the moment, I will be focusing on a set of *most frequent* nouns in the English language that I have gotten from `wordfrequency.info`<sup>8</sup> that's been calculated on COCA<sup>7</sup>.
- Senses: I have gotten access to the Merriam-Webster Dictionary API<sup>11</sup> to calculate the sense counts in their dictionary.
	- I have worked on gathering sense counts for the most frequent 2500~ nouns in the script `src/gather_senses.py`. The code is mostly written. There are some differences in the response data for different nouns, I need to take them into account.
- Corpus: I will use *COCA*<sup>7</sup> itself to figure out the smallest distance necessary for a sense distinction in a dictionary and also calculate distances for an eventual sense shift detection. I have gotten a significantly large and *free* sample of the corpus from `corpusdata.org`<sup>9</sup>, since the corpus itself is proprietary.

## Experiments

I have experimented with manually created sentences which clearly have certain words in different senses to see if the cosine distance with the embeddings from *BERT* is capable of capturing the distinction.

### Example

- I have calculated the distances of the token `bank`'s embeddings between pairs of the following 4 sentences:
	1. The river *bank* was full of dead fishes.
	2. The *bank* was closed since it was Sunday.
	3. I went to the *bank* to deposit my money.
	4. I went to the *bank* to withdraw my money.
- Cosine distances between the following pairs of sentences are
	- 1-2: $0.2266$,
	- 1-3: $0.3717$,
	- 1-4: $0.3458$,
	- 2-3: $0.3333$,
	- 2-4: $0.3063$,
	- 3-4: $0.0241$.

It's expected that the 3rd and 4th embeddings of the token `bank` is very close. On the other hand, it's surprising that the second smallest distance is between the 1st and 2nd usages which are not of the same meaning. I need to find a better way of distinguishing semantic differences represented by quite different sentences but with clearly same usages of words.

## Repository

I'm putting all the code and references in a repository<sup>10</sup>.

## References

1. [Welcome to Python.org](https://www.python.org)
2. [🤗 Transformers](https://huggingface.co/docs/transformers/index)
3. [PyTorch](https://pytorch.org)
4. [SciPy](https://scipy.org)
5. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (Devlin et al., ACL 2019)
6. [pandas - Python Data Analysis Library](https://pandas.pydata.org)
7. [English-Corpora: COCA](https://www.english-corpora.org/coca)
8. [Word frequency: based on one billion word COCA corpus](https://www.wordfrequency.info/samples.asp)
9. [Full-text data from English-Corpora.org: billions of words of downloadable data](https://www.corpusdata.org/formats.asp)
10. [furkanakkurt1335/58t-app: Application project for CMPE58T](https://github.com/furkanakkurt1335/58t-app)
11. [Merriam-Webster Dictionary API](https://www.dictionaryapi.com)
