"""# Questions

`hemlock.Question` and `hemlock.ChoiceQuestion` are 'question skeletons';
most useful when fleshed out. See section on question polymorphs.
"""

from ..app import db
from .bases import Data, HTMLMixin
from .choice import Choice, Option

from flask import render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable import MutableListType, MutableModelBase, MutableType

import os
from copy import copy


class Question(HTMLMixin, Data, MutableModelBase):
    """
    Base object for questions. Questions are displayed on their page in index 
    order.

    It inherits from 
    [`hemlock.models.Data` and `hemlock.models.HTMLMixin`](bases.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Question label.

    template : str, default='form-group.html'
        Template for the question `body`.

    Attributes
    ----------
    default : sqlalchemy_mutable.MutableType
        Default question response.

    error : str or None, default=None
        Text of the question error message.

    label : str or None, default=None
        Question label.

    response : sqlalchemy_mutable.MutableType
        Participant's response.

    Relationships
    -------------
    part : hemlock.Participant or None
        The participant to which this question belongs. Derived from 
        `self.page`.

    branch : hemlock.Branch or None
        The branch to which this question belongs. Derived from `self.page`.

    page : hemlock.Page or None
        The page to which this question belongs.

    compile : list of hemlock.Compile, default=[]
        List of compile functions; run before the question is rendered.

    validate : list of hemlock.Validate, default=[]
        List of validate functions; run to validate the participant's response.

    submit : list of hemlock.Submit, default=[]
        List of submit functions; run after the participant's responses have been validated for all questions on a page.

    debug : list of hemlock.Debug, default=[]
        List of debug functions; run during debugging. The default debug function is unique to the question type.
    """
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    question_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': question_type
    }

    # relationships
    @property
    def part(self):
        return None if self.page is None else self.page.part

    @property
    def branch(self):
        return None if self.page is None else self.page.branch

    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    compile = db.relationship(
        'Compile',
        backref='question',
        order_by='Compile.index',
        collection_class=ordering_list('index')
    )

    validate = db.relationship(
        'Validate', 
        backref='question', 
        order_by='Validate.index',
        collection_class=ordering_list('index')
    )
    
    submit = db.relationship(
        'Submit',
        backref='question',
        order_by='Submit.index',
        collection_class=ordering_list('index')
    )

    _debug_functions = db.relationship(
        'Debug',
        backref='question',
        order_by='Debug.index',
        collection_class=ordering_list('index')
    )

    @property
    def debug(self):
        return self._debug_functions

    @debug.setter
    def debug(self, val):
        if os.environ.get('DEBUG_FUNCTIONS') != 'False':
            self._debug_functions = val

    # Column attributes
    default = db.Column(MutableType)
    response = db.Column(MutableType)
    has_responded = db.Column(db.Boolean, default=False)

    def __init__(self, label='', template=None, **kwargs):
        kwargs['label'] = label
        super().__init__(template, **kwargs)

    # BeautifulSoup shortcuts
    @property
    def error(self):
        return self.body.text('.error-txt')

    @error.setter
    def error(self, val):
        """
        Add the 'error' class to the form-group tag and set the error text
        """
        form_grp_cls = self.body.select_one('div.form-group')['class']
        if not val:
            try:
                form_grp_cls.remove('error')
            except:
                pass
        elif 'error' not in form_grp_cls:
            form_grp_cls.append('error')
        self.body.set_element('span.error-txt', val)

    @property
    def form_group(self):
        return self.body.select_one('div.form-group')

    @property
    def label(self):
        return self.body.text('.label-txt')

    @label.setter
    def label(self, val):
        self.body.set_element('.label-txt', val)

    # methods
    def clear_error(self):
        """
        Clear the error message.

        Returns
        -------
        self : hemlock.Question
        """
        self.error = None
        return self

    def clear_response(self):
        """
        Clear the response.

        Returns
        -------
        self : hemlock.Question
        """
        self.response = None
        self.has_responded = False
        return self

    # methods executed during study
    def _compile(self):
        [f(self) for f in self.compile]
        return self

    def _render(self, body=None):
        return body or self.body.copy()

    def _record_response(self):
        self.has_responded = True
        self.response = request.form.get(self.model_id)
        return self
        
    def _validate(self):
        """Validate Participant response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for f in self.validate:
            error = f(self)
            if error:
                self.error = error
                return False
        self.error = None
        return True

    def _record_data(self):
        self.data = self.response
        return self
    
    def _submit(self):
        [f(self) for f in self.submit]
        return self

    def _debug(self, driver):
        [f(driver, self) for f in self.debug]
        return self


class ChoiceQuestion(Question):
    """
    A question which contains choices. Inherits from `hemlock.Question`.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Question label.

    choices : list, default=[]
        Choices which belong to this question. List items are usually 
        `hemlock.Choice` or `hemlock.Option`.

    template : str or None, default=None
        Template for the question body.

    Attributes
    ----------
    choices : list, default=[]
        Set from `choices` parameter.

    choice_cls : class, default=hemlock.Choice
        Class of the choices in the `choices` list.

    multiple : bool, default=False
        Indicates that the participant can select multiple choices.

    Notes
    -----
    `choices` can be set using the following formats:
    1. list of choice objects.
    2. list of `str`, treated as choice labels.
    3. list of `(choice label, value)` tuples.
    4. list of `(choice label, value, name)` tuples.
    5. list of dictionaries with choice keyword arguments.
    """
    multiple = db.Column(db.Boolean, default=False)
    choice_cls = Choice
    _choices = db.Column(MutableListType)

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, choices):
        def convert(choice):
            if isinstance(choice, self.choice_cls):
                return choice
            if isinstance(choice, dict):
                return self.choice_cls(**choice)
            if isinstance(choice, (tuple, list)):
                if len(choice) == 2:
                    return self.choice_cls(label=choice[0], value=choice[1])
                if len(choice) == 3:
                    return self.choice_cls(
                        label=choice[0], value=choice[1], name=choice[2]
                    )
            return self.choice_cls(label=str(choice))
        
        self._choices = [convert(choice) for choice in choices]

    def __init__(self, label='', choices=[], template=None, **kwargs):
        self.choices = choices
        super().__init__(label, template, **kwargs)

    def _render(self, body=None):
        """Add choice HTML to `body`"""
        body = body or self.body.copy()
        choice_wrapper = body.select_one('.choice-wrapper')
        [
            choice_wrapper.append(choice._render(self, idx)) 
            for idx, choice in enumerate(self.choices)
        ]
        return body

    def _record_response(self):
        """Record response

        The response is a single choice or a list of choices (if multiple 
        choices are allowed).
        """
        self._has_responded = True
        idx = request.form.getlist(self.model_id)
        self.response = [self.choices[int(i)].value for i in idx]
        if not self.multiple:
            self.response = self.response[0] if self.response else None
        return self

    def _record_data(self):
        """Record data

        For single choice questions, the data is the selected choice's 
        `value`.

        For multiple choice questions, the data is a dictionary mapping 
        each choice's `value` to a binary indicator that it was selected.
        """
        if self.multiple:
            self.data = {
                choice.value: int(choice.value in self.response)
                for choice in self.choices
            }
        else:
            self.data = self.response
        return self
    
    def _pack_data(self):
        """Pack data for storage in the `DataStore`

        For multiple choice questions, the packed data dictionary is similar to the data, but with the question's variable prepended to the key.
        """
        var = self.var
        if not self.multiple or var is None:
            return super()._pack_data()
        if self.data is None:
            packed_data = {
                var+c.value: None 
                for c in self.choices if c.value is not None
            }
        elif isinstance(self.data, dict):
            packed_data = {var+key: val for key, val in self.data.items()}
        else:
            packed_data = self.data
        return super()._pack_data(packed_data)