# -*- coding: utf-8 -*-
# Copyright (c) 2018 Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
from luxon import g
from luxon.core.config import Config
from luxon.core.logger import GetLogger
from luxon.core.utils.app import determine_app_root
from luxon.core.config.defaults import defaults as default_config
from luxon.core.template import TachyonicLoader, Environment
from luxon.utils.timezone import format_datetime, now
from luxon.core.utils.theme import Theme

log = GetLogger(__name__)


class App(object):
    """Initialises application

    Loads the app config from the *settings.ini* file or
    from a given file

    Configures the logger for the app

    Args:
        name (str): Application name.
        path (str): Application root path.
        ini (file obj): Configuration file provided.
        defaults (bool): Load default configuration
    """

    __slots__ = ('_name', '_path', '_debug', '_config', '_jinja')

    def __init__(self, name, path=None, ini=None, defaults=True):

        # Set Application Name
        self._name = name

        # Prepare configuration object
        self._config = Config()

        # Attempt to determine application root.
        self._path = path = determine_app_root(name, path).rstrip('/')

        if defaults:
            self._config.read_dict(default_config)

        if ini is not False:
            if ini is None:
                self._config.load(path + '/settings.ini')
            else:
                self._config.load(ini)

        # Configure Logger.
        log.configure(self.config)

        # Load Templating Engine
        self._jinja = Environment(loader=TachyonicLoader(path))
        self._jinja.globals['G'] = g
        self._jinja.globals['format_datetime'] = format_datetime
        self._jinja.globals['now'] = now
        self._jinja.globals['theme'] = Theme(self)

        # Set APP globally.
        g.app = self

    @property
    def templating(self):
        return self._jinja

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def debug(self):
        try:
            return self._debug
        except AttributeError:
            try:
                self._debug = self.config.getboolean('application', 'debug')
            except Exception:
                self._debug = True
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def config(self):
        return self._config
