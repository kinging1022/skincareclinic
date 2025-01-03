import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
    state: () => ({
        items: JSON.parse(localStorage.getItem('cartItems')) || [], 
    }),
    getters: {
        totalItems(state) {
            return state.items.reduce((total, item) => total + item.quantity, 0);
        },
        totalPrice(state) {
            return state.items.reduce((total, item) => total + item.price * item.quantity, 0).toFixed(2);
        },
        totalWeight(state) {
            return state.items.reduce((total, item) => total + item.weight, 0).toFixed(2);
        },
    },
    actions: {
        addItem(product) {
            const existingItem = this.items.find(item => item.id === product.id);
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                this.items.push({ ...product, quantity: 1 });
            }
            this.saveCart();
        },
        removeItem(productId) {
            this.items = this.items.filter(item => item.id !== productId);
            this.saveCart();
        },
        updateQuantity(productId, quantity) {
            const item = this.items.find(item => item.id === productId);
            if (item) {
                item.quantity = quantity;
            }
            this.saveCart();
        },
        clearCart() {
            this.items = [];
            this.saveCart();
        },
        saveCart() {
            localStorage.setItem('cartItems', JSON.stringify(this.items));
        },
    },
});
