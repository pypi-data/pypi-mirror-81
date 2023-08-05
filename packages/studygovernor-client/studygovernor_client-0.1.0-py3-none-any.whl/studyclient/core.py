from typing import Mapping, Optional, Union


class StudyClientBaseObject:
    def __init__(self, session, uri: str, data: Mapping):
        self.uri = uri
        self.session = session
        self._data = dict(**data)  # Copy initial data in cache to avoid fetching when only summary is required
        self.caching = True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'<{type(self).__name__} {self.uri}>'

    @property
    def logger(self):
        return self.session.logger

    # Function for getting data in a lazy/cached way when possible
    def _update_data(self):
        object_data = self.session.get_json(self.uri)
        self._data = object_data

    def _get_data_field(self, name):
        if not self.caching or name not in self._data:
            self._update_data()

        return self._data[name]

    # Some cache management methods
    def clearcache(self):
        self._data.clear()

    @property
    def caching(self):
        if self._caching is not None:
            return self._caching
        else:
            return self.session.caching

    @caching.setter
    def caching(self, value):
        self._caching = value

    @caching.deleter
    def caching(self):
        self._caching = None


class Subject(StudyClientBaseObject):
    def __init__(self,
                 session,
                 uri: Optional[str]=None,
                 data: Optional[Mapping]=None,
                 label: Optional[str]=None,
                 date_of_birth: Optional[str]=None):
        if uri is not None:
            if data is None:
                data = {}

            super().__init__(session, uri=uri, data=data)
        else:
            if not label:
                raise ValueError("Cannot create a subject without a label")
            data = {
                "label": label,
                "date_of_birth": date_of_birth,
            }

            response = session.post('/subjects', json=data)
            data = response.json()

            session.create_object(Subject, data)

    def __str__(self):
        return f'<Subject {self.label}>'

    @property
    def id(self):
        return int(self.uri.rsplit('/', 1)[1])

    @property
    def label(self):
        return self._get_data_field('label')

    @property
    def date_of_birth(self):
        return self._get_data_field('date_of_birth')

    @property
    def external_ids(self):
        return self._get_data_field('external_ids')

    @property
    def experiments(self):
        return [self.session.create_object(Experiment, x) for x in self._get_data_field('experiments')]


class Experiment(StudyClientBaseObject):
    def __init__(self,
                 session,
                 uri: Optional[str]=None,
                 data: Optional[Mapping]=None,
                 label: Optional[str]=None,
                 subject: Union[str, Subject]=None,
                 scandate: Optional[str]=None,
                 workflow: Optional[Union[str, 'Workflow']]=None):
        if uri is not None:
            if data is None:
                data = {}

            super().__init__(session, uri=uri, data=data)
        else:
            if not subject:
                raise ValueError('Need to specify a subject to create an Experiment')

            if not label:
                raise ValueError('Need to specify a label to create an Experiment')

            if isinstance(subject, Subject):
                subject = subject.label

            if isinstance(workflow, Workflow):
                workflow = workflow.label

            data = {
                "label": label,
                "subject": subject,
                "scandate": scandate,
                "workflow": workflow,
            }

            response = session.post('/subjects', json=data)
            data = response.json()

            session.create_object(Subject, data)

    def __str__(self):
        return f'<Experiment {self.label}>'

    @property
    def label(self):
        return self._get_data_field('label')

    @property
    def scandate(self):
        return self._get_data_field('scandate')

    @property
    def external_ids(self):
        return self._get_data_field('external_ids')

    @property
    def subject(self):
        return self.session.create_object(Subject, self._get_data_field('subject'))

    @property
    def state(self):
        data = self.session.get_json(self._get_data_field('state'))
        return self.session.create_object(State, data['state'])


class State(StudyClientBaseObject):
    def __str__(self):
        return f'<State {self.label}>'

    @property
    def label(self):
        return self._get_data_field('label')

    @property
    def callback(self):
        return self._get_data_field('callback')

    @property
    def lifespan(self):
        return self._get_data_field('lifespan')

    @property
    def freetext(self):
        return self._get_data_field('freetext')

    @property
    def workflow(self):
        return self.session.create_object(Workflow, self._get_data_field('workflow'))

    @property
    def experiments(self):
        data = self.session.get_json(self._get_data_field('experiments'))
        return [self.session.create_object(Experiment, x) for x in data['experiments']]


class Workflow(StudyClientBaseObject):
    def __str__(self):
        return f'<Workflow {self.label}>'

    @property
    def label(self):
        return self._get_data_field('label')

    @property
    def states(self):
        data = self.session.get_json(f'{self.uri}/states')
        return [self.session.create_object(State, x) for x in data['states']]

