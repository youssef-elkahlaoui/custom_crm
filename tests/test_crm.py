from odoo.tests import common

class TestCRM(common.TransactionCase):

    def setUp(self):
        super(TestCRM, self).setUp()
        self.opportunity_model = self.env['crm.lead']

    def test_archive_opportunities(self):
        # Créer des opportunités anciennes
        old_opportunity = self.opportunity_model.create({
            'name': 'Ancienne Opportunité',
            'create_date': '2022-01-01',
        })
        # Appeler la méthode de cron
        self.opportunity_model._cron_archive_opportunities()
        # Vérifier qu'elles sont archivées
        self.assertTrue(old_opportunity.active == False)