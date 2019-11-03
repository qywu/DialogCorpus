# DialogCorpus
A large scale dialog corpus for training the Next-Gen Dialog System.

## How to Use?

First download the repository.
```bash
# download
git clone https://github.com/qywu/DialogCorpus.git
cd DialogCorpus

# download data for the specific task
python daily_dialog/download_data.py
# process the data
python daily_dialog/process_data.py
# the processed data is stored as the {folder_name}.json
vi daily_dialog/data/daily_dialog.json
```

## Detailed Dialog Filtering Process for each dataset:
Except noted, all of the following processed dialogue contains test set of the original dataset. If you want to exclude test set, please change the dataset path in the script.

* Daily Dialog
    * Removed tokenization space for punctuations

* Persona Chat
    * Used huggingface's version [[link]](https://s3.amazonaws.com/datasets.huggingface.co/personachat/personachat_self_original.json)
    * Recovered lower cased utterances
    * Removed tokenization space for punctuations

* Cornell Movie Corpus
    * 

* conversations-gone-awry-cmv-corpus
    * replace email

* conversations-gone-awry-cmv-corpus
    * replace email
    * delete sign sentence at the beginning of dialogue. which contain "=="

* friends
    * regular process

* iq2-corpus
    * nothing left after process

* movie-corpus
    * Some sentences since lack end. But it seems overlaps with the cornell movie dataset, which may contain the full sentence.
    * delete "--" at the end of sentence. Replace "--" in the middle with ","
    
* parliament-corpus
    * since it is Q-A pair, each dialogue in it only contains one turn.
    * But Q-A contain a lot of useful knowledge and could endow the model the understanding of answer language pattern.

* persuasionforgood-corpus
    *regular process

* reddit-coarse-discourse-corpus
    * Contains some reddit feature. For example, product is mark by "**certain_product**", which is reserved.
    * Some sentence is not capitalized, which is also reserved as feature.

* subreddit-corpus
    * This contain many unusual unicode, which requires a converter from unusual character to related usual character. Or it could be fixed by find function in editor.
    Also contains some reddit feature.

* supreme-corpus
    * delete repeat words that sep by "--"
    * Also contains nonsense "--", delete "--"
    * "--" seems replacement of some text
    
* tennis-corpus
    * nothing left
    
* wiki-corpus
    * replace double dash

* wiki-politeness-annotated-corpus
    * nothing left
    
* wikiconv-corpus
    * only year 0f 2018

* winning-args-corpus
    * nothing left

###issue left:
1. should we delete all the 1 turn dialogue?
2. wiki-corpus, movie corpus takes too long to process, figure it out
3. More process on supreme
4. check all processed dataset.

Links


* [Daily Dialog](http://yanran.li/dailydialog) [[link]](https://github.com/qywu/DialogCorpus/tree/master/daily_dialog)

* [Conversational flow in Oxford-style debates](http://tisjune.github.io/research/iq2) [[link]](https://github.com/qywu/DialogCorpus/tree/master/debates)

* [Persona-chat](https://github.com/facebookresearch/ParlAI/tree/master/parlai/tasks/convai2) [[Google Drive](https://drive.google.com/open?id=1VacuNTaQo9-tXv52XaHczPxXejRuJk9T)] 


Thanks for Jing Gu processing the data. If you have questions, you can contact jkgu@ucdavis.edu.