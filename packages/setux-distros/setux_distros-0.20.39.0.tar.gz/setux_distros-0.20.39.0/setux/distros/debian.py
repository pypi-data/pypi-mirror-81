from setux.core.distro import Distro


class Debian(Distro):
    Package = 'apt'
    Service = 'SystemD'
    pkgmap = dict(
        pip        = 'python3-pip',
        setuptools = 'python3-setuptools',
        sqlite     = 'sqlite3',
        p7zip      = 'p7zip-full',
        xz         = 'xz-utils',
        ctag       = 'exuberant-ctags',
        unrar      = 'unrar-free',
    )
    svcmap = dict(
    )

    @classmethod
    def release_name(cls, infos):
        did = infos['ID'].strip()
        ver = infos['VERSION_ID'].strip('\r"')
        return f'{did}_{ver}'


class debian_9(Debian):
    pass


class debian_10(Debian):
    pass
