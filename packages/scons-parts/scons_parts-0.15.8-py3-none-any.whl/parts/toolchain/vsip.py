# compatibility with 0.8 .. should be removed later



def vssdk_setup(env, ver):
    env['VSSDK_VERSION'] = ver


def resolve(env, version):
    def func(x): return vssdk_setup(x, version)
    return [
        ('vssdk', func)
    ]
