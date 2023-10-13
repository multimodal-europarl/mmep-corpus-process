# MultiModal Europarl Corpus -- process repository

This is the parent repository for development of the Multimodal Europarl Corpus (MMEP henceforth). It contains the MMEP corpus itself, a python module for working with the corpus --- `pymmep` --- and other materials related to curation, development and quality testing the corpus and the python module.

Important to note that:

* mmep-corpus
* pymmep

are git submodules. This is a design decision; in principle the corpus data, the code to use corpus data, and code for _the process_ (curating, structuring, assessing quality) are distinct and kept separate to signal this conceptualization

Many principles have been adopted directly from the [SWERIK](https://swerik-project.github.io/) project. Reference to publication(s) will come...

## Working guidelines

(unordered)

1. Work DRY-ly in corpus data and code
	- corpus data shouldn't be duplucated anywhere
	- repetative code --> pymmep function


2. Process corpus and submodules are public repositories because we _encourage_ contributions from anyone who wants to work with and improve the state of data in the corpus
	- contributions via branch->work->PR workflow
		- Pull Requests are assessed to ensure the contribution does not
			+ degrade quality of corpus data
			+ introduce bugs (unintended changes)

3. static files (audio/video, images) are not tracked in version control
	TODO:
        - how to make them available?
        - are we allowed?


4. Semantic versioning in releases to ensure backward compatibility and repetition/verification of analyses performed using corpus materials
	TODO
        - define release cycles? 


5. Usability:
    - Corpus "API" (data and user-oriented code),  under `mmep-corpus/` and `pymmep/` as submodules
	    + conceptual separation
	    + ease of interoperability without relying on the ecosystem developed in this repository

    - all code functions necessary to curate and work with data are to be part of the pymmep module
        + `scripts/` to store files containing a minimal shell to run module functions 
        + code under `scripts/` may, of course, be reused by consumers of the corpus, but not necessarily intended for that purpose
   - `IO/`, `test/` not part of API -- for "internal" use, specifically related to _the process_ (curation, structure, assessment) 