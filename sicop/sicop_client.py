"""Cliente automatizado de SICOP (sicop.com.ar) para descargar el 'Estado de Situación'
de proveedores/fleteros. No usa navegador (el entorno lo bloquea): replica el flujo
ASP.NET WebForms por HTTP directo.

Credenciales por variable de entorno (NUNCA hardcodear):
    SICOP_USER, SICOP_PASS

Flujo:
    login -> seleccionar empresa (Cambiar Cuenta) -> Proveedores -> Filtrar
    -> por cada CUIT: leer token 'prosta' de la fila -> ProveedorEdit
    -> cargar widget Estado de Situación -> descargar .xlsx
"""
import os, re, subprocess, tempfile
from html.parser import HTMLParser

BASE = 'https://sicop.com.ar/Argentina'
INICIO = BASE + '/Privado/Inicio.aspx'
DEFAULT = BASE + '/Default.aspx'
PROVLIST = BASE + '/Privado/Proveedores/ProveedorList.aspx'
CA = '/root/.ccr/ca-bundle.crt'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')


class _Form(HTMLParser):
    def __init__(self):
        super().__init__(); self.f = {}; self._cs = None; self._co = []; self._sv = None; self._ta = None
    def handle_starttag(self, t, at):
        a = dict(at)
        if t == 'input':
            n = a.get('name')
            if not n: return
            ty = (a.get('type') or 'text').lower()
            if ty in ('submit', 'button', 'image', 'reset'): return
            if ty in ('checkbox', 'radio'):
                if 'checked' in a: self.f[n] = a.get('value', 'on')
            else:
                self.f[n] = a.get('value', '')
        elif t == 'select':
            self._cs = a.get('name'); self._co = []; self._sv = None
        elif t == 'option' and self._cs:
            v = a.get('value', '')
            if 'selected' in a: self._sv = v
            self._co.append(v)
        elif t == 'textarea':
            self._ta = a.get('name'); self._tx = ''
    def handle_data(self, d):
        if self._ta is not None: self._tx += d
    def handle_endtag(self, t):
        if t == 'select' and self._cs:
            self.f[self._cs] = self._sv if self._sv is not None else (self._co[0] if self._co else ''); self._cs = None
        elif t == 'textarea' and self._ta is not None:
            self.f[self._ta] = self._tx; self._ta = None


class SicopClient:
    def __init__(self, empresa_id, user=None, pwd=None, ca=CA, workdir=None):
        self.empresa_id = str(empresa_id)
        self.user = user or os.environ.get('SICOP_USER')
        self.pwd = pwd or os.environ.get('SICOP_PASS')
        if not self.user or not self.pwd:
            raise RuntimeError('Faltan credenciales: definí SICOP_USER y SICOP_PASS')
        self.ca = ca
        self.wd = workdir or tempfile.mkdtemp(prefix='sicop_')
        self.cj = os.path.join(self.wd, 'cookies.txt')

    def _curl(self, args):
        base = ['curl', '-sS', '-c', self.cj, '-b', self.cj, '-A', UA]
        # Solo usar --cacert si hay un bundle (entorno con proxy). En una PC normal
        # curl usa el almacén de certificados del sistema.
        if self.ca and os.path.exists(self.ca):
            base += ['--cacert', self.ca]
        return subprocess.run(base + args, capture_output=True, text=True)

    def _parse(self, path):
        p = _Form(); p.feed(open(path, encoding='utf-8', errors='replace').read()); return p.f

    def _post(self, infile, outfile, action, extra, target='', argument='', binary=False):
        f = self._parse(infile); f['__EVENTTARGET'] = target; f['__EVENTARGUMENT'] = argument; f.setdefault('__LASTFOCUS', '')
        for k, v in extra.items(): f[k] = v
        args = ['-L', '-e', action, '-H', 'Content-Type: application/x-www-form-urlencoded',
                action, '-o', outfile, '-w', '%{http_code} %{content_type} %{size_download}']
        for k, v in f.items(): args += ['--data-urlencode', f'{k}={v}']
        return self._curl(args).stdout.strip()

    def _get(self, url, outfile):
        return self._curl(['-L', url, '-o', outfile]).stdout.strip()

    def login(self):
        p = lambda n: os.path.join(self.wd, n)
        self._get(DEFAULT, p('login.html'))
        lf = self._parse(p('login.html'))
        lf.update({'lgSicop$UserName': self.user, 'lgSicop$Password': self.pwd,
                   'lgSicop$LoginButton': 'Ingresar', '__EVENTTARGET': '', '__EVENTARGUMENT': ''})
        args = ['-L', '-e', DEFAULT, '-H', 'Content-Type: application/x-www-form-urlencoded',
                DEFAULT, '-o', p('home.html'), '-w', '%{url_effective}']
        for k, v in lf.items(): args += ['--data-urlencode', f'{k}={v}']
        url = self._curl(args).stdout.strip()
        if 'Inicio.aspx' not in url:
            raise RuntimeError('Login falló (¿credenciales?). Terminó en ' + url)
        # seleccionar empresa + entrar a Proveedores
        self._get(INICIO, p('i0.html'))
        self._post(p('i0.html'), p('i1.html'), INICIO, {'ctl00$Content$ddlEmpresa': self.empresa_id}, 'ctl00$Content$ddlEmpresa')
        self._post(p('i1.html'), p('prov.html'), INICIO, {}, 'ctl00$lkbProveedor')
        return True

    def _filtrar(self, contratista_cuit):
        p = lambda n: os.path.join(self.wd, n)
        extra = {'ctl00$Content$tbBuscarPor': contratista_cuit, 'ctl00$Content$ddlBuscarPor': '3',
                 'ctl00$Content$ddlEstado': '2', 'ctl00$Content$ddlEdificio': '0',
                 'ctl00$Content$ddlRubroActividad': '0', 'ctl00$Content$ddlPag': '10',
                 'ctl00$Content$pagProveedor': '10', 'ctl00$Content$btnFiltrar': 'Filtrar'}
        self._post(p('prov.html'), p('grid.html'), PROVLIST, extra)
        s = open(p('grid.html'), encoding='utf-8', errors='replace').read()
        mp = {}
        idxs = [m.start() for m in re.finditer(r'<tr[^>]*grid-setup-td', s)]
        for i, st in enumerate(idxs):
            end = idxs[i + 1] if i + 1 < len(idxs) else s.find('</table', st)
            row = s[st:end]
            c = re.search(r'(\d{11})', row); tok = re.search(r"ProveedorEdit\.aspx\?prosta=([^\"&' <]+)", row)
            if c and tok: mp[c.group(1)] = tok.group(1)
        return mp

    def descargar_estado(self, contratista_cuit, cuit, outfile, reintentos=2):
        """Descarga el Estado de Situación (.xlsx) de un proveedor. Devuelve outfile o lanza.

        La sesión de SICOP expira rápido y a veces la grilla vuelve vacía; ante eso
        se vuelve a loguear y se reintenta.
        """
        p = lambda n: os.path.join(self.wd, n)
        tok = None
        for intento in range(1, reintentos + 1):
            mp = self._filtrar(contratista_cuit)
            tok = mp.get(cuit)
            if tok:
                break
            if intento < reintentos:
                self.login()  # re-login y reintentar
        if not tok:
            raise RuntimeError(f'CUIT {cuit} no está en la grilla del contratista {contratista_cuit}')
        edurl = BASE + '/Privado/Proveedores/ProveedorEdit.aspx?prosta=' + tok
        self._get(edurl, p('edit.html'))
        self._post(p('edit.html'), p('edit2.html'), edurl, {}, 'ctl00$Content$EstadoSituacionDw$_lkbLoad')
        st = self._post(p('edit2.html'), outfile, edurl, {},
                        'ctl00$Content$EstadoSituacionDw$lkbDescarga', argument='0', binary=True)
        with open(outfile, 'rb') as fh:
            if fh.read(2) != b'PK':
                raise RuntimeError('La descarga no es un XLSX válido: ' + st)
        return outfile
