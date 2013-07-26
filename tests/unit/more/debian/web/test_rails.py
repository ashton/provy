from mock import call
from nose.tools import istest

from provy.more.debian import RailsRole, AptitudeRole, GemRole, SupervisorRole
from provy.more.debian.web.rails import PACKAGES_TO_INSTALL
from tests.unit.tools.helpers import ProvyTestCase


class RailsRoleTest(ProvyTestCase):
    def setUp(self):
        super(RailsRoleTest, self).setUp()
        self.role = RailsRole(prov=None, context={'owner': 'some-owner'})
        self.supervisor_role = SupervisorRole(prov=None, context=self.role.context)

    @istest
    def installs_necessary_packages_to_provision(self):
        methods_to_mock = (
            'execute',
            'register_template_loader',
            'remote_exists_dir',
            'update_file',
            'change_file_mode',
            'ensure_dir',
        )
        with self.using_stub(AptitudeRole) as aptitude, self.using_stub(GemRole) as gem, self.mock_role_methods(*methods_to_mock):
            self.role.remote_exists_dir.return_value = False

            self.role.provision()

            self.role.register_template_loader.assert_called_once_with('provy.more.debian.web')
            self.assertEqual(aptitude.ensure_package_installed.mock_calls, [call(package) for package in PACKAGES_TO_INSTALL])
            self.assertEqual(gem.ensure_package_installed.mock_calls, [call('bundler'), call('passenger')])
            self.role.remote_exists_dir.assert_called_once_with('/etc/nginx')
            self.assertEqual(self.role.ensure_dir.mock_calls, [
                call('/var/log/nginx', sudo=True),
                call('/etc/nginx/sites-available', sudo=True),
                call('/etc/nginx/sites-enabled', sudo=True),
                call('/etc/nginx/conf.d', sudo=True),
            ])
            self.role.execute.assert_called_once_with('passenger-install-nginx-module --auto --auto-download --prefix=/etc/nginx', sudo=True, stdout=False)
            self.assertEqual(self.role.update_file.mock_calls, [
                call('rails.nginx.conf.template', '/etc/nginx/conf/nginx.conf', sudo=True),
                call('rails.nginx.init.template', '/etc/init.d/nginx', sudo=True),
            ])
            self.role.change_file_mode.assert_called_once_with('/etc/init.d/nginx', 755)

    @istest
    def provisions_even_if_nginx_already_exists(self):
        methods_to_mock = (
            'register_template_loader',
            'remote_exists_dir',
            'update_file',
            'change_file_mode',
            'ensure_dir',
        )
        with self.using_stub(AptitudeRole), self.using_stub(GemRole), self.mock_role_methods(*methods_to_mock):
            self.role.remote_exists_dir.return_value = True

            self.role.provision()

            self.assertEqual(self.role.ensure_dir.mock_calls, [
                call('/etc/nginx/sites-available', sudo=True),
                call('/etc/nginx/sites-enabled', sudo=True),
                call('/etc/nginx/conf.d', sudo=True),
            ])