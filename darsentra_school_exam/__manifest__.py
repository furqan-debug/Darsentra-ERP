{
    'name': 'Darsentra - Pakistan School Exam & Progress Report Card',
    'version': '19.0.1.0',
    'category': 'Education/Exam',
    'summary': 'Subject Marks, 1st/2nd/3rd Class Positions, BISE School Grading, Teacher Remarks, and Printable Term Progress Report Cards',
    'author': 'Darsentra ERP',
    'website': 'https://github.com/furqan-debug/Darsentra-ERP',
    'license': 'LGPL-3',
    'depends': [
        'openeducat_core',
        'openeducat_exam',
        'darsentra_school_core',
    ],
    'data': [
        'report/report_menu.xml',
        'report/report_progress_card_template.xml',
        'views/school_exam_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
