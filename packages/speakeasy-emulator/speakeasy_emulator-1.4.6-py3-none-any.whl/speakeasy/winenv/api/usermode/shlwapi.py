# Copyright (C) 2020 FireEye, Inc. All Rights Reserved.

import ntpath

from .. import api


class Shlwapi(api.ApiHandler):

    """
    Implements exported functions from shlwapi.dll
    """

    name = 'shlwapi'
    apihook = api.ApiHandler.apihook
    impdata = api.ApiHandler.impdata

    def __init__(self, emu):

        super(Shlwapi, self).__init__(emu)

        self.funcs = {}
        self.data = {}
        self.window_hooks = {}
        self.handle = 0
        self.win = None

        super(Shlwapi, self).__get_hook_attrs__(self)

    @apihook('PathIsRelative', argc=1)
    def PathIsRelative(self, emu, argv, ctx={}):
        '''
        BOOL PathIsRelativeA(
            LPCSTR pszPath
        );
        '''

        pszPath, = argv

        cw = self.get_char_width(ctx)
        pn = ''
        rv = False
        if pszPath:
            pn = self.read_mem_string(pszPath, cw)
            if '..' in pn:
                rv = True

            argv[0] = pn

        return rv

    @apihook('StrStrI', argc=2)
    def StrStrI(self, emu, argv, ctx={}):
        '''
        PCSTR StrStrI(
            PCSTR pszFirst,
            PCSTR pszSrch
        );
        '''

        hay, needle = argv

        cw = self.get_char_width(ctx)

        if hay:
            _hay = self.read_mem_string(hay, cw)
            argv[0] = _hay
            _hay = _hay.lower()

        if needle:
            needle = self.read_mem_string(needle, cw)
            argv[1] = needle
            needle = needle.lower()

        ret = _hay.find(needle)
        if ret != -1:
            ret = hay + ret
        else:
            ret = 0

        return ret

    @apihook('PathFindExtension', argc=1)
    def PathFindExtension(self, emu, argv, ctx={}):
        """LPCSTR PathFindExtensionA(
          LPCSTR pszPath
        );
        """
        pszPath, = argv
        cw = self.get_char_width(ctx)
        s = self.read_mem_string(pszPath, cw)
        argv[0] = s
        idx1 = s.rfind('\\')
        t = s[idx1 + 1:]
        idx2 = t.rfind('.')
        if idx2 == -1:
            return pszPath + len(s)

        argv[0] = t[idx2:]
        return pszPath + idx1 + 1 + idx2

    @apihook('StrCmpI', argc=2)
    def StrCmpI(self, emu, argv, ctx={}):
        """
        int StrCmpI(
        PCWSTR psz1,
        PCWSTR psz2
        );
        """
        psz1, psz2 = argv

        cw = self.get_char_width(ctx)
        s1 = self.read_mem_string(psz1, cw)
        s2 = self.read_mem_string(psz2, cw)
        rv = 1

        argv[0] = s1
        argv[1] = s2

        if s1.lower() == s2.lower():
            rv = 0

        return rv

    @apihook('PathFindFileName', argc=1)
    def PathFindFileName(self, emu, argv, ctx={}):
        """
        LPCSTR PathFindFileNameA(
          LPCSTR pszPath
        );
        """
        pszPath, = argv
        cw = self.get_char_width(ctx)
        s = self.read_mem_string(pszPath, cw)
        argv[0] = s
        idx = s.rfind('\\')
        if idx == -1:
            return pszPath + len(s)

        argv[0] = s[idx + 1:]
        return pszPath + idx + 1

    @apihook('PathRemoveExtension', argc=1)
    def PathRemoveExtension(self, emu, argv, ctx={}):
        """
        void PathRemoveExtensionA(
          LPSTR pszPath
        );
        """
        pszPath, = argv
        cw = self.get_char_width(ctx)
        s = self.read_mem_string(pszPath, cw)
        argv[0] = s
        idx1 = s.rfind('\\')
        t = s[idx1 + 1:]
        idx2 = t.rfind('.')
        if idx2 == -1:
            return pszPath

        s = s[:idx1 + 1 + idx2]
        argv[0] = s
        self.write_mem_string(s, pszPath, cw)
        return pszPath

    @apihook('PathStripPath', argc=1)
    def PathStripPath(self, emu, argv, ctx={}):
        """
        void PathStripPath(
        LPSTR pszPath
        );
        """
        pszPath, = argv
        cw = self.get_char_width(ctx)
        s = self.read_mem_string(pszPath, cw)
        argv[0] = s
        mod_name = ntpath.basename(s) + '\x00'

        enc = self.get_encoding(cw)
        mod_name = mod_name.encode(enc)
        self.mem_write(pszPath, mod_name)

    @apihook('wvnsprintfA', argc=4)
    def wvnsprintfA(self, emu, argv, ctx={}):
        """
        int wvnsprintfA(
            PSTR    pszDest,
            int     cchDest,
            PCSTR   pszFmt,
            va_list arglist
        );
        """
        buffer, count, _format, argptr = argv
        rv = 0

        fmt_str = self.read_mem_string(_format, 1)
        fmt_cnt = self.get_va_arg_count(fmt_str)

        vargs = self.va_args(argptr, fmt_cnt)

        fin = self.do_str_format(fmt_str, vargs)
        fin = fin[:count] + '\x00'

        rv = len(fin)
        self.mem_write(buffer, fin.encode('utf-8'))
        argv[0] = fin.replace('\x00', '')
        argv[1] = fmt_str

        return rv
