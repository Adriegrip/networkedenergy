
{
    'name': "Hardware Delivery Date",
    'version': '14.0.1.0.0',
    'summary': """This module is to manage delivery date for hardware in crm""",
    'description': """This module is to manage delivery date for hardware in crm""",
    'category': '',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['web_studio', 'crm'],

    'data': [
        'security/ir.model.access.csv',
        'views/hardware_delivery_date_view.xml',
    ],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}