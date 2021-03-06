from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/pay.kv')


class Pay(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Pay, self).__init__(**kwargs)
        # We hide the confirmation buttons for now
        self.ids.pay.opacity = 0.0
        self.bolt11 = ''

    def show_payment_details(self, bolt11):
        """
        Shows the payment details for validation.
        :param invoice: (str) the bolt11 invoice.
        """
        try:
            bolt11 = bolt11.lower()
            decoded = self.manager.app.account.decode_invoice(bolt11)
            # Converting the time until expiration to min and msat to sat
            decoded['expiry'] = int(decoded['expiry'])/60
            sat = int(decoded['msatoshi'])/1000
            usd = self.manager.app.to_usd(sat)
            self.ids.payment_details.text = 'Pay {} satoshis ({}$) to {} ?\nDescription : {}\nThis invoice expires in {} min.'.format(
                sat, usd, decoded['payee'], decoded['description'], decoded['expiry']) # Python 3.5 :'(
            # We keep the valid invoice and activate the confirmation button
            self.bolt11 = bolt11
            self.invoice_desc = decoded['description']
            self.ids.pay.opacity = 1.0
        except:
            self.ids.payment_details.text = 'Could not decode invoice. Maybe you should try again.'

    def pay(self):
        """
        Confirms the payment of the invoice.
        """
        # TODO : clean the UI animations for wait, confirm, error
        self.ids.payment_details.text = 'Sending the payment, waiting for confirmation..'
        if self.bolt11:
            try:
                confirmed = self.manager.app.account.pay(self.bolt11, self.invoice_desc)
                if confirmed:
                    self.ids.payment_details.text = '[size=22sp][b][color=00B808]Success ![/color][/b][/size]'
                else:
                    self.ids.payment_details.text = 'Something went wrong, maybe you should try again'
            except Exception as e:
                # For debugging
                self.ids.payment_details.text = str(e)
                print(str(e))
        else:
            self.ids.payment_details.text = 'You did not specify any invoice'
                    
                    
