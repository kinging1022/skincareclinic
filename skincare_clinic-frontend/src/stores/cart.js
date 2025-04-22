import { defineStore } from 'pinia';
import { useToastStore } from './toast.js';

const CART_EXPIRY_TIME = 5 * 60 * 60 * 1000; // 5 hours in milliseconds

export const useCartStore = defineStore('cart', {
    state: () => ({
        items: JSON.parse(localStorage.getItem('cartItems')) || [], 
        timestamp: JSON.parse(localStorage.getItem('cartTimestamp')) || null,
    }),
    getters: {
        totalItems(state) {
            return state.items.reduce((total, item) => total + item.quantity, 0);
        },
        subtotal() {
            return this.items.reduce((total, item) => total + item.price * item.quantity, 0)
        },
        
        total() {
            return this.subtotal 
        },
        totalWeight(state) {
            const total = state.items.reduce((total, item) => {
              const itemWeight = Number(item.weight) || 0
              return total + (itemWeight * item.quantity)
            }, 0)
            return parseFloat(total.toFixed(2))
          },
        isCartExpired(state) {
            if (!state.timestamp) return false;
            const currentTime = new Date().getTime();
            return currentTime - state.timestamp > CART_EXPIRY_TIME;
        },
    },
    actions: {
        addItem(product) {
            if (this.isCartExpired) {
                this.clearCart();
            }
            const existingItem = this.items.find(item => item.id === product.id);
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                this.items.push({ ...product, quantity: 1 });
            }
            const brandName = product.brand?.name || " "; 
            const message = `Added ${brandName} ${product.name} to cart`;
            const toastStore = useToastStore(); 
            toastStore.showToast(5000, message, "bg-[#0a5c3e] text-white");
            this.saveCart();
        },
        removeItem(productId) {
            if (this.isCartExpired) {
                this.clearCart();
            }
            this.items = this.items.filter(item => item.id !== productId);
            this.saveCart();
        },
        updateQuantity(productId, quantity) {
            if (this.isCartExpired) {
                this.clearCart();
            }
            const item = this.items.find(item => item.id === productId);
            if (item) {
                item.quantity = quantity;
            }
            this.saveCart();
        },
        clearCart() {
            this.items = [];
            this.timestamp = null;
            localStorage.removeItem('cartItems');
            localStorage.removeItem('cartTimestamp');
        },
        saveCart() {
            this.timestamp = new Date().getTime();
            localStorage.setItem('cartItems', JSON.stringify(this.items));
            localStorage.setItem('cartTimestamp', JSON.stringify(this.timestamp));
        },
        updateStock(productId, stock) {
            const item = this.items.find(item => item.id === productId);
            if (item) {
            item.stock = stock;
            }
            this.saveCart();
        },
        initializeCart() {
            const savedCart = JSON.parse(localStorage.getItem('cartItems')) || [];
            const savedTimestamp = JSON.parse(localStorage.getItem('cartTimestamp')) || null;
            const currentTime = new Date().getTime();

            if (savedTimestamp && currentTime - savedTimestamp > CART_EXPIRY_TIME) {
                this.clearCart();
            } else {
                this.items = savedCart;
                this.timestamp = savedTimestamp;
            }
        },
    },
});
