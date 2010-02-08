def update_price(item, new_price):
    if not require_admin_privilege('update_price'):
        return
    item.price = newprice

def update_qty(item, new_qty):
    if not require_admin_privilege('update_qty'):
        return
    item.qty = max(0, newqty)

def update_rating(item, stars):
    item.total_stars += max(0,min(5,stars))
    item.total_ratings = item.total_ratings + 1

def update_specs(item, new_spec):
    if not require_admin_privilege('update_qty'):
        return
    item.specs = new_specs[0:400]
