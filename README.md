# Home task for adjust

It is a basic app to expose the sample dataset using Django.


### Built With
-   Django
-   Django REST Framework
-   Python3.7


## Installation

 1. Clone the repository ```git clone https://github.com/gedomer/adjust_task.git```
 2. Create and active your python3 environment
 3. Install requirements ```cd adjust_task && pip install -r requirements/dev.txt```
 4. Copy example env file in ```"config/"``` into root of project as .env.
 5. Run ```python manage.py migrate```
 6. Create initial data: ```python manage.py import_metrics --file=dataset_path.```
 (Sample dataset: `https://gist.github.com/kotik/3baa5f53997cce85cc0336cb1256ba8b/`).
 7. Start development server ```python manage.py runserver 0.0.0.0:8002```

### Run tests

 Run ```python manage.py test```
