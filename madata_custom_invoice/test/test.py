def button_confirm1(self):
    pols=self.env["purchase.order.line"].search([('order_id', '=', self.id)])
    for pol in pols:
        stms=self.env["stock.move"].search([('product_id', '=', pol.product_id.id)])
        qt=pol.product_uom_qty
        for stm in stms:
            if stm.quantite_cmde>0 and stm.quantite_achat == 0:
                if stm.quantite_cmde<qt:
                    qt -= stm.quantite_cmde
                    stm.quantite_achat=stm.quantite_cmde
                    stm.ref_po=self.name
                else:
                    stm.quantite_achat=qt
                    stm.ref_po=self.name
            elif stm.quantite_cmde>0 and stm.quantite_achat != 0:
                if stm.quantite_cmde <qt:
                    qt -= stm.quantite_cmde
                    stm.quantite_achat += stm.quantite_cmde
                    stm.ref_po=stm.ref_po + ',' + self.name
                else:
                    stm.quantite_achat += qt
                    stm.ref_po=stm.ref_po + ',' + self.name
            else:
                pass 
                
    res = super(PurchaseOrderCustom, self).button_confirm()
    return res


def button_confirm(self):
    pols=self.env["purchase.order.line"].search([('order_id', '=', self.id)])
    for pol in pols:
        stms=self.env["stock.move"].search([('product_id', '=', pol.product_id.id)])
        qt=pol.product_uom_qty
        for stm in stms:
            if stm.quantite_cmde>0 and stm.quantite_cmde<qt:
                qt -= stm.quantite_cmde
                stm.quantite_achat += stm.quantite_cmde
                stm.ref_po=self.name
            elif stm.quantite_cmde>0 and stm.quantite_cmde <qt:
                qt -= stm.quantite_cmde
                stm.quantite_achat += stm.quantite_cmde
                stm.ref_po=stm.ref_po + ',' + self.name
            else:
                stm.quantite_achat += qt
                stm.ref_po=stm.ref_po + ',' + self.name
                

def button_confirm(self):
    pols=self.env["purchase.order.line"].search([('order_id', '=', self.id)])
    for pol in pols:
        stms=self.env["stock.move"].search([('product_id', '=', pol.product_id.id)])
        qt=pol.product_uom_qty
        for stm in stms:
            if stm.quantite_cmde>0 and stm.quantite_achat == 0:
                if stm.quantite_cmde<qt:
                    qt -= stm.quantite_cmde
                    stm.quantite_achat=stm.quantite_cmde
                    stm.ref_po=self.name
                else:
                    stm.quantite_achat=qt
                    stm.ref_po=self.name
            elif stm.quantite_cmde>0 and stm.quantite_achat != 0:
                if stm.quantite_cmde <qt:
                    qt -= stm.quantite_cmde
                    stm.quantite_achat += stm.quantite_cmde
                    stm.ref_po=stm.ref_po + ',' + self.name
                else:
                    stm.quantite_achat += qt
                    stm.ref_po=stm.ref_po + ',' + self.name
            else:
                pass
                
    res = super(PurchaseOrderCustom, self).button_confirm()
    return res


class PurchaseOrderCustom(models.Model):
    _inherit=('purchase.order')

    def button_confirm(self):
        pols=self.env["purchase.order.line"].search([('order_id', '=', self.id)])
        for pol in pols:
            qt=pol.product_uom_qty
            stms=self.env["stock.move"].search([('product_id', '=', pol.product_id.id)])
            for stm in stms:
                if stm.quantite_cmde>0 and stm.quantite_achat == 0:
                    if stm.quantite_cmde<qt:
                        qt -= stm.quantite_cmde
                        stm.quantite_achat = stm.quantite_cmde
                        stm.ref_po=self.name
                    else:
                        stm.quantite_achat = pol.product_uom_qty
                        stm.ref_po=self.name
                elif stm.quantite_cmde>0 and stm.quantite_achat != 0:
                    if stm.quantite_cmde <qt:
                        qt -= stm.quantite_cmde
                        stm.quantite_achat = stm.quantite_cmde  
                        stm.ref_po=stm.ref_po + ',' + self.name
                    else:
                        stm.quantite_achat += pol.product_uom_qty
                        stm.ref_po=stm.ref_po + ',' + self.name
                else:
                    pass        
        res = super(PurchaseOrderCustom, self).button_confirm()
        return res
    

    def button_confirm(self):
        for rec in self:
            pols=self.env["purchase.order.line"].search([('order_id', '=', rec.id)])
            for pol in pols:
                qt=pol.product_uom_qty
                stms=self.env["stock.move"].search([('product_id', '=', pol.product_id.id)])
                for stm in stms:
                    if stm.quantite_cmde>0 and stm.quantite_achat == 0:
                        if stm.quantite_cmde< qt:
                            qt -= stm.quantite_cmde
                            stm.quantite_achat = stm.quantite_cmde
                            stm.ref_po=self.name
                        else:
                            stm.quantite_achat = pol.product_uom_qty
                            stm.ref_po=self.name
                    elif stm.quantite_cmde>0 and stm.quantite_achat != 0:
                        if stm.quantite_cmde < qt:
                            qt -= stm.quantite_cmde
                            stm.quantite_achat += stm.quantite_cmde 
                            stm.ref_po=stm.ref_po + ',' + self.name
                        else:
                            stm.quantite_achat += pol.product_uom_qty
                            stm.ref_po=stm.ref_po + ',' + self.name        
                    else:
                        pass