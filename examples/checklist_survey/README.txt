README
======

This is a prototypical web application implementing checklist-style
quick surveys based on HTML check-boxes only. It uses Bootstrap for
a decent HTML layout, Bootstraptoogles for modern, mobile-friendly
check-boxes, and D3 for graphically rendering results as bubbles.


Files
-----

::

    run.py: the flask app
    templates/
        index.html: main entry point
        survey.html: a single checklist-list survey
        result_bubbles.html: a graphical result
    data/
        survey_python_use.json: sample survey data (questions)
        ballots_all.jsrec: the 'logfile' storing the individual 'votings'
    static/
        css/
            bootstrap-toggle.css
        js/
            bubbles.js: 
            bootstrap-toggle.js: 
            final_python_use.json: sample result tree to be rendered by D3


Installation
------------

.. code-block:: bash

    cd checklist_survey
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python run.py
    # open in browser...
    deactivate


Usage
-----

Open the following URLs:

- http://127.0.0.1:5000
- http://127.0.0.1:5000/surveys/python_use
- http://127.0.0.1:5000/results/python_use
