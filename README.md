# [FAIR](https://www.go-fair.org/fair-principles/) metadata html page generator

### Description

A simple Python script to generate a static [HTML](https://html.spec.whatwg.org/) page for viewing a [JSON-LD](https://json-ld.org/) metadata description of a dataset using [Schema.org](https://schema.org/) markup vocabulary.

[Structured](https://developers.google.com/search/docs/guides/intro-structured-data), machine-readable metadata about datasets are helpful for improving the [Findability, Accessibility, Interoperability and Reusability](https://www.go-fair.org/fair-principles/) of data. [Google](https://www.google.com/), for example, is gradually developing support for [dataset search tools](https://datasetsearch.research.google.com/) to help researchers find and reuse relevant data. Providing machine-readable descriptions of datasets is helpful for search engine indexing software to process and display data descriptions to users.

I have developed a Python script [here](https://github.com/kodymoodley/fair-metadata-generator) to generate such a description in JSON-LD using [Schema.org](https://schema.org/) markup vocabulary. 

However, after this JSON-LD description is generated, it is often useful to publish a webpage describing the content of the JSON-LD file for viewing by humans. Given an input JSON-LD file describing a dataset, the script ``jsonld_to_html.py`` generates a single static HTML page accomplishing this.

### Requirements

+ [Python 3.7+](https://www.python.org/downloads/)
+ Python libraries specified in ``requirements.txt`` in this repository
+ A JSON-LD file compliant with the [Schema.org](https://schema.org/) [Dataset](https://schema.org/Dataset) entity description. If you do not have one of these files at hand, you can generate one using [this tool](https://github.com/kodymoodley/fair-metadata-generator). Alternatively, there is an example file under ``testdata/inputdata/`` in this repository.

To install the required libraries in ``requirements.txt`` run: ``pip install -r requirements.txt`` in your command line environment (after installing Python).

### Usage

Run ``python jsonld_to_html.py <relative path to input json-ld file> <relative path to output html file>`` in your command line environment after installing Python and the required libraries. For example: ``python jsonld_to_html.py testdata/inputdata/test.jsonld testdata/outputdata/test.html``

**Note:** the styling of the output HTML page(s) is defined in the ``style.css`` [CSS](https://www.w3.org/TR/css-2020/) file located in ``testdata/outputdata/``. If you prefer a different styling, this is the file to modify. The output HTML files also expect the CSS file to be located in a folder called ``css/`` in the same directory as the output HTML file(s). 

### Developer notes

This tool makes use of the [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) templating engine for Python. I have defined an HTML template ``templates/html_template.html`` in this repository. If you would like to customise your HTML files for viewing the JSON-LD metadata, you can modify this template or add new custom templates in this folder. You would then need to update references to this template file in ``jsonld_to_html.py`` and also make necessary modifications to the ``mappings/jsonld_to_htmltemplate_mapping.csv`` file. This file defines a mapping between JSON-LD keys for Schema.org [datasets](https://schema.org/Dataset) and the Jinja variables (in the HTML template file) that should hold the values for these keys. I plan to include the mapping file and the HTML template as arguments for the ``json_to_html.py`` script in the near future.

### License and contributions

The FAIR metadata html page generator is copyrighted by [Kody Moodley](https://sites.google.com/site/kodymoodley/) and released under the [GNU Affero License](https://www.gnu.org/licenses/agpl-3.0.txt)

Contributions and bug reports are helpful and welcome.

