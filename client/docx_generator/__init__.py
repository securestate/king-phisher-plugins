import os

import king_phisher.client.gui_utilities as gui_utilities
import king_phisher.client.mailer as mailer
import king_phisher.client.plugins as plugins
import king_phisher.client.widget.extras as extras


import jinja2.exceptions

try:
	from docxtpl import DocxTemplate,RichText
except (ImportError, FileNotFoundError):
	has_docxtpl = False
else:
	has_docxtpl = True



class Plugin(getattr(plugins, 'ClientPluginMailerAttachment', plugins.ClientPlugin)):
	authors = ['Samira Karimi Aghmiuni']
	classifiers = ['Plugin :: Client :: Email :: Attachment']
	title = 'Generate DOCX'
	description = """
	Generates a DOCX file from an TemplateFile that process client King Phisher Jinja variables
	allowing embed variables to your attach file that so users that open DOCX  can be tracked."""
	homepage = 'https://github.com/securestate/king-phisher-plugins'
	req_min_version = '1.8.0'
	req_packages = {
		'docxtpl==0.11.1': has_docxtpl
	}
	req_platforms = ('Linux',)
	version = '1.0'
	
	def initialize(self):
		self.add_menu_item('Tools > Create DOCX Preview', self.make_preview)
		return True

	def make_preview(self, _):
		mailer_tab = self.application.main_tabs['mailer']
		config_tab = mailer_tab.tabs['config']
		config_tab.objects_save_to_config()		
		input_path = self.application.config['mailer.attachment_file']
				
		if not (os.path.isfile(input_path) and os.access(input_path, os.R_OK)):
			gui_utilities.show_dialog_error(
				'DOCX Build Error',
				self.application.get_active_window(),
				'Attachment path is invalid or is not readable.'
			)
			return


		_, input_path_extension = os.path.splitext(input_path)
		if (input_path_extension.lower() != '.docx'):
			gui_utilities.show_dialog_error(
				'DOCX Build Error',
				self.application.get_active_window(),
				'Attachment file is invalid or is not readable.'
			)
			return
				
		dialog = extras.FileChooserDialog('Save Generated DOCX File', self.application.get_active_window())		
		response = dialog.run_quick_save('DOCX Preview.docx')
		dialog.destroy()		
		if response is None:
			return

		output_path = response['target_path']
		if not self.process_attachment_file(input_path, output_path):
			gui_utilities.show_dialog_error(
				'DOCX Build Error',
				self.application.get_active_window(),
				'Template file is invalid or is not readable.'
			)
			return
		gui_utilities.show_dialog_info(
			'DOCX Created',
			self.application.get_active_window(),
			'Successfully created the DOCX file.'
		)
		

	def process_attachment_file(self, input_path, output_path, target=None):
		try:		
			output_path, _ = os.path.splitext(output_path)
			output_path += '.DOCX'		
			doc = DocxTemplate(input_path)
			rt = RichText()
			template_vars = mailer.render_DOC_template_var(self.application.config, target)
			rt.add('Alibaba',url_id=doc.build_url_id(template_vars['url']['webserver']))
			context = {'target_name': template_vars['client']['first_name'], 'target_email_address': template_vars['client']['email_address'], 'secret_id': template_vars['uid'], 'example': rt }	
			doc.render(context)
			doc.save(output_path)		
			return output_path
		except:
			return 0
