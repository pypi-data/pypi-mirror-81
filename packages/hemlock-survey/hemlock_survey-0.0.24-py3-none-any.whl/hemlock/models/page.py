"""# Page

The survey 'flow' is:

1. **Compile.** Execute a page's compile functions. By default, a page's 
first compile function runs its questions' compile methods in index order.

2. **Render.** Render the page for the participant and wait for them to 
respond.

3. **Record response.** Record the participant's response to every question on
the page. This sets the `response` attribute of the questions.

4. **Validate.** When the participant attempts to submit the page, validate 
the responses. As with the compile method, the validate method executes a 
page's validate functions in index order. By default, a page's first 
validate function runs its questions' validate methods in index order.

5. **Record data.** Record the data associated with the participant's
responses to every question on the page. This sets the `data` attribute of the
questions.

6. **Submit.** Execute the page's submit functions. By default, a page's 
first submit function runs its questions' submit methods in index order.

7. **Navigate.** If the page has a navigate function, create a new branch 
originating from this page.
"""

from ..app import db, settings
from ..tools import Img
from .bases import BranchingBase, HTMLMixin
from .embedded import Timer
from .worker import _set_worker
from .functions import Compile, Validate, Submit, Debug

from bs4 import BeautifulSoup, Tag
from flask import Markup, current_app, render_template, request
from sqlalchemy import inspect
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable import MutableType
from sqlalchemy_mutablesoup import MutableSoupType

import os
import re
import webbrowser
from random import shuffle, random
from tempfile import NamedTemporaryFile
from time import sleep

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

BANNER = Img(src='/hemlock/static/img/hemlock_banner.png', align='center')
BANNER.img['style'] = 'max-width:200px;'
BANNER.img['alt'] = 'Hemlock banner'

@Compile.register
def compile_questions(page):
    """
    Execute the page's questions' compile methods in index order.

    Parameters
    ----------
    page : hemlock.Page
    """
    [q._compile() for q in page.questions]

@Validate.register
def validate_questions(page):
    """
    Execute the page's questions' validate methods in index order.

    Parameters
    ----------
    page : hemlock.Page
    """
    [q._validate() for q in page.questions]
    
@Submit.register
def submit_questions(page):
    """
    Execute the page's questions' submit methods in index order.

    Parameters
    ----------
    page : hemlock.Page
    """
    [q._submit() for q in page.questions]

@Debug.register
def debug_questions(driver, page):
    """
    Execute the page's questions' debug methods in  *random* order.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page
    """
    order = list(range(len(page.questions)))
    shuffle(order)
    [page.questions[i]._debug(driver) for i in order]

@Debug.register
def navigate(driver, page, p_forward=.8, p_back=.1, sleep_time=3):
    """
    Randomly navigate forward or backward, or refresh the page. By default, it
    is executed after the default page debug function.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    page : hemlock.Page

    p_forward : float, default=.8
        Probability of clicking the forward button.

    p_back : float, default=.1
        Probability of clicking the back button.

    sleep_time : float, default=3
        Number of seconds to sleep if there is no forward or back button on
        the page.

    Notes
    -----
    The probability of refreshing the page is `1-p_forward-p_back`.
    """
    forward_exists = back_exists = True
    if random() < p_forward:
        try:
            return driver.find_element_by_id('forward-btn').click()
        except:
            forward_exists = False
    if random() < p_back / (1 - p_forward):
        try:
            return driver.find_element_by_id('back-btn').click()
        except:
            back_exists = False
    if not (forward_exists or back_exists):
        sleep(sleep_time)
        navigate(driver, page, p_forward, p_back, sleep_time)
    driver.refresh()

settings['Page'] = {
    'css': open(os.path.join(DIR_PATH, 'page-css.html'), 'r').read(),
    'js': open(os.path.join(DIR_PATH, 'page-js.html'), 'r').read(),
    'back': False,
    'forward': True,
    'banner': BANNER.render(),
    'terminal': False,
    'compile': compile_questions,
    'validate': validate_questions,
    'submit': submit_questions,
    'debug': [debug_questions, navigate],
}


class Page(HTMLMixin, BranchingBase, db.Model):
    """
    Pages are queued in a branch. A page contains a list of questions which it
    displays to the participant in index order.
    
    It inherits from [`hemlock.model.HTMLMixin`](bases.md).

    Parameters
    ----------
    \*questions : list of hemlock.Question, default=[]
        Questions to be displayed on this page.

    template : str, default='hemlock/page-body.html'
        Template for the page `body`.

    Attributes
    ----------
    back : str or None, default=None
        Text of the back button. If `None`, no back button will appear on the 
        page. You may also set `back` to `True`, which will set the text to 
        `'<<'`.

    banner : str or bs4.Tag, default=hemlock banner
        Banner at the bottom of the page.

    cache_compile : bool, default=False
        Indicates that this page should cache the result of its compile 
        functions. Specifically, it removes all compile functions and the 
        compile worker from the page self `self._compile` is called.

    direction_from : str or None, default=None
        Direction in which the participant navigated from this page. Possible 
        values are `'back'`, `'invalid'`, or `'forward'`.

    direction_to : str or None, default=None
        Direction in which the participant navigated to this page. Possible 
        values are `'back'`, `'invalid'`, and `'forward'`.

    error : str or None, default=None
        Text of the page error message.

    forward : str or None, default='>>'
        Text of the forward button. If `None`, no forward button will appear 
        on the page. You may also set `forward` to `True`, which will set the 
        text to `'>>'`.

    g : dict, default={}
        Dictionary of miscellaneous objects.

    index : int or None, default=None
        Order in which this page appears in its branch's page queue.

    navbar : sqlalchemy_mutablesoup.MutableSoupType
        Navigation bar.

    terminal : bool, default=False
        Indicates that the survey terminates on this page.

    viewed : bool, default=False
        Indicates that the participant has viewed this page.

    Relationships
    -------------
    part : hemlock.Participant or None, default=None
        Participant to which this page belongs. Read only; derived from `self.
        branch`.

    branch : hemlock.Branch or None, default=None
        Branch to which this page belongs.

    next_branch : hemlock.Branch or None, default=None
        Branch which originated from this page. This is automatically set 
        when this page runs its navigate function.

    back_to : hemlock.Page or None
        Page to which this page navigates when going back. If `None`, this 
        page navigates back to the previous page.

    forward_to : hemlock.Page or None
        Page to which this page navigates when going forward. If `None`, this 
        page navigates to the next page.

    embedded : list of hemlock.Embedded, default=[]
        List of embedded data elements.

    timer : hemlock.Timer or None, default=hemlock.Timer
        Tracks timing data for this page.
        1. Timer can be set as a `Timer` object.
        2. Setting `timer` to a `str` or `None` sets the timer object 
        variable.
        3. Setting `timer` to a `tuple` sets the timer object variable and 
        data rows.
        4. Setting `timer` to a `dict` sets the timer object attributes. The
        `dict` maps attribute names to values.

    questions : list of hemlock.Question, default=[]
        List of questions which this page displays to its participant.

    data_elements : list of hemlock.DataElement
        List of data elements which belong to this page; in order, `self.
        timer`, `self.embedded`, `self.questions`.

    compile : list of hemlock.Compile
        List of compile functions; run before the page is rendered. The 
        default page compile function runs its questions' compile functions 
        in index order.

    compile_worker : hemlock.Worker or None, default=None
        Worker which sends the compile functions to a Redis queue.

    validate : list of hemlock.Validate
        List of validate functions; run to validate participant responses. 
        The default page validate function runs its questions' validate 
        functions in index order.

    validate_worker : hemlock.Worker or None, default=None
        Worker which sends the validate functions to a Redis queue.

    submit : list of hemlock.Submit
        List of submit functions; run after participant responses have been 
        validated. The default submit function runs its questions' submit 
        functions in index order.

    submit_worker : hemlock.Worker or None, default=None
        Worker which sends the submit functions to a Redis queue.

    navigate : hemlock.Navigate or None, default=None
        Navigate function which returns a new branch originating from this 
        page.

    navigate_worker : hemlock.Worker
        Worker which sends the navigate function to a Redis queue.

    debug_functions : list of hemlock.Debug
        List of debug functions; run during debugging. The default debug 
        function runs its questions' debug functions in *random* order.

    Examples
    --------
    ```python
    from hemlock import Page, push_app_context

    app = push_app_context()

    Page(Label('<p>Hello World</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # relationships
    @property
    def part(self):
        return None if self.branch is None else self.branch.part

    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _branch_head_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    next_branch = db.relationship(
        'Branch',
        back_populates='origin_page',
        uselist=False,
        foreign_keys='Branch._origin_page_id'
    )
    
    _back_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    back_to = db.relationship(
        'Page',
        foreign_keys=_back_to_id,
        remote_side=[id]
    )
        
    _forward_to_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    forward_to = db.relationship(
        'Page',
        foreign_keys=_forward_to_id,
        remote_side=[id]
    )
    
    embedded = db.relationship(
        'Embedded',
        backref='page',
        order_by='Embedded.index',
        collection_class=ordering_list('index'),
    )

    _timer = db.relationship(
        'Timer', 
        uselist=False,
        foreign_keys='Timer._timed_page_id'
    )

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, val):
        if isinstance(val, Timer):
            self._timer = val
            return
        if not hasattr(self, '_timer') or self._timer is None:
            self._timer = Timer()
        if isinstance(val, str) or val is None:
            self._timer.var = val
        elif isinstance(val, tuple):
            self._timer.var, self._timer.data_rows = val
        elif isinstance(val, dict):
            [setattr(self._timer, key, value) for key, value in val.items()]
        else:
            raise ValueError('Invalid value {} for timer'.format(val))        

    questions = db.relationship(
        'Question', 
        backref='page',
        order_by='Question.index',
        collection_class=ordering_list('index')
    )

    @property
    def data_elements(self):
        timer = [self.timer] if self.timer else []
        return self.embedded + timer + self.questions
    
    compile = db.relationship(
        'Compile',
        backref='page',
        order_by='Compile.index',
        collection_class=ordering_list('index')
    )
    _compile_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._compile_id'
    )

    @property
    def compile_worker(self):
        return self._compile_worker

    @compile_worker.setter
    def compile_worker(self, val):
        _set_worker(self, val, self._compile, '_compile_worker')

    validate = db.relationship(
        'Validate',
        backref='page',
        order_by='Validate.index',
        collection_class=ordering_list('index')
    )
    _validate_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._validate_id'
    )

    @property
    def validate_worker(self):
        return self._validate_worker

    @validate_worker.setter
    def validate_worker(self, val):
        _set_worker(self, val, self._validate, '_validate_worker')

    submit = db.relationship(
        'Submit',
        backref='page',
        order_by='Submit.index',
        collection_class=ordering_list('index')
    )
    _submit_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._submit_id'
    )

    @property
    def submit_worker(self):
        return self._submit_worker

    @submit_worker.setter
    def submit_worker(self, val):
        _set_worker(self, val, self._submit, '_submit_worker')

    navigate = db.relationship(
        'Navigate', 
        backref='page', 
        uselist=False
    )
    _navigate_worker = db.relationship(
        'Worker', uselist=False, foreign_keys='Worker._navigate_page_id'
    )

    @property
    def navigate_worker(self):
        return self._navigate_worker

    @navigate_worker.setter
    def navigate_worker(self, val):
        _set_worker(self, val, self._navigate, '_navigate_worker')

    _debug_functions = db.relationship(
        'Debug',
        backref='page',
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
    cache_compile = db.Column(db.Boolean)
    direction_from = db.Column(db.String(8))
    direction_to = db.Column(db.String(8))
    g = db.Column(MutableType)
    index = db.Column(db.Integer)
    navbar = db.Column(MutableSoupType)
    terminal = db.Column(db.Boolean)
    viewed = db.Column(db.Boolean, default=False)

    def __init__(
            self, *questions, template='hemlock/page-body.html', **kwargs
        ):
        self.questions = list(questions)
        kwargs['timer'] = kwargs['timer'] if 'timer' in kwargs else None
        super().__init__(template, **kwargs)

    # BeautifulSoup shortcuts
    @property
    def error(self):
        return self.body.text('div.error-msg')

    @error.setter
    def error(self, val):
        self.body.set_element(
            'span.error-msg', val,
            target_selector='div.error-msg', 
            gen_target=self._gen_error
        )

    def _gen_error(self):
        """Generate error tag"""
        err = Tag(name='div')
        err['class'] = 'error-msg alert alert-danger w=100'
        err['style'] = 'text-align: center;'
        return err

    @property
    def back(self):
        return self.body.text('#back-btn')

    @back.setter
    def back(self, val):
        val = '<<' if val is True else val
        self.body.set_element(
            'span.back-btn', val,
            target_selector='#back-btn', 
            gen_target=self._gen_submit,
            args=['back']
        )

    @property
    def forward(self):
        return self.body.text('#forward-btn')

    @forward.setter
    def forward(self, val):
        val = '>>' if val is True else val
        self.body.set_element(
            'span.forward-btn', val,
            target_selector='#forward-btn', 
            gen_target=self._gen_submit,
            args=['forward']
        )

    def _gen_submit(self, direction):
        """Generate submit (back or forward) button"""
        btn = Tag(name='button')
        btn['id'] = direction+'-btn'
        btn['name'] = 'direction'
        btn['type'] = 'submit'
        btn['class'] = 'btn btn-outline-primary'
        float_ = 'left' if direction == 'back' else 'right'
        btn['style'] = 'float: {};'.format(float_)
        btn['value'] = direction
        return btn

    @property
    def banner(self):
        return self.body.select_one('span.banner')
    
    @banner.setter
    def banner(self, val):
        self.body.set_element('span.banner', val)

    # methods
    def clear_error(self):
        """
        Clear the error message from this page and all of its questions.

        Returns
        -------
        self : hemlock.Page
        """
        self.error = None
        [q.clear_error() for q in self.questions]
        return self
    
    def clear_response(self):
        """
        Clear the response from all of this page's questions.

        Returns
        -------
        self : hemlock.Page
        """
        [q.clear_response() for q in self.questions]
        return self
    
    def first_page(self):
        """
        Returns
        -------
        is_first_page : bool
            Indicator that this is the first page in its participant's survey.
        """
        if self.part is None:
            return False
        for b in self.part.branch_stack:
            if b.pages:
                first_nonempty_branch = b
                break
        return self.branch == first_nonempty_branch and self.index == 0

    def is_valid(self):
        """
        Returns
        -------
        valid : bool
            Indicator that all of the participant's responses are valid. That 
            is, that there are no error messages on the page or any of its 
            questions.
        """
        return not (self.error or any([q.error for q in self.questions]))

    def preview(self, driver=None):
        """
        Preview the page in a browser window.

        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver or None, default=None
            Driver to preview page debugging. If `None`, the page will be
            opened in a web browser.

        Returns
        -------
        self : hemlock.Page

        Notes
        -----
        If running in WSL, first specify the distribution as an environment
        variable. For example, if running in Ubuntu:

        ```bash
        $ export WSL_DISTRIBUTION=Ubuntu
        ```

        This method does not run the compile functions.
        """
        dist = os.environ.get('WSL_DISTRIBUTION')
        soup = self._render(as_str=False)
        self._convert_rel_paths(soup, 'href', dist)
        self._convert_rel_paths(soup, 'src', dist)
        with NamedTemporaryFile('w', suffix='.html', delete=False) as f:
            f.write(str(soup))
            uri = 'file://'+('wsl$/'+ dist + f.name if dist else f.name)
            if hasattr(current_app, 'tmpfiles'):
                current_app.tmpfiles.append(f.name)
        if driver is None:
            webbrowser.open(uri)
        else:
            driver.get(uri)
        return self

    def _convert_rel_paths(self, soup, url_attr, dist=None):
        """
        Convert relative url paths to local file paths for preview.

        Parameters
        ----------
        soup : bs4.BeautifulSoup
            Soup whose elements with url attributes will be converted.

        url_attr : str
            Name of the url attribute (e.g. `'src'` or `'href'`).

        dist : str or None, default=None
            WSL distribution.
        """
        def get_local_path(url, static_folder, static_url_path):
            return dist + static_folder + url[len(static_url_path):]

        dist = '/'+dist if dist else ''
        app_static_url_path = current_app.static_url_path
        app_static_folder = current_app.static_folder
        hlk = current_app.blueprints['hemlock']
        hlk_static_url_path = hlk.static_url_path
        hlk_static_folder = hlk.static_folder

        elements = soup.select('[{}]'.format(url_attr))
        for e in elements:
            url = e.attrs.get(url_attr)
            if url is not None:
                if url.startswith(app_static_url_path):
                    e.attrs[url_attr] = get_local_path(
                        url, app_static_folder, app_static_url_path
                    )
                elif url.startswith(hlk_static_url_path):
                    e.attrs[url_attr] = get_local_path(
                        url, hlk_static_folder, hlk_static_url_path
                    )

    def view_nav(self, indent=0):
        """
        Print the navigation starting at this page for debugging purposes.
        
        Parameters
        ----------
        indent : int, default=0
            Starting indentation.

        Returns
        -------
        self : hemlock.Page
        """
        # Note to self: the commented lines were very useful for me when 
        # debugging the navigation system; less so for users

        # HEAD_PART = '<== head page of participant'
        # HEAD_BRANCH = '<== head page of branch'
        HEAD_PART = 'C '
        head_part = HEAD_PART if self == self.part.current_page else ''
        # head_branch = HEAD_BRANCH if self == self.branch.current_page else ''
        # print(' '*indent, self, head_branch, head_part)
        terminal = 'T' if self.terminal else ''
        print(' '*indent, self, head_part+terminal)
        if self.next_branch in self.part.branch_stack:
            self.next_branch.view_nav()
        return self

    # methods executed during study
    def _compile(self):
        """
        Run the page's compile functions. If `self.cache_compile`, the page's 
        compile functions and compile worker are removed.

        Returns
        -------
        self
        """
        if inspect(self).detached:
            # self will be detached if _compile is called from Redis
            self = Page.query.get(self.id)
        [f(self) for f in self.compile]
        if self.cache_compile:
            self.compile.clear()
            self.compile_worker = None
        if self.timer is not None:
            self.timer.start()
        return self
    
    def _render(self, as_str=True):
        """Render page
        
        This method performs the following functions:
        1. Add participant metadata if in test mode
        2. Remove submit buttons if applicable
        3. Append question HTML

        Parameters
        ----------
        as_str : bool, default=True
            Return rendered html as `str` as opposed to `bs4.BeautifulSoup`.

        Returns
        -------
        rendered : str or bs4.BeautifulSoup
        """
        html = render_template('hemlock/page.html', page=self)
        soup = BeautifulSoup(html, 'html.parser')
        self._add_part_metadata(soup)
        self._handle_btns(soup)
        question_html = soup.select_one('span.question-html')
        [question_html.append(q._render()) for q in self.questions]
        return str(soup) if as_str else soup
    
    def _add_part_metadata(self, soup):
        """Add page metadata to soup
        
        Metadata is the page's participant's `id` and strongly random `key`. 
        For security, these must match for a participant to access a page.

        Metadata are only necessary for debugging, where a researcher may 
        want to have multiple survey windows open simultaneously. In this 
        case, page metadata are used to associate participants with their 
        pages, rather than Flask-Login's `current_user`.

        To use this functionality, access the URL as {ULR}/?Test=1.
        """
        if self.part is not None and self.part.meta.get('Test') == '1':
            meta_html = render_template('hemlock/page-meta.html', page=self)
            meta_soup = BeautifulSoup(meta_html, 'html.parser')
            form = soup.select_one('form')
            if form is not None:
                form.insert(0, meta_soup)
    
    def _handle_btns(self, soup):
        """Handle submit buttons

        Back button should not be present on the first page of the survey.
        Forward button should not be present on the terminal page.
        """
        if not self.back or self.first_page():
            back_btn = soup.select_one('span.back-btn')
            if back_btn is not None:
                back_btn.clear()
        if not self.forward or self.terminal:
            forward_btn = soup.select_one('span.forward-btn')
            if forward_btn is not None:
                forward_btn.clear()

    def _record_response(self):
        """Record participant response
        
        Begin by updating the total time. Then get the direction the 
        participant requested for navigation (forward or back). Finally, 
        record the participant's response to each question.
        """
        if self.timer is not None:
            self.timer.pause()
        self.direction_from = request.form.get('direction')
        [q._record_response() for q in self.questions]
        return self
    
    def _validate(self):
        """Validate response
        
        Check validate functions one at a time. If any returns an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        if inspect(self).detached:
            self = Page.query.get(self.id)
        self.error = None
        for f in self.validate:
            error = f(self)
            if error:
                self.error = error
                break
        is_valid = self.is_valid()
        self.direction_from = 'forward' if is_valid else 'invalid'
        return is_valid
    
    def _submit(self):
        if inspect(self).detached:
            self = Page.query.get(self.id)
        [q._record_data() for q in self.questions]
        [f(self) for f in self.submit]
        return self

    def _debug(self, driver):
        [f(driver, self) for f in self.debug]
        return self