from conans import AutoToolsBuildEnvironment, tools
from .conanfilemeson import ConanFileMeson


class ConanFileAutoTools(ConanFileMeson):
    def _configure_builder(self):
        if self._builder:
            return self._builder

        with tools.chdir(self._source_subfolder):
            self.run('NOCONFIGURE=1 ./autogen.sh -fi')

        if self._args:
            args = self._args
        else:
            args = []

        if self.options.shared:
            args.extend(['--disable-static', '--enable-shared'])
        else:
            args.extend(['--disable-shared', '--enable-static'])

        self._builder = AutoToolsBuildEnvironment(self)
        self._builder.configure(args=self._args, configure_dir=self._source_subfolder)
        return self._builder

    def build(self):
        builder = self._configure_builder()
        builder.make()
