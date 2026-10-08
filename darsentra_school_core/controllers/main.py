import logging
from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.home import Home

_logger = logging.getLogger(__name__)


class DarsentraLandingController(http.Controller):

    @http.route('/', type='http', auth='public', website=True, sitemap=True)
    def landing_page(self, **kw):
        user = request.env.user
        is_logged_in = bool(user and not user._is_public())
        has_completed_setup = bool(is_logged_in and user.company_id and user.company_id.is_school_setup_completed)
        return request.render('darsentra_school_core.landing_page', {
            'is_logged_in': is_logged_in,
            'has_completed_setup': has_completed_setup,
            'company': request.env.company,
        })


class DarsentraOnboardingController(http.Controller):

    @http.route('/school/onboarding', type='http', auth='user', website=True, methods=['GET', 'POST'], csrf=True)
    def school_onboarding(self, **kw):
        user = request.env.user
        company = request.env.company

        # If returning user already completed setup, allow them to view or edit, otherwise redirect to dashboard
        if request.httprequest.method == 'GET':
            if company.is_school_setup_completed and not kw.get('edit'):
                return request.redirect('/web')
            return request.render('darsentra_school_core.school_onboarding', {
                'company': company,
                'user': user,
                'error': kw.get('error'),
            })

        # POST: Process Basic School Setup Details
        school_name = kw.get('school_name', '').strip()
        school_city = kw.get('school_city', '').strip()
        school_phone = kw.get('school_phone', '').strip()
        school_board = kw.get('school_board', 'punjab')
        school_level = kw.get('school_level', 'comprehensive')
        academic_session = kw.get('academic_session', '2025-2026').strip()

        if not school_name or not school_city or not school_phone:
            return request.render('darsentra_school_core.school_onboarding', {
                'company': company,
                'user': user,
                'error': _('Please fill in all required fields (School Name, Campus City, and Official Contact Number).'),
                'form_data': kw,
            })

        try:
            # 1. Update Company Basic Profile
            vals = {
                'is_school_setup_completed': True,
                'school_campus_city': school_city,
                'school_board': school_board,
                'school_level': school_level,
                'academic_session': academic_session or '2025-2026',
            }
            if school_name:
                vals['name'] = school_name
            if school_phone:
                vals['phone'] = school_phone
                vals['admin_whatsapp'] = school_phone
            if school_city:
                vals['city'] = school_city

            company.sudo().write(vals)

            # 2. Ensure Academic Year exists for OpenEduCat core
            if academic_session:
                AcadYear = request.env['op.academic.year'].sudo()
                existing_year = AcadYear.search([('name', '=', academic_session)], limit=1)
                if not existing_year:
                    year_str = academic_session.split('-')[0] if '-' in academic_session else academic_session
                    try:
                        start_yr = int(year_str)
                    except ValueError:
                        start_yr = 2025
                    AcadYear.create({
                        'name': academic_session,
                        'start_date': f"{start_yr}-04-01",
                        'end_date': f"{start_yr + 1}-03-31",
                        'company_id': company.id,
                    })

            # Redirect directly to ERP Dashboard
            return request.redirect('/web')

        except Exception as e:
            _logger.exception("Error saving school onboarding data: %s", e)
            return request.render('darsentra_school_core.school_onboarding', {
                'company': company,
                'user': user,
                'error': _('An unexpected error occurred while saving school setup. Please try again.'),
                'form_data': kw,
            })


class DarsentraHomeController(Home):

    def _login_redirect(self, uid, redirect=None):
        """Redirect newly signed up or unconfigured users to School Setup before Dashboard."""
        user = request.env['res.users'].sudo().browse(uid)
        if user.exists() and not user._is_public() and not user.company_id.is_school_setup_completed:
            return '/school/onboarding'
        return super()._login_redirect(uid, redirect)

    @http.route(['/web', '/odoo', '/odoo/<path:subpath>', '/scoped_app/<path:subpath>'], type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        """Enforce School Setup completion before opening the ERP web client."""
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.exists() and not user._is_public() and not user.company_id.is_school_setup_completed:
                return request.redirect('/school/onboarding')
        return super().web_client(s_action=s_action, **kw)
