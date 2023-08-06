"""# Textarea"""

from ..app import db, settings
from ..functions.debug import send_keys
from ..models import Question
from .input_group import InputGroup

from flask import render_template

settings['Textarea'] = {'debug': send_keys, 'rows': 3}


class Textarea(InputGroup, Question):
    """
    Textareas provide large text boxes for free responses.

    Inherits from [`hemlock.qpolymorphs.InputGroup`](input_group.md) and 
    [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Textarea label.

    template : str, default='hemlock/textarea.html'
        Template for the textarea body.

    Attributes
    ----------
    textarea : bs4.Tag
        The `<textarea>` tag.

    Notes
    -----
    Textareas have a default javascript which displays the character and word 
    count to participants. This will be appended to any `js` and `extra_js`
    arguments passed to the constructor.

    Examples
    --------
    ```python
    from hemlock import Page, Textarea, push_app_context

    app = push_app_context()

    Page(Textarea('<p>This is a textarea.</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'textarea'}

    _html_attr_names = [
        'autofocus',
        'cols',
        'disabled',
        'maxlength',
        'placeholder',
        'readonly',
        'required',
        'rows',
        'wrap'
    ]

    @property
    def attrs(self):
        return self.textarea.attrs

    @attrs.setter
    def attrs(self, val):
        self.textarea.attrs = val
        self.body.changed()

    @property
    def textarea(self):
        return self.body.select_one('textarea#'+self.model_id)

    def __init__(self, page=None, template='hemlock/textarea.html', **kwargs):
        super().__init__(page, template, **kwargs)
        self.add_internal_js(
            render_template('hemlock/textarea.js', self_=self)
        )

    def textarea_from_driver(self, driver):
        """
        Get textarea from the webdriver for debugging.
        
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            Selenium webdriver (does not need to be `Chrome`).

        Returns
        -------
        textarea : selenium.webdriver.remote.webelement.WebElement
            Web element of the `<textarea>` tag associated with this model.
        """
        return driver.find_element_by_css_selector('textarea#'+self.model_id)

    def _render(self, body=None):
        body = body or self.body.copy()
        textarea = body.select_one('#'+self.model_id)
        textarea.string = self.response or self.default or ''
        return super()._render(body)