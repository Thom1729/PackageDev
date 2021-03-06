import sublime_plugin

from .sublime_lib.path import root_at_packages, get_package_name


PLUGIN_NAME = get_package_name()

SETTINGS_SYNTAX = ("Packages/%s/Package/Sublime Text Settings/Sublime Settings.tmLanguage"
                   % PLUGIN_NAME)
TPL = "{\n\t$0\n}"


class NewSettingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = self.window.new_file()
        v.settings().set('default_dir', root_at_packages('User'))
        v.set_syntax_file(SETTINGS_SYNTAX)
        v.run_command('insert_snippet', {'contents': TPL})
