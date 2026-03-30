import threading
import time
import random
import os
from enum import Enum
from datetime import datetime


class OrderState(Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

def audit_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    with open("audit_log.txt", "a") as f:
        f.write(log_entry + "\n")
    print(f"📝 {log_entry}")

class Product:
    def __init__(self, pid, name, price, stock):
        self.pid, self.name, self.price, self.stock = pid, name, price, stock
        self.reserved = 0
        self.lock = threading.Lock() 


class ProductService:
    def __init__(self):
        self.products = {}

    def add_product(self, pid, name, price, stock):
        if pid in self.products: return "❌ Duplicate ID"
        if stock < 0: return "❌ Stock cannot be negative"
        self.products[pid] = Product(pid, name, price, stock)
        audit_log(f"Admin added: {name}")
        return "✅ Success"

class CartService:
    def __init__(self, ps):
        self.carts = {} 
        self.ps = ps

    def add_to_cart(self, uid, pid, qty):
        p = self.ps.products.get(pid)
        if not p: return " Product not found"
        
        with p.lock: 
            if (p.stock - p.reserved) >= qty:
                p.reserved += qty
                user_cart = self.carts.get(uid, {})
                user_cart[pid] = user_cart.get(pid, 0) + qty
                self.carts[uid] = user_cart
                audit_log(f"{uid} reserved {qty} of {pid}")
                return " Added to cart"
        return "Insufficient Stock"

class OrderService:
    def __init__(self, ps, cs):
        self.ps, self.cs, self.orders = ps, cs, {}
        self.failure_mode = False

    def checkout(self, uid, coupon=None):
        cart = self.cs.carts.get(uid)
        if not cart: return "Cart Empty"

        order_id = f"ORD_{random.randint(1000, 9999)}"
        reserved_list = []
        
        try:
            
            subtotal = 0
            for pid, qty in cart.items():
                p = self.ps.products[pid]
                item_price = p.price * qty
                if qty > 3: item_price *= 0.95
                subtotal += item_price
                reserved_list.append((pid, qty))

            if subtotal > 1000: subtotal *= 0.90 
            if coupon == "SAVE10": subtotal *= 0.90
            elif coupon == "FLAT200": subtotal -= 200

            
            if self.failure_mode and random.random() < 0.7:
                raise Exception("Network Payment Timeout")

            
            for pid, qty in reserved_list:
                p = self.ps.products[pid]
                with p.lock:
                    p.stock -= qty
                    p.reserved -= qty

            self.orders[order_id] = {"status": OrderState.PAID, "total": max(0, subtotal)}
            self.cs.carts[uid] = {} 
            audit_log(f"Order {order_id} PAID: ₹{subtotal}")
            return f" Order {order_id} Successful!"

        except Exception as e:
            
            for pid, qty in reserved_list:
                p = self.ps.products[pid]
                with p.lock: p.reserved -= qty
            audit_log(f"Rollback: {order_id} failed ({e})")
            return f"Transaction Failed: {e}"


def main():
    ps, cs = ProductService(), CartService(None)
    cs.ps = ps
    os_svc = OrderService(ps, cs)
    uid = "USER_1"

    while True:
        print(f"\n--- BACKEND SIMULATOR (Failure Mode: {'ON' if os_svc.failure_mode else 'OFF'}) ---")
        print("1. Add Product | 2. View Inventory | 3. Add to Cart | 5. View Cart | 7. Checkout | 13. View Logs | 14. Toggle Failure | 0. Exit")
        choice = input("Option: ")

        if choice == '1':
            print(ps.add_product(input("ID: "), input("Name: "), float(input("Price: ")), int(input("Stock: "))))
        elif choice == '2':
            for p in ps.products.values():
                print(f"[{p.pid}] {p.name} | Stock: {p.stock} | Reserved: {p.reserved}")
        elif choice == '3':
            print(cs.add_to_cart(uid, input("PID: "), int(input("Qty: "))))
        elif choice == '7':
            print(os_svc.checkout(uid, input("Coupon: ")))
        elif choice == '13':
            if os.path.exists("audit_log.txt"):
                with open("audit_log.txt", "r") as f: print(f.read())
        elif choice == '14':
            os_svc.failure_mode = not os_svc.failure_mode
        elif choice == '0': break

if __name__ == "__main__":
    main()