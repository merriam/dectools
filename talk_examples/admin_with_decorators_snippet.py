
@require_admin_privilege
def update_price(item, new_price):
    item.price = newprice

@require_admin_privilege        
def update_qty(item, new_qty):
    item.qty = max(0, newqty)

def update_rating(item, stars):
    item.total_stars += max(0,min(5,stars))
    item.total_ratings = item.total_ratings + 1

@require_admin_privilege
def update_specs(item, new_spec):
    item.specs = new_specs[0:400]

