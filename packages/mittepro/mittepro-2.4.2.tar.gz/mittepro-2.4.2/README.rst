Client service, to send simple text emails or, using a template created at MittePro, send more complex emails.

In order to use this library, you must create an account in MittePro.

** **It is not currently possible to create an account in MittePro, but will soon be** **

How to install:
    pip install mittepro

Follow the examples below to send simple emails or emails with templates:

**Simple Emails:**

    from mittepro.models import Mail
    from mittepro.client import MittePro

    mittepro = MittePro(key='<your_account_public_key>', secret='<your_account_secret_key>')

    def send(self):
        mail = Mail(
            recipient_list=[
                'Foo Bar <foo.bar@gmail.com>',
                'Fulano <fulano@gmail.com>',
                '<ciclano@gmail.com>'
            ],
            message="Just a Test, delete if you want.",
            from_='Beutrano <beutrano@mail.com>',
            subject="Just a test"
        )
        response = mittepro.send(mail)

**Template Emails:**

    from mittepro.models import Mail
    from mittepro.client import MittePro

    mittepro = MittePro(key='<your_account_public_key>', secret='<your_account_secret_key>')

    def send(self):
        mail = Mail(
            recipient_list=[
                'Foo Bar <foo.bar@gmail.com>',
                'Fulano <fulano@gmail.com>',
                '<ciclano@gmail.com>'
            ],
            from_='Beutrano <beutrano@mail.com>',
            template_slug='test-101',
            context={'foobar': True},
            context_per_recipient={
                "foo.bar@gmail.com": {"foo": True},
                "fulano@gmail.com.br": {"bar": True}
            },
            use_tpl_default_subject=True,
            use_tpl_default_email=False,
            use_tpl_default_name=False
        )
        response = mittepro.send_template(mail)

**Mail Parameters:**

Parameter - Type - Required - Description

recipient_list - List - Yes - List of all the recipients. The expected format is 'Name `<email>`' or '`<email>`'.

subject - String - Yes* - The subject of the email. *In case your sending an email with template and pass `use_tpl_default_subject` as `True` then you don't need to pass the `subject`.

message_text - String - Yes* - The `message` of the email on text format. *Only Required if your gonna send a simple text email.

message_html - String - No - The `message` of the email on html format. *If pass this and an `template_slug` MittePro is going to ignore the template's html.

tags - Dict/List - No - The `tags` must be an dictionary containing keys and simple values or an list with strings.

from_ - String - No* - The email of the sender. The expected format is 'Name `<email>`' or '`<email>`'. *In case your sending an email with template and pass `use_template_email` as `true` then you don't need to pass this parameter.

template_slug - String - Yes* - The `template_slug` is the slug of the template. *Just pass this if your gonna send a email with template.

use_tpl_default_name - Bool - No* - If set to `True` it use the default value set to the sender's name.

use_tpl_default_email - Bool - No* - If set to `True` it use the default value set to the sender's email.

use_tpl_default_subject - Bool - No* - If set to `True` it use the default value set to the subject.

expose_recipients_list - Bool - No* - If set to `True` every recipient will see the entire list of recipients.

get_text_from_html - Bool - No* - If set to `True` MittePro will extract from your html template an text version. This will only happen if your template doesn't already have an text version.

activate_tracking - Bool - No* - If set to `True` MittePro will track if your email will be open and how many times. Also it will track any links clicked inside the email.

context - Dict - No - Global variables use in the Template. The format is expressed in the example (above).

context_per_recipient - Dict - No - Variables set for each recipient. The format is expressed in the example (above).

**Client Parameters:**

Parameter - Type - Required - Description

key - String - Yes - Your account's public key in the MittePro.

secret - String - Yes - Your account's private key in the MittePro.

fail_silently - Bool - No - If set to `True` the lib will raise it's exceptions. Default `False`.
