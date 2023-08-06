from ftw.upgrade import UpgradeStep
from ftw.htmlblock.config import IS_PLONE_5


class ProvidePrecompiledBundle(UpgradeStep):
    """Provide precompiled bundle.
    """

    def __call__(self):
        if IS_PLONE_5:
            self.install_upgrade_profile()
