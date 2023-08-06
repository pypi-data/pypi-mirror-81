# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2010 ISA srl (<http://www.isa.it>).
#    Copyright (C) 2014 Associazione Odoo Italia
#    http://www.openerp-italia.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp import fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    registration_date = fields.Date(
        'Registration Date',
        states={
            'paid': [('readonly', True)],
            'open': [('readonly', True)],
            'close': [('readonly', True)]
            },
        select=True,
        help="Keep empty to use the current date",
        copy=False)

    def _get_period_from_dates(self, cr, uid, invoice):
        period_model = self.pool['account.period']

        date_start = invoice.registration_date or invoice.date_invoice \
            or time.strftime('%Y-%m-%d')
        date_stop = invoice.registration_date or invoice.date_invoice \
            or time.strftime('%Y-%m-%d')

        period_ids = period_model.search(
            cr, uid,
            [
                ('date_start', '<=', date_start),
                ('date_stop', '>=', date_stop),
                ('company_id', '=', invoice.company_id.id),
                ('special', '!=', True),
                ])
        if period_ids:
            period_id = period_ids[0]
        else:
            period_id = False
        return period_id, date_start, date_stop

    def action_move_create(self, cr, uid, ids, context=None):

        if not context:
            context = {}

        sequence_model = self.pool['ir.sequence']

        for inv in self.browse(cr, uid, ids):
            if inv.type in ('in_invoice', 'in_refund'):
                date_invoice = inv.date_invoice
                reg_date = inv.registration_date
                if not inv.registration_date:
                    if not inv.date_invoice:
                        reg_date = time.strftime('%Y-%m-%d')
                    else:
                        reg_date = inv.date_invoice

                if date_invoice and reg_date and date_invoice > reg_date:
                    raise UserError(
                        _("The invoice date cannot be later than"
                          " the date of registration!"))

                period_id, date_start, date_stop = self._get_period_from_dates(
                    cr, uid, inv)
                if not period_id:
                    raise Warning(
                        _("Can't find a non special period for %s - %s (%s)")
                        % (date_start, date_stop, inv.company_id.name)
                    )

                invoice_values = {'registration_date': reg_date,
                                  'period_id': period_id}

                # ----- For in invoice or refund, force the sequence based on
                #       registration date
                if not inv.internal_number:
                    period = self.pool['account.period'].browse(
                        cr, uid, period_id, context)
                    invoice_number_context = {
                        'fiscalyear_id': period.fiscalyear_id.id}
                    internal_number = sequence_model.next_by_id(
                        cr, uid, inv.journal_id.sequence_id.id,
                        invoice_number_context)
                    invoice_values.update({'internal_number': internal_number})

                self.write(cr, uid, [inv.id], invoice_values)

        super(AccountInvoice, self).action_move_create(
            cr, uid, ids, context=context)

        account_move_model = self.pool['account.move']

        for inv in self.browse(cr, uid, ids):
            if inv.type in ('in_invoice', 'in_refund'):

                mov_date = inv.registration_date or inv.date_invoice or \
                    time.strftime('%Y-%m-%d')

                account_move_model.write(
                    cr, uid, [inv.move_id.id], {'state': 'draft'})

                period_id, date_start, date_stop = self._get_period_from_dates(
                    cr, uid, inv)

                cr.execute(
                    'update account_move_line '
                    'set period_id = %s ,date=%s where move_id = %s',
                    (str(period_id), mov_date, str(inv.move_id.id),)
                )

                account_move_model.write(
                    cr, uid, [inv.move_id.id],
                    {'period_id': period_id, 'date': mov_date})

                account_move_model.write(
                    cr, uid, [inv.move_id.id], {'state': 'posted'})

        self._log_event(cr, uid, ids)
        return True
