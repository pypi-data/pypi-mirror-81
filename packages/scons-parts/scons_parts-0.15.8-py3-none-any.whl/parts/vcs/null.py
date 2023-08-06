

import parts.api as api
import parts.common as common

from .base import base


class null_t(base):
    """an empty vcs class, used when there is no vcs object for a part to use

    This basically allow the use of the VCS object in a way that does not break any logic
    expecting an vcs object. It will basically say it is always up to data.
    """
    __slots__ = ['_path']

    def __init__(self, path=''):
        self._path = path
        super(null_t, self).__init__("", '')

    def NeedsToUpdate(self):
        return False

    @property
    def _cache_filename(self):
        # Should be implemented in derived class
        return ''

    @base.CacheFileExists.getter
    def CacheFileExists(self):
        return True

    def UpdateEnv(self):
        '''
        Update the with information about the current VCS object
        '''

        self._env['VCS'] = common.namespace(
            TYPE='null',
            CHECKOUT_DIR=self._path,
        )


null = null_t()
api.register.add_global_object('VcsLocal', null_t)
api.register.add_global_object('ScmLocal', null_t)
