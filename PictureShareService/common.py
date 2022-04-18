import os
from dotenv import dotenv_values
from pathlib import Path
import PictureShareService.settings


class EnvVars:

    def __init__(self, django_environment_var_name='DJANGO_ENVIRONMENT'):
        self.django_environment_var_name = django_environment_var_name
        self.env_vars = self.get_variables_from_dotenv_file()

    # loading environment related variables
    def get_variables_from_dotenv_file(self):

        DJANGO_ENVIRONMENT = os.getenv(self.django_environment_var_name) \
            if os.getenv(self.django_environment_var_name) is not None else ''
        env_path = Path('EnvVars/%s.env' % (DJANGO_ENVIRONMENT))
        return dotenv_values(dotenv_path=env_path, verbose=True)

    def get_value(
            self,
            var_name,
            default_value = None,
            variable_prefix = 'DJANGO_'
    ):
        var_fulname = '%s%s' % (variable_prefix, var_name)
        os_env_var_value = os.getenv(var_fulname)
        if os_env_var_value is None:
            return_value = self.env_vars[var_fulname] if var_fulname in self.env_vars \
                else default_value
        else:
            return_value = os_env_var_value
        return return_value
